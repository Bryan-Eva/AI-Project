from flask import Flask, request, render_template
import json
import random

app = Flask(__name__)

navigation_items = [
    {"name": "觀看課程", "url": "/course"},
    {"name": "測驗", "url": "/test"},
    {"name": "知識查詢", "url": "/search"},
    {"name": "知識分享與討論", "url": "/discuss"},
    {"name": "登入", "url": "/login"}
]


@app.route("/")
def index():
    members = [
        {
            'name': '卓柏辰',
            'imageUrl': "https://media.canva.com/v2/image-resize/format:JPG/height:800/quality:92/uri:s3%3A%2F%2Fmedia-private.canva.com%2F6DP7w%2FMAF0M96DP7w%2F1%2Fp.jpg/watermark:F/width:600?csig=AAAAAAAAAAAAAAAAAAAAAH8q1IhRBrqXITFCh4J-jeIcgJ1jOa-ssQGapLgkRYrj&exp=1734652839&osig=AAAAAAAAAAAAAAAAAAAAADcgWtqPvpkpG59Bo_TcC6k9ynyL46uqyjnDr64DSK31&signer=media-rpc&x-canva-quality=screen"
        },
        {
            'name': '鄭重雨',
            'imageUrl': "https://media.canva.com/v2/image-resize/format:PNG/height:800/quality:100/uri:s3%3A%2F%2Fmedia-private.canva.com%2FAd_84%2FMAGVITAd_84%2F1%2Fp.png/watermark:F/width:484?csig=AAAAAAAAAAAAAAAAAAAAAIMSco7vnobh4FWtBZvn1ZouNSZR_N-qjYPJ8Wn1bakx&exp=1734652094&osig=AAAAAAAAAAAAAAAAAAAAAHBHQC0m3Mdd5ndwyJ8gEsj0UhRbKr3L0YlGDVDe3XFP&signer=media-rpc&x-canva-quality=screen"
        },
        {
            'name': '林品緯',
            'imageUrl': "https://media.canva.com/v2/image-resize/format:JPG/height:200/quality:75/uri:s3%3A%2F%2Fmedia-private.canva.com%2FdW9w4%2FMAGVIYdW9w4%2F1%2Fp.jpg/watermark:F/width:200?csig=AAAAAAAAAAAAAAAAAAAAAJo9rqfpDQEG8HoViYG_-BRYBnP8-8OIaHfnTtIem5iT&exp=1734653261&osig=AAAAAAAAAAAAAAAAAAAAAGbpNZFkdVThO2KCES6TY4bk6ooYjhCFPSMoNH42j9_t&signer=media-rpc&x-canva-quality=thumbnail"
        },
        {
            'name': '呂念庭',
            'imageUrl': "https://media.canva.com/v2/image-resize/format:JPG/height:200/quality:75/uri:s3%3A%2F%2Fmedia-private.canva.com%2F9exn4%2FMAF4vD9exn4%2F1%2Fp.jpg/watermark:F/width:200?csig=AAAAAAAAAAAAAAAAAAAAAFmXdSTHma8xh-PKo63hFGmtSqM6ICIXNCT6YmhKZxOg&exp=1734653103&osig=AAAAAAAAAAAAAAAAAAAAAOuB1fP99O476g2215WaUTaxnfVyF7VZ8boJmq7AOIh_&signer=media-rpc&x-canva-quality=thumbnail"
        },
        {
            'name': '張睿恩',
            'imageUrl': "https://media.canva.com/v2/image-resize/format:PNG/height:200/quality:100/uri:s3%3A%2F%2Fmedia-private.canva.com%2FQXNK0%2FMAGVIRQXNK0%2F1%2Fp.png/watermark:F/width:200?csig=AAAAAAAAAAAAAAAAAAAAAHoU9EBdU8tjFJS_TOc2vwKjGIrYEgbK0BhOxzV9EfJu&exp=1734653755&osig=AAAAAAAAAAAAAAAAAAAAAIUAx54z5lAsgPU-2yqIRytQjTSF4hc7z7t9AyrxndCr&signer=media-rpc&x-canva-quality=thumbnail"
        },
        {
            'name': '顏子毅',
            'imageUrl': "https://media.canva.com/v2/image-resize/format:JPG/height:200/quality:75/uri:s3%3A%2F%2Fmedia-private.canva.com%2FkW6Wg%2FMAGVIckW6Wg%2F1%2Fp.jpg/watermark:F/width:200?csig=AAAAAAAAAAAAAAAAAAAAAIY3u1U2lpO2Ha8cAdhSPf8h34bmYflYD4LjHBLP4ZYw&exp=1734651267&osig=AAAAAAAAAAAAAAAAAAAAAKBytsO0SimSrrq46maNMVUe6w75fEKzQr1DM_HtWwjd&signer=media-rpc&x-canva-quality=thumbnail"
        }
    ]

    return render_template("index.html", navigation_items=navigation_items, members=members)


@ app.route("/search")
def search():
    return render_template("search.html", navigation_items=navigation_items)


@ app.route("/test")
def test():
    items = get_demo_test()
    random.shuffle(items)
    return render_template("test.html", navigation_items=navigation_items, items=items[:20])


def get_demo_test():
    with open("test/demo.json", encoding='utf-8') as f:
        return json.load(f)


@app.route("/submit", methods=["POST"])
def submit():
    data = request.form
    answers = list(data.items())
    answers = map(lambda x: (int(x[0]), int(x[1])), answers)
    answers = sorted(answers, key=lambda x: x[0])
    questionNumbers = list(map(lambda x: x[0], answers))
    correctAnswers = sorted(map(lambda x: (x['questionNumber'], x['correctIndex']), filter(
        lambda x: x['questionNumber'] in questionNumbers, get_demo_test())), key=lambda x: x[0])
    score = 0
    for answer, correctAnswer in zip(answers, correctAnswers):
        if answer[1] == correctAnswer[1]:
            score += 5
    return render_template("test_result.html", navigation_items=navigation_items, score=score)


@ app.route("/course")
def course():
    items = get_demo_course()
    return render_template("course.html", navigation_items=navigation_items, items=items)


def get_demo_course():
    with open("course/demo.json", encoding='utf-8') as f:
        return json.load(f)


@ app.route("/discuss")
def discuss():
    return render_template("discuss.html", navigation_items=navigation_items)


if __name__ == "__main__":
    app.run(debug=True)


def start_server():
    app.run()
