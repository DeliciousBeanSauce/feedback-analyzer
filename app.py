# app.py
from flask import Flask, render_template, request, redirect, url_for
import os
import glob
import openai
import json
import csv
from datetime import datetime
from dotenv import load_dotenv, find_dotenv


app = Flask(__name__)

# Set up OpenAI API
_ = load_dotenv(find_dotenv())

openai.api_key = os.getenv(
    'OPENAI_API_KEY')


def load_feedback():
    feedback_data = {}
    feedback_folder = "feedback"

    # Get all CSV files in the feedback folder
    csv_files = glob.glob(os.path.join(feedback_folder, "*.csv"))

    for file_path in csv_files:
        month_year = os.path.basename(file_path).replace(".csv", "")
        feedbacks = []

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header row
            for row in reader:
                feedback = {
                    "datetime": row[0],
                    "rating": row[1],
                    "comment": row[2],
                }
                feedbacks.append(feedback)

        feedback_data[month_year] = feedbacks

    return feedback_data


feedback_data = load_feedback()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/query', methods=['POST'])
def query():
    user_query = request.form['user_query']
    start_date = request.form['start_date']
    end_date = request.form['end_date']

    filtered_feedback = []
    for month_year, feedbacks in feedback_data.items():
        for feedback in feedbacks:
            feedback_date = datetime.strptime(
                feedback["datetime"].split('@')[0], '%Y-%m-%d')
            if start_date <= feedback_date.strftime('%Y-%m-%d') <= end_date:
                filtered_feedback.append(feedback)

    # Prepare feedback text for the prompt
    feedback_text = "\n".join(
        [f"Kuupäev: {item['datetime']}, NPS: {item['rating']}, Kommentaar: {item['comment']}" for item in filtered_feedback])

    # Create a conversation context for GPT-3.5-turbo in Estonian
    conversation_context = f"Sa oled abivalmis assistent, kes analüüsib antud ajavahemiku jooksul saadud klienditagasisidet. Siin on tagasiside {start_date}-st {end_date}-ni:\n\n{feedback_text}\n\nKasutaja: Palun anna konkreetne ja lühike vastus järgmisele küsimusele: {user_query}"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": conversation_context},
        ],
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )

    response_text = response['choices'][0]['message']['content'].strip()
    return json.dumps({"response_text": response_text})


if __name__ == '__main__':
    load_feedback()
    app.run(debug=True, host='0.0.0.0')
