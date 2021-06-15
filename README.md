Cách chạy:
```python
python meanshift_objecttracking.py --video slow_traffic.mp4
```

Meanshift chính là một thuật toán phân cụm trong machine learning, khác với K-Means cần biết số cụm trước Meanshift có thể tự động phân chia dữ liệu theo cụm. Meanshift có nhiều ứng dụng, một trong số đó là object tracking.

Ý tưởng phía sau Meanshift cũng khá đơn giản. Giả sử có tập hợp các điểm (có thể là phân bố pixel như histogram backprojection). Một window nhỏ được cho (có thể là vòng tròn), nhiệm vụ là di chuyển window đó đến nơi có mật độ pixel lớn nhất (số lượng điểm lớn nhất)
<img src="https://docs.opencv.org/master/meanshift_basics.jpg" style="display:block; margin-left:auto; margin-right:auto">

Window đầu "C1" có màu xanh, center của nó là "C1_o", tuy nhiên centroid của nó là "C1_r" (trung bình các tọa độ của các điểm trong window màu xanh). "C1_o" và "C1_r" không khớp với nhau. Bây giờ sẽ dịch chuyển window sau cho center của window mới trùng với centroid của window trước đó. Tuy nhiên center của window hiện tại lại không trùng với centroid của window hiện tại. Cứ thực hiện như vậy cho đến khi center và centroid của window trùng nhau (có sai số). Cuối cùng chúng ta đạt được window với phân bố pixel lớn nhất, được đánh dấu bằng màu xanh lá "C2".
<img src="https://docs.opencv.org/master/meanshift_face.gif" style="display:block; margin-left:auto; margin-right:auto">

Để sử dụng meanshift trong OpenCV, đầu tiên chúng ta cần xác định mục tiêu tracking, tìm histogram của nó để mà có thể backproject mục tiêu lên mỗi frame để phục vụ tính toán meanshift. Chúng ta cũng cần cung cấp vị trí đầu tiên của window (chưa mục tiêu). Đối với histogram cúng ta sẽ sử dụng **Hue**, ở đây không sử dụng **Saturation và Value** vì chúng bị ảnh hưởng bởi điều kiện sáng môi trường.

Meanshift có một số nhược điểm như sau:
* Phải tạo trước window, cần xác định vị trí của mục tiêu
* Khi vật thể ra khỏi khung hình, window vẫn còn, khi vật thể quay lại phải ở vị trí gần window nó mới track được
* Kích thước của window không đổi khi vật thể đi xa gần camera. Trong bài tiếp theo chúng ta sẽ nói về Camshift để giải quyết vấn đề này.


#### Tài liệu tham khảo
1. https://docs.opencv.org/master/d7/d00/tutorial_meanshift.html
2. https://www.youtube.com/watch?v=EDT0vHsMy34
3. https://www.bogotobogo.com/python/OpenCV_Python/images/mean_shift_tracking/slow_traffic_small.mp4
