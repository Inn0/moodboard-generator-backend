import os
from google_images_search import GoogleImagesSearch
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
CX = os.getenv('CX')

gis = GoogleImagesSearch(API_KEY, CX)


def fetch_images(keywords: [str], quantity: int) -> [str]:
    """
    This method returns image URLs based on certain keywords.

    :param keywords: The list of keywords.
    :type keywords: list of str
    :param quantity: The amount of images needed.
    :type quantity: int
    :return: List of URLs.
    :rtype: list of str
    """
    search_terms = ""
    for word in keywords:
        search_terms += word
        search_terms += ", "

    search_params = {
        'q': search_terms,
        'num': quantity,
        'fileType': 'jpg'
    }

    gis.search(search_params=search_params, path_to_dir="./temp")

    image_urls = []
    for image in gis.results():
        image_urls.append(image.url)

    return image_urls
