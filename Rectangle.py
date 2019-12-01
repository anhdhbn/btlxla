#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import os

class Rectangle(object):
    def __init__(self, origin, result, result_full, folder="./test"):
        self.origin = origin
        self.result = result
        self.result_full = result_full
        self.folder = folder
        self.try_mkdir(self.folder)
        self.height, self.width = result.shape

    def try_mkdir(self, folder):
        try:
            os.remove(filename)
        except:
            pass
        try:
            os.mkdir(folder)
        except:
            pass
    
    def sort_contours(self, cnts, method="left-to-right"):
        reverse = False
        i = 0

        if method == "right-to-left" or method == "bottom-to-top":
            reverse = True

        if method == "top-to-bottom" or method == "bottom-to-top":
            i = 1


        boundingBoxes = [cv2.boundingRect(c) for c in cnts]
        (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                            key=lambda b: b[1][i], reverse=reverse))
        return (cnts, boundingBoxes)

    def get_pieces(self, image, full=True):
        contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        (contours, boundingBoxes) = self.sort_contours(contours, method="top-to-bottom")
        positions = [cv2.boundingRect(c) for c in contours ]
        positions = [(x, y, w, h) for x, y, w, h in positions if w != self.width and h != self.height ]
        pieces = []
        if not full:
            pieces = [Piece((x, y, w, h), self.origin[y:y+h, x:x+w]) for x, y, w, h in positions]
        else:
            pieces = [PieceFull((x, y, w, h), self.origin[y:y+h, x:x+w]) for x, y, w, h in positions]
        pieces = sorted(pieces, key=lambda x: (x.x))
        return pieces, positions

    def cut(self):
        pieces, position1 = self.get_pieces(self.result )
        pieces_full, position2 = self.get_pieces(self.result_full, True)

        init = 1
        hor, ver = init, init
        for idx in range(len(pieces_full)):
            piece = pieces_full[idx]
            
            if (idx + 1 == len(pieces_full)):
                piece.numhor, piece.numver = hor, ver
            else:
                next_piece = pieces_full[idx + 1]
                piece.numhor, piece.numver = hor, ver
                # piece.write_img(f"{self.folder}/{piece.numver}-{piece.numhor}.png")
                if next_piece.y < piece.y:
                    hor += 1
                    ver = init
                else:
                    ver += 1
        for piece in pieces:
            temp = [piece_full for piece_full in pieces_full if piece_full.compare_in(piece)]
            piece.append(temp)

        return pieces

        # for piece in pieces:
        #     piece.write_img(f"{self.folder}/{piece.arr[0].numver}-{piece.arr[0].numhor}.png")




class Piece(object):
    def __init__(self, position, new_img):
        self.x, self.y, self.w, self.h = position
        self.image = new_img
        self.numver, self.numhor = 0, 0
    
    def write_img(self, path):
        cv2.imwrite(path, self.image)

    def compare_in(self, piece):
        x1, y1, x2, y2 = piece.x, piece.y, piece.x + piece.w, piece.y  + piece.h
        if self.x >= x1 and self.x + self.w <= x2 and self.y >= y1 and self.y + self.h <= y2:
            return True
        else: return False



class PieceFull(Piece):
    def __init__(self, position, new_img):
        Piece.__init__(self, position, new_img)
        self.arr = []
    def append(self, pieces_full):
        self.arr += pieces_full
    
    def get_positon(self):
        return self.arr[0].numver, self.arr[0].numhor

