import requests
#from Capstone import key_config
from geopy.distance import geodesic
import streamlit as st
import geocoder




# Replace 'YOUR_API_KEY' with your actual Google API key
API_KEY = 'AIzaSyA-g8VD1vQWQngkBUgH4V1uERxdSi1Wd60'

st.title("Endocrinologist Near You")
def get_coordinates_from_address(address):
    geocoding_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": API_KEY,
    }

    response = requests.get(geocoding_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data.get("status") == "OK":
            location = data["results"][0]["geometry"]["location"]
            return f"{location['lat']},{location['lng']}"
        else:
            print("Error: Unable to retrieve coordinates from the provided address.")
    else:
        print("Error: Unable to connect to the Google Geocoding API.")


def find_endocrinologists_near_address(location, range_in_meters):

    if location:
        base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        params = {
            "location": location,
            "radius": range_in_meters,
            "type": "doctor",
            "keyword": "endocrinologist",
            "key": API_KEY,
        }

        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "OK":
                endocrinologists = data.get("results", [])
                if not endocrinologists:
                    st.info("No endocrinologists found near the provided address.")
                else:

                    for i, endo in enumerate(endocrinologists):
                        rating = endo.get("rating", "No rating available")
                        total_rating = endo['user_ratings_total']
                        name = endo['name']
                        address = endo['vicinity']
                        coordinates = f"{endo['geometry']['location']['lat']},{endo['geometry']['location']['lng']}"
                        distance = geodesic(location, coordinates).miles
                        # Generate a Google Maps link for directions
                        maps_link = f"https://www.google.com/maps/dir/?api=1&destination={coordinates}"

                        st.subheader(f"{i+1}. {name}")
                        st.write(f"Address: {address}")
                        st.write(f"Rating: {rating}({total_rating})")
                        st.write(f"Distance: {distance:.2f} miles")
                        st.write(f"Directions: [Click here]({maps_link})")
                        st.markdown("---")

            else:
                st.error("No endocrinologists found near the provided address.")
        else:
            st.error("Error: Unable to connect to the Google Places API.")
    else:
        st.error("No coordinates were obtained from the provided address.")



# Streamlit UI elements


#user_address = st.text_input("Address", placeholder="123 Main St, City, ZIP Code")

# Get the user's current location using geocoder
user_geolocation = geocoder.ip("me")
user_location = (user_geolocation.latlng[0], user_geolocation.latlng[1])
user_address = f"{user_location[0]},{user_location[1]}"
print(user_address)
range_in_miles = st.slider("Range (miles)", 0, 100, 1)
range_in_meters = 1609.344 * range_in_miles
if st.button("Find Endocrinologists"):
    if user_address:
        find_endocrinologists_near_address(user_address, range_in_meters)
st.markdown("---")
