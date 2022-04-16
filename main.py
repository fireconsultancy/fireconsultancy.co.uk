import os
from datetime import datetime

from flask import Flask
from flask import render_template, request, redirect

app = Flask(__name__)

# import config file with MySQL Host, User, Password and Database
app.config.from_pyfile(os.path.join(".", "app.conf"), silent=False)
mysql = MySQL(app)

# serve index page
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/favicon.ico")
def favicon():
    return "200"
    
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8082, debug=True)