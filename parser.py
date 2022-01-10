import numpy as np
import cv2
from PIL import ImageGrab, Image
import os
import pytesseract

import requests

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Juane\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'


# observer_name = str(input('Introduce your observer name: ')).lower()
# observer_pass = str(input('Introduce your given password: '))

# observer_config = {'observer': observer_name, 'key': observer_pass, 'url': ''}


#This loop allows opencv to capture the screen continuously

player_observed = ''


while True:

  print('try')

  #IMPORTANT -- Replace the coordinates here with the ones for your screen.
  #You want the image to cover only the health bar and make it really tight
  img = ImageGrab.grab(bbox=[700,855, 1075, 900])

  #Convert the image to numpy array
  img_np = np.array(img)

  #This converts the image from BGR to RGB. On my PC this helps the tesseract engine.
  #If tesseract is not picking up your health, change this to cv2.COLOR_BGR2GRAY
  frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)

  #Write the image to disk as a temporary file so we can use the tesseract engine on it
  filename = "{}.png".format(os.getpid())
  cv2.imwrite(filename, frame)

  # load the image as a PIL/Pillow image, apply OCR, and then delete
  # the temporary file
  text = pytesseract.image_to_string(Image.open(filename))
  os.remove(filename)
  #This line will continuously print what the OCR sees so terminal so you can monitor it
  #for correctness, remove if not needed


  if text != player_observed:
      player_observed = text
      print('Observing a new player: ', player_observed)
      requests.post('http://localhost:3000/urlBanderita/Juane', json={'player': player_observed, "key": "1234"})


  #Your health is now represented by the 'text' variable. Do whatever you want with it!
  #
  #
  #

  #Open a window displaying what opencv is seeing. Use this to position your coordinates
  cv2.imshow("Screen", frame)

  # if cv2.waitKey(1) == 27:
  #  break

cv2.destroyAllWindows()
