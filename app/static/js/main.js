$(document).ready(function(){
    var locationEnabled = "false";
	if (navigator.geolocation){
		navigator.geolocation.getCurrentPosition( getWeatherInfo );
		locationEnabled = "true"
	}else{
		debug.log( "geoLocation not supported." );
	}

	$("#new-todo").click(function(e){
	    e.preventDefault();
	    $("#todo-block").slideToggle("fast");
	});

	$("#toDoForm").submit(function(e){
	    e.preventDefault();
	    var postData = $(this).serializeFormJSON();
	    console.debug(postData);
	    $.ajax({
			url : '/corkboard/api/v1/todos/add/',
			contentType: 'application/json;charset=UTF-8',
			type    :   'POST',
			dataType :  'json',
			data    :   JSON.stringify(postData),
			success: function (data) {
				console.debug( data );
			},
			error : function (data) { console.debug("there was an error"); }
		});
	});
});
