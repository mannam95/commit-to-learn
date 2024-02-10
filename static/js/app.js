function onPageLoad() {
  console.log( "document loaded" );
  // var url = "http://127.0.0.1:8787/get_location_names"; // Use this if you are NOT using nginx which is first 7 tutorials
  // Use this if  you are using nginx. i.e tutorial 8 and onwards
  var url = "/get_dashboard_stats"; 
  $.get(url,function(data, status) {
      console.log("got response for get_location_names request");
      if(data) {
          console.log(data['stats']);

          var base64WeatherImage = "data:image/png;base64," + data['stats']['weather_stats'];
          var base64MAIImage = "data:image/png;base64," + data['stats']['maintenance_alert_stats'];
          var base64AirImage = "data:image/png;base64," + data['stats']['air_level_stats'];
          var base64FuelImage = "data:image/png;base64," + data['stats']['fuel_level_stats'];

          //weather_stats
          $("#weather_stats").attr("src", base64WeatherImage);

          //fuel_level_stats
          $("#fuel_level_stats").attr("src", base64FuelImage);

          //maintenance_alert_stats
          $("#maintenance_stats").attr("src", base64MAIImage);

          //air_quality_stats
          $("#air_level_stats").attr("src", base64AirImage);

      }
  });
}

window.onload = onPageLoad;
