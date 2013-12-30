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
	    $("#submit-todo").attr('disabled','disabled');
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
				var item = "<p class='item' id='msg-" + data.record.id + "' style='display:none;'>" + data.record.timestamp + " - " + data.record.message + "</p>";
				console.debug(item);
				if( $("#todos .item").length < 1 ){
				   $("#todos").append(item);
				}else{
				   $("#todos .item:first").before(item);
				}

                $("#todos .item:first").slideDown('fast', function(){
                    $("#toDoForm textarea").val('');
                    $("#submit-todo").delay(2000).queue(function() {
                        $(this).removeAttr('disabled');
                    });
                });
			},
			error : function (data) {
			    console.debug("there was an error");
			    $(this).attr('disabled', '');
			}
		});
	});
});
