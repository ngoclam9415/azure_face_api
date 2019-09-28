import requests, json
import config as Config
from utils.database import Database

class SimilarityFinder:
    def __init__(self):
        self.headers_detect = {
                # Request headers
                'Content-Type': 'application/octet-stream',
                'Ocp-Apim-Subscription-Key': Config.subscription_key,
                }
        
        self.params_detect = {
            'recognitionModel' : 'recognition_02',
            'detectionModel': 'detection_02'
        }

        self.headers_find_similar = {
                # Request headers
                'Content-Type': 'application/json',
                'Ocp-Apim-Subscription-Key': Config.subscription_key,
                }


    def get_detected_face_id(self, image_path):
        body = open(image_path, "rb")
        response = requests.post(Config.http_endpoint+"/face/v1.0/detect", params=self.params_detect, headers=self.headers_detect, data=body)
        return response.json()

    def find_similar(self, image_path):
        detect_response = self.get_detected_face_id(image_path)
        # print(detect_response)
        detect_face_id = detect_response[0]["faceId"]
        body = {"faceId":detect_face_id,
                "faceListId":Config.faceListId,
                "maxNumOfCandidatesReturned ":4,
                }
        find_similar_response = requests.post(Config.http_endpoint+"/face/v1.0/findsimilars",headers=self.headers_find_similar, data=json.dumps(body))
        return find_similar_response.json()

if __name__ == "__main__":
    import numpy as np
    import glob, os
    from utils.database import Database
    import time

    image_path = "/mnt/sda2/face_dataset/VN-celeb/855/8.png"
    SF = SimilarityFinder()
    DB = Database()
    images_folder = Config.dataset_folder
    images_subfolders = glob.glob(os.path.join(images_folder, "*"))
    positive = 0
    batch_subfolders = images_subfolders[1:800]
    for index, subfolder in enumerate(batch_subfolders):
        images = glob.glob(os.path.join(subfolder, "*"))
        image = images[-1]
        print(image)
        try:
            response = SF.find_similar(image)
            predicted_persistedFaceId = response[0]["persistedFaceId"]
            predicted_faceId = DB.find_FaceId(predicted_persistedFaceId)
            gt_faceId = image.split("/")[-2]
            if gt_faceId == predicted_faceId:
                positive += 1
            else:
                print("{}./ Image : {}\n\tgroudtruth : {}, predicted : {}".format(index, image, gt_faceId, predicted_faceId))
        except Exception as e:
            print(e)
            time.sleep(60)
            try:
                response = SF.find_similar(image)
                predicted_persistedFaceId = response[0]["persistedFaceId"]
                predicted_faceId = DB.find_FaceId(predicted_persistedFaceId)
                gt_faceId = image.split("/")[-2]
                if gt_faceId == predicted_faceId:
                    positive += 1
                else:
                    print("{}./ Image : {}\n\tgroudtruth : {}, predicted : {}".format(index, image, gt_faceId, predicted_faceId))
            except:
                continue
    print("Azure total accuracy : ", positive/len(batch_subfolders))

