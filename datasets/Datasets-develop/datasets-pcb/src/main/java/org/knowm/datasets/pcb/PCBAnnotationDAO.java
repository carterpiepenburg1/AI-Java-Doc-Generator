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
package org.knowm.datasets.pcb;

import java.util.List;

import org.knowm.yank.Yank;

/**
 * @author timmolter
 */
public class PCBAnnotationDAO extends PCBParentDAO {

  public static int dropTable() {

    return Yank.execute("DROP TABLE IF EXISTS PCB_ANNOTATIONS", null);
  }

  public static int createTable() {

    return Yank.executeSQLKey("KEY_CREATE_TABLE_PCB_ANNOTATIONS", null);
  }

  public static int insert(PCBAnnotation pcbAnnotation) {

    Object[] params = new Object[] {

        // @formatter:off
        pcbAnnotation.getPcbid(),
        pcbAnnotation.getId(),
        pcbAnnotation.getX(),
        pcbAnnotation.getY(),
        pcbAnnotation.getWidth(),
        pcbAnnotation.getHeight(),
        pcbAnnotation.getRotation(),
        pcbAnnotation.getName()
        // @formatter:on
    };

    String PCB_INSERT = "INSERT INTO PCB_ANNOTATIONS (pcbid, id, x, y, width, height, rotation, name) VALUES (?, ?, ?, ?, ?, ?, ?, ?)";
    return Yank.execute(PCB_INSERT, params);
  }

  public static List<PCBAnnotation> selectList(int pcbID) {

    Object[] params = new Object[] { pcbID };

    String SELECT = "SELECT * FROM PCB_ANNOTATIONS WHERE pcbid = ?";

    return Yank.queryBeanList(SELECT, PCBAnnotation.class, params);
  }

  public static long selectCount() {

    String SELECT_COUNT = "SELECT COUNT(*) FROM PCB_ANNOTATIONS";

    return Yank.queryScalar(SELECT_COUNT, Long.class, null);
  }

  public static long selectMaxID() {

    String SELECT_MAX = "SELECT MAX(`id`) FROM PCB_ANNOTATIONS WHERE pcbid = ?";

    return Yank.queryScalar(SELECT_MAX, Long.class, null);
  }

  public static void updateName(String name, int pcbID, int pcbAnnotationID) {

    Object[] params = new Object[] {

        // @formatter:off
        name,
        pcbID,
         pcbAnnotationID
          // @formatter:on
    };

    String UPDATE = "UPDATE PCB_ANNOTATIONS SET name = ? WHERE PCBID = ? and ID = ?";

    Yank.execute(UPDATE, params);
  }

  public static PCBAnnotation select(int pcbID, int id) {

    Object[] params = new Object[] { pcbID, id };

    String SELECT = "SELECT * FROM PCB_ANNOTATIONS WHERE pcbid = ? and id = ?";

    return Yank.queryBean(SELECT, PCBAnnotation.class, params);
  }
}
