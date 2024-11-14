import cv2

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

ret, frame = cap.read()

if ret:
    cv2.imwrite("image.jpg", frame)
    print("Image saved as pi_camera_image.jpg")
else:
    print("Failed to capture image")

cap.release()
