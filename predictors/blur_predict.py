import cv2
import os

# THRESHOLD = 250
# IMG_DIM = (512,512)

def var_of_laplacian(img):
    return cv2.Laplacian(img, cv2.CV_64F).var()

def clear_directory(directory_path):
    for item in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            clear_directory(item_path)
            os.rmdir(item_path)

def predict_blurry(path, THRESHOLD, IMG_DIM):
    predictions = [[],[]]
    for file in os.listdir(path):
        if file == '.DS_Store': continue
        image_path = os.path.join(path, file)
        img = cv2.imread(image_path)
        resized = cv2.resize(img, IMG_DIM, cv2.INTER_AREA)
        grayscale = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        var = var_of_laplacian(grayscale)
        if var < THRESHOLD:
            # Blurry
            predictions[0].append(file)
        else:
            # Sharp
            predictions[1].append(file)
    return predictions