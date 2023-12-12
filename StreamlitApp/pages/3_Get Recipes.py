import requests
import streamlit as st

# Edamam API endpoint and credentials
api_endpoint = "https://api.edamam.com/search"
app_id = "5498c428"
app_key = "c698a2d65571fe086a7610b037dece20"


# Function to get recipe suggestions based on a query
def get_recipe_suggestions(query, app_id, app_key):
    params = {
        'q': query,
        'app_id': app_id,
        'app_key': app_key,
    }

    # Make a request to the Edamam API
    response = requests.get(api_endpoint, params=params)
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()

        # Display recipe information using Streamlit
        for hit in data.get('hits', []):
            recipe = hit['recipe']

            # Create columns for each recipe
            col1, col2 = st.columns(2)

            # Display image in the first column with a fixed width
            col2.image(recipe['image'], use_column_width=True, width=200)

            # Display recipe information in the second column
            with col1:
                st.write(f"**Recipe:** {recipe['label']}")
                # Display health labels and ingredients without bullet points
                st.info(
                    f"**Ingredients:** {', '.join([ingredient['text'] for ingredient in recipe['ingredients']])}")
                st.success(f"**Health Labels:** {', '.join(recipe['healthLabels'])}")
                # Display clickable text to open the recipe URL in a new tab
                url_text = f"[View Recipe]({recipe['url']})"
                st.markdown(url_text, unsafe_allow_html=True)
                st.write("\n")
                st.markdown("---")


    else:
        st.error(f"Error: {response.status_code}")


# Streamlit UI
st.title("Recipe Suggestions for Diabetics")
user_input = st.text_input("",placeholder="What would you like to have?")
if st.button("Get Recipes"):
    st.markdown("---")
    query = f"{user_input} for diabetics"
    get_recipe_suggestions(query, app_id, app_key)
