import cv2
import csv

class MCQ():
    def __init__(self, data):
        self.question = data[0]
        self.choice1 = data[1]
        self.choice2 = data[2]
        self.choice3 = data[3]
        self.choice4 = data[4]
        self.answer = int(data[5])

        self.userAns = None

    def update(self, img, cursor, boxs, ansPadding=[50, 50, 50, 50]):
        for x, box in enumerate(boxs):
            x1, y1, x2, y2 = box
            if x1-(ansPadding[3]+2) < cursor[0] < x2+ansPadding[2] and y1-(ansPadding[3]+2) < cursor[1] < y2+ansPadding[1]:
                self.userAns = x+1
                cv2.rectangle(img, (x1-(ansPadding[3]), y1-ansPadding[0]), (x2+(ansPadding[3]+2), y2+ansPadding[1]), (0, 255, 0), cv2.FILLED)



def readData():
    # import csv file data
    pathCSV = "questions.csv"

    with open(pathCSV, newline='\n') as f:
        reader = csv.reader(f)
        dataAll = list(reader)[1:]

    mcqList = []
    for q in dataAll:
        mcqList.append(MCQ(q))

    return mcqList