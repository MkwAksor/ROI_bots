import pyautogui
import random
import time
import cv2
import numpy as np
import mss
import keyboard
import os


"""Данная библиотека создана для упрощения написания
   программ, схожих с теми, что находятся в репозитории
   Я понимаю, что библиотека плохая и почти никому не нужна
   мне всё равно, она создана в первую очередь для личного
   пользования в рамках одного проекта"""


prev_time = time.time()
fps_list = []

def help():
    print("""
          Данную библиотеку рекомендую импортировать как 'rbl'
          
          Обязательно добавьте в свою программу переменные
          
            Для FPS:
              prev_time = time.time()
              fps_list = []
             Функция FPS() добавляет проблем, так что думайте перед использованием в проекте
             
            Для start():
              run = False
              или начинайте цикл таким образом:
                run = rbl.start()
                while run:
                    ...
                    ...
          """)

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
    keyboard.add_hotkey('esc', lambda: os._exit(0))
    print('Запуск программы...')
    return True

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
    roi = {"top": 0, "left": 0, "width": 400, "height": 300}
    start()
    with mss.MSS() as sct:
        while True:
            img = np.array(sct.grab(roi))
            frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            FPS(frame)
            cv2.imshow('Original', frame)
            
            if cv2.waitKey(1) == ord('q'):
                break
            
    cv2.destroyAllWindows()
