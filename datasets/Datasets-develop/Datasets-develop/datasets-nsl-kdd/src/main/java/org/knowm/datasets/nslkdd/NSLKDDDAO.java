/**
 * (The MIT License)
 *
 * Copyright 2015-2017 Knowm Inc. (http://knowm.org) and contributors.
 * Copyright 2013-2015 Xeiam LLC (http://xeiam.com) and contributors.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of
 * this software and associated documentation files (the "Software"), to deal in
 * the Software without restriction, including without limitation the rights to
 * use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
 * of the Software, and to permit persons to whom the Software is furnished to do
 * so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */
/**
 * This product currently only contains code developed by authors
 * of specific components, as identified by the source code files.
 *
 * Since product implements StAX API, it has dependencies to StAX API
 * classes.
 *
 * For additional credits (generally to people who reported problems)
 * see CREDITS file.
 */
package org.knowm.datasets.nslkdd;

import org.knowm.datasets.common.business.DatasetsDAO;
import org.knowm.yank.Yank;

/**
 * An explanation of the fields can be found here: https://archive.ics.uci.edu/ml/machine-learning-databases/kddcup99-mld/task.html
 *
 * @author timmolter
 */
public class NSLKDDDAO extends DatasetsDAO {

  public static void init(String dataFilesDir) {

    String dataFileID = "0ByP7_A9vXm17Q2w5LTFCb3ZEVFE";
    String propsFileID = "0ByP7_A9vXm17Nl9PRGJQeVp0NGc";
    String scriptFileID = "0ByP7_A9vXm17eWhldXZiNWxRSnc";

    init("DB_NSL_KDD", dataFilesDir, dataFileID, propsFileID, scriptFileID, null, true);
  }

  public static int dropTable() {

    return Yank.execute("DROP TABLE IF EXISTS NSL_KDD", null);
  }

  public static int getTrainTestSplit() {

    return 125973;
  }

  public static int createTable() {

    return Yank.executeSQLKey("KEY_CREATE_TABLE", null);
  }

  public static int insert(NSLKDD nSLKDD) {

    Object[] params = new Object[] {

        // @formatter:off
        nSLKDD.getId(), nSLKDD.getDuration(), nSLKDD.getProtocol_type(), nSLKDD.getService(), nSLKDD.getFlag(), nSLKDD.getSrc_bytes(),
        nSLKDD.getDst_bytes(), nSLKDD.getLand(), nSLKDD.getWrong_fragment(), nSLKDD.getUrgent(), nSLKDD.getHot(), nSLKDD.getNum_failed_logins(),
        nSLKDD.getLogged_in(), nSLKDD.getNum_compromised(), nSLKDD.getRoot_shell(), nSLKDD.getSu_attempted(), nSLKDD.getNum_root(),
        nSLKDD.getNum_file_creations(), nSLKDD.getNum_shells(), nSLKDD.getNum_access_files(), nSLKDD.getNum_outbound_cmds(),
        nSLKDD.getIs_host_login(), nSLKDD.getIs_guest_login(), nSLKDD.getConcurrentcount(), nSLKDD.getSrv_count(), nSLKDD.getSerror_rate(),
        nSLKDD.getSrv_serror_rate(), nSLKDD.getRerror_rate(), nSLKDD.getSrv_rerror_rate(), nSLKDD.getSame_srv_rate(), nSLKDD.getDiff_srv_rate(),
        nSLKDD.getSrv_diff_host_rate(), nSLKDD.getDst_host_count(), nSLKDD.getDst_host_srv_count(), nSLKDD.getDst_host_same_srv_rate(),
        nSLKDD.getDst_host_diff_srv_rate(), nSLKDD.getDst_host_same_src_port_rate(), nSLKDD.getDst_host_srv_diff_host_rate(),
        nSLKDD.getDst_host_serror_rate(), nSLKDD.getDst_host_srv_serror_rate(), nSLKDD.getDst_host_rerror_rate(),
        nSLKDD.getDst_host_srv_rerror_rate(), nSLKDD.getTruth(),

        // @formatter:on
    };

    String NSL_KDD_INSERT = "INSERT INTO NSL_KDD (id, duration, protocol_type, service, flag, src_bytes, dst_bytes, land, wrong_fragment, urgent, hot, num_failed_logins, logged_in, num_compromised, root_shell, su_attempted, num_root,"
        + "num_file_creations, num_shells, num_access_files, num_outbound_cmds, is_host_login, is_guest_login, concurrentcount, srv_count, serror_rate, srv_serror_rate,"
        + "rerror_rate, srv_rerror_rate, same_srv_rate, diff_srv_rate, srv_diff_host_rate, dst_host_count, dst_host_srv_count, dst_host_same_srv_rate,"
        + "dst_host_diff_srv_rate, dst_host_same_src_port_rate, dst_host_srv_diff_host_rate, dst_host_serror_rate, dst_host_srv_serror_rate, dst_host_rerror_rate,"
        + "dst_host_srv_rerror_rate, truth"

        + ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";

    return Yank.execute(NSL_KDD_INSERT, params);
  }

  public static NSLKDD selectSingle(int id) {

    Object[] params = new Object[] { id };

    String SELECT_SINGLE = "SELECT * FROM NSL_KDD WHERE id = ?";

    return Yank.queryBean(SELECT_SINGLE, NSLKDD.class, params);
  }

  public static long selectCount() {

    String SELECT_COUNT = "SELECT COUNT(*) FROM NSL_KDD";

    return Yank.queryScalar(SELECT_COUNT, Long.class, null);
  }
}
