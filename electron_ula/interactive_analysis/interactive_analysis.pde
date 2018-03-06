PImage img;
boolean zoomed = false; // true to show 1:1 zoom
boolean drawing_segment = false;
int imgX = 0, imgY = 0; // center point of window
int mouseClickX = 0, mouseClickY = 0; // last click point
boolean changed = false;

ArrayList<GridLine> gridlines = new ArrayList();
GridLine gridline = null, // gridline currently being entered
  closest_gridline = null; // gridline closest to the cursor

void save_data() {
  JSONObject data = new JSONObject();
  JSONArray a = new JSONArray();
  for (GridLine gl : gridlines) {
    JSONObject o = gl.asJson();
    a.append(o);
  }
  data.setJSONArray("gridlines", a);
  saveJSONObject(data, "../manual_features.json");
}

void load_data() {
  JSONObject data = loadJSONObject("../manual_features.json");
  JSONArray gls = data.getJSONArray("gridlines");
  for (int i = 0; i < gls.size(); ++i) {
    print("add gridline ", i, "\n");
    gridlines.add(new GridLine(gls.getJSONObject(i)));
  }
}

void setup() {
  size(800, 600);
  surface.setResizable(true);
  changed = true;
  
  load_data();
  
  print("loading image\n");
  //img = new PImage(8000, 8000);
  img = loadImage("../ElectronULA_32mm_1.5X_GX7_DxO.png");
  print("loaded image\n");
}

void draw() {
  if (!changed) return;
  changed = false;
  
  if (zoomed) {
    // showing at 1:1 scale
    pushMatrix();
    translate(-imgX, -imgY);
    image(img, 0, 0);
    
    int ptrX = imgX + mouseX, ptrY = imgY + mouseY;
    
    // draw all saved gridlines
    stroke(color(255, 0, 0));
    closest_gridline = null;
    for (GridLine gl : gridlines) {
      if (gl.distFrom(ptrX, ptrY) < 10.0) {
        strokeWeight(3);
        closest_gridline = gl;
      } else {
        strokeWeight(1);
      }
      line(gl.x0, gl.y0, gl.x1, gl.y1);
    }
    // draw the gridline we're entering right now
    if (drawing_segment) {
      strokeWeight(3);
      line(gridline.x0, gridline.y0, gridline.x1, gridline.y1);
    }
    strokeWeight(1);
    popMatrix();
    
    // draw mouse crosshairs
    stroke(color(0, 0, 255));
    line(0, mouseY, width, mouseY);
    line(mouseX, 0, mouseX, height);
  } else {
    // entire image view
    float x_scale = (float)width / (float)img.width;
    float y_scale = (float)height / (float)img.height;
    float actual_scale = min(x_scale, y_scale);
    
    // plot full image
    pushMatrix();
    scale(actual_scale);
    translate(0, 0);
    image(img, 0, 0);
    popMatrix();

    // draw the gridline we're entering right now
    if (drawing_segment) {
      strokeWeight(3);
      line(gridline.x0, gridline.y0, gridline.x1, gridline.y1);
      strokeWeight(1);
    }

    // calculate new position
    imgX = (int)((float)mouseX / actual_scale) - width/2;
    imgY = (int)((float)mouseY / actual_scale) - height/2;
    
    // draw box around where we'll end up if we zoom in now
    stroke(color(255, 0, 0));
    float w = width/2 * actual_scale,
          h = height/2 * actual_scale;
    line(mouseX - w/2, mouseY - h/2, mouseX + w/2, mouseY - h/2);
    line(mouseX - w/2, mouseY + h/2, mouseX + w/2, mouseY + h/2);
    line(mouseX - w/2, mouseY - h/2, mouseX - w/2, mouseY + h/2);
    line(mouseX + w/2, mouseY - h/2, mouseX + w/2, mouseY + h/2);
  }
}

void mouseMoved() {
  changed = true;
  if (drawing_segment) {
    gridline.x1 = imgX + mouseX;
    gridline.y1 = imgY + mouseY;
  }
}

void mousePressed() {
  changed = true;
  mouseClickX = mouseX;
  mouseClickY = mouseY;
}

double dist(int x0, int y0, int x1, int y1) {
  return Math.sqrt((x1 - x0) * (x1 - x0) + (y1 - y0) * (y1 - y0)); 
}

void mouseDragged() {
  if (!zoomed) return;
  changed = true;
  
  int ptrX = mouseX + imgX, ptrY = mouseY + imgY;
  
  if (!drawing_segment && closest_gridline != null) {
    // move gridline we're close to
    if (dist(ptrX, ptrY, closest_gridline.x0, closest_gridline.y0) < dist(ptrX, ptrY, closest_gridline.x1, closest_gridline.y1)) {
      closest_gridline.x0 += mouseX - mouseClickX;
      closest_gridline.y0 += mouseY - mouseClickY;
    } else {
      closest_gridline.x1 += mouseX - mouseClickX;
      closest_gridline.y1 += mouseY - mouseClickY;
    }
  } else {
    // move image
    imgX -= mouseX - mouseClickX;
    imgY -= mouseY - mouseClickY;
  }
  mouseClickX = mouseX;
  mouseClickY = mouseY;
}

void keyPressed() {
  if (key == ESC) {
    // save and quit
    save_data();
  } else if (key == ' ') {
    zoomed = !zoomed;
  } else if (key == 's' && zoomed) {
    if (drawing_segment) {
      drawing_segment = false;
      gridlines.add(gridline);
      gridline = null;
    } else {
      drawing_segment = true;
      gridline = new GridLine(imgX + mouseX, imgY + mouseY);
    }
  } else if (key == 'z') {
    if (drawing_segment) {
      drawing_segment = false;
    } else {
      gridlines.remove(gridlines.size() - 1);
    }
  }
  changed = true;
}