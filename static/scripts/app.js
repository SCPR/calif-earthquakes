//begin main function
$(document).ready(function(){

    console.log('works');

	//path is to the python function
	$.getJSON($SCRIPT_ROOT + '/return_data_from_database', {
	}, function(data) {
		console.log(data);
	});

    return false;

});
//end main function
