from flask import Flask, request, render_template
import json
import random
from flask_socketio import SocketIO, emit
from chat import get_default_chat_instance

app = Flask(__name__)

socketio = SocketIO(app, async_mode="eventlet")

chat_instance = None


@socketio.on("client_event")
def client_msg(msg):
    print(f"Message from client: {msg.get('data')}")
    for chunk in chat_instance.ask_stream(msg.get("data")):
        if answer_chunk := chunk.get("answer"):
            emit("server_response", {"data": answer_chunk})
            socketio.sleep(0.01)
    emit("server_response_end", {"data": "End of response"})


@socketio.on("connect")
def connected_msg():
    emit("server_response", {"data": "Connected"})
    emit("server_response_end", {"data": "End of response"})


@socketio.on("disconnect")
def disconnected_msg():
    print("Client disconnected")


with open("demo data/navigation.json", encoding="utf-8") as f:
    navigation = json.load(f)


@app.route("/")
def index():
    with open("demo data/member.json", encoding="utf-8") as f:
        members = json.load(f)

    return render_template("index.html", navigation=navigation, members=members)


@app.route("/search")
def search():
    return render_template("search.html", navigation=navigation)


@app.route("/test")
def test():
    items = get_demo_test()
    random.shuffle(items)
    return render_template("test.html", navigation=navigation, items=items[:20])


def get_demo_test():
    with open("demo data/test.json", encoding="utf-8") as f:
        return json.load(f)


@app.route("/submit", methods=["POST"])
def submit():
    data = request.form
    answers = list(data.items())
    answers = list(map(lambda x: (int(x[0]), int(x[1])), answers))
    question_numbers = list(map(lambda x: x[0], answers))
    correct_answers = list(
        filter(lambda x: x["questionNumber"] in question_numbers, get_demo_test())
    )
    correct_answers = sorted(
        correct_answers, key=lambda x: question_numbers.index(x["questionNumber"])
    )
    correct_count = 0
    for answer, correct_answer in zip(answers, correct_answers):
        correct_answer["userAnswer"] = answer[1]
        if correct_answer["correctIndex"] == answer[1]:
            correct_count += 1
    return render_template(
        "test_result.html",
        navigation=navigation,
        items=correct_answers,
        correct_count=correct_count,
    )


@app.route("/course")
def course():
    courses = get_demo_course()
    return render_template("course.html", navigation=navigation, items=courses)


def get_demo_course():
    with open("demo data/course.json", encoding="utf-8") as f:
        return json.load(f)


@app.route("/discuss")
def discuss():
    return render_template("discuss.html", navigation=navigation)


def start_server(chat=None):
    global chat_instance

    if chat:
        chat_instance = chat
    else:
        chat_instance = get_default_chat_instance()

    socketio.run(app, host="127.0.0.1", port=5555, debug=True)


if __name__ == "__main__":
    start_server()
