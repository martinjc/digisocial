/*global google root_url static_url console HeatmapOverlay*/

var map;
var heatmap;

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
        var points = {};
        var hmap_data = {};
        var url = root_url + '/api/crimes/?ne=' + ne.lat() + ',' + ne.lng() + '&sw=' + sw.lat() + ',' + sw.lng() + '&sy=' + sy + '&sm=' + sm + '&ey=' + ey + '&em=' + em;
        console.log(url);
        $.getJSON(url, {}, function(data) {
            var crimes = data.crimes;
            for(var i in crimes){
                var lat = roundNumber(crimes[i].crime.point.lat, 5);
                var lng = roundNumber(crimes[i].crime.point.lng, 5);
                var point = lat + ',' + lng;
                if (points[point] === undefined) {
                    points[point] = 1;
                } else {
                    points[point] = points[point] + 1;
                }
            }
            console.log(points);
            for(var i in crimes) {
                var lat = roundNumber(crimes[i].crime.point.lat, 5);
                var lng = roundNumber(crimes[i].crime.point.lng, 5);
                var p = lat + ',' + lng;
                var count = points[p];
                heatmap.addDataPoint(lat, lng, count);
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

    heatmap = new HeatmapOverlay(map, {"radius":1, "visible":true, "opacity":60});
    var testData={max: 6, data: [{lat: 51.466, lng:-3.18383, count: 4},{lat: 51.479, lng:-3.15653, count: 6},{lat: 51.482, lng:-3.16588, count: 1}]};

    google.maps.event.addListener(map, "idle", function(){
        heatmap.setDataSet(testData);
    });
}


$(document).ready(function(){

    var map = new DataMap(document.getElementById("map-canvas"));

});
