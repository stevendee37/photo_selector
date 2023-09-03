import cv2
import torch
import numpy as np
from predictors.relic1_model import NIMA
from torchvision import transforms
import os

def get_score(y_pred):
    w = torch.from_numpy(np.linspace(1,10,10))
    w = w.type(torch.FloatTensor)

    w_single = w.repeat(y_pred.size(0))

    score = (y_pred * w_single).sum()

    score_np = score.data.numpy()
    return score, score_np

def predict_aesthetic(path):
    model_state_dict = torch.load("predictors/relic1_model.pth", map_location=torch.device('cpu'))
    model = NIMA()
    model.load_state_dict(model_state_dict)
    model.eval()

    convert_tensor = transforms.ToTensor()
    result = [[],[],[],[]]
    for file in os.listdir(path):
        if file == '.DS_Store': continue
        image_path = os.path.join(path, file)
        img = cv2.imread(image_path)
        resized = cv2.resize(img, (224,224), cv2.INTER_AREA)
        tensor = convert_tensor(resized)

        pred = model(tensor.unsqueeze(0))
        score, score_np = get_score(pred)
        score = int(score)
        if score > 5:
            result[0].append(file)
        elif score > 4:
            result[1].append(file)
        elif score > 3:
            result[2].append(file)
        else:
            result[3].append(file)
    return result
