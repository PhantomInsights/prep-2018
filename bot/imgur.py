"""This module uploads an image to Imgur and returns back the permanent link url."""

import requests

import config


def upload_image(file_name, image_path):
    """Uploads an image to Imgur and returns the permanent link url.

    Parameters
    ----------
    file_name : str
        The name of the file used for the log.
    image_path : str
        The path of the file to be uploaded.

    Returns
    -------
    str
        The url generated from the Imgur API.

    """

    url = "https://api.imgur.com/3/image"
    headers = {"Authorization": "Client-ID " + config.IMGUR_CLIENT_ID}
    files = {"image": open(image_path, "rb")}

    with requests.post(url, headers=headers, files=files) as response:

        # We extract the new link from the response.
        image_link = response.json()["data"]["link"]

        # Update the log with the latest url and timestamp.
        with open("imgur-log.txt", "a", encoding="utf-8") as log_file:
            log_file.write("{} - {}\n".format(image_link, file_name))

        return image_link
