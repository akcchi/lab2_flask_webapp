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


# Function to retrieve commit info for a GitHub repo
# Parameters: GitHub owner username, GitHub repo name
# Returns: list containing below data on latest commit
#       commit sha/hash
#       commit author name
#       commit date
#       commit time (UTC)
#       commit message
def get_commit_info(user, repo):
    response = requests.get(
        f"https://api.github.com/repos/{user}/{repo}/commits")
    temp_return = []
    if response.status_code == 200:
        commits = response.json()

        for entry in commits:
            link = entry["html_url"]
            link = (
                f'<a href="{link}" target="_blank">Direct link to commit</a>')
            sha = entry["sha"]
            sha = "Commit ID (SHA hash): " + sha

            author = ((entry["commit"])["author"])["name"]
            author = "Commit author: " + author

            # date = ((entry["commit"])["author"])["date"]

            msg = (entry["commit"])["message"]
            msg = "Commit message: " + msg

            temp_timestamp = ((entry["commit"])["author"])["date"]
            commit_date, temp_time = temp_timestamp.split("T")
            commit_time = temp_time.rstrip("Z")
            commit_time += " UTC"
            commit_date = "Commit date: " + commit_date
            commit_time = "Commit time: " + commit_time

            # temp_return.append(entry["sha"])
            # temp_return.append(((entry["commit"])["author"])["name"])
            # temp_return.append(commit_date)
            # temp_return.append(commit_time)
            # temp_return.append((entry["commit"])["message"])
            temp_return.append(sha)
            temp_return.append(author)
            temp_return.append(commit_date)
            temp_return.append(commit_time)
            temp_return.append(msg)
            temp_return.append(link)

            break  # Get only latest commit

    else:
        temp_return = ["Commit info could not be retrieved"]

    return temp_return


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
    repo_dict_big = {}
    in_name = request.form.get("user")
    response = requests.get(f"https://api.github.com/users/{in_name}/repos")
    if response.status_code == 200:
        repos = response.json()  # Returns list of repo entities

        # List containing names
        for repo in repos:
            temp_commit_info = get_commit_info(in_name, repo["name"])
            repo_list.append(repo["full_name"])
            repo_dict_big[repo["full_name"]] = temp_commit_info
        # Dict containing name: updated time
        repo_dict = {repo["full_name"]: repo["updated_at"] for repo in repos}

    return render_template(
        "result_user.html", user=in_name, repo_list=repo_list,
        repo_dict=repo_dict, temp_dict=repo_dict_big)
