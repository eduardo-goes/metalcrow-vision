import cv2
import numpy
import math


class ImageProcessor:
    def pre_process(frame):
        return frame
    def process(self, frame): # método pra processar as imagens

        # Menores valores possiveis pra Threshold HSV (peguei do GRIP)
        low_H = 0
        low_S = 0
        low_V = 0

        # Maiores valores possiveis para Threshold HSV (peguei do GRIP)
        high_H = 255
        high_S = 30
        high_V = 100

        # filtro
        frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # converte o frame pra HSV
        frame_threshold = cv2.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V)) # troca os frames que nao batem com os valores pra preto
        cv2.imshow('hsv', frame_HSV)
        cv2.imshow('padrao', frame)
 
        return frame_threshold # retorna o frame processado

class FindObject:
    ratioFilter = [0.0, 1.0] # remove figuras sem sentido
    solidityFilter = [0.0, 1.0] # remove buracos

    def find_detection(self, frame, bbox = [0, 0, 283, 283]):
        x1, y1, w, h = bbox
        x2 = x1 + w
        y2 = y1 + h
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        roi = frame[y1:y2, x1:x2]
        print(roi.dtype)
        height, width = frame.shape
        object_list = []
        img, contours, hierarchy = cv2.findContours(roi, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            x,y,w,h = cv2.boundingRect(contour) # pega um retangulo baseado no contorno
            rectangle = [x, y, w, h]
            object_list.append(DetectedObject(rectangle, width, height, area))
            drawn_frame = frame
            cv2.rectangle(roi, (x,y), (x+w, y+h), (255,255,255), 2)
        return object_list


class DetectedObject:
    def __init__(self, rectangle, frameWidth, frameHeight, area):

        #retangulo
        self.rectangle = rectangle #retangulo que circunda o contorno
        
        scale = 5

        self.final_area = area
        
        x,y,w,h = self.rectangle #pontos x e y do ponto inferior esquerdo do retangulo, sua altura e sua largura

        #frames
        self.frameWidth = frameWidth #largura da imagem
        
        self.frameHeight = frameHeight #altura da imagem

ip = ImageProcessor()
fo = FindObject()
img = cv2.imread('centralizado.png', 1)
img_processada = ip.process(img)
print(img.dtype)
areas = []
objetos = fo.find_detection(img_processada)
for objeto in objetos:
    tracked = objetos[0]
    areas.append(tracked.final_area)

for a in areas:
    print('area: {0}'.format(a))
    
cv2.imshow('process', img_processada)
