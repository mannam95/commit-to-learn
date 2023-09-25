import easyocr

reader = easyocr.Reader(['en','de'])

def get_detected_text(image_path):
    try:
        bounds = reader.readtext(image_path)

        if len(bounds) == 0:
            return "No text detected1"
        else:
            detected_texts = [bound[1] for bound in bounds]

            result_string = " \n ".join(detected_texts)

            return result_string
    except:
        return "No text detected2"

def get_translated_text():
    try:
        return get_detected_text("./images/dummy1.png")
    except:
        return "No text detected3"