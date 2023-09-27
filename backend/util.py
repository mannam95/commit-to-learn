import os, io
from google.cloud import vision
import pandas as pd


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"eminent-bond-278322-2cfd6c241bfa.json"

def detect_text_from_image(image_path):
    detected_text = "No text detected"
    try: 
      """Detects text in the file located in Google Cloud Storage or on the Web."""

      file_name = os.path.abspath(image_path)

      with io.open(file_name, 'rb') as image_file:
          content = image_file.read()

      # construct an image instance
      client = vision.ImageAnnotatorClient()
      image = vision.Image(content=content)

      """
      # or we can pass the image url
      image = vision.types.Image()
      image.source.image_uri = 'https://edu.pngfacts.com/uploads/1/1/3/2/11320972/grade-10-english_orig.png'
      """

      response = client.text_detection(image=image)
      texts = response.text_annotations

      for text in texts:
          detected_text = text.description
          break

      if response.error.message:
          raise Exception(
              "{}\nFor more info on error messages, check: "
              "https://cloud.google.com/apis/design/errors".format(response.error.message)
          )
      return detected_text
    except:
      return detected_text

def get_translated_text():
    try:
        return detect_text_from_image("./images/dummy1.png")
    except:
        return "No text detected"