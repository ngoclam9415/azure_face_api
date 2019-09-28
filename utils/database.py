from pymongo import MongoClient
from config import Mongo

class Database:
    def __init__(self):
        self.mongo_client = MongoClient(Mongo.IP, Mongo.PORT)
        self.face_info = self.mongo_client[Mongo.face_info_db]
        self.azure_id = self.face_info[Mongo.azure_collection]

    def add_FaceId(self, image_path, persistedFaceId):
        faceid = image_path.split('/')[-2]
        data = {"image_path" : image_path,
                "persistedFaceId" : persistedFaceId, 
                "faceid" : faceid}
        self.azure_id.insert_one(data)

    def find_FaceId(self, persistedFaceId):
        cursor = self.azure_id.find_one({"persistedFaceId" : persistedFaceId})
        try:
            face_id = cursor["faceid"]
            return face_id
        except:
            pass
        return None
        

if __name__ == "__main__":
    DB = Database()
    # DB.add_FaceId("/mnt/sda2/face_dataset/VN-celeb/1021/thanhlong.jpg", "e50cc3d5-0ce3-45fc-af9b-4fef5277e724")
    cursor = DB.find_FaceId("e50cc3d5-0ce3-45fc-af9b-4fef5277e724")
    print(cursor)