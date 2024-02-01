import firebase_admin
from firebase_admin import credentials, firestore, storage
import datetime


cred = credentials.Certificate('/home/rpi/firebase_keys/out-of-sight-814f2-firebase-adminsdk-3ozx8-8e66ae3f96.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'out-of-sight-814f2.appspot.com'
})

# Storage에 파일 업로드20y
bucket = storage.bucket()
file_path = '/home/rpi/Documents/sensors/camera/Videos/video.mp4'  # 로컬 파일 경로
storage_path = 'videos/video.mp4'      # Storage에서의 파일 경로
blob = bucket.blob(storage_path)
blob.upload_from_filename(file_path)
blob.make_public()  # 파일을 공개적으로 접근 가능하게 만듭니다

# get URL of uploaded file
video_url = blob.public_url

# save URL in Firestore
db = firestore.client()
video_data = {
    'videoUrl': video_url,
    'timestamp': datetime.datetime.now(),
    'userId' : "inkinkb"
}
db.collection('VIDEO').add(video_data)