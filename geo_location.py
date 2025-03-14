import geocoder
import requests

def get_current_location():
    try:
        g = geocoder.ip('me')
        if g.latlng is not None:
            return g.latlng
        else:
            print("Failed")
        # response = requests.get('http://ip-api.com/json', timeout=15)

        # if response.status_code == 200:
        #     data = response.json()
        #     if data['status'] == 'success':
        #         return data['lat'], data['lon']
            # else:
            #     print(f"GEolocation service returned no coordinates: API error- {data.get('message', 'Unknown error')}")
        # else:
        #     print(f'HTTP Error: {response.status_code}')
    except Exception as e:
        print(f"An error occurred while retrieving GPS coordinates: {e}")
        return None


if __name__ == "__main__":
    coordinates = get_current_location()
    # g = geocoder.ip('me')
    # print(g)
    # print(g.json)
    if coordinates is not None:
        latitude, longitude = coordinates
        print("Your current location is:")
        print("Latitude: ", latitude)
        print("Longitude: ", longitude)

    else:
        print("Unable to retrieve your coordinates.")