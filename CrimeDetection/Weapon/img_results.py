import cv2
from ultralytics import YOLO
import os
import requests

img_pth=r'C:\Users\HP\OneDrive\Desktop\PranCode\MLH\Vandalism\img1.jpg'
model_pth=r'C:\Users\HP\OneDrive\Desktop\PranCode\MLH\Weapon.pt'
result_pth=r'C:\Users\HP\OneDrive\Desktop\PranCode\MLH\Vandalism'

cap=cv2.VideoCapture(0)
camera_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
camera_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

model=YOLO(model_pth)

img=cv2.imread(img_pth)

results=model.predict(source=img,show=False,conf=0.3)
for r in results:
            length=len(r.boxes)
            print(length)
            stacked_tensor=r.boxes.xywhn
            for (x,y,w,h) in stacked_tensor:
                x=int(float(x)*camera_width)
                y=int(float(y)*camera_height)
                w=int(float(w)*camera_width)
                h=int(float(h)*camera_height)
                x1=int(x-w/2)
                y1=int(y-h/2)
                cv2.rectangle(img,pt1=(x1,y1),pt2=(x1+w,y1+h),color=(0,0,255),thickness=2)
                cv2.imwrite(os.path.join(result_pth,'Result.jpg'),img)


                # url = 'http://127.0.0.1:5000/'
                # myobj = {'camera': {'location_id': '', 'ip': '192.168.50.80', 'activity_detected': 'warning message'}}
                # x = requests.post(url, json = myobj)

