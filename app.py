from flask import Flask, render_template, request, jsonify
import openai
import requests
import json
from flask_cors import CORS  # Import Flask-CORS
# Customize your medical advice list if necessary.
advice_list = '''
# Medical Advice List

## General Health:

- Healthy Diet  
  - Tips: Include a variety of fruits and vegetables in your diet. Limit processed foods.
  
- Regular Exercise  
  - Tips: Aim for at least 30 minutes of moderate exercise most days of the week.

- Adequate Sleep  
  - Tips: Ensure you get 7-9 hours of sleep per night for overall well-being.

## Common Ailments:
- Cold and Flu Remedies  
  - Tips: Stay hydrated, get plenty of rest, and consider over-the-counter cold remedies.

- Headache Relief  
  - Tips: Drink water, rest in a quiet room, and consider over-the-counter pain relievers.

- Stress Management  
  - Tips: Practice deep breathing, meditation, or engage in activities you enjoy.

## Common Symptoms and Solutions:
- Fever  
  - Tips: Stay hydrated, rest, and consider over-the-counter fever reducers.

- Cough  
  - Tips: Stay hydrated, use cough drops, and consider over-the-counter cough medicine.

- Sore Throat  
  - Tips: Gargle with warm saltwater, stay hydrated, and rest your voice.

- Fatigue  
  - Tips: Ensure you get enough sleep, maintain a balanced diet, and consider stress-reducing activities.

## Specialized Advice:
- Chronic Conditions  
  - Tips: Follow your prescribed treatment plan and attend regular check-ups.

- Mental Health Support  
  - Tips: Reach out to a mental health professional if you're struggling emotionally.

- Healthy Aging  
  - Tips: Stay socially active, exercise regularly, and attend routine health check-ups.

## Emergency Situations:
- First Aid for Burns  
  - Tips: Run cold water over the burn, cover with a clean cloth, and seek medical attention.

- CPR Guidelines  
  - Tips: Call for help, start chest compressions, and follow emergency protocols.

'''

context_doctor = [{'role': 'system',
                   'content': f"""
You are DoctorBot, an AI assistant providing medical advice and information.

Your role is to assist users with general health inquiries, provide advice on common ailments, offer specialized health tips, and guide users in emergency situations.

Be empathetic and informative in your interactions.

We offer a variety of medical advice across categories such as General Health, Common Ailments, Common Symptoms and Solutions, Specialized Advice, and Emergency Situations.

The Current Medical Advice List is as follows:

```{advice_list}```

Encourage users to ask questions about their health, provide relevant advice, and remind them to consult with a healthcare professional for personalized guidance.
"""}]

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Load OpenAI API key (replace with your actual API key)
api_key = "openai_api_key"
api_url = 'https://api.openai.com/v1/chat/completions'

# Function to get the response from DoctorBot (GPT)
def get_response_from_doctorbot(user_message,api_key,api_url):
    try:
        headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
        }
        context_doctor.append({'role':'user', 'content':f"{user_message}"})
        data = {
            "model": "gpt-4o-mini",  
            "messages": context_doctor,
            "temperature": 0.7
        }
        response = requests.post(api_url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            reply = response.json()['choices'][0]['message']['content']
            return reply
        else:
            return f"Error: {response.status_code}, {response.text}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Route to serve the HTML frontend
@app.route('/')
def index():
    return render_template('index.html')  # This serves the HTML page

# API route to handle chat requests
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json  # Expect JSON with the user input
    user_input = data.get('message', '')  # Get the 'message' key from JSON
    if not user_input:
        return jsonify({'error': 'No input provided'}), 400
    
    bot_response = get_response_from_doctorbot(user_input,api_key,api_url)  # Generate response from GPT
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)