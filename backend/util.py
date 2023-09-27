import os
from google.cloud import vision


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"/google/apijson/eminent-bond-278322-2cfd6c241bfa.json"

def get_img_content(api_request):

    is_file = False
    img_content = "No text detected"

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
    detected_text = "No text detected"
    try: 
        """Detects text in the file located in Google Cloud Storage or on the Web."""

        #   file_name = os.path.abspath(image_path)

        #   with io.open(file_name, 'rb') as image_file:
        #       content = image_file.read()

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

def get_translated_text(api_request):
    try: 
        is_file, file_content = get_img_content(api_request)

        if is_file == False:
            return file_content
        
        return detect_text_from_image(file_content)
    except:
        return "No text detected"