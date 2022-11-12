import shutil

from utils.ImageCrawler import fetch_images
from utils.ImageUtil import get_all_images_from_directory, delete_all_images_from_directory
from machine_learning.ml_model_functions import predict_multiple, train_model
import os

liked_dir = "data/liked"
disliked_dir = "data/disliked"


def create_moodboard(keywords: [str], quantity=15) -> [str]:
    """
    Generates a moodboard from a list of keywords.
    :param keywords: List of keywords.
    :param quantity: Amount of images generated.
    :return: List of image URLs.
    """
    cancel()

    images = fetch_images(keywords, quantity)
    local_images = get_all_images_from_directory("./temp")
    preferences = predict_multiple(local_images)

    liked_urls = []
    for i in range(len(preferences)):
        if preferences[i] == "liked":
            liked_urls.append(images[i])
        else:
            os.remove(local_images[i])

    return liked_urls


def cancel():
    """
    Cancel the "creation" of a moodboard. Deletes all temporary data and doesn't train the model.
    """
    if os.path.exists("temp"):
        shutil.rmtree("temp")
        print("temporary folder deleted")


def save_moodboard(images: [str]):
    """
    Save a moodboard, and train the machine learning model with the contents and the images removed from it.
    :param images:
    :return:
    """
    local_images = get_all_images_from_directory("./temp")

    stripped_images = []
    for img in images:
        stripped = img.split("/")
        stripped = stripped[len(stripped) - 1].split("?")
        stripped_images.append(stripped[0])

    # Move all the images that are liked to the liked folder
    for img in stripped_images:
        for local_img in local_images:
            if img in local_img:
                shutil.move(local_img, liked_dir)

    # Move all the images that are not liked to the disliked folder
    disliked = get_all_images_from_directory("./temp")
    for img in disliked:
        shutil.move(img, disliked_dir)

    # Train model
    train_model()

    # remove contents from liked and disliked folders after training
    delete_all_images_from_directory(liked_dir)
    delete_all_images_from_directory(disliked_dir)
