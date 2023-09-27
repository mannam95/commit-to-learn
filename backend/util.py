import os
from google.cloud import vision
from deep_translator import GoogleTranslator


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"/google/apijson/eminent-bond-278322-2cfd6c241bfa.json"

error_text = "Kein Text erkannt"

def get_img_content(api_request):

    is_file = False
    img_content = error_text

    try:
        print("API Request:", api_request)

        if 'fileName' not in api_request.files:
            print("error: No file part")
        
        file = api_request.files['fileName']
        if file.filename == '':
            print("error: No selected file")
        
        img_content = file.read()
        is_file = True

        return (is_file, img_content)

    except:
        return (is_file, img_content)


def detect_text_from_image(file_content):
    detected_text = error_text
    try: 
        """Detects text in the file located in Google Cloud Storage or on the Web."""

        content = file_content

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
            print(response.error.message)
            raise Exception(
                "{}\nFor more info on error messages, check: "
                "https://cloud.google.com/apis/design/errors".format(response.error.message)
            )
        return detected_text
    except:
        return detected_text

def translate_detected_text(detected_text):
    try: 
        translated_text = GoogleTranslator(source='auto', target='de').translate(detected_text) 
        
        return translated_text
    except:
        return error_text# Path: backend/util.py

def get_translated_text(api_request):
    try: 
        is_file, file_content = get_img_content(api_request)

        if is_file == False:
            return file_content
        
        detected_text = detect_text_from_image(file_content)

        return translate_detected_text(detected_text)
    except:
        return error_text