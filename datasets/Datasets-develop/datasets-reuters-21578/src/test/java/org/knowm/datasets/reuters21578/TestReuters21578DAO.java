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
package org.knowm.datasets.reuters21578;

import static org.hamcrest.CoreMatchers.equalTo;
import static org.hamcrest.CoreMatchers.not;
import static org.hamcrest.MatcherAssert.assertThat;

import java.util.List;

import org.junit.AfterClass;
import org.junit.BeforeClass;
import org.junit.Ignore;
import org.junit.Test;

/**
 * @author timmolter
 */
@Ignore
public class TestReuters21578DAO {

  @BeforeClass
  public static void setUpDB() {

    Reuters21578DAO.init(new String[0]);
  }

  @AfterClass
  public static void tearDownDB() {

    Reuters21578DAO.release();
  }

  // @Test
  public void testSelectAll() {

    List<Reuters21578> allData = Reuters21578DAO.selectAll();
    assertThat(allData.size(), equalTo(21578));
  }

  // @Test
  public void testSelectRange() {

    List<Reuters21578> data = Reuters21578DAO.selectRange(10, 100);
    assertThat(data.size(), equalTo(100));
  }

  // @Test
  public void testSelectRandom() {

    List<Reuters21578> data1 = Reuters21578DAO.selectRandomList(10);
    assertThat(data1.size(), equalTo(10));

    List<Reuters21578> data2 = Reuters21578DAO.selectRandomList(10);
    assertThat(data2.size(), equalTo(10));

    assertThat(data1.get(0).getNewid(), not(equalTo(data2.get(0).getNewid())));

  }

  // @Test
  public void testSelectModApte() {

    List<Reuters21578> data = Reuters21578DAO.selectModApte("TRAIN", true);
    assertThat(data.size(), equalTo(9603));

    data = Reuters21578DAO.selectModApte("TEST", true);
    assertThat(data.size(), equalTo(3299));

    data = Reuters21578DAO.selectModApte("TRAIN", false);
    assertThat(data.size(), equalTo(5065));

    data = Reuters21578DAO.selectModApte("TEST", false);
    assertThat(data.size(), equalTo(2889));
  }

  @Test
  public void testSelectSingle() {

    Reuters21578 reuters21578 = Reuters21578DAO.selectSingle(1);
    assertThat(reuters21578.getNewid(), equalTo(1));
    assertThat(reuters21578.getTopics(), equalTo("cocoa"));
    assertThat(reuters21578.getPlaces(), equalTo("el-salvador,usa,uruguay"));

  }
}
