/*global google root_url static_url console HeatmapOverlay*/function roundNumber(e,t){var n=Math.round(e*Math.pow(10,t))/Math.pow(10,t);return n}function show_error_message(e){var t='<div class="alert alert-block alert-error fade in" id="error-msg"><button type="button" class="close" data-dismiss="alert">&times;</button><h4>Oh No!</h4>'+e+"</div>";$("#error-msg").html(t)}function validate(){var e,t,n,r,i,s,o,u,a,f,l,c,h,p,d,v;$("#error-msg").html("");$("#from-date-group").removeClass("error");$("#to-date-group").removeClass("error");console.log("A FUCKING FORM!");e=$("#from_date").prop("valueAsNumber");t=$("#from_date").prop("value");n=$("#to_date").prop("valueAsNumber");r=$("#to_date").prop("value");console.log(e);console.log(t);console.log(n);console.log(r);if(n<e){console.log("Date selection Error");show_error_message("Date selection error - Start date must be before end date!");$("#from-date-group").addClass("error");$("#to-date-group").addClass("error")}else if(r===""||t===""){console.log("No Date selection Error");show_error_message("Date selection error - No start or end date selected!");$("#from-date-group").addClass("error");$("#to-date-group").addClass("error")}else{i=t.split("-");s=r.split("-");o=i[0];u=i[1];a=s[0];f=s[1];console.log(i);console.log(s);l=map.getBounds();c=l.getNorthEast();h=l.getSouthWest();console.log(map.getBounds());p={};d={};v=root_url+"/api/crimes/?ne="+c.lat()+","+c.lng()+"&sw="+h.lat()+","+h.lng()+"&sy="+o+"&sm="+u+"&ey="+a+"&em="+f;console.log(v);$.getJSON(v,{},function(e){var t,n,r,i,s,o,u=e.crimes;for(t in u){n=roundNumber(u[t].crime.point.lat,5);r=roundNumber(u[t].crime.point.lng,5);i=n+","+r;p[i]===undefined?p[i]=1:p[i]=p[i]+1}console.log(p);for(t in u){n=roundNumber(u[t].crime.point.lat,5);r=roundNumber(u[t].crime.point.lng,5);s=n+","+r;o=p[s];heatmap.addDataPoint(n,r,o)}})}}function DataMap(e){var t,n=new google.maps.LatLng(51.481307,-3.1804986);this.map_options={zoom:14,mapTypeId:google.maps.MapTypeId.ROADMAP};map=new google.maps.Map(e,this.map_options);navigator.geolocation&&navigator.geolocation.getCurrentPosition(function(e){n=new google.maps.LatLng(e.coords.latitude,e.coords.longitude)});map.setCenter(n);heatmap=new HeatmapOverlay(map,{radius:1,visible:!0,opacity:60});t={max:6,data:[{lat:51.466,lng:-3.18383,count:4},{lat:51.479,lng:-3.15653,count:6},{lat:51.482,lng:-3.16588,count:1}]};google.maps.event.addListener(map,"idle",function(){heatmap.setDataSet(t)})}var map,heatmap;$(document).ready(function(){var e=new DataMap(document.getElementById("map-canvas"))});