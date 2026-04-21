from flask import Flask, redirect

app = Flask(__name__)

# This sends anyone who hits the Vercel URL to your Render URL
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    # Change the URL below if you renamed your Render app!
    return redirect("https://flask-vroi.onrender.com/", code=301)
