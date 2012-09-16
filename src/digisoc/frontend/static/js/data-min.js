/*global google root_url static_url console*/function roundNumber(e,t){var n=Math.round(e*Math.pow(10,t))/Math.pow(10,t);return n}function show_error_message(e){var t='<div class="alert alert-block alert-error fade in" id="error-msg"><button type="button" class="close" data-dismiss="alert">&times;</button><h4>Oh No!</h4>'+e+"</div>";$("#error-msg").html(t)}function clear_map(){var e;for(e in heatmaps)heatmaps[e].setMap(null);heatmaps=[];for(e in food_markers)food_markers[e].setMap(null);food_markers=[];$("#details").addClass("hidden")}function get_outcome_data(e,t){var n=e.split("-"),r=t.split("-"),i=n[0],s=n[1],o=r[0],u=r[1],a=map.getBounds(),f=a.getNorthEast(),l=a.getSouthWest(),c=root_url+"/api/outcomes/?ne="+f.lat()+","+f.lng()+"&sw="+l.lat()+","+l.lng()+"&sy="+i+"&sm="+s+"&ey="+o+"&em="+u,h=[];$.getJSON(c,{},function(e){var t,n,r,i,s,o,u=e.outcomes;for(t in u){n=roundNumber(u[t].outcome.point.lat,5);r=roundNumber(u[t].outcome.point.lng,5);h.push({location:new google.maps.LatLng(n,r),weight:u[t].outcome.severity})}i=new google.maps.MVCArray(h);s=new google.maps.visualization.HeatmapLayer({data:i,opts:{radius:30,visible:!0,opacity:60}});s.setMap(map);o=["rgba(0, 255, 255, 0)","rgba(0, 255, 255, 1)","rgba(0, 191, 255, 1)","rgba(0, 127, 255, 1)","rgba(0, 63, 255, 1)","rgba(0, 0, 255, 1)","rgba(0, 0, 223, 1)","rgba(0, 0, 191, 1)","rgba(0, 0, 159, 1)","rgba(0, 0, 127, 1)","rgba(63, 0, 91, 1)","rgba(127, 0, 63, 1)","rgba(191, 0, 31, 1)","rgba(255, 0, 0, 1)"];s.setOptions({gradient:s.get("gradient")?null:o});heatmaps.push(s);$(".overlay").addClass("hidden")})}function add_marker_click(e,t,n,r,i){google.maps.event.addListener(e,"click",function(){var e,s;$("#details").removeClass("hidden");$("#venue-name").html(r);$("#food-rating").html(i);e=root_url+"/api/crimeInArea/?lat="+t+"&lon="+n;$.getJSON(e,{},function(e){var t=e.num_crimes;$("#crime-numbers").html(t)});s=root_url+"/api/crimeIntensity/?lat="+t+"&lon="+n;$.getJSON(s,{},function(e){var t=e.crime_intensity;$("#crime-intensity").html(t)})})}function get_food_data(){var e=map.getBounds(),t=e.getNorthEast(),n=e.getSouthWest(),r=root_url+"/api/food/?ne="+t.lat()+","+t.lng()+"&sw="+n.lat()+","+n.lng();$.getJSON(r,{},function(e){var t,n,r,i,s,o,u,a=e.establishments;for(t in a){n=roundNumber(a[t].Latitude,5);r=roundNumber(a[t].Longitude,5);i=parseInt(a[t].RatingValue);s=a[t].BusinessName;o=new google.maps.MarkerImage(static_url+"img/"+i+".png",new google.maps.Size(32,32),new google.maps.Point(0,0),new google.maps.Point(16,32),new google.maps.Size(24,24));u=new google.maps.Marker({position:new google.maps.LatLng(n,r),map:map,title:s,icon:o});add_marker_click(u,n,r,s,i);food_markers.push(u)}$(".overlay").addClass("hidden")})}function get_crime_data(e,t){var n=e.split("-"),r=t.split("-"),i=n[0],s=n[1],o=r[0],u=r[1],a=map.getBounds(),f=a.getNorthEast(),l=a.getSouthWest(),c=root_url+"/api/crimes/?ne="+f.lat()+","+f.lng()+"&sw="+l.lat()+","+l.lng()+"&sy="+i+"&sm="+s+"&ey="+o+"&em="+u,h=[];$.getJSON(c,{},function(e){var t,n,r,i,s,o=e.crimes;for(t in o){n=roundNumber(o[t].crime.point.lat,5);r=roundNumber(o[t].crime.point.lng,5);h.push({location:new google.maps.LatLng(n,r),weight:o[t].crime.severity})}i=new google.maps.MVCArray(h);s=new google.maps.visualization.HeatmapLayer({data:i,opts:{radius:30,visible:!0,opacity:60}});s.setMap(map);heatmaps.push(s)});$(".overlay").addClass("hidden")}function show_date_error(e){show_error_message(e);$("#from-date-group").addClass("error");$("#to-date-group").addClass("error")}function reset_error_state(){$("#error-msg").html("");$("#from-date-group").removeClass("error");$("#to-date-group").removeClass("error")}function validate(e){var t,n,r,i;$(".overlay").removeClass("hidden");reset_error_state();clear_map();t=$("#from_date").prop("valueAsNumber");n=$("#from_date").prop("value");r=$("#to_date").prop("valueAsNumber");i=$("#to_date").prop("value");if(r<t)show_date_error("Date selection error - Start date must be before end date!");else if(i===""||n==="")show_date_error("Date selection error - No start or end date selected!");else{$("#crime-data").attr("checked")&&get_crime_data(n,i);$("#outcome-data").attr("checked")&&get_outcome_data(n,i);$("#food-data").attr("checked")&&get_food_data()}google.maps.event.addListener(map,"idle",function(){validate($(e))})}function DataMap(e){var t=new google.maps.LatLng(51.481307,-3.1804986);this.map_options={zoom:14,mapTypeId:google.maps.MapTypeId.ROADMAP};map=new google.maps.Map(e,this.map_options);navigator.geolocation&&navigator.geolocation.getCurrentPosition(function(e){t=new google.maps.LatLng(e.coords.latitude,e.coords.longitude)});map.setCenter(t);$(".overlay").addClass("hidden")}var map,heatmaps=[],food_markers=[];$(document).ready(function(){var e=new DataMap(document.getElementById("map-canvas"))});