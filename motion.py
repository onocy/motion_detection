import cv2

initial_frame = None
capture = cv2.VideoCapture(0)

while True: 
    state, current_frame = capture.read()
    gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(21,21),0)
    
    if initial_frame is None:
        initial_frame = gray
        continue
        
    delta = cv2.absdiff(initial_frame, gray)
    threshold = cv2.threshold(delta, 30, 255, cv2.THRESH_BINARY)[1]
    threshold = cv2.dilate(threshold, None, iterations=2)
    
    (contours,_)=cv2.findContours(threshold.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) < 15000:
            continue

        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(current_frame, (x, y), (x+w, y+h), (255,0,0), 2)
    
    cv2.imshow("Gray", gray)
    cv2.imshow("Delta", delta)
    cv2.imshow("Threshold", threshold)
    cv2.imshow("Color", current_frame)
    
    key = cv2.waitKey(1) 
    if key==ord('q'):
        break 
    
capture.release()
cv2.destroyAllWindows