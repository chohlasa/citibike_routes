// Mapstyling
 var mapCSS = {
   population: "#vis_data { polygon-opacity: 0.8; line-color: #DDD; line-width: 0.25; line-opacity: 1; polygon-fill: #B10026; } #vis_data [ total_population <= 1767] {   polygon-fill: #B10026;}#vis_data [ total_population <= 1034] {   polygon-fill: #E31A1C;}#vis_data [ total_population <= 684] {   polygon-fill: #FC4E2A;}#vis_data [ total_population <= 559] {   polygon-fill: #FD8D3C;}#vis_data [ total_population <= 375] {   polygon-fill: #FEB24C;}#vis_data [ total_population <= 200] {   polygon-fill: #FED976;}#vis_data [ total_population <= 182] {   polygon-fill: #FFFFB2;}#vis_data [ total_population <= 15] {   polygon-fill: #BBB;}"
,
   density: "#vis_data{  polygon-opacity: 0.8;  line-color: #DDD;  line-width: 0.5;  line-opacity: 1;} #vis_data [ total_population <= 75.724159016339] {   polygon-fill: #B10026;} #vis_data [ total_population <= 42.6821497291779] {   polygon-fill: #E31A1C;}#vis_data [ total_population <= 30.8545416849473] {   polygon-fill: #FC4E2A;}#vis_data [ total_population <= 20.491274339861] {   polygon-fill: #FD8D3C;}#vis_data [ total_population <= 15.09629362344672] {   polygon-fill: #FEB24C;}#vis_data [ total_population <= 12.60580181990758] {   polygon-fill: #FED976;}#vis_data [ total_population <= 10.57900798530735] {   polygon-fill: #FFFFB2;}#vis_data [ total_population <= 2.40798530735] {   polygon-fill: #BBB;}"
 };
var styles = [{"stylers":[{"saturation":-100}]},{"featureType":"water","stylers":[{"gamma":1.67},{"lightness":27}]},{"elementType":"geometry","stylers":[{"gamma":1.31},{"lightness":12}]},{"featureType":"administrative","elementType":"labels","stylers":[{"lightness":51},{"gamma":0.94}]},{},{"featureType":"road","elementType":"labels","stylers":[{"lightness":0}]},{"featureType":"poi","elementType":"labels","stylers":[{"lightness":42}]}]


// Set height of header spacer
$('.spacer').height(function() { return $('#header').outerHeight(true) - 20; });
var map;

// Setup map
 function initialize() {
   var mapOptions = {
     center: new google.maps.LatLng(40.722, -73.99),
     zoom: 13
   };
   map = new google.maps.Map(document.getElementById("bike_map"),
				 mapOptions);

   map.setOptions({styles: styles, minZoom: 13, maxZoom:17, scrollwheel:false});

   cartodb.createLayer(map, 'http://chohlasa.cartodb.com/api/v2/viz/4b86adf8-c8c0-11e3-adb2-0e73339ffa50/viz.json')
          .addTo(map)
          .on('done', function(layer) {
     var sublayer = layer.getSubLayer(0);
   })
		  .on('error', function() {
     cartodb.log.log("some error occurred");
   });
   
}

google.maps.event.addDomListener(window, 'load', initialize);

$('.Fst_Ave').click(function() {
    map.panTo(new google.maps.LatLng(40.727011, -73.986203));
    map.setZoom(16);
});

$('.Broadway').click(function() {
    map.panTo(new google.maps.LatLng(40.749203, -73.986420));
    map.setZoom(16);
});

$('.Eth_Ave').click(function() {
    map.panTo(new google.maps.LatLng(40.747790, -73.998584));
    map.setZoom(16);
});

$('.HRG').click(function() {
    map.panTo(new google.maps.LatLng(40.729574, -74.007027));
    map.setZoom(15);
});

$('.FrtySnd').click(function() {
    map.panTo(new google.maps.LatLng(40.752373, -73.978610));
    map.setZoom(16);
});

$('.Seventh').click(function() {
    map.panTo(new google.maps.LatLng(40.746960, -73.993158));
    map.setZoom(16);
});

$('.Pearl').click(function() {
    map.panTo(new google.maps.LatLng(40.709166, -74.000674));
    map.setZoom(16);
});

$('.Third').click(function() {
    map.panTo(new google.maps.LatLng(40.727435, -73.993968));
    map.setZoom(16);
});
