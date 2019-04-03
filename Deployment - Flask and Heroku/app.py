from flask import Flask, render_template, request, url_for,flash,redirect,session
from get_lyrics_and_moods import *
import requests

app = Flask(__name__)

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]

@app.route("/home")

def home():
    my_song_df = dummy_main()
    #print(type(my_song_df.columns.values))
    new_df = my_song_df[['icon_url','title','artist','mood']]
    return render_template('home.html', tables=[new_df.to_html(classes='data')], titles = new_df.columns.values)

@app.route("/index", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def index():
    error = "None"
    try:
        if request.method == "POST":
            song_name = request.form["song_name"]
            artist_name = request.form["artist_name"]
            lyrics = get_lyrics_by_api_call(song_name, artist_name)
            lyrics_dict = lyrics.to_dict(orient="records")
            my_song_df = dummy_main()
            data = my_song_df.to_dict(orient="records")
            #print(data)
            headers = my_song_df.columns
            #print(headers)
            return render_template("index.html", data=data, lyrics_dict=lyrics_dict, headers=headers)
        else:
            my_song_df = dummy_main()
            data = my_song_df.to_dict(orient="records")
            #print(data)
            headers = my_song_df.columns
            #print(headers)
            return render_template("index.html", data=data, headers=headers)

    except Exception as e:
        flash("Some Error occured")
        return render_template("index.html", error = error)



if __name__ == '__main__':
    # app.secret_key = 'super secret key'
    # app.config['SESSION_TYPE'] = 'filesystem'
    # session.init_app(app)
    app.run(debug=True)