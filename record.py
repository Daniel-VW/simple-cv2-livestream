import cv2

stream_url = "http://192.168.30.142:8443"

cap = cv2.VideoCapture(stream_url)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for mp4 file
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame.")
        break

    # Write the frame into the file
    out.write(frame)

    # Show the live stream in a window
    cv2.imshow('Live Stream', frame)

    # Stop recording and close windows when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release everything when done
cap.release()
out.release() 
cv2.destroyAllWindows()
