function getResource(url, callback){
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.onreadystatechange = function(){
      if (xmlHttp.readyState == 4 && xmlHttp.status == 200){
          callback(xmlHttp.responseText);
      }
  }
  xmlHttp.open("GET", url, true);
  xmlHttp.send();
}

function degrees2Radians(degrees) {
  return degrees * Math.PI / 180;
}

function distance(lon1, lat1, lon2, lat2) {
  var earthRadius = 6371;
  var dLat = degrees2Radians(lat2-lat1);
  var dLon = degrees2Radians(lon2-lon1); 
  var a = Math.sin(dLat/2) * Math.sin(dLat/2) +
          Math.cos(degrees2Radians(lat1)) * Math.cos(degrees2Radians(lat2)) * 
          Math.sin(dLon/2) * Math.sin(dLon/2); 
  var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
  var d = earthRadius * c;
  return d;
}

function floatTime2HumanReadable(time) {
  if (time == 0) {
    return "now";
  }
  var hours = Math.round(time - time % 1);
  var minutes = Math.round(time % 1 * 60);
  var humanReadable = "";
  if (hours > 0) {
    humanReadable += hours  + " hours and ";
  }
  humanReadable += Math.abs(minutes) + " minutes";
  if (minutes < 0) {
    humanReadable += " ago";
  }
  return humanReadable;
}

function addressLink(branch) {
  var protocol = "http://"
  var coordinates = branch.position.lat + "," + branch.position.lng;
  if( (navigator.platform.indexOf("iPhone") != -1) 
      || (navigator.platform.indexOf("iPod") != -1)
      || (navigator.platform.indexOf("iPad") != -1)) {
       protocol = "maps://";
  }
  return protocol + "maps.google.com/maps?daddr=" + coordinates + "&amp;ll=";
}

function addBranchToList(branch) {
  var timeUntilHalfPrice = floatTime2HumanReadable(branch.timeUntilHalfPrice);
  var branchHtml = '<div class="branch"><span class="branch-name">' + branch.name + '</span>';
  branchHtml += '<span class="branch-time-until">' + timeUntilHalfPrice + '</span>'
  branchHtml += '<span class="branch-distance">' + Math.round(branch.distance, 2) + ' km</span>';
  branchHtml += '<span class="branch-address"><a href="' + addressLink(branch) + '">' + branch.address + ', ' + branch.postCode + '</a></span>';
  branchHtml += '</div>';
  var branchesHtml = document.getElementById('branches').innerHTML;
  document.getElementById('branches').innerHTML = branchesHtml + branchHtml;
}

document.addEventListener("DOMContentLoaded", function(event) {
  var distanceLimit = 10;
  var now = new Date();
  var currentTime = now.getHours() + now.getMinutes()/60;
  var currentDay = now.getDay();
  var possibleBranches = [];
  window.navigator.geolocation.getCurrentPosition(function(pos) { 
    var currentLat = pos.coords.latitude;
    var currentLng = pos.coords.longitude;
    getResource("sushi-data.json", function(data) {
      data = JSON.parse(data);
      for (var i = 0; i < data.length; i++) {
        var e = data[i];
        if (e.halfPriceTimes[currentDay] != null) {
          e.timeUntilHalfPrice = e.halfPriceTimes[currentDay] - currentTime;
          if (e.timeUntilHalfPrice >= -0.5) {
            e.distance = distance(currentLng, currentLat, e.position.lng, e.position.lat);
            if (e.distance <= distanceLimit) {
              possibleBranches.push(e);
            }
          }
        }
      }
      var sortedPossibleBranches = possibleBranches.sort(function (a, b) {
          return a.timeUntilHalfPrice - b.timeUntilHalfPrice || a.distance - b.distance;
      });
      document.getElementById('branches').innerHTML = '';
      for (var i  = 0; i < sortedPossibleBranches.length; i++) {
        var e = sortedPossibleBranches[i];
        addBranchToList(e);
      }
    });
  })
});