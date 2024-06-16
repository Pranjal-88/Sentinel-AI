from ultralytics import YOLO
import cv2
import requests

num=0
model_pth=r'C:\Users\HP\OneDrive\Desktop\PranCode\MLH\Weapon.pt'
# model_pth=r'C:\Users\HP\OneDrive\Desktop\PranCode\MLH\Vandalism\vandalism.pt'

model=YOLO(model_pth)
cap=cv2.VideoCapture(0)
camera_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
camera_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
while True:
    _,frame=cap.read(0)
    results=model.predict(frame,show=True,save=False,conf=0.6)
    for r in results:
        x=len(r.boxes)
        if (x!=0):
            url = 'http://127.0.0.1:5000/'
            myobj = {'camera': {'location_id': '', 'ip': '192.168.50.80', 'activity_detected': 'warning message'}}
            x = requests.post(url, json = myobj)
    k=cv2.waitKey(1)
    if k==27:
        break

cap.release()
cv2.destroyAllWindows()






