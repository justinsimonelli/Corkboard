function getWeatherInfo( location ){
	var lat = location.coords.latitude,
		lng = location.coords.longitude,
		now = new Date().getTime(),
		cookieVal = getCookie( 'weatherFetchedTimestamp' ),
		textObj = $("#weather > #location");

	if( !isBlank( cookieVal ) && ( now <= cookieVal ) ){
		var weather = getStorageVal('local', 'weatherData'),
			weatherJson;

		if( !isBlank(weather) )
		{
			weatherJson = JSON.parse( weather );
			$(textObj).fadeOut(200, function(){
				console.debug( weatherJson );
				$(this).html("Right now, it's " + weatherJson.current.data.summary + ", with a temperature of ");
				generateForecast(weatherJson);
			}).fadeIn(200);
		}

	}else{
		debug.log("fetching new weather data");
		$.ajax({
			url : WEATHER_API_URL + lat + '/' + lng + '/',
			dataType : 'json',
			success: function (data) {
				console.debug( data );
				$(textObj).fadeOut(200, function(){
					$(this).html( "Right now, it's " + data.current.data.summary );
					generateForecast(data);
				}).fadeIn(200);
				setStorageVal( 'local', 'weatherData', JSON.stringify(data) );
				setCookie( 'weatherFetchedTimestamp', null, 15 );
			},
			error : function (data) { errorFunction(data) }
		});
	}
}

function getCookie(name) {
  var parts = document.cookie.split(name + "=");
  if (parts.length == 2){
  	return parts.pop().split(";").shift();
  }
}

//params = name, now (currentDate to create cookie from), exp( expiration date in minutes )
function setCookie(name, value, exp)
{
	var exdate = new Date();
	exdate.setTime( exdate.getTime() + (exp * 1000 * 60) );
	var c_value = exdate.getTime();
	debug.log( name + "=" + c_value );
	document.cookie=name + "=" + c_value;
}

function getStorageVal(type, name) {
  var storage = window[type + 'Storage'];
  //return right away, not supported
  if (!storage) return;

  return storage.getItem( name );

 }

function setStorageVal( type, key, val ){
	var storage = window[type + 'Storage'];
	if (!storage) return;

	storage.setItem( key, val );

}

function generateForecast( data ){
	var days = data.daily.data,
		date,
		day,
		dayText,
		high,
		low;

	for( x in days ){
		day = days[x],
		date = new Date();
		date.setTime((day.time) * 1000),
		high = parseInt(day.temperatureMax),
		low = parseInt(day.temperatureMin);

		if( x <= 3 ){//only show 3 days
			if( x == 0 ){
				dayText = 'Today';
			}else{
				dayText = DAYS_OF_WEEK[date.getDay()];
			}
			dayText += " - " + day.summary + ". High: " + high + "&deg;, Low: " + low + "&deg;. " ;

			if( !isBlank(day.precipType) ){
				dayText += "Chance of " + day.precipType + ": " + ( parseFloat( day.precipProbability ) * 100 ) + "%";
			}

			$("#forecast").append( "<p>" + dayText +"</p>" );
		}
	}
}

function isBlank(str) {
    return (!str || /^\s*$/.test(str));
}

function errorFunction( data ){
	console.debug( data );
}

(function($) {
$.fn.serializeFormJSON = function() {

   var o = {};
   var a = this.serializeArray();
   $.each(a, function() {
       if (o[this.name]) {
           if (!o[this.name].push) {
               o[this.name] = [o[this.name]];
           }
           o[this.name].push(this.value || '');
       } else {
           o[this.name] = this.value || '';
       }
   });
   return o;
};
})(jQuery);