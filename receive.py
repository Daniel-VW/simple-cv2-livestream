import cv2

stream_url = "http://your_livestream_url_here"

cap = cv2.VideoCapture(stream_url)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame.")
        break

    cv2.imshow('Live Stream', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
