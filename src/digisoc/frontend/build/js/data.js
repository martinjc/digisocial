/*global google root_url static_url console*/

var map;

function roundNumber(rnum, rlength) {
    var newnumber = Math.round(rnum * Math.pow(10, rlength)) / Math.pow(10, rlength);
    return newnumber;
}

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
    var start_date_val = $('#from_date').prop('value');
    var end_date = $('#to_date').prop('valueAsNumber');
    var end_date_val = $('#to_date').prop('value');
    console.log(start_date);
    console.log(start_date_val);
    console.log(end_date);
    console.log(end_date_val);
    if(end_date < start_date) {
        console.log('Date selection Error');
        show_error_message('Date selection error - Start date must be before end date!');
        $('#from-date-group').addClass('error');
        $('#to-date-group').addClass('error');
    }
    else if(end_date_val === '' || start_date_val === '') {
        console.log('No Date selection Error');
        show_error_message('Date selection error - No start or end date selected!');
        $('#from-date-group').addClass('error');
        $('#to-date-group').addClass('error');
    }
    else {
        var start = start_date_val.split('-');
        var end = end_date_val.split('-');
        var sy = start[0];
        var sm = start[1];
        var ey = end[0];
        var em = end[1];
        console.log(start);
        console.log(end);
        var bounds = map.getBounds();
        var ne = bounds.getNorthEast();
        var sw = bounds.getSouthWest();
        console.log(map.getBounds());
        var point_count = {};
        var url = root_url + '/api/crimes/?ne=' + ne.lat() + ',' + ne.lng() + '&sw=' + sw.lat() + ',' + sw.lng() + '&sy=' + sy + '&sm=' + sm + '&ey=' + ey + '&em=' + em;
        console.log(url);
        $.getJSON(url, {}, function(data) {
            var crimes = data.crimes;
            for(var i in crimes){
                console.log(crimes[i].crime.point);
            }
        });
    }
}


function DataMap(map_location) {

    var initial_location = new google.maps.LatLng(51.481307,-3.18049860);

    this.map_options = {
        zoom: 14,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    map = new google.maps.Map(map_location, this.map_options);

    // Try W3C Geolocation (Preferred)
    if(navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            initial_location = new google.maps.LatLng(position.coords.latitude,position.coords.longitude);
        });
    }

    map.setCenter(initial_location);
}


$(document).ready(function(){

    var map = new DataMap(document.getElementById("map-canvas"));

});
