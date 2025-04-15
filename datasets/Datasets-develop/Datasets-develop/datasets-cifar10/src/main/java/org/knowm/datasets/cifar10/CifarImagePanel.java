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
package org.knowm.datasets.cifar10;

import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.geom.AffineTransform;
import java.awt.image.AffineTransformOp;
import java.awt.image.BufferedImage;

import javax.swing.JPanel;

/**
 * @author alexnugent
 */
public class CifarImagePanel extends JPanel {

  private BufferedImage image;

  public CifarImagePanel(int[][] red, int[][] green, int[][] blue, int scale) {

    image = new BufferedImage(red.length * scale, red[0].length * scale, BufferedImage.TYPE_INT_RGB);

    for (int y = 0; y < red.length; y++) {
      for (int x = 0; x < red[0].length; x++) {
        int value = red[y][x] << 16 | green[y][x] << 8 | blue[y][x];
        image.setRGB(x, y, value);
      }
    }
    scale(scale);

    setPreferredSize(new Dimension(red.length * scale, red[0].length * scale));
  }

  public CifarImagePanel(int[][][] rgb, int scale) {

    image = new BufferedImage(rgb.length * scale, rgb[0].length * scale, BufferedImage.TYPE_INT_RGB);

    for (int y = 0; y < rgb.length; y++) {
      for (int x = 0; x < rgb[0].length; x++) {
        int value = rgb[y][x][0] << 16 | rgb[y][x][1] << 8 | rgb[y][x][2];
        image.setRGB(x, y, value);
      }
    }
    scale(scale);

    setPreferredSize(new Dimension(rgb.length * scale, rgb[0].length * scale));
  }

  private void scale(int scale) {

    int w = image.getWidth();
    int h = image.getHeight();
    BufferedImage after = new BufferedImage(w, h, BufferedImage.TYPE_INT_ARGB);
    AffineTransform at = new AffineTransform();
    at.scale(scale, scale);
    AffineTransformOp scaleOp = new AffineTransformOp(at, AffineTransformOp.TYPE_BILINEAR);
    after = scaleOp.filter(image, after);

    this.image = after;

  }

  @Override
  public void paintComponent(Graphics g) {

    super.paintComponent(g);
    g.drawImage(image, 0, 0, null); // see javadoc for more info on the parameters
  }

}
