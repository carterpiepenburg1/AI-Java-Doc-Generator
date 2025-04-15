/**
 * (The MIT License)
 *
 * <p>Copyright 2015-2017 Knowm Inc. (http://knowm.org) and contributors. Copyright 2013-2015 Xeiam
 * LLC (http://xeiam.com) and contributors.
 *
 * <p>Permission is hereby granted, free of charge, to any person obtaining a copy of this software
 * and associated documentation files (the "Software"), to deal in the Software without restriction,
 * including without limitation the rights to use, copy, modify, merge, publish, distribute,
 * sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * <p>The above copyright notice and this permission notice shall be included in all copies or
 * substantial portions of the Software.
 *
 * <p>THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
 * BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
 * DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */
/**
 * This product currently only contains code developed by authors of specific components, as
 * identified by the source code files.
 *
 * <p>Since product implements StAX API, it has dependencies to StAX API classes.
 *
 * <p>For additional credits (generally to people who reported problems) see CREDITS file.
 */
package org.knowm.datasets.censusincome;

import static org.hamcrest.CoreMatchers.equalTo;
import static org.hamcrest.MatcherAssert.assertThat;

import org.junit.AfterClass;
import org.junit.BeforeClass;
import org.junit.Ignore;
import org.junit.Test;
import org.knowm.yank.PropertiesUtils;
import org.knowm.yank.Yank;

/** @author timmolter */
@Ignore
public class TestCensusIncomeDAO {

  @BeforeClass
  public static void setUpDB() {

    Yank.setupDefaultConnectionPool(
        PropertiesUtils.getPropertiesFromClasspath("DB_HSQLDB_FILE.properties"));
  }

  @AfterClass
  public static void tearDownDB() {

    CensusIncomeDAO.release();
  }

  @Test
  public void testSelectCount() {

    long count = CensusIncomeDAO.selectCount();
    assertThat(count, equalTo(48842L));
  }
}
