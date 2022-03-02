import numpy as np
import cv2
from PIL import ImageGrab, Image
import os
import pytesseract
import crayons
import requests

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Juane\AppData\Local\Programs\tesseract.exe'


player_observed = ''


while True:

  print(crayons.yellow('Observing current player'))

  img = ImageGrab.grab(bbox=[750,855, 1075, 900])

  img_np = np.array(img)

  frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)

  filename = "{}.png".format(os.getpid())
  cv2.imwrite(filename, frame)

  text = pytesseract.image_to_string(Image.open(filename))
  os.remove(filename)


  if text != player_observed:
      player_observed = text
      print('Observing a new player: ', player_observed)
      requests.post('http://localhost:3000/urlWidget/Juane', json={'player': player_observed, "key": "1234"})


  cv2.imshow("Screen", frame)

cv2.destroyAllWindows()