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
package org.knowm.datasets.lshtc4;

import static org.hamcrest.CoreMatchers.equalTo;
import static org.hamcrest.MatcherAssert.assertThat;

import java.util.List;

import org.junit.AfterClass;
import org.junit.BeforeClass;
import org.junit.Ignore;
import org.junit.Test;
import org.knowm.datasets.lshtc4.LSHTC4Hierarchy;
import org.knowm.datasets.lshtc4.LSHTC4HierarchyDAO;

/**
 * @author timmolter
 */
@Ignore
public class TestLSHTC4HierarchyDAO {

  @BeforeClass
  public static void setUpDB() {

    LSHTC4HierarchyDAO.init(new String[0]);

  }

  @AfterClass
  public static void tearDownDB() {

    LSHTC4HierarchyDAO.release();
  }

  @Test
  public void testSelectCount() {

    long count = LSHTC4HierarchyDAO.selectCount();
    assertThat(count, equalTo(863261L));

  }

  @Test
  public void test() {

    List<LSHTC4Hierarchy> all = LSHTC4HierarchyDAO.selectAll();
    assertThat(all.size(), equalTo(863261));

    // System.out.println(all.get(0));
    LSHTC4Hierarchy lSHTC4Hierarchy = LSHTC4HierarchyDAO.selectSingle(2214730);
    int parentID = lSHTC4Hierarchy.getParentid();
    assertThat(parentID, equalTo(2244783));

  }

}
