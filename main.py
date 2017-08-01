from flask import Flask, render_template, url_for, request, redirect, session
from data import data_manager
import json
import psycopg2
import pw_hash

app = Flask('codecool_series')
app.secret_key = "This is a super secret key, i am the only one, who knows the content of this string"


@app.route("/table_data", methods=["GET", "POST"])
def table_data():
    result = data_manager.top_rated_shows()
    for dictionary in result:
        for k, v in dictionary.items():
            if k == "genres":
                v = v.split(",")
                if len(v) > 3:
                    del v[3:]
                dictionary[k] = v
                dictionary[k] = ', '.join(dictionary[k])
        stringified_dict = dict((k, str(v)) for k, v in dictionary.items())
        dictionary.update(stringified_dict)
    json_obj = json.dumps(result)
    return json_obj


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('main.html')


@app.route('/registration', methods=["GET", "POST"])
def registration():
    try:
        if request.method == "POST":
            name = request.form['name']
            email = request.form['email']
            username = request.form['username']
            password = request.form['password']
            confirm_pw = request.form['confirm']
            if password == confirm_pw:
                password = pw_hash.hash_pw(password)
                data_manager.reg_new_user(data_manager.establish_connection(), name, email, username, password)
            else:
                message = "Passwords don't match. Try again."
                return render_template('main.html', message=message)
    except psycopg2.IntegrityError:
        return redirect('/')
    return render_template('main.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        password = pw_hash.hash_pw(password)
        data_from_db = data_manager.get_user_data(username)
        if data_from_db == []:
            print("no user named like this")
        else:
            for elem in data_from_db:
                if elem['username'] == username and elem['password'] == password:
                    session['username'] = username
                elif elem['password'] != password:
                    print("Wrong password")
    return render_template("main.html")


@app.route("/detailed/<show_id>", methods=["GET", "POST"])
def detailed(show_id):
    detailed_info = data_manager.detailed_info(show_id)
    season_info = data_manager.season_list(show_id)
    return render_template("detailed_page.html", detailed_info=detailed_info, season_info=season_info)


@app.route("/detailed/<show_id>/youtube", methods=["GET", "POST"])
def youtube_link(show_id):
    link = request.form["youtube_link"]
    link = link.replace("watch?v=", "embed/")
    data_manager.youtube_link(data_manager.establish_connection(), link, show_id)
    return redirect(url_for("detailed", show_id=show_id))


@app.route("/detailed/overview/<show_id>/<season_id>", methods=["GET", "POST"])
def overview_handler(show_id, season_id):
    overview_data = request.form["overview_input_data"]
    data_manager.overview(overview_data, season_id)
    return redirect(url_for("detailed", show_id=show_id, season_id=season_id))


@app.route("/edit/<show_id>", methods=["GET", "POST"])
def edit_show(show_id):
    detailed_info = data_manager.detailed_info(show_id)
    return render_template("edit_show.html", detailed_info=detailed_info)


@app.route("/edit/<show_id>/new_data", methods=["GET", "POST"])
def new_data(show_id):
    season = request.form["season"]
    episode = request.form["episode"]
    title = request.form["name"]
    length = request.form["length"]
    print(season, episode, title, length)
    return redirect(url_for("edit_show"), new_data=new_data)


@app.route("/delete/<show_id>", methods=["GET", "POST"])
def delete_show(show_id):
    data_manager.delete(data_manager.establish_connection(), show_id)
    return redirect("/")


@app.route("/deleted_shows")
def deleted_page():
    deleted = data_manager.display_deleted_shows()
    return render_template("deleted.html", deleted=deleted)


@app.route("/deleted/restore", methods=["GET", "POST"])
def restore_deleted_show():
    show_id = request.form['deletedShowId']
    return redirect(url_for("deleted_page"))


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
