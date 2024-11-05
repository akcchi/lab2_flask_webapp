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
                f'<a href="{link}" target="_blank">GitHub link&#128279</a>')
            link = (
                '<th align="left">Direct link to commit</th>' +
                f"<td>{link}</td>")

            sha = entry["sha"]
            sha = (
                '<th align="left">Commit ID (SHA hash)</th>' +
                f"<td>{sha}</td>")

            author = ((entry["commit"])["author"])["name"]
            author = (
                '<th align="left">Commit author</th>' + f"<td>{author}</td>")

            # date = ((entry["commit"])["author"])["date"]

            msg = (entry["commit"])["message"]
            msg = '<th align="left">Commit message</th>' + f"<td>{msg}</td>"

            temp_timestamp = ((entry["commit"])["author"])["date"]
            commit_date, temp_time = temp_timestamp.split("T")
            commit_time = temp_time.rstrip("Z")
            commit_time += " UTC"
            commit_date = (
                '<th align="left">Commit date</th>' +
                f"<td>{commit_date}</td>")
            commit_time = (
                '<th align="left">Commit time</th>' +
                f"<td>{commit_time}</td>")

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
    # repo_list = []
    repo_dict_big = {}
    in_name = request.form.get("user")
    user_plain = in_name
    response = requests.get(f"https://api.github.com/users/{in_name}/repos")
    if response.status_code == 200:
        user_link = f"https://github.com/{in_name}"
        in_name = f'<a href="{user_link}" target="_blank">{in_name}</a>'
        repos = response.json()  # Returns list of repo entities

        for repo in repos:
            temp_commit_info = get_commit_info(user_plain, repo["name"])
            # repo_list.append(repo["full_name"])
            temp_name = repo["full_name"]
            temp_link = repo["html_url"]
            key = f'<a href="{temp_link}" target="_blank">{temp_name}</a>'
            repo_dict_big[key] = temp_commit_info
        # Dict containing name: updated time
        # repo_dict = {repo["full_name"]: repo["updated_at"] for repo in repos}
    else:
        in_name += (
            " (USERNAME NOT FOUND/DOES NOT EXIST - " +
            "no public repos to show)")
        repo_dict_big["Nothing to show"] = ""

    return render_template(
        "result_user.html", user=in_name, user_plain=user_plain,
        temp_dict=repo_dict_big)
