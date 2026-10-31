import ROI_bot_lib as rbl

import numpy as np
import mss
import cv2

rbl.help()

if __name__ == '__main__':
    ROI = {"top": 0, "left": 0, "width": 400, "height": 300}
    run = rbl.start()
    with mss.MSS() as sct:
        while run:
            img = np.array(sct.grab(ROI))
            frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            rbl.FPS(frame=frame)
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    cv2.destroyAllWindows()
