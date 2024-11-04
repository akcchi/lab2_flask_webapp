from flask import Flask, render_template, request
import requests

app = Flask(__name__)


# Function takes in query value and returns corresponding result
def process_query(query):
    if query == "dinosaurs":
        ans = "Dinosaurs ruled the Earth 200 million years ago"
    elif query == "asteroids":
        ans = "Unknown"
    else:
        ans = "Invalid query provided"
    return f"{ans}"


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


@app.route("/query", methods=["GET"])
def query():
    query = request.args.get("q")
    return process_query(query)


@app.route("/lab5")
def hello_user():
    return render_template("hello_user.html")


@app.route("/submit_user", methods=["POST"])
def submit_user():
    repo_list = []
    # repo_list = "<ul>"
    in_name = request.form.get("user")
    response = requests.get(f"https://api.github.com/users/{in_name}/repos")
    if response.status_code == 200:
        repos = response.json()  # Returns list of repo entities
        for repo in repos:
            temp_name = repo["full_name"]
            # temp_append = "<li>" + str(temp_name) + " /li>"
            temp_append = str(temp_name)
            # repo_list.append(temp_append)
            repo_list.append(temp_append)
        # repo_list += "</ul>"

    return render_template(
        "result_user.html", user=in_name, repo_list=repo_list)
