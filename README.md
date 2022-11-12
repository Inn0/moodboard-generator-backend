# Moodboard Generator
This application serves as the back-end for the Moodboard Generator project. 

The front-end for this project can be found [here](https://github.com/Inn0/moodboard-generator-frontend).

## Installation     
Clone, or download and extract the project to your local machine. Make sure you have Python and Pip installed. Run `pip install -r requirements.txt` in the root directory to download and install all the packages. 

## Running the project
Make sure the project is properly installed on your machine.
Run `python main.py` in the root directory, et voila.

## Endpoints
| URL       | Method | Body             | Type             | Returns                                      | Return type      |
|-----------|--------|------------------|------------------|----------------------------------------------|------------------|
| /generate | POST   | List of keywords | Array of Strings | List of image URLs representing a Moodboard. | Array of Strings |
| /save     | POST   | List of URLs     | Array of Strings | Nothing                                      | Void             |

---
Project made by [Daan Brocatus](https://daanbrocatus.nl/)
