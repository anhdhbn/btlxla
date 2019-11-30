import cv2
import numpy as np
import helper
import math
import imutils

from Rectangle import Rectangle
# image = helper.remove_text("1.png")
horizontal, vertical, result, origin = helper.remove_text("2.png")

horizontal_full  =  helper.draw_fulline(horizontal)
vertical_full  =  helper.draw_fulline(vertical)

result_full = helper.combine_two_image(horizontal_full, vertical_full)

rectange = Rectangle(origin, result, result_full)
rectange.cut()