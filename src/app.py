from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    input_name = request.form.get("name")
    input_age = request.form.get("age")

    input_pet_1 = request.form.get("choice1")
    input_pet_2 = request.form.get("choice2")

    # Show different page depending on choice
    if input_pet_1 and input_pet_2:
        pref = "You like both cats and dogs!"
        show = "hello.html"
    elif input_pet_1:
        pref = "Cats are better!"
        show = "hello_cat.html"
    elif input_pet_2:
        pref = "Dogs are better!"
        show = "hello_dog.html"
    else:
        pref = "You don't like cats or dogs :("
        show = "hello_neither.html"

    return render_template(show, name=input_name, age=input_age, pet=pref)


@app.route("/query")
def process_query():
    query = request.args.get['q']
    if query == "dinosaurs":
        query = "Dinosaurs ruled the Earth 200 illion years ago"
        out = query
    elif query == "asteroids":
        query = "Unknown"
        out = query
    else:
        query = "No query provided"
        out = query
    return render_template(query.html, show=out)
