#Mangpor
from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os
from pathlib import Path

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")

ACCESS_CODE = os.environ.get("ACCESS_CODE", "MangporBest")
DATA_FILE = Path(__file__).with_name("highway_exam_1_20.json")

with open(DATA_FILE, "r", encoding="utf-8") as f:
    QUESTIONS = json.load(f)


def reset_quiz():
    session["authorized"] = False
    session["current_index"] = 0
    session["score"] = 0
    session["results"] = []
    session["last_answer"] = None


@app.route("/")
def home():
    if "current_index" not in session:
        reset_quiz()
    return render_template("home.html")


@app.route("/login", methods=["POST"])
def login():
    code = request.form.get("access_code", "").strip()
    if code == ACCESS_CODE:
        session["authorized"] = True
        session["current_index"] = 0
        session["score"] = 0
        session["results"] = []
        session["last_answer"] = None
        return redirect(url_for("quiz"))

    flash("รหัสยืนยันไม่ถูกต้อง")
    return redirect(url_for("home"))


@app.route("/quiz")
def quiz():
    if not session.get("authorized"):
        return redirect(url_for("home"))

    current_index = session.get("current_index", 0)

    if current_index >= len(QUESTIONS):
        return redirect(url_for("summary"))

    question = QUESTIONS[current_index]
    last_answer = session.get("last_answer")

    if last_answer and last_answer.get("question_id") == question["id"]:
        return render_template(
            "feedback.html",
            question=question,
            last_answer=last_answer,
            current_no=current_index + 1,
            total=len(QUESTIONS),
        )

    return render_template(
        "quiz.html",
        question=question,
        current_no=current_index + 1,
        total=len(QUESTIONS),
    )


@app.route("/submit", methods=["POST"])
def submit():
    if not session.get("authorized"):
        return redirect(url_for("home"))

    current_index = session.get("current_index", 0)

    if current_index >= len(QUESTIONS):
        return redirect(url_for("summary"))

    question = QUESTIONS[current_index]
    selected = request.form.get("choice")

    if selected is None:
        flash("กรุณาเลือกคำตอบก่อน")
        return redirect(url_for("quiz"))

    selected_index = int(selected)
    is_correct = selected_index == question["correct_index"]

    results = session.get("results", [])
    result_item = {
        "question_id": question["id"],
        "question": question["question"],
        "selected_index": selected_index,
        "selected_choice": question["choices"][selected_index],
        "correct_index": question["correct_index"],
        "correct_choice": question["correct_choice"],
        "is_correct": is_correct,
        "explanation": question["explanation"],
        "source_page": question["source_page"],
    }
    results.append(result_item)
    session["results"] = results

    if is_correct:
        session["score"] = session.get("score", 0) + 1

    session["last_answer"] = result_item
    return redirect(url_for("quiz"))


@app.route("/next", methods=["POST"])
def next_question():
    if not session.get("authorized"):
        return redirect(url_for("home"))

    current_index = session.get("current_index", 0)
    session["current_index"] = current_index + 1
    session["last_answer"] = None

    if session["current_index"] >= len(QUESTIONS):
        return redirect(url_for("summary"))

    return redirect(url_for("quiz"))


@app.route("/summary")
def summary():
    if not session.get("authorized"):
        return redirect(url_for("home"))

    results = session.get("results", [])
    score = session.get("score", 0)
    wrong_items = [r for r in results if not r["is_correct"]]

    return render_template(
        "summary.html",
        score=score,
        total=len(QUESTIONS),
        wrong_items=wrong_items,
        results=results,
    )


@app.route("/restart", methods=["POST"])
def restart():
    session.clear()
    reset_quiz()
    return redirect(url_for("home"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)