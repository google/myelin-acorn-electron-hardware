import processing.data.*;

class GridLine {
  public int x0, y0, x1, y1;
  
  GridLine(JSONObject j) {
    this.x0 = j.getInt("x0");
    this.y0 = j.getInt("y0");
    this.x1 = j.getInt("x1");
    this.y1 = j.getInt("y1");
  }
  
  GridLine(int x0, int y0, int x1, int y1) {
    this.x0 = x0;
    this.y0 = y0;
    this.x1 = x1;
    this.y1 = y1;
  }
  
  GridLine(int x0, int y0) {
    this.x0 = x0;
    this.y0 = y0;
    this.x1 = x0;
    this.y1 = y0;
  }
  
  double distFrom(int x, int y) {
    // calculate distance between (x, y) and the line
    if (this.x0 == this.x1) {
      // vertical line
      return Math.abs(x - this.x0);
    }
    if (this.y0 == this.y1) {
      // horizontal line
      return Math.abs(y - this.y0);
    }
    // diagonal line; use formula from https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line
    double yd = (double)(y1 - y0), xd = (double)(x1 - x0);
    return Math.abs(yd * (double)x - xd * (double)y + x1*y0 - y1*x0) / Math.sqrt(yd * yd + xd * xd);
  }
  
  JSONObject asJson() {
    JSONObject j = new JSONObject();
    j.setInt("x0", x0);
    j.setInt("y0", y0);
    j.setInt("x1", x1);
    j.setInt("y1", y1);
    return j;
  }
}