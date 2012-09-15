/*global google root_url static_url console*/

function show_error_message(message) {
    var html = '<div class="alert alert-block alert-error fade in" id="error-msg"><button type="button" class="close" data-dismiss="alert">&times;</button><h4>Oh No!</h4>' + message + '</div>';
    $('#error-msg').html(html);
}

function validate(document) {
    // reset form
    $('#error-msg').html('');
    $('#from-date-group').removeClass('error');
    $('#to-date-group').removeClass('error');
    console.log('A FUCKING FORM!');
    var start_date = $('#from_date').prop('valueAsNumber');
    var end_date = $('#to_date').prop('valueAsNumber');
    console.log(start_date);
    console.log(end_date);
    if(end_date < start_date) {
        console.log('Date selection Error');
        show_error_message('Date selection error - Start date must be before end date!');
        $('#from-date-group').addClass('error');
        $('#to-date-group').addClass('error');
    }
}


function DataMap(map_location) {

    var initial_location = new google.maps.LatLng(51.481307,-3.18049860);

    this.map_options = {
        zoom: 14,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    this.map = new google.maps.Map(map_location, this.map_options);

    // Try W3C Geolocation (Preferred)
    if(navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            initial_location = new google.maps.LatLng(position.coords.latitude,position.coords.longitude);
        });
    }

    this.map.setCenter(initial_location);
}


$(document).ready(function(){

    var map = new DataMap(document.getElementById("map-canvas"));

});
