from flask import Flask, render_template

app = Flask(__name__)

prfiles = [
    {"name": "soso", "surname": "kereselidze", "age": 16}
]

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/sign-up")
def register():
    pass

@app.route("/profile/<profile_id>")
def profile(profile_id):
    return f"Hello {profile_id}"

if __name__ == "__main__":
    app.run(debug = True) 

