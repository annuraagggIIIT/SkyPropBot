"# SkyPropBot" 
# Property Chatbot Web Application

This project implements a web-based chatbot interface that allows users to query property details using natural language.

## Features

- **Query Capabilities**: Allows users to ask questions about property details such as average price, average size, available locations, property details, amenities, and price ranges.
- **Interactive Chat Interface**: Provides a user-friendly interface to interact with the chatbot.
- **Backend**: Uses a Flask server to handle backend logic and integrate with transformers and pandas libraries for data processing and conversational AI.

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python, Flask
- **Libraries**: pandas, transformers

## Getting Started

### Prerequisites

- Python 3.6+
- Node.js (for local development with npm)
- Flask (`pip install Flask`)
- pandas (`pip install pandas`)
- transformers (`pip install transformers`)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/property-chatbot.git
   cd property-chatbot
   pip install -r requirements.txt
   py app.py
   Open http://localhost:5000
   ```

  ### Usage
- Enter your query about property details in the input field and click "Submit".
- The chatbot will process your query and display the response below the input field.
