// script.js

let map;
getLocation();
var cameras=cameras;


async function initMap(latitude, longitude) {
    map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: latitude, lng: longitude }, // Default to San Francisco coordinates
        zoom: 16,
        styles: [
            {
                featureType: 'poi',
                elementType: 'labels',
                stylers: [{ visibility: 'off' }],
            },
        ],
        streetViewControl: false, 
    });

    const map_icons = {
        camera_green: {icon:'https://i.ibb.co/ynZ7dZ6/icons8-cctv-48-1.png'},
        camera_red: {icon:'https://i.ibb.co/tCNKdZb/icons8-cctv-48.png'},
    }

    var map_cameras = []

    for (var i = 1; i < 4 ; i++){
        map_cameras.push({
            lat: cameraDetails[i].lat,
            lng: cameraDetails[i].lng,
            type: 'camera_green',
        });
    }

    var pos = new google.maps.Marker({
        position: new google.maps.LatLng(30.516372999484418, 76.65977779435349),
        map: map,
      });

    for (var i = 1; i < 4 ; i++) {
        console.log('adding marker')
        const marker = new google.maps.Marker({
            position: new google.maps.LatLng(map_cameras[i].lat, map_cameras[i].lng),
            icon: map_icons[map_cameras[i].type].icon,
            map: map,
          });
    }
}

function getLocation() {
    if (navigator.geolocation) {
        var options = {
            enableHighAccuracy: true, // Request high accuracy
            timeout: 10000, // Timeout in milliseconds (adjust as needed)
            maximumAge: 0 // Force a new location retrieval
        };
        navigator.geolocation.getCurrentPosition(showPosition, showError, options);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

    function showPosition(position) {
        // var latitude = position.coords.latitude;
        // var longitude = position.coords.longitude;
        google.maps.event.addDomListener(window, 'load', initMap(30.516372999484418,76.65977779435349));

    // You can now send this information to your server or perform any other desired action.
    // For example, you can use AJAX to send the data to your server.
    // Here's a basic example using fetch:
    // fetch('/your-server-endpoint', {
    //     method: 'POST',
    //     headers: {
    //         'Content-Type': 'application/json',
    //     },
    //     body: JSON.stringify({ latitude, longitude }),
    // })
    // .then(response => response.json())
    // .then(data => console.log('Success:', data))
    // .catch((error) => {
    //     console.error('Error:', error);
    // });
}


function showError(error) {
    switch(error.code) {
        case error.PERMISSION_DENIED:
            alert("User denied the request for geolocation.");
            break;
        case error.POSITION_UNAVAILABLE:
            alert("Location information is unavailable.");
            break;
        case error.TIMEOUT:
            alert("The request to get user location timed out.");
            break;
        case error.UNKNOWN_ERROR:
            alert("An unknown error occurred.");
            break;
    }
}

$(document).ready(function () {
setCameraStreams();
  var socket = io.connect(
    location.protocol +
      "//" +
      window.location.hostname +
      ":" +
      location.port +
      "/listener"
  );
  console.log('socket connected');
  socket.on("listener", function (msg) {
    console.log(msg)
    const videoElement = document.getElementById('cameraStream1');
    playAlert();
    highlightCameraStream(findCameraIdByIP(msg.camera.ip));
    var latlng = findLatLngByIP(msg.camera.ip);
    var red_mark = new google.maps.Marker({
        position: new google.maps.LatLng(latlng.lat, latlng.lng),
        icon: 'https://i.ibb.co/tCNKdZb/icons8-cctv-48.png',
        map: map,
      });

      setTimeout(()=> {
        removeHighlightCameraStream();
      }, 7000);

  })})


  const cameraDetails = {
    1: {"ip": "192.168.50.80", "name": "Square One Cafeteria", "lat": 30.51511298901009, "lng":76.65986803414162},
    2: {"ip": "192.168.50.26", "name": "Picasso Block", "lat": 30.517297553772746, "lng":76.65940166312487},
    3: {"ip": "192.168.50.26", "name": "Turing Block", "lat": 30.516605786143447, "lng": 76.6607354827045},
};

function findCameraIdByIP(ipToFind) {
    for (const [cameraId, cameraInfo] of Object.entries(cameraDetails)) {
        if (cameraInfo.ip === ipToFind) {
            return parseInt(cameraId);
        }
    }
    // If the IP is not found, return null or any other value indicating not found
    return null;
}

function findLatLngByIP(ipToFind) {
    for (const cameraInfo of Object.values(cameraDetails)) {
        if (cameraInfo.ip === ipToFind) {
            return { lat: cameraInfo.lat, lng: cameraInfo.lng };
        }
    }
    // If the IP is not found, return null or any other value indicating not found
    return null;
}

// Function to set img src for each camera stream
function setCameraStreams() {
    Object.keys(cameraDetails).forEach(cameraId => {
        const ip = cameraDetails[cameraId].ip;
        if (ip) {
            const imgElement = document.getElementById(`cameraStream${cameraId}`);
            imgElement.src = `http://${ip}:4747/video`; // Replace with the actual stream URL
        }
    });
}


// Function to highlight the camera stream with thick red borders
function highlightCameraStream(cameraId) {
    // Remove highlight from all streams
    document.querySelectorAll('.stream-box').forEach(box => box.classList.remove('highlight'));

    // Add highlight to the specified stream
    const streamBox = document.getElementById(`cameraStream${cameraId}`).parentElement;
    streamBox.classList.add('highlight');
}

function removeHighlightCameraStream() {
    // Remove highlight from all streams
    document.querySelectorAll('.stream-box').forEach(box => box.classList.remove('highlight'));
}

function playAlert() {
    // Replace 'audio-file.mp3' with the path to your audio file
    const audio = new Audio('static/beep-warning-6387.mp3');
    audio.play();
}