import os, os.path
import glob


def get_all_images_from_directory(directory: str) -> [str]:
    """
    Returns paths for all images within a directory in a list.
    :param directory: The directory to get all the images from.
    :return: List of image locations.
    """
    imgs = []
    valid_images = [".jpg", ".png"]
    for f in os.listdir(directory):
        ext = os.path.splitext(f)[1]
        if ext.lower() not in valid_images:
            continue
        imgs.append(os.path.join(directory, f))
    return imgs


def delete_all_images_from_directory(directory: str):
    """
    Deletes all images from specified directory.
    :param directory: Location of the directory.
    """
    files = glob.glob(directory + '/*')
    for f in files:
        os.remove(f)
