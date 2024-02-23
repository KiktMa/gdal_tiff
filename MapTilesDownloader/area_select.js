const viewer = new Cesium.Viewer("cesiumContainer", {
  timeline: false,
  animation: false,
  sceneModePicker: false,
  baseLayerPicker: false,
});

// The globe does not need to be displayed,
// since the Photorealistic 3D Tiles include terrain
viewer.scene.globe.show = false;

// Add Photorealistic 3D Tiles
try {
  const tileset = await Cesium.createGooglePhotorealistic3DTileset();
  viewer.scene.primitives.add(tileset);
} catch (error) {
  console.log(`Error loading Photorealistic 3D Tiles tileset.
  ${error}`);
}

// Point the camera at the Googleplex
//viewer.scene.camera.setView({
//  destination: new Cesium.Cartesian3(
//    -2693797.551060477,
//    -4297135.517094725,
//    3854700.7470414364
//  ),
//  orientation: new Cesium.HeadingPitchRoll(
//    4.6550106925119925,
//    -0.2863894863138836,
//    1.3561760425773173e-7
//  ),
//}); 

viewer.scene.debugShowFramesPerSecond = true;
viewer.scene.screenSpaceCameraController.enableTranslate = false;
//viewer.scene.screenSpaceCameraController.enableTilt = false;
viewer.scene.screenSpaceCameraController.enableLook = false;
viewer.scene.screenSpaceCameraController.enableCollisionDetection = false;
viewer.imageryLayers.get(0).brightness = 0.7;

var selector;
var rectangleSelector = new Cesium.Rectangle();
var screenSpaceEventHandler = new Cesium.ScreenSpaceEventHandler(viewer.scene.canvas);
var cartesian = new Cesium.Cartesian3();
var tempCartographic = new Cesium.Cartographic();
var center = new Cesium.Cartographic();
var firstPoint = new Cesium.Cartographic();
var firstPointSet = false;
var mouseDown = false;
var camera = viewer.camera;
var left_bottom = new Cesium.Cartographic(0, 0, 0);
var right_top = new Cesium.Cartographic(0, 0, 0);

//Draw the selector while the user drags the mouse while holding shift
screenSpaceEventHandler.setInputAction(function drawSelector(movement) {
  if (!mouseDown) {
    return;
  }

  cartesian = camera.pickEllipsoid(movement.endPosition, viewer.scene.globe.ellipsoid, cartesian);

  if (cartesian) {
    //mouse cartographic
    tempCartographic = Cesium.Cartographic.fromCartesian(cartesian, Cesium.Ellipsoid.WGS84, tempCartographic);

    if (!firstPointSet) {
      Cesium.Cartographic.clone(tempCartographic, firstPoint);
      firstPointSet = true;
    }
    else {
      rectangleSelector.east = Math.max(tempCartographic.longitude, firstPoint.longitude);
      rectangleSelector.west = Math.min(tempCartographic.longitude, firstPoint.longitude);
      rectangleSelector.north = Math.max(tempCartographic.latitude, firstPoint.latitude);
      rectangleSelector.south = Math.min(tempCartographic.latitude, firstPoint.latitude);
      selector.show = true;
    }
  }
}, Cesium.ScreenSpaceEventType.MOUSE_MOVE, Cesium.KeyboardEventModifier.SHIFT);

var getSelectorLocation = new Cesium.CallbackProperty(function getSelectorLocation(time, result) {
    return Cesium.Rectangle.clone(rectangleSelector, result);
  }, false);

  screenSpaceEventHandler.setInputAction(function startClickShift() {
    mouseDown = true;
    selector.rectangle.coordinates = getSelectorLocation;
  }, Cesium.ScreenSpaceEventType.LEFT_DOWN, Cesium.KeyboardEventModifier.SHIFT);

  screenSpaceEventHandler.setInputAction(function endClickShift() {
    mouseDown = false;
    firstPointSet = false;
    selector.rectangle.coordinates = rectangleSelector;
    Cesium.Rectangle.southwest(rectangleSelector, left_bottom);
    Cesium.Rectangle.northeast(rectangleSelector, right_top);
    console.log('south: '+ Cesium.Math.toDegrees(left_bottom.latitude) + 'west: '+ Cesium.Math.toDegrees(left_bottom.longitude));
    console.log('north: '+ Cesium.Math.toDegrees(right_top.latitude) + 'east: '+ Cesium.Math.toDegrees(right_top.longitude));
    console.log(Cesium.Math.toDegrees(left_bottom.latitude) + ' '+ Cesium.Math.toDegrees(left_bottom.longitude) + ' ' + Cesium.Math.toDegrees(right_top.latitude)+ ' ' +   Cesium.Math.toDegrees(right_top.longitude));
  }, Cesium.ScreenSpaceEventType.LEFT_UP, Cesium.KeyboardEventModifier.SHIFT);


//Hide the selector by clicking anywhere
screenSpaceEventHandler.setInputAction(function hideSelector() {
  selector.show = false;
}, Cesium.ScreenSpaceEventType.LEFT_CLICK);


selector = viewer.entities.add({
  selectable: false,
  show: false,
  rectangle: {
    coordinates: getSelectorLocation,
    material: Cesium.Color.BLACK.withAlpha(0.5)
  }
});
