/*
    let latitude;
    let longitude;
    let map
    let mapData;
    let marker;

    function initMap() {
        // Your code to call getAddressFromCoordinates goes here
    }
    /*
    function getAddressFromCoordinates(lat, lng) {
        const geocoder = new google.maps.Geocoder();
        const latlng = { lat: parseFloat(lat), lng: parseFloat(lng) };

        geocoder.geocode({ 'location': latlng }, function(results, status) {
            if (status === google.maps.GeocoderStatus.OK) {
                if (results[0]) {
                    console.log("Address: " + results[0].formatted_address);
                    document.getElementById('{{ form.location.auto_id }}').value = `${lat}, ${lng}, ${results[0].formatted_address}`;
                } else {
                    console.log("No results found");
                }
            } else {
                console.log("Geocoder failed due to: " + status);
            }
        });
    }
    */

    function getAddressFromCoordinates(lat, lng) {
        const url = `https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lng}&format=json`;
    console.log("No address found");
        fetch(url)
            .then(response => response.json())
            .then(data => {
                if (data.address) {
                    mapData = data;
                    console.log("Address: " + data.display_name);
                    document.getElementById('{{ form.location.auto_id }}').value = `${data.display_name}`;
                    document.getElementById('address').innerText = mapData.display_name;
                } else {
                    console.log("No address found");
                }
            })
            .catch(error => console.log("Error:", error));
    }

     function drawMap(lat, lng, zoomValue){
            // Initialize map
            map = L.map('map').setView([lat, lng], zoomValue); // Zoom level 18 for details

            // Add OpenStreetMap tile layer
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; OpenStreetMap contributors'
            }).addTo(map);

            map.on('zoomend', function() {
                var zoomLevel = map.getZoom();
                console.log("Current Zoom Level: " + zoomLevel);
                document.getElementById('zoomLevel').innerText = "Zoom: " + zoomLevel;
            });

    }

    document.getElementById('getLocation').addEventListener('click', function() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                 latitude = position.coords.latitude;
                 longitude = position.coords.longitude;
                    console.log("location: " + latitude + ", " + longitude);
                    getAddressFromCoordinates(latitude, longitude); // Use actual coordinates here
                    addAMarker(latitude, longitude, "Mamelodi");
            }, function(error) {
                alert('Error fetching location. Ensure location is enabled.');
            });
        } else {
            alert('Geolocation is not supported by this browser.');
        }
    });

    drawMap(0, 1, 4);

    function addAMarker(lat, lng, address) {
            if (marker) {
                map.removeLayer(marker); // Remove previous marker
            }

            if(map.getZoom() < 14)
            {
                map.setView([lat, lng], 14);
            }else{
                map.setView([lat, lng]);
            }

            marker = L.marker([lat, lng]).addTo(map)
                .bindPopup(address)
                .openPopup();
        }
*/