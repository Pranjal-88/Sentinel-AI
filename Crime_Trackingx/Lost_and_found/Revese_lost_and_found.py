from sympy import false
import ultralytics
from ultralytics import YOLO
import cv2
import mediapipe as mp
import numpy as np
import os

folder_pth=r'C:\Users\HP\OneDrive\Desktop\PranCode\MLH\Lost_and_found\Owner'
print("hi")
#->BLAZEFACE
mp_face_detection=mp.solutions.face_detection
face_detection=mp_face_detection.FaceDetection(min_detection_confidence=0.45)


def distance(x1,x2,y1,y2):
    pt1=np.array([x1,y1])
    pt2=np.array([x2,y2])
    d=np.linalg.norm(pt1-pt2)
    return d

x1=0
y1=0
num=0
threshold_distance=0
current_dist=0

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)
camera_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
camera_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

model_pth = r'C:\Users\HP\OneDrive\Desktop\PranCode\MLH\Lost_and_found\yolov8l.pt'
model = YOLO(model_pth)

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while True:
        _, frame = cap.read()

        results = model.predict(frame, show=False, classes=[24, 26], conf=0.3, save=False)
        for r in results:
            num=len(r.boxes)
            stacked_tensor=r.boxes.xywhn
            for (x,y,w,h) in stacked_tensor:
                x = int(float(x) * camera_width)
                y = int(float(y) * camera_height)
                w = int(float(w) * camera_width)
                h = int(float(h) * camera_height)
                
                x1=x
                y1=y
                threshold_distance=int(1.5*w)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame)
        frame=cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
        if (num!=0):
            if results.pose_landmarks:
                left_wrist = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
                right_wrist = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]

                h, w, _ = frame.shape
                left_wrist_x, left_wrist_y = int(left_wrist.x * camera_width), int(left_wrist.y * camera_height)
                right_wrist_x, right_wrist_y = int(right_wrist.x * camera_width), int(right_wrist.y *camera_height)

                cv2.circle(frame, (left_wrist_x, left_wrist_y), 1, (0, 255, 0), -1)
                d1=distance(x1,left_wrist_x,y1,left_wrist_y)
                cv2.circle(frame, (right_wrist_x, right_wrist_y), 1, (0, 255, 0), -1)
                d2=distance(x1,left_wrist_x,y1,left_wrist_y)

                if (d1>d2):
                    main_x=left_wrist_x
                    main_y=left_wrist_y
                    current_dist=d2
                else:
                    main_x=right_wrist_x
                    main_y=right_wrist_y
                    current_dist=d1

                if (current_dist>=threshold_distance):
                    color=(0,0,255)
                    nose=results.pose_landmarks.landmark[0]
                    w=distance(left_wrist_x,right_wrist_x,left_wrist_y,right_wrist_y)
                    nose_x,nose_y=int(nose.x*camera_width),int(nose.y*camera_height)
                    cv2.rectangle(frame,pt1=(int(nose_x-w/2),int(nose_y-w/2)),pt2=(int(nose_x+w/2),int(nose_y+w/2)),color=(255,0,0),thickness=2)
                    new_img=frame[int(nose_y-w/2):int(nose_y+w/2),int(nose_x-w/2):int(nose_x+w/2)]
                    cv2.imwrite(os.path.join(folder_pth,'Expected_owner.jpg'),new_img)
                else:
                    color=(0,255,0)
                cv2.line(frame,pt1=(x1,y1),pt2=(main_x,main_y),color=color,thickness=1,lineType=cv2.LINE_AA)

        cv2.imshow('Frame', frame)

        k = cv2.waitKey(1)
        if k == 27:
            break

cap.release()
cv2.destroyAllWindows()
