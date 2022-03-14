import mediapipe as mp # Import mediapipe
import cv2 # Import opencv
import pydirectinput

mp_drawing = mp.solutions.drawing_utils # Drawing helpers
mp_holistic = mp.solutions.holistic # Mediapipe Solutions
mp_pose = mp.solutions.pose


cap = cv2.VideoCapture(1)
cap.set(3, 720)
cap.set(4, 540)
pose = ""
status = 0

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    
    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        # Recolor Feed
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)     
        
        # Make Detections
        results = holistic.process(image)   
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        height, width, _ = image.shape
        
        try: 
            right_hand = (results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].x * width,
                              results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].y * height)

        
            line_x1 = width//3
            line_x2 = 2 * (width//3)
            line_y1=height//3
            line_y2 = 2*(height//3)

            
            if (right_hand[0]>line_x2) and (right_hand[1]<line_y1) and  (right_hand[1]>0):
                pose = "Start"
                pydirectinput.keyDown('space')
                pydirectinput.keyUp('space')
                status = 1
            
            elif (right_hand[0]>line_x2) and (right_hand[1]>line_y1) and  (right_hand[1]<line_y2) and status == 1:
                pose = "Right"
                pydirectinput.keyDown('right')
                pydirectinput.keyUp('right')
            elif  (right_hand[0]<line_x1) and (right_hand[1]>line_y1) and  (right_hand[1]<line_y2) and status == 1:
                pose = "Left"
                pydirectinput.keyDown('left')
                pydirectinput.keyUp('left')
            elif (right_hand[1]<line_y1) and status == 1:
                pose="Jump"
                pydirectinput.keyDown('up')
                pydirectinput.keyUp('up')
            elif (right_hand[1]>line_y2) and status == 1:
                pose="Slide"
                pydirectinput.keyDown('down')
                pydirectinput.keyUp('down')
            elif status == 0:
                pose = "Please start the Game"
            else:
                pose="Run"
                
        except:
            pass

        cv2.putText(image, pose, (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,0), 3)
        cv2.line(image, (width//3, 0), (width//3, height), (255, 255, 255), 2)
        cv2.line(image, (2*(width//3), 0), (2*(width//3), height), (255, 255, 255), 2)

        cv2.line(image, (0, height//3), (width, height//3), (255, 255, 255), 2)
        cv2.line(image, (0, 2*(height//3)), (width,2*(height//3)), (255, 255, 255), 2)


        
        
        # 4. Pose Detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS, 
                                 mp_drawing.DrawingSpec(color=(180, 105, 255), thickness=5, circle_radius=8),
                                 mp_drawing.DrawingSpec(color=(255,255,255), thickness=10, circle_radius=10)
                                 )
                        
        cv2.imshow('Raw Webcam Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()