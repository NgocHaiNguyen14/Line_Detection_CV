import cv2
import time
import math

global set_time
def record_video(output_filename='output.mp4', fps=20.0, resolution=(640, 480)):
    global set_time
    now = time.time()
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_filename, fourcc, fps, resolution)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        """out.write(frame)
        cv2.imshow('Recording...', frame)
        if (cv2.waitKey(1) & 0xFF == ord('q')) or (time.time() - now) >= set_time:
            break"""
        img = frame
        height, width, channels = img.shape
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.bilateralFilter(gray_img, 9, 75, 75)
        edges_img = cv2.Canny(blurred, 50, 150)  

        height_area_target = int(height * 0.85)
        width_area_target_1 = int(width * 0.25)
        width_area_target_2 = int(width * 0.75)

        x_target = 1e9
        y_target = 1e9
        u = 1e9
        u_old = 2e9

        for i in range(int(height * 0.9), int(height * 0.95), 1):
            check = False
            a, b, c = 1e9, 1e9, 1e9
            for j in range(width_area_target_1, width_area_target_2, 1):
                if edges_img[i][j] != 0 and check == False:
                    a, b = i, j
                    check = True
                elif edges_img[i][j] != 0 and check == True:
                    c = j
                    break
            if check == False or a == 1e9 or b == 1e9 or c == 1e9:
                continue
            khoang_cach = math.sqrt(
                abs(int((height + height_area_target) / 2) - a) * 2 + abs(int(width / 2) - int(b + c) / 2) * 2)
            # print()
            # print("x1 =",b, "y1 =", a, "x2 =", c, "y2 =", a, "dis =", khoang_cach, "u = ",u ,"u_old =",u_old)
            if a == 1e9 or b == 1e9 or c == 1e9 or khoang_cach == u_old:
                continue
            if khoang_cach < u and abs(khoang_cach - u) < abs(u - u_old) and u_old != 1e9:
                # print(abs(khoang_cach-u))
                # print("x1 =", b, "y1 =", a, "x2 =", c, "y2 =", a, "dis =", khoang_cach)
                x_target = int((height + height_area_target) / 2)
                y_target = int((b + c) / 2)
                u_old = u
                u = khoang_cach

        cv2.rectangle(img, (width_area_target_1, height_area_target), (width_area_target_2, int(height * 1.05)),
                      (0, 0, 255), int(height * width / 1e5))  
        cv2.line(img, (int(width / 2) - 2, int(height * 0.98)), (int(width / 2) + 2, int(height * 0.98)), (0, 255, 0),
                 int(height * width / 1e5) + 5)
        cv2.line(img, (int(y_target - 2), int(x_target * 0.98)), (int(y_target + 2), int(x_target * 0.98)),
                 (0, 255, 255), int(height * width / 1e5) + 5)
        print(x_target, y_target)
        out.write(edges_img)
        cv2.imshow('video', img)
        cv2.imshow('video_edge', edges_img)
        if cv2.waitKey(1) & 0xFF == ord('q') or (time.time() - now) >= set_time:
            break
    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    set_time = 50000 
    record_video()
