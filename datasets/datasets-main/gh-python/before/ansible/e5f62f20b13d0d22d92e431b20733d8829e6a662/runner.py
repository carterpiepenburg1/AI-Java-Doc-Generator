# Copyright (c) 2012 Michael DeHaan <michael.dehaan@gmail.com>
#
# Permission is hereby granted, free of charge, to any person 
# obtaining a copy of this software and associated documentation 
# files (the "Software"), to deal in the Software without restriction, 
# including without limitation the rights to use, copy, modify, merge, 
# publish, distribute, sublicense, and/or sell copies of the Software, 
# and to permit persons to whom the Software is furnished to do so, 
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be 
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR 
# ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION 
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import fnmatch
import multiprocessing
import os
import json
import traceback
import paramiko # non-core dependency
import ansible.constants as C 

def _executor_hook(x):
    ''' callback used by multiprocessing pool '''
    (runner, host) = x
    return runner._executor(host)

class Runner(object):

    def __init__(self, 
        host_list=C.DEFAULT_HOST_LIST, 
        module_path=C.DEFAULT_MODULE_PATH,
        module_name=C.DEFAULT_MODULE_NAME, 
        module_args=C.DEFAULT_MODULE_ARGS, 
        forks=C.DEFAULT_FORKS, 
        timeout=C.DEFAULT_TIMEOUT, 
        pattern=C.DEFAULT_PATTERN,
        remote_user=C.DEFAULT_REMOTE_USER,
        remote_pass=C.DEFAULT_REMOTE_PASS,
        verbose=False):
    
        ''' 
        Constructor
        host_list   -- file on disk listing hosts to manage, or an array of hostnames
        pattern ------ a fnmatch pattern selecting some of the hosts in host_list
        module_path -- location of ansible library on disk
        module_name -- which module to run
        module_args -- arguments to pass to module
        forks -------- how parallel should we be? 1 is extra debuggable.
        remote_user -- who to login as (default root)
        remote_pass -- provide only if you don't want to use keys or ssh-agent
        '''

        self.host_list   = self._parse_hosts(host_list)
        self.module_path = module_path
        self.module_name = module_name
        self.forks       = forks
        self.pattern     = pattern
        self.module_args = module_args
        self.timeout     = timeout
        self.verbose     = verbose
        self.remote_user = remote_user
        self.remote_pass = remote_pass

    def _parse_hosts(self, host_list):
        ''' parse the host inventory file if not sent as an array '''
        if type(host_list) != list:
            host_list = os.path.expanduser(host_list)
            return file(host_list).read().split("\n")
        return host_list


    def _matches(self, host_name, pattern=None):
        ''' returns if a hostname is matched by the pattern '''
        if host_name == '':
            return False
        if not pattern:
            pattern = self.pattern
        subpatterns = pattern.split(";")
        for subpattern in subpatterns:
            if fnmatch.fnmatch(host_name, subpattern):
                return True
        return False

    def _connect(self, host):
        ''' 
        obtains a paramiko connection to the host.
        on success, returns (True, connection) 
        on failure, returns (False, traceback str)
        '''
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(host, username=self.remote_user, allow_agent=True, 
              look_for_keys=True, password=self.remote_pass)
            return [ True, ssh ]
        except:
            return [ False, traceback.format_exc() ]

    def _return_from_module(self, conn, host, result):
        conn.close()
        try:
            return [ host, True, json.loads(result) ]
        except:
            return [ host, False, result ]

    def _delete_remote_files(self, conn, files):
        for filename in files:
            self._exec_command(conn, "rm -f %s" % filename)

    def _transfer_file(self, conn, source, dest):
        self.remote_log(conn, 'COPY remote:%s local:%s' % (source, dest))
        ftp = conn.open_sftp()
        ftp.put(source, dest)
        ftp.close()

    def _transfer_module(self, conn):
        outpath = self._copy_module(conn)
        self._exec_command(conn, "chmod +x %s" % outpath)
        return outpath

    def _execute_module(self, conn, outpath):
        cmd = self._command(outpath)
        result = self._exec_command(conn, cmd)
        self._delete_remote_files(conn, [ outpath ])
        return result

    def _execute_normal_module(self, conn, host):
        ''' transfer a module, set it executable, and run it '''

        module = self._transfer_module(conn)
        result = self._execute_module(conn, module)
        return self._return_from_module(conn, host, result)

    def _execute_copy(self, conn, host):
        ''' handler for file transfer operations '''

        # transfer the file to a remote tmp location
        source = self.module_args[0]
        dest   = self.module_args[1]
        tmp_dest = self._get_tmp_path(conn, dest.split("/")[-1])
        self._transfer_file(conn, source, tmp_dest)

        # install the copy  module
        self.module_name = 'copy'
        module = self._transfer_module(conn)

        # run the copy module
        self.module_args = [ tmp_dest, dest ]
        result = self._execute_module(conn, module)
        self._delete_remote_files(conn, tmp_dest)
        return self._return_from_module(conn, host, result)

    def _execute_template(self, conn, host):
        ''' handler for template operations '''

        source   = self.module_args[0]
        dest     = self.module_args[1]
        metadata = '/etc/ansible/setup'

        # first copy the source template over
        tempname = os.path.split(source)[-1]
        temppath = self._get_tmp_path(conn, tempname)
        self._transfer_file(conn, source, temppath)

        # install the template module
        self.module_name = 'template'
        module = self._transfer_module(conn)

        # run the template module
        self.module_args = [ temppath, dest, metadata ]
        result = self._execute_module(conn, module)
        self._delete_remote_files(conn, [ temppath ])
        return self._return_from_module(conn, host, result)


    def _executor(self, host):
        ''' 
        callback executed in parallel for each host.
        returns (hostname, connected_ok, extra)
        where extra is the result of a successful connect
        or a traceback string
        '''

        ok, conn = self._connect(host)
        if not ok:
            return [ host, False, conn ]
        if self.module_name not in [ 'copy', 'template' ]:
            return self._execute_normal_module(conn, host)
        elif self.module_name == 'copy':
            return self._execute_copy(conn, host)
        elif self.module_name == 'template':
            return self._execute_template(conn, host)
        else:
            raise Exception("???")

    def _command(self, outpath):
        ''' form up a command string '''
        cmd = "%s %s" % (outpath, " ".join(self.module_args))
        return cmd

   
    def remote_log(self, conn, msg):
        stdin, stdout, stderr = conn.exec_command('/usr/bin/logger -t ansible -p auth.info %r' % msg)

    def _exec_command(self, conn, cmd):
        ''' execute a command over SSH '''
        msg = '%s: %s' % (self.module_name, cmd)
        self.remote_log(conn, msg)
        stdin, stdout, stderr = conn.exec_command(cmd)
        results = "\n".join(stdout.readlines())
        return results

    def _get_tmp_path(self, conn, file_name):
        output = self._exec_command(conn, "mktemp /tmp/%s.XXXXXX" % file_name)
        return output.split("\n")[0]

    def _copy_module(self, conn):
        ''' transfer a module over SFTP '''
        in_path = os.path.expanduser(
            os.path.join(self.module_path, self.module_name)
        )
        out_path = self._get_tmp_path(conn, "ansible_%s" % self.module_name)

        sftp = conn.open_sftp()
        sftp.put(in_path, out_path)
        sftp.close()
        return out_path

    def match_hosts(self, pattern=None):
        ''' return all matched hosts '''
        return [ h for h in self.host_list if self._matches(h, pattern) ]

    def run(self):
        ''' xfer & run module on all matched hosts '''

        # find hosts that match the pattern
        hosts = self.match_hosts()

        # attack pool of hosts in N forks
        hosts = [ (self,x) for x in hosts ]
        if self.forks > 1:
            pool = multiprocessing.Pool(self.forks)
            results = pool.map(_executor_hook, hosts)
        else:
            results = [ _executor_hook(x) for x in hosts ]

        # sort hosts by ones we successfully contacted
        # and ones we did not
        results2 = {
          "contacted" : {},
          "dark"      : {}
        }
        for x in results:
            (host, is_ok, result) = x
            if not is_ok:
                results2["dark"][host] = result
            else:
                results2["contacted"][host] = result

        return results2


if __name__ == '__main__':

    # test code...

    r = Runner(
       host_list = DEFAULT_HOST_LIST,
       module_name='ping',
       module_args='',
       pattern='*',
       forks=3
    )   
    print r.run()

 

