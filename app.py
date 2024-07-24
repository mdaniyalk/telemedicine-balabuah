from flask import Flask, render_template, request, jsonify
import markdown2 as markdown

from telemedicine.core.configuration import Configuration
from telemedicine.core.paraphraser import paraphrase
from telemedicine.session import ChatSession


app = Flask(__name__)
 
@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/start-session", methods=["GET"])
def start_session():
    session = ChatSession()
    session.initialize()
    return jsonify(sessionId=session.session_id)


@app.route("/chat", methods=["GET", "POST"])
def chat():
    # try:
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
            return response
        elif response_type == "json":
            response = session.get_response(msg, html=False)
            session.save_session()
            return jsonify(response=response)
    # except Exception as e:
    #     print(e)
    #     error_msg = paraphrase("An error occurred: " + str(e), text_type='error-msg')
    #     if response_type == "html":
    #         return markdown.markdown(error_msg)
    #     elif response_type == "json":
    #         return jsonify(error=error_msg)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8000', debug=True)