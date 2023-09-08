import cv2
import mediapipe as mp
import pyautogui
import random
import numpy as np

height = 720
width = 1280
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()

x_coordinates = random.randint(0, screen_width-50)
y_coordinates = 0

show_shape = True
frame = []
index_x = 0
index_y = 0
center = 0
score = 0

shape_choices = ['rectangle', 'circle', 'triangle']
shape = random.choice(shape_choices)
colors = [(0, 0, 255), (0, 255, 0), (0, 255, 255)]
selected_color = random.choice(colors)

text = f"Score: {score}"
text_x = width - 160
text_y = 30
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
font_thickness = 2
font_color = (0,0,0)

shape_spawned = False

while True:
    
    _, frame = cap.read()
    # frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame = cv2.flip(frame, 1)
    # frame_height, frame_width, _ = frame.shape
    # print(frame.shape)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks
       
    if show_shape == True:  
        if shape =='rectangle':
            cv2.rectangle(frame, (x_coordinates, y_coordinates), (x_coordinates + 30, y_coordinates + 30), selected_color, thickness=-1)
            center = (x_coordinates+30)/2 + (y_coordinates+30)/2
        elif shape == 'circle':    
            cv2.circle(frame, (x_coordinates, y_coordinates), 20, selected_color, -1)
            
        elif shape == 'triangle':
            p1 = (x_coordinates, y_coordinates)
            p2 = (x_coordinates - 30, y_coordinates + 30)
            p3 = (x_coordinates + 30, y_coordinates + 30)
            # Define the vertices of the triangle
            vertices = [p1, p2, p3]
            # Convert vertices to NumPy array
            vertices = np.array(vertices)
            # Fill the triangle with the selected color
            cv2.fillPoly(frame, [vertices], selected_color)
            
    y_coordinates += 5
    
    
    if y_coordinates >= height:
        y_coordinates = 0
        x_coordinates = random.randint(0,width-50)
        shape = random.choice(shape_choices)
        selected_color = random.choice(colors)
        
        
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * width)
                y = int(landmark.y * height)
                
                if id == 8: # index tip
                    cv2.circle(img= frame, center= (x, y), radius= 10, color= (0,255,255))
                    index_x = screen_width/width*x
                    index_y = screen_height/height*y
                    
                    pyautogui.moveTo(index_x, index_y)
                                        
                # if id == 4: # thumb tip
                #     cv2.circle(img= frame, center= (x, y), radius= 10, color= (0,255,255))
                #     thumb_x = screen_width/width*x
                #     thumb_y = screen_height/height*y 
                #     # print("Outside", abs(index_y - thumb_y))
                #     if abs(index_y - thumb_y) < 20:
                #         pyautogui.click()
                
    distance = (abs(x_coordinates - index_x), abs(y_coordinates - index_y))
    
    if distance[0] <= 30 and distance[1] <= 30:
        print(distance)
        
        if selected_color == colors[0]:
            score -= 3
        elif selected_color == colors[1]:
            score += 5
        elif selected_color == colors[2]:
            score -= 2
    
        text = f"Score: {score}"
        y_coordinates = 0
        x_coordinates = random.randint(0,width-50)
        shape = random.choice(shape_choices)
        selected_color = random.choice(colors) 
        
        
    cv2.putText(frame, text, (text_x, text_y), font, font_scale, font_color, font_thickness)
    cv2.imshow('Virtual Mouse', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
    