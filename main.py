#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import helper
import math
import imutils

from Rectangle import Rectangle


"""
input_file: là đường dẫn của file cần xử lý 


hàm helper.remove_text() trả về ảnh không có text
horizontal: ảnh chỉ có các đường nằm ngang
vertical: ảnh chỉ có các đường nằm dọc
result: gộp lại của 2 ảnh trên
origin: ảnh gốc

horizontal_full: ảnh cắt tất cả theo chiều ngang: ví dụ trong ảnh 2.png, Cột họ và tên bị cắt làm đôi
vertical_full: tuơng tự như trên
result_full: ảnh gộp lại của 2 ảnh trên, bị cắt thành các phần nhỏ nhất có thể

Output
hàm rectange.cut(): trả về danh sách các mảnh
gọi hàm get_positon sẽ trả về thứ tự lần lựot nằm ngang và nằm dọc của ảnh

"""

input_file = "2.png"

horizontal, vertical, result, origin = helper.remove_text(input_file)

horizontal_full  =  helper.draw_fulline(horizontal)
vertical_full  =  helper.draw_fulline(vertical)

result_full = helper.combine_two_image(horizontal_full, vertical_full)

rectange = Rectangle(origin, result, result_full)
pieces = rectange.cut()

for piece in pieces:
    ver, hor = piece.get_positon()
    piece.write_img(f"{rectange.folder}/{ver}-{hor}.png")