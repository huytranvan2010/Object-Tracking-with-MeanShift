import numpy as np
import cv2
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=True, help='path to the video')
args = vars(ap.parse_args())

# Đọc video
video = cv2.VideoCapture(args["video"])

# Lấy frame đầu tiên
ret, frame = video.read()

# Xác định vị trí đầu tiên của window
x, y, w, h = 300, 200, 100, 50      # hardcode, tùy thuộc vào video
track_window = (x, y, w, h)

# vùng ROI để tracking
roi = frame[y:y+h, x:x+w]

# chuyển ROI về HSV space nhé
hsv_roi =  cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

# Tạo mask, để tránh ảnh hưởng điều kiện sáng tối, ở đây để H chạy toàn dải từ 0 đến 180
# Có thể bỏ mask đi, khi đó phần lấy roi_hist ở dòng 28 phải chuyển thành None
mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))

# Lấy histogram chỉ của vùng ROI, ở đây chỉ lấy histogram cho duy nhất 1 kênh H - Hue
# 1-st parameter là ảnh, 2-nd parameter thể hiện lấy 1 kênh, 3-st parameter là mask, 4-th là số bins, 5-th là khoảng giá trị
roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0,180])

# normalize histogram về khoảng giá trị 0-255, tham số thứ hai là giá trị trả về, cuối cùng là norm type
cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

# Setup the termination criteria, either 10 iteration or move by atleast 1 pt
term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

while True:
    ret, frame = video.read()

    if ret == True:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv], [0], roi_hist, [0,180], 1)

        # apply meanshift to get the new location
        ret, track_window = cv2.meanShift(dst, track_window, term_crit)

        # Draw it on image
        x,y,w,h = track_window
        img = cv2.rectangle(frame, (x,y), (x+w,y+h), 255,2)
        cv2.imshow('img', img)

        k = cv2.waitKey(30) & 0xff
        if k == ord("q"):       # nhấn q để thoát
            break
    else:
        break

cv2.destroyAllWindows()