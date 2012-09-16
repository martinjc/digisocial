/*global google root_url static_url console*/

var map;

var heatmaps = [];
var food_markers = [];

function roundNumber(rnum, rlength) {
    var newnumber = Math.round(rnum * Math.pow(10, rlength)) / Math.pow(10, rlength);
    return newnumber;
}

function show_error_message(message) {
    var html = '<div class="alert alert-block alert-error fade in" id="error-msg"><button type="button" class="close" data-dismiss="alert">&times;</button><h4>Oh No!</h4>' + message + '</div>';
    $('#error-msg').html(html);
}

function clear_map() {
    for(var i in heatmaps) {
        heatmaps[i].setMap(null);
    }
    heatmaps = [];
    for(var i in food_markers) {
        food_markers[i].setMap(null);
    }
    food_markers = [];
}

function get_outcome_data(start_date_val, end_date_val) {
    var start = start_date_val.split('-');
    var end = end_date_val.split('-');
    var sy = start[0];
    var sm = start[1];
    var ey = end[0];
    var em = end[1];
    var bounds = map.getBounds();
    var ne = bounds.getNorthEast();
    var sw = bounds.getSouthWest();
    var url = root_url + '/api/outcomes/?ne=' + ne.lat() + ',' + ne.lng() + '&sw=' + sw.lat() + ',' + sw.lng() + '&sy=' + sy + '&sm=' + sm + '&ey=' + ey + '&em=' + em;
    console.log(url);
    var map_data = [];
    $.getJSON(url, {}, function(data) {
        var outcomes = data.outcomes;
        for(var i in outcomes){
            var lat = roundNumber(outcomes[i].outcome.point.lat, 5);
            var lng = roundNumber(outcomes[i].outcome.point.lng, 5);
            map_data.push({location: new google.maps.LatLng(lat, lng), weight: outcomes[i].outcome.severity});
        }
        var pointArray = new google.maps.MVCArray(map_data);
        var heatmap = new google.maps.visualization.HeatmapLayer({
            data:pointArray,
            opts:{"radius":30, "visible":true, "opacity":60}

        });
        heatmap.setMap(map);
        var gradient = [
          'rgba(0, 255, 255, 0)',
          'rgba(0, 255, 255, 1)',
          'rgba(0, 191, 255, 1)',
          'rgba(0, 127, 255, 1)',
          'rgba(0, 63, 255, 1)',
          'rgba(0, 0, 255, 1)',
          'rgba(0, 0, 223, 1)',
          'rgba(0, 0, 191, 1)',
          'rgba(0, 0, 159, 1)',
          'rgba(0, 0, 127, 1)',
          'rgba(63, 0, 91, 1)',
          'rgba(127, 0, 63, 1)',
          'rgba(191, 0, 31, 1)',
          'rgba(255, 0, 0, 1)'
        ];
        heatmap.setOptions({
          gradient: heatmap.get('gradient') ? null : gradient
        });
        heatmaps.push(heatmap);
        $('.overlay').addClass('hidden');
    });
}

function get_food_data() {
    var bounds = map.getBounds();
    var ne = bounds.getNorthEast();
    var sw = bounds.getSouthWest();
    var url = root_url + '/api/food/?ne=' + ne.lat() + ',' + ne.lng() + '&sw=' + sw.lat() + ',' + sw.lng();
    console.log(url);
    $.getJSON(url, {}, function(data) {
        var establishments = data.establishments;
        for(var i in establishments){
            var lat = roundNumber(establishments[i].Latitude, 5);
            var lng = roundNumber(establishments[i].Longitude, 5);
            var severity = parseInt(establishments[i].RatingValue);
            var image = new google.maps.MarkerImage(
                static_url + "img/" + severity + ".png",
                new google.maps.Size(32, 32),
                new google.maps.Point(0, 0),
                new google.maps.Point(16, 32),
                new google.maps.Size(24,24)
            );
            var marker = new google.maps.Marker({
                position: new google.maps.LatLng(lat, lng),
                map: map,
                title: establishments[i].BusinessName,
                icon: image
            });
            food_markers.push(marker);
        }
        $('.overlay').addClass('hidden');
    });
}

function get_crime_data(start_date_val, end_date_val) {
    var start = start_date_val.split('-');
    var end = end_date_val.split('-');
    var sy = start[0];
    var sm = start[1];
    var ey = end[0];
    var em = end[1];
    var bounds = map.getBounds();
    var ne = bounds.getNorthEast();
    var sw = bounds.getSouthWest();
    var url = root_url + '/api/crimes/?ne=' + ne.lat() + ',' + ne.lng() + '&sw=' + sw.lat() + ',' + sw.lng() + '&sy=' + sy + '&sm=' + sm + '&ey=' + ey + '&em=' + em;
    console.log(url);
    var map_data = [];
    $.getJSON(url, {}, function(data) {
        var crimes = data.crimes;
        for(var i in crimes){
            var lat = roundNumber(crimes[i].crime.point.lat, 5);
            var lng = roundNumber(crimes[i].crime.point.lng, 5);
            map_data.push({location: new google.maps.LatLng(lat, lng), weight: crimes[i].crime.severity});
        }
        var pointArray = new google.maps.MVCArray(map_data);
        var heatmap = new google.maps.visualization.HeatmapLayer({
            data:pointArray,
            opts:{"radius":30, "visible":true, "opacity":60}
        });
        heatmap.setMap(map);
        heatmaps.push(heatmap);
    });
    $('.overlay').addClass('hidden');
}

function show_date_error(error_msg) {
        show_error_message(error_msg);
        $('#from-date-group').addClass('error');
        $('#to-date-group').addClass('error');
}

function reset_error_state() {
    $('#error-msg').html('');
    $('#from-date-group').removeClass('error');
    $('#to-date-group').removeClass('error');
}

function validate(document) {
    $('.overlay').removeClass('hidden');
    // reset form
    reset_error_state();
    // reset map
    clear_map();

    // get start_date and end_date
    var start_date = $('#from_date').prop('valueAsNumber');
    var start_date_val = $('#from_date').prop('value');
    var end_date = $('#to_date').prop('valueAsNumber');
    var end_date_val = $('#to_date').prop('value');

    // basic validation on dates
    if(end_date < start_date) {
        show_date_error('Date selection error - Start date must be before end date!');
    }
    else if(end_date_val === '' || start_date_val === '') {
        show_date_error('Date selection error - No start or end date selected!');
    }
    else {
        // decide which data to show
        if($('#crime-data').attr('checked')) {
            console.log('crime-data checked');
            get_crime_data(start_date_val, end_date_val);
        }
        if($('#outcome-data').attr('checked')) {
            console.log('outcome-data checked');
            get_outcome_data(start_date_val, end_date_val);
        }
        if($('#food-data').attr('checked')) {
            console.log('food-data checked');
            get_food_data();
        }

    }
    google.maps.event.addListener(map, 'idle', function(){
        validate($(document));
    });
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
    $('.overlay').addClass('hidden');
}


$(document).ready(function(){

    var data_map = new DataMap(document.getElementById("map-canvas"));

});
