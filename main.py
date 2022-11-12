import os.path
import shutil

from flask import Flask
from flask_cors import CORS
from controllers.MoodboardController import moodboard_controller

app = Flask(__name__)
# CORS(app)
app.register_blueprint(moodboard_controller)

if __name__ == "__main__":
    if os.path.exists("temp"):
        shutil.rmtree("temp")
        print("temporary folder deleted")
    app.run()
