import pyautogui
import keyboard
import time
import os
import cv2
import numpy as np
import mss

version = 0.1

print("=======================================================")
print(f"||ROI_bot version: {version}")
print("=======================================================")
print('||Данный бот создан для афк рыбалки в майнкрафте')
print("=======================================================")
print('||Для корректной работы необходимо запустить игру')
print('||в небольшом окне (1/4 экрана) и расположить окно')
print('в нижнем правом углу, около часов, включить субтитры')
print("||в игре, поставить русский язык, стоять на земле или")
print("||убрать из поля зрения песок или белые блоки")
print("=======================================================")
print("||Клавиши считываются только на английской раскладке!!!")
print("=======================================================")
print("||Нажмите 'S' для запуска / паузы")
print("||Нажмите 'Esc' для выхода")
print("=======================================================")

keyboard.add_hotkey('esc', lambda: os._exit(0))

sct = mss.MSS()
monitor = {"top": 880, "left": 1710, "width": 210, "height": 140}

WHITE_THRESHOLD_PERCENT = 0.83

run = False
stop = True

def start():
    global run
     
    run = True
    
if __name__ == '__main__':      

    start()
        
    while run:
        print("Бот запущен (режим подсчета белого цвета)! Нажмите 'Esc' для выхода.")
        
        while True:
            # 1. Захватываем экран и переводим в оттенки серого
            img = np.array(sct.grab(monitor))
            gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)

            # 2. Оставляем ТОЛЬКО ярко-белые пиксели (буквы субтитров имеют яркость ~240-255)
            # Все пиксели темнее 220 станут черными (0), а светлее 220 — чисто белыми (255)
            _, mask = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)

            # 3. Считаем процент белого цвета в области
            white_pixels = cv2.countNonZero(mask)
            total_pixels = mask.shape[0] * mask.shape[1]
            white_percent = (white_pixels / total_pixels) * 100

            # 4. Проверяем условие поклевки
            if white_percent >= WHITE_THRESHOLD_PERCENT and (not stop):
                print(f"[+] СРАБОТАЛО! Белого цвета: {white_percent:.2f}% ({white_pixels} пикс.)")
                
                pyautogui.click(button='right')  # Подсекаем
                time.sleep(0.4)                  # Ждем возврата поплавка
                pyautogui.click(button='right')  # Закидываем снова

                print('Откат 3.5 секунды')
                
                # ВАЖНО: Ждем 3.5 секунды, чтобы исчез субтитр от самого броска удочки ("Поплавок летит"),
                # иначе бот тут же среагирует на белые буквы от собственного заброса!
                time.sleep(3.5)
                prev_time = time.time()
                print('Откат прошёл')


            # Делаем копию маски, чтобы текст FPS не влиял на подсчет пикселей
            display_frame = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            cv2.putText(display_frame, f'White: {white_percent:.2f}%', (10, 25), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2)

            if cv2.waitKey(1) & 0xFF == ord("s"):
                if not stop:
                    stop = True
                else:
                    stop = False 
            
            if stop:
                cv2.putText(display_frame, 'stopped', (10, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (128, 128, 128), 2)

            # В окне будет черный фон и ТОЛЬКО белые буквы (и частицы), которые видит бот
            cv2.imshow('White Mask Vision', display_frame)

cv2.destroyAllWindows()
