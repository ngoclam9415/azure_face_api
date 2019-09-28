import http.client, urllib.request, urllib.parse, urllib.error, base64, json, requests
import config as Config


class AddFace:
    def __init__(self):
        self.headers = {
            # Request headers
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': Config.subscription_key,
        }

        self.params = {
            # Request parameters
            'detectionModel': 'detection_02',
        }
    def add_face(self, image_path):

        body = open(image_path, "rb")
        response = requests.post(Config.http_endpoint+"/face/v1.0/facelists/{}/persistedFaces".format(Config.faceListId), params=self.params, headers=self.headers, data=body)
        return response.json()


if __name__ == "__main__":
    import numpy as np
    import glob, os
    from utils.database import Database
    import time
    DB = Database()
    requester = AddFace()
    images_folder = Config.dataset_folder
    images_subfolders = glob.glob(os.path.join(images_folder, "*"))
    skip = True
    for index, subfolder in enumerate(images_subfolders[0:800]):
        print(subfolder)
        if subfolder.split("/")[-1] == "855":
            skip = False
        if not skip:
            images = glob.glob(os.path.join(subfolder, "*"))
            image = images[0]
            try:
                request = requester.add_face(image)
                DB.add_FaceId(image, request["persistedFaceId"])
                print("{}./Finish adding {} with id {}".format(index, image, request["persistedFaceId"]))
            except Exception as e:
                print(e)
                time.sleep(60)
                try:
                    request = requester.add_face(image)
                    DB.add_FaceId(image, request["persistedFaceId"])
                    print("{}./ Finish adding {} with id {}".format(index, image, request["persistedFaceId"]))
                except:
                    continue


    # image_path = "/mnt/sda2/face_dataset/VN-celeb/1017/0.png"
    # response = requester.add_face(image_path)
    # print(response)
