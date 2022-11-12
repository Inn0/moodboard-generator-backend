import numpy as np
import tensorflow as tf
from PIL.Image import Image

img_height = 128
img_width = 128
model_name = "default_model"
class_names = ["liked", "disliked"]
data_dir = "./data"


def load_ds():
    """
    This method loads the dataset provided in the `data` directory. It returns a training dataset and a validation
    dataset using the 80/20 split.
    :returns: Tuple of datasets.
    :rtype: tuple
    """
    batch_size = 1

    train_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size)

    val_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size)

    return train_ds, val_ds


def create_model():
    """
    This method creates and compiles a machine learning model.
    :returns: The compiled model.
    """
    model = tf.keras.Sequential([
        tf.keras.layers.Rescaling(1. / 255),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(len(class_names))
    ])
    compiled_model = compile_model(model)
    return compiled_model


def compile_model(model):
    """
    This method compiles a model.
    :param model: The model to be compiled.
    :return: The compiled model.
    """
    model.compile(
        optimizer='adam',
        loss=tf.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=['accuracy']
    )
    return model


def train_model():
    """
    This method trains and saves the machine learning model.
    """
    epochs = 1
    model = load_model()
    train_ds, val_ds = load_ds()

    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs
    )
    save_model(model)


def preprocess_image(url: str) -> Image:
    """
    This method preprocesses an image for use in machine learning.
    :param url: URL to the (local) image.
    :return: Preprocessed image.
    :rtype: Image
    """
    return tf.keras.preprocessing.image.load_img(
        url, target_size=(img_height, img_width)
    )


def prediction(test_image_url: str) -> str:
    """
    Cast a prediction on a singular image.

    :param test_image_url: Path to local image.
    :return: 'liked' or 'disliked'
    """
    model = load_model()
    test_image = preprocess_image(test_image_url)

    # Create a batch with one image in it
    input_array = tf.keras.preprocessing.image.img_to_array(test_image)
    input_array = np.array([input_array])
    prediction = model.predict(input_array)[0]
    prediction_index = np.argmax(prediction)
    return class_names[prediction_index]


def predict_multiple(images: [str]) -> [str]:
    """
    Cast a prediction on an array of images.

    :param images: Array of images to cast predictions on.
    :return: Array of 'liked' or 'disliked'.
    """
    images_to_predict = []
    model = load_model()
    for img in images:
        img = preprocess_image(img)
        img = tf.keras.preprocessing.image.img_to_array(img)
        img = np.array([img])
        images_to_predict.append(img)

    result = model.predict(np.vstack(images_to_predict))
    prediction_results = []
    for res in result:
        prediction_results.append(class_names[np.argmax(res)])

    save_model(model)

    return prediction_results


def save_model(model):
    """
    Save a model to the `ml_models/` directory
    :param model: The model that should be saved.
    """
    model.save("ml_models/" + model_name)


def load_model():
    """
    Load or create a machine learning model. Creates a new model if one does not already exist with the specified name.
    :return: Machine Learning model.
    """
    try:
        return tf.keras.models.load_model("ml_models/" + model_name)
    except OSError:
        return create_model()
