from flask import Blueprint, request
from services.MoodboardService import create_moodboard, save_moodboard
from machine_learning.ml_model_functions import predict_multiple, load_model, prediction
from utils.ImageUtil import get_all_images_from_directory

moodboard_controller = Blueprint('moodboard_controller', __name__)


@moodboard_controller.route("/generate", methods=["POST"])
def generate_moodboard():
    """
    This method handles POST calls to the `/generate` endpoint. It returns URls of images found using the keywords provided.
    Example body: ["dog", "blue"]

    """
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        json = request.json
        if isinstance(json, list) and len(json) >= 1:
            print(json)
            return create_moodboard(json)
        else:
            print("Please provide at least one keyword in an array! (e.g. [\"dog\"])")
    else:
        return 'Content-Type not supported!'


@moodboard_controller.route("/save", methods=["POST"])
def save():
    """
    This endpoint 'saves' a moodboard, and trains the model with this saved moodboard.
    Example body: ["URL1.jpg", "URL2.jpg"]
    """
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        json = request.json
        if isinstance(json, list) and len(json) >= 1:
            print(json)
            save_moodboard(json)
            return "Model trained!"
        else:
            print("Please provide at least one image url in an array! (e.g. [\"url\"])")
    else:
        return 'Content-Type not supported!'
