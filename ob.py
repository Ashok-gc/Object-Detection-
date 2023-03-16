import cv2

# Set threshold to detect objects
thres = 0.45

# Load class names
classNames = []
classFile = 'coco.names'
with open(classFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

# Load model
configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'frozen_inference_graph.pb'
net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

# For image
# img = cv2.imread('lena.png')
# classIds, confs, bbox = net.detect(img, confThreshold=thres)

# For video clip or real time
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4,720)
cap.set(10,70)

while True:
    success, img = cap.read()
    classIds, confs, bbox = net.detect(img, confThreshold=thres)

    # Draw bounding box and label for each object detected
    if len(classIds) != 0:
        for classId, confidence, box in zip(classIds.flatten(),confs.flatten(),bbox):
            cv2.rectangle(img, box, color=(0,255,0),thickness=3)
            cv2.putText(img, classNames[classId-1].upper(), (box[0]+10, box[1]+30),
                cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
            cv2.putText(img, str(round(confidence*100,2)), (box[0] + 200, box[1] + 30),
                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    # Display output image or video
    cv2.imshow("Output",img)

    # Exit on 's' key press
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        break

# Release video capture and close windows
cap.release()
cv2.destroyAllWindows()
