from flask import Flask, render_template, request
from markupsafe import escape
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html", message="Привет!")


@app.route("/user/<username>")
def user(username):
    return f"Привет, {username}!"


@app.route("/contact", methods=["GET", "POST"])
def contact_form():
    if request.method == "POST":
        data_user = request.form["username"].strip()
        data_msg = request.form["message"].strip()
        try:
            with open("contact_form.txt", "a", encoding="utf-8") as f:
                f.write(f"{data_user}\n{data_msg}\n---\n")
        except Exception as e:
            return f"Ошибка при сохранении: {e}", 500
        return f"You sent:<br>user_name: {escape(data_user)}<br>with message: {escape(data_msg)}"
    return render_template("contact_form.html")

@app.route("/feedbacks", methods=["GET"])
def feedbacks():
    try:
        with open("feedback.txt", "r", encoding="utf-8") as f:
            messages = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        messages = []
    return render_template("feedbacks.html", messages=messages)


@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        data = request.form["message"]
        # Сохраняем сообщение в файл
        with open("feedback.txt", "a", encoding="utf-8") as f:
            f.write(data + "\n")
        return f"Вы отправили: {data}"
    return render_template("form.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    results = []
    query = ""
    if request.method == "POST":
        query = request.form["query"].strip().lower()
        try:
            with open("feedback.txt", "r", encoding="utf-8") as f:
                for line in f:
                    words = [w.strip().lower() for w in line.split()]
                    if query in words:
                        results.append(line.strip())
        except FileNotFoundError:
            results = []
    return render_template("search.html", results=results, query=query)

if __name__ == '__main__':
    app.run(debug=True)
