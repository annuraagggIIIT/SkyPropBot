import pandas as pd
from flask import Flask, request, jsonify
from transformers import pipeline
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load CSV file
try:
    df = pd.read_csv('Property details.csv', header=None, on_bad_lines='skip', encoding='utf-8')
    df.columns = range(df.shape[1])
    print("CSV file loaded successfully.")
except Exception as e:
    print(f"Error reading CSV: {e}")
    df = None

if df is not None:
    print(df.head())

    # Initialize the chatbot pipeline
    try:
        chatbot = pipeline('text-generation', model='microsoft/DialoGPT-medium')
    except Exception as e:
        print(f"Error initializing chatbot: {e}")
        chatbot = None

    # Define the process_query function
    def process_query(query):
        query = query.lower()
        try:
            if 'average price' in query or 'mean price' in query:
                prices = df[1].str.extract(r'(\$[\d,]+)')[0].str.replace(',', '').str.replace('$', '').astype(float)
                result = prices.mean()
                return f"The average price is ${result:.2f}/mo"
            elif 'location' in query or 'locations' in query:
                locations = df[6].unique()
                return f"The available locations are: {', '.join(map(str, locations))}"
            elif 'average size' in query or 'mean size' in query:
                sizes = df[5].str.extract(r'(\d+,\d+)')[0].str.replace(',', '').astype(float)
                result = sizes.mean()
                return f"The average size is {result:.2f} sqft"
            elif 'property at index' in query:
                try:
                    index = int(query.split()[-1])
                    property_details = df.iloc[index].to_dict()
                    return f"Property details: {', '.join([f'{key}: {value}' for key, value in property_details.items()])}"
                except Exception as e:
                    return f"Error: {e}"
            elif 'amenities' in query:
                amenities_list = df[8].explode().dropna().unique()
                return f"Amenities available: {', '.join(map(str, amenities_list))}"
            elif 'price below' in query:
                try:
                    max_price = float(query.split('below')[-1].strip().replace('$', '').replace(',', ''))
                    filtered_properties = df[df[1].str.replace('$', '').str.replace(',', '').astype(float) < max_price]
                    return f"Properties below ${max_price:.2f}: \n{filtered_properties.to_string(index=False)}"
                except Exception as e:
                    return f"Error: {e}"
            else:
                return "I can help with average price, average size, available locations, property details, amenities, and price ranges."
        except Exception as e:
            return f"Error processing query: {e}"

    @app.route('/chat', methods=['POST'])
    def chat():
        user_input = request.json.get('query')
        custom_query_result = process_query(user_input)
        if custom_query_result != "I can help with average price, average size, available locations, property details, amenities, and price ranges.":
            response = custom_query_result
        else:
            conversation = chatbot(user_input)
            response = conversation[0]['generated_text']
        return jsonify({'response': response})

    if __name__ == '__main__':
        app.run(debug=True)
else:
    print("DataFrame is not defined. Please check the CSV file and try again.")
