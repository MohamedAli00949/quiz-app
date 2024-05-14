import cv2
import time
from cvzone.HandTrackingModule import HandDetector
from draw_rect import addRectText
from read_data import readData

# 0 is the id of the front camera
cameraCapture = cv2.VideoCapture(0)
# create cameraCapture
cameraCapture.set(3, 1280)
cameraCapture.set(4, 720)

# detectionCon: Minimum Detection Confidence Threshold
detector = HandDetector(detectionCon=0.8)

mcqList = readData()

q_no = 0
q_total = len(mcqList)

while True:
    if cameraCapture:
        success, img = cameraCapture.read()
        img = cv2.flip(img, 1)

        if success:
            hands, img = detector.findHands(img, flipType=False)
            if q_no < q_total:
                mcq = mcqList[q_no]
                (q_x_max, q_y_max) = addRectText(img, mcq.question, 100, 100)

                ch1_x_min = 150
                ch1_y_min = q_y_max + 150
                (ch1_x_max, ch1_y_max) = addRectText(img, mcq.choice1, ch1_x_min, ch1_y_min, [50, 50, 50, 50])

                ch2_x_min = int(int(int(q_x_max)/2) + 150)
                ch2_y_min = q_y_max + 150
                (ch2_x_max, ch2_y_max) = addRectText(img, mcq.choice2, ch2_x_min, ch2_y_min, [50, 50, 50, 50])

                ch3_x_min = 150
                ch3_y_min = (ch1_y_max + 150)
                (ch3_x_max, ch3_y_max) = addRectText(img, mcq.choice3, ch3_x_min, ch3_y_min, [50, 50, 50, 50])

                ch4_x_min = int(int(int(q_x_max)/2) + 150)
                ch4_y_min = (ch1_y_max + 150)
                (ch4_x_max, ch4_y_max) = addRectText(img, mcq.choice4, ch4_x_min, ch4_y_min, [50, 50, 50, 50])

                if hands:
                    lmList = hands[0]['lmList']
                    cursor = lmList[8]
                    length, info, img = detector.findDistance([lmList[8][0], lmList[8][1]], [lmList[12][0], lmList[12][1]], img, (255, 255, 0), 10)
                    if length < 50:
                        mcq.update(img, cursor, [
                            [ch1_x_min, ch1_y_min,  ch1_x_max, ch1_y_max],
                            [ch2_x_min, ch2_y_min, ch2_x_max, ch2_y_max],
                            [ch3_x_min, ch3_y_min, ch3_x_max, ch3_y_max],
                            [ch4_x_min, ch4_y_min, ch4_x_max, ch4_y_max]
                        ])
                        if mcq.userAns is not None:
                            time.sleep(0.2)
                            q_no += 1
            else:
                score = 0
                for mcq in mcqList:
                    if mcq.answer == mcq.userAns:
                        score += 1

                score = round((score / q_total) * 100, 2)

                (score_x_max, score_y_max) = addRectText(img, "Quiz completed", 250, 300)
                (score_x_max, score_y_max) = addRectText(img, f'Your Score: {score}', 700, 300)

            # draw progress bar
            progress = 150 + (950//q_total)*q_no
            cv2.rectangle(img, (150, 600), (progress, 650), (0, 255, 0), cv2.FILLED)
            cv2.rectangle(img, (150, 600), (1100, 650), (255, 0, 255), 5)
            addRectText(img, f'{round((q_no / q_total) * 100)}%', 1150, 610, [10, 15, 10, 10])


            cv2.imshow("image", img)
            # cv2.waitKey(1)
            if cv2.waitKey(1) == ord('q'):
                break
        else:
            print("Error: Unable to capture camera frame")