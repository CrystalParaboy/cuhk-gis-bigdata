// List of Buildings With Confirmed / Probable Cases of COVID-19 within 14 days
const casesArray = ['Block 3, Chelsea Heights',
    '110 Fa Yuen Street',
    'Wang Yat House, Lok Fu Estate',
    '122 Nga Tsin Wai Road',
    'Sau Wai House, Sau Mau Ping Estate',
    'Un On Building, 128 Camp Street',
    'King Fat House, Cheung Fat Estate',
    'Shek Lin House, Shek Wai Kok Estate',
    'Kwok Keung Building',
    'Chui King House, Choi Hung Estate']

// List of local Hong Kong attractions
const attractionsArray = [
    {
        coords: { lat: 22.456785, lng: 114.142456 },
        iconImage: './assets/lantern.png',
        content: '<p>Lam Tsuen Wishing Tree</p>'
    },
    {
        coords: { lat: 22.253227, lng: 113.853752 },
        iconImage: './assets/love.png',
        content: '<p>Tai O Heritage Hotel</p>'
    },
    {
        coords: { lat: 22.394575, lng: 114.108218 },
        iconImage: './assets/coffee-shop.png',
        content: '<p>Duen Kee Tea House</p>'
    },
    {
        coords: { lat: 22.283431, lng: 114.151254 },
        iconImage: './assets/graffiti.png',
        content: '<p>Shing Wong Street</p>'
    },
    {
        coords: { lat: 22.218027, lng: 114.202103 },
        iconImage: './assets/love.png',
        content: '<p>Chung Hom Kok Beach</p>'
    },
    {
        coords: { lat: 22.292141, lng: 114.010147 },
        iconImage: './assets/outdoor.png',
        content: '<p>Chung Hom Kok Beach</p>'
    },
];
function passvalue() {
  const API_KEY = AIzaSyDmZQImxjUjMf3-nX8m4h30SMNp-LqS1p4;
  localStorage.setItem("API_KEY", API_KEY);
  console.log("API Key entered: " + API_KEY);

}

function initMap() {
  // Map options
  var options = {
    zoom: 11,
    center: {
      lat: 22.409506,
      lng: 114.032065
    }
  }

  // New map
  var map = new google.maps.Map(document.getElementById('map'), options);

  // Loop through buildings with confirmed cases
  for (var i = 0; i < casesArray.length; i++) {
    addCases(i);
  }

  // Loop through local atttractions
  for (var i = 0; i < attractionsArray.length; i++) {
    addMarker(attractionsArray[i]);
  }

  // Add Confirmed Cases Function
  function addCases(index) {
    let data;
    let name = casesArray[index];
    var query = name.split(' ').join('+');
    fetch('https://maps.googleapis.com/maps/api/geocode/json?address=' + query + '&key=AIzaSyD5Ftd85SKpFEYBCJSzuOXK3zPgrCD5UdE')
      .then(response => response.json())
      .then(result => {
        data = result.results[0].geometry.location;
        entry = {
          coords: data,
          // iconImage:'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png',
          content: '<p>Covid Case:</p>' + name
        }
        addMarker(entry);
      });
  }

  // Add Marker Function
  function addMarker(props) {
    var marker = new google.maps.Marker({
      position: props.coords,
      map: map,
      //icon:props.iconImage
    });

    // Check for customicon
    if (props.iconImage) {
      // Set icon image
      marker.setIcon(props.iconImage);
    }

    // Click marker to see the details
    if (props.content) {
      var infoWindow = new google.maps.InfoWindow({
        content: props.content
      });

      marker.addListener('click', function() {
        infoWindow.open(map, marker);
      });
    }
  }
}
