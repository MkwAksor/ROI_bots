import pyautogui
import keyboard
import random
import time
import os
import cv2
import numpy as np
import mss

version = 0.1

print("=======================================================")
print(f"||ROI_bot version: {version}")
print("=======================================================")
print('||Данный бот создан для принятия следующего матча в игре Pixel Gun 3D')
print("||в игре Pixel Gun 3D")
print("=======================================================")
print("||Клавиши считываются только на английской раскладке!!!")
print("=======================================================")
print("||Нажмите 'S' для запуска / паузы")
#print("||Нажмите 'Q' для остановки")
print("||Нажмите 'Esc' для выхода")
print("=======================================================")
# Завершение при нажатии клавиши 'Esc'
keyboard.add_hotkey('esc', lambda: os._exit(0))

# Настройка захвата экрана
sct = mss.MSS()
monitor = {"top": 820, "left": 1500, "width": 300, "height": 200}

# Получаем размеры экрана
screen_width, screen_height = pyautogui.size()

# Настройка диапазона зелёного цвета в HSV
lower_green = np.array([40, 50, 50])
upper_green = np.array([80, 255, 255])

# Переменные для расчета FPS
prev_time = time.time()
fps_list = []

# Глобальные переменные
run = False
stop = True

# Функция для клика с случайной длительностью 
def click():
    
    def interval_rand():
        interval = (random.randint(1, 5) / 100) + (random.randint(1, 9) / 1000)
        return interval

    pyautogui.mouseDown()
    time.sleep(interval_rand())
    pyautogui.mouseUp()
    time.sleep(interval_rand())

# Старт программы
def start():
    global run
     
    run = True

def FPS(frame):
    global prev_time, fps_list
    # === Расчет FPS ===
    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time
    fps_list.append(fps)

    if len(fps_list) > 10:
        fps_list.pop(0)
    avg_fps = sum(fps_list) / len(fps_list)

    cv2.putText(frame, f'FPS: {int(avg_fps)}', (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 25, 160), 2)
    # === Конец FPS ===        

if __name__ == '__main__':      

    start()
        
    while run:
        # Захват области экрана
        img = sct.grab(monitor)
        
        # Конвертация скриншота в NumPy массив (формат BGR для OpenCV)
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        
        # Получаем размеры кадра
        frame_height, frame_width = frame.shape[:2]

        FPS(frame) #Потеря производительности, проблемы
        
        # Определяем область правого нижнего угла (размером 1/4 от всего кадра) + 80 пикселей влево
        # Правая нижняя область размером 1/2 по ширине и 1/2 по высоте от четверти кадра
        roi_x = frame_width // 2 + frame_width // 4 - 80  # Начало области по X (3/4 ширины кадра)
        roi_y = frame_height // 2 + frame_height // 4  # Начало области по Y (3/4 высоты кадра)
        roi_width = frame_width // 4 + 80  # Ширина области (1/4 от ширины кадра)
        roi_height = frame_height // 4  # Высота области (1/4 от высоты кадра)

        # Вырезаем область интереса (ROI)
        roi = frame[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width]

        # Обрабатываем только область правого нижнего угла
        hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        mask_roi = cv2.inRange(hsv_roi, lower_green, upper_green)
        kernel = np.ones((5,5), np.uint8)
        mask_roi = cv2.morphologyEx(mask_roi, cv2.MORPH_CLOSE, kernel)
        
        # Поиск контуров зеленых областей в ROI
        contours, _ = cv2.findContours(mask_roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        cv2.rectangle(frame, (roi_x, roi_y), (roi_x + roi_width, roi_y + roi_height), (128, 128, 128), 1)
        cv2.putText(frame, 'Search Zone', (roi_x, roi_y - 5), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (128, 128, 128), 1)
        
        if not stop:
            found_green = False
            # Работа с найденными контурами
            for contour in contours:
                # Фильтруем маленькие контуры (шум)
                area = cv2.contourArea(contour)
                if area > 100:  # Минимальная площадь для обработки
                    found_green = True
                    # Получаем ограничивающий прямоугольник относительно ROI
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # 1. Центр объекта относительно захваченной картинки (300х200)
                    local_center_x = x + w // 2
                    local_center_y = y + h // 2
                    
                    # 2. Перевод в абсолютные координаты экрана
                    screen_x = monitor["left"] + local_center_x + 100
                    screen_y = monitor["top"] + local_center_y + 140

                    #pyautogui.click(screen_x, screen_y)
                    pyautogui.moveTo(screen_x, screen_y)
                    print(f"Клик по координатам: ({screen_x}, {screen_y})")
                    time.sleep(0.01)
                    break
                
            #if not found_green:
                #click()

        if cv2.waitKey(1) & 0xFF == ord("s"):
            if not stop:
                stop = True
            else:
                stop = False 
        
        if stop:
            cv2.putText(frame, 'stopped', (10, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (128, 128, 128), 2)
        
        # Отображение окон
        cv2.imshow('Original', frame)

time.sleep(2)
cv2.destroyAllWindows()
