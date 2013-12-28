$(document).ready(function(){
	if (navigator.geolocation){
		navigator.geolocation.getCurrentPosition( getWeatherInfo );
	}else{
		debug.log( "geoLocation not supported." );
	}
});
