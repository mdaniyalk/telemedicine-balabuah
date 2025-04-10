from datetime import datetime
from flask import Flask, render_template, request, jsonify
import markdown2 as markdown
from dotenv import load_dotenv
import os

import certifi
from pymongo import MongoClient

from telemedicine.core.configuration import Configuration
from telemedicine.core.paraphraser import paraphrase
from telemedicine.session import ChatSession


app = Flask(__name__)

app_state = {'num_request': 0, "last_check": ""}

@app.route("/")
def index():
    if app_state["num_request"] < 50:
        return render_template("chat.html")
    else:
        if app_state["last_check"] == datetime.now(datetime.UTC).strftime("%d-%m-%Y"):
            return render_template("chat_limit.html")
        else:
            app_state["num_request"] = 0
            app_state["last_check"] = datetime.now(datetime.UTC).strftime("%d-%m-%Y")
            return render_template("chat.html")

@app.route("/start-session", methods=["GET"])
def start_session():
    session = ChatSession()
    session.initialize()
    return jsonify(sessionId=session.session_id)


@app.route("/chat", methods=["GET", "POST"])
def chat():
    # try:
        import time

        start_time = time.time()  # Start timing the process
        msg = request.form.get("msg")
        session_id = request.form.get("session_id")
        response_type = request.form.get("response_type", "html")
        if msg is None or session_id is None or response_type is None:
            msg = request.json.get("msg")
            session_id = request.json.get("session_id")
            response_type = request.json.get("response_type", "html")
        session = ChatSession()
        session.load(session_id)
        if response_type == "html":
            response = session.get_response(msg)
            session.save_session()
            elapsed_time = time.time() - start_time  # Calculate elapsed time
            print(f"Processing time: {elapsed_time:.2f} seconds")  # Log the processing time
            return response
        elif response_type == "json":
            response = session.get_response(msg, html=False)
            session.save_session()
            elapsed_time = time.time() - start_time  # Calculate elapsed time
            print(f"Processing time: {elapsed_time:.2f} seconds")  # Log the processing time
            return jsonify(response=response)
    # except Exception as e:
    #     print(e)
    #     error_msg = paraphrase("An error occurred: " + str(e), text_type='error-msg')
    #     if response_type == "html":
    #         return markdown.markdown(error_msg)
    #     elif response_type == "json":
    #         return jsonify(error=error_msg)

mongo_uri = os.getenv('MONGO_URI')
client = MongoClient(mongo_uri, tlsCAFile=certifi.where())
collection_name = os.getenv('MONGO_COLLECTION_USAGE')
collection = client["session_data"]["usage"]

@app.route('/api/stats/daily', methods=['GET'])
def get_daily_stats():
    pipeline = [
        {
            '$addFields': {
                'timestamp': {
                    '$dateFromString': {
                        'dateString': "$timestamp",
                        'format': "%Y-%m-%d %H:%M:%S"
                    }
                }
            }
        },
        {
            '$group': {
                '_id': {
                    'date': { '$dateToString': { 'format': "%Y-%m-%d", 'date': "$timestamp" } },
                    'model_name': "$model_name"
                },
                'total_tokens': { '$sum': "$total_tokens" },
                'unique_sessions': { '$addToSet': "$session_id" }
            }
        },
        {
            '$group': {
                '_id': '$_id.date',
                'models': {
                    '$push': {
                        'model_name': '$_id.model_name',
                        'total_tokens': '$total_tokens',
                        'unique_sessions_count': { '$size': '$unique_sessions' }
                    }
                },
                'total_daily_tokens': { '$sum': '$total_tokens' },
                'total_unique_sessions': { '$sum': { '$size': '$unique_sessions' } }
            }
        },
        { '$sort': { '_id': 1 } }
    ]
    data = list(collection.aggregate(pipeline))
    return jsonify(data)

@app.route('/api/stats/weekly', methods=['GET'])
def get_weekly_stats():
    pipeline = [
        {
            '$addFields': {
                'timestamp': {
                    '$dateFromString': {
                        'dateString': "$timestamp",
                        'format': "%Y-%m-%d %H:%M:%S"
                    }
                }
            }
        },
        {
            '$group': {
                '_id': {
                    'week': { '$isoWeek': "$timestamp" },
                    'year': { '$isoWeekYear': "$timestamp" },
                    'model_name': "$model_name"
                },
                'total_tokens': { '$sum': "$total_tokens" },
                'unique_sessions': { '$addToSet': "$session_id" }
            }
        },
        { '$sort': { '_id.year': 1, '_id.week': 1 } }
    ]
    data = list(collection.aggregate(pipeline))
    return jsonify(data)

@app.route('/api/stats/monthly', methods=['GET'])
def get_monthly_stats():
    pipeline = [
        {
            '$addFields': {
                'timestamp': {
                    '$dateFromString': {
                        'dateString': "$timestamp",
                        'format': "%Y-%m-%d %H:%M:%S"
                    }
                }
            }
        },
        {
            '$group': {
                '_id': {
                    'month': { '$month': "$timestamp" },
                    'year': { '$year': "$timestamp" }
                },
                'total_tokens': { '$sum': "$total_tokens" },
                'unique_sessions': { '$addToSet': "$session_id" }
            }
        },
        { '$sort': { '_id.year': 1, '_id.month': 1 } }
    ]
    data = list(collection.aggregate(pipeline))
    return jsonify(data)




@app.route("/admin/open/usage/stats")
def stats():
    return render_template("stats.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8000', debug=True)