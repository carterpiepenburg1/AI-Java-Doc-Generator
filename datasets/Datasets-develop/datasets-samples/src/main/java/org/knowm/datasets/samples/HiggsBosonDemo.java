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
package org.knowm.datasets.samples;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

import org.knowm.datasets.common.data.HistogramDataInspector;
import org.knowm.datasets.higgsboson.HiggsBoson;
import org.knowm.datasets.higgsboson.HiggsBosonDAO;

/**
 * @author timmolter
 */
public class HiggsBosonDemo extends HistogramDataInspector<HiggsBoson> {

  public static void main(String[] args) {

    try {
      HiggsBosonDAO.init("/usr/local/Datasets"); // setup data

      HiggsBosonDemo higgsBosonInspector = new HiggsBosonDemo();
      higgsBosonInspector.go();

    } catch (Exception e) {
      e.printStackTrace();
    } finally {
      HiggsBosonDAO.release(); // release data resources
    }
  }

  @Override
  public List<HiggsBoson> getFirstSamples() {

    return HiggsBosonDAO.selectSignal();
  }

  @Override
  public List<HiggsBoson> getSecondSamples() {

    return HiggsBosonDAO.selectBackground();
  }

  @Override
  public String getFirstLabel() {

    return "Signal";
  }

  @Override
  public String getSecondLabel() {

    return "Background";
  }

  /**
   * Overriding this to weed out the -999.0 values in the dataset
   */
  @Override
  public void addToMap(Map<String, String> properties, Map<String, List<Float>> rawHistogramData) {

    // System.out.println(Arrays.toString(properties.entrySet().toArray()));0
    for (Entry<String, String> entrySet : properties.entrySet()) {

      String key = entrySet.getKey();
      String value = entrySet.getValue();

      try {

        Float floatValue = Float.parseFloat(value);
        if (floatValue > -900.0f) {
          List<Float> rawDataForSingleProperty = rawHistogramData.get(key);
          if (rawDataForSingleProperty == null) {
            rawDataForSingleProperty = new ArrayList<Float>();
          }
          rawDataForSingleProperty.add(floatValue);
          rawHistogramData.put(key, rawDataForSingleProperty);
        }
      } catch (NumberFormatException e) {
        // wasn't a float, skip.
      }
    }
  }
}
