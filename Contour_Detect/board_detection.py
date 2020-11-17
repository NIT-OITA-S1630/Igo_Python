import cv2
import numpy as np
import matplotlib.pyplot as plt
import pyperclip
import csv
from _detect_corners import *
from _trim_board import *
import os
os.system('cls')

def show_fitted(img, x):
    cntr = np.int32(x.reshape((4, 2)))
    blank = np.copy(img)
    cv2.drawContours(blank, [cntr], -1, (0,255,0), 2)
    return blank

def split_image(img, x, y, line):
    height, width, channels = img.shape
    h = height//y
    w = width//x
    line_h = round(h*line)
    line_w = round(w*line)
    counter = 0
    for split_y in range(1, y+1):
        for split_x in range(1, x+1):
            counter += 1
            clp = img[ (h*(split_y-1))+line_h:(h*(split_y))-line_h, (w*(split_x-1))+line_w:(w*(split_x))-line_w]
            cv2.imwrite("./raw_img/{}.png".format(counter), clp)
    counter = 0

def draw_ruled_line(img, show=True):
    base_size = 32
    w = base_size * 15
    h = base_size * 15
    img = img.copy()
    for i in range(20):
        x = int((w / 18) * i)
        y = int((h / 18) * i)
        cv2.line(img, (x, 0), (x, h), (0, 0, 255), 1)
        cv2.line(img, (0, y), (w, y), (0, 0, 255), 1)
    if show:
        display_cv_image(img)
    return img

def perspectiveTransform(img, pts_input, pts_output):
    raws, cols, ch = img.shape
    M = cv2.getPerspectiveTransform(pts_input, pts_output)
    outputImg = cv2.warpPerspective(img, M, (800, 800))
    return outputImg

# ノイズ処理用の関数
def reduceNoise(img, medianBoxSize, kernelSize):
    cv2.medianBlur(img, medianBoxSize)
    kernel = np.ones((kernelSize, kernelSize), np.uint8)
    outputImg = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    return outputImg

def retCrossPoints(img):
    crossPoints = []
    interval = img.shape[0]/18
    for i in range(19):
        row = []
        for j in range(19):
            x = int(i*interval)
            y = int(j*interval)
            if i==0:
                x += 7
            if j==0:
                y += 7
            if i==18:
                x -= 7
            if j==18:
                y -= 7
            row.append([y, x])    
        crossPoints.append(row)
    return crossPoints

def drawCrossPoints(img):
    outputImg = img.copy()
    crossPoints = retCrossPoints(img)    
    for p_row in crossPoints:
        for p in p_row:
            cv2.circle(outputImg, (p[0],p[1]), 2, (0, 0, 255), 3)   

    return outputImg

def checkStonePosition(img):
    crossPoints = retCrossPoints(img)
    conditionOfBoard = []
    none = 10.0
    blackStone = 80.0
    whiteStone = 120.0

    for p_row in crossPoints:
        condition_row = []
        for p in p_row:
            
            rect = img[p[1]-3:p[1]+7, p[0]-3:p[0]+7]
            colorAve = np.average(rect)
            #print('aveColor around' + str([p[1],p[0]]) + ':' +str(colorAve))
                      
            if colorAve < none:
                condition_row.append(-1)
            elif colorAve < blackStone:
                condition_row.append(0)
            elif colorAve > whiteStone:
                condition_row.append(255)
                
        conditionOfBoard.append(condition_row)
    return conditionOfBoard


def addStateToNeighbourhood(state, neighbourhood):
    isAdded = False
    if state<11 and state>=0:
        neighbourhood.append(0)
        isAdded = True
    elif state>244:
        neighbourhood.append(255)
        isAdded = True
    return [neighbourhood, isAdded]

def checkTeritory(point,territoryTable):
    x, y = point[:]
    neighbourhood = []
    
    # 周りの確定済みの状態を近傍リストに追加
    # 左上
    if x>0 and y>0:
        leftUpperState = territoryTable[x-1][y-1]
        neighbourhood = addStateToNeighbourhood(leftUpperState, neighbourhood)[0]
    # 上
    if x>0:
        upperState = territoryTable[x-1][y]
        neighbourhood = addStateToNeighbourhood(upperState,neighbourhood)[0]
    # 右上
    if x>0 and y+1<19:
        rightUpperState = territoryTable[x-1][y+1]
        neighbourhood = addStateToNeighbourhood(rightUpperState,neighbourhood)[0]
    # 左
    if y>0:
        leftState = territoryTable[x][y-1]
        neighbourhood = addStateToNeighbourhood(leftState,neighbourhood)[0]

    # 残りの状態を石に当たるまで走査
    # 右
    j = 1
    while y+j<19:
        rightState = territoryTable[x][y+j]
        neighbourhood,flag = addStateToNeighbourhood(rightState,neighbourhood)[:]
        if flag:
            break
        else:
            j += 1
    # 左下
    i = 1
    j = 1
    while x+i<19 and y-j>=0:
        leftButtomState = territoryTable[x+i][y-j]
        neighbourhood,flag = addStateToNeighbourhood(leftButtomState,neighbourhood)[:]
        if flag:
            break
        else:
            i += 1
            j += 1
    # 下
    i = 1
    while x+i<19:
        buttomState = territoryTable[x+i][y]
        neighbourhood,flag = addStateToNeighbourhood(buttomState,neighbourhood)[:]
        if flag:
            break
        else:
            i += 1
    # 右下
    i = 1
    j = 1
    while x+i<19 and y+j<19:
        rightButtomState = territoryTable[x+i][y+j]
        neighbourhood,flag = addStateToNeighbourhood(rightButtomState,neighbourhood)[:]
        if flag:
            break
        else:
            i += 1
            j += 1

    # 近傍のリストのどちらが多いか
    if neighbourhood.count(0) > neighbourhood.count(255):
        targetState = 10
    else:
        targetState = 245

    territoryTable[x][y] = targetState
    return territoryTable

def makeTerritoryTable(stonePosition):
    territoryTable = stonePosition.copy()
    for x in range(19):
        for y in range(19):
            if territoryTable[x][y]==-1:
                point = [x,y]
                territoryTable = checkTeritory(point,territoryTable)            
    return territoryTable

def drawTerritoryColor(img,territoryTable):
    outputImg = img.copy()
    crossPoints = retCrossPoints(img)
    i = 0
    for p_row in crossPoints:
        j = 0
        for p in p_row:
            state = territoryTable[i][j]
            if state==10:
                cv2.circle(outputImg, (p[0],p[1]), 2, (0, 0, 0), 3)
            elif state==245:
                cv2.circle(outputImg, (p[0],p[1]), 2, (255, 255, 255), 3)
            j += 1
        i += 1
    return outputImg


def calculateTerritory(territoryTable):
    black = 0
    white = 0
    for row in territoryTable:
        black += row.count(10)
        white += row.count(245)
    return [black, white]


if __name__ == "__main__":
    raw_img = cv2.imread("testdata.png")
    fit_img = fit_size(raw_img, 800, 800)

    polies = convex_poly(fit_img, False)
    poly = select_corners(fit_img, polies)
    x0 = poly.flatten()
    img = show_fitted(fit_img, x0)

    rect, score = convex_poly_fitted(img)

    trimed = trim_board(raw_img, normalize_corners(rect) * (raw_img.shape[0] / img.shape[0]))
    lined = draw_ruled_line(trimed, False)

    cv2.imshow('fit_img', fit_img)
    cv2.waitKey(0)
    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.imshow('trimed', trimed)
    cv2.waitKey(0)
    cv2.imshow('lined', lined)
    cv2.waitKey(0)

    #   ---追加: 交点付与のやつ
    boardWithPointsImg = drawCrossPoints(trimed)

    cv2.imshow("boardWithPointsImg",boardWithPointsImg)
    cv2.waitKey(0)

    # ノイズ処理
    noiseReducedImg = reduceNoise(trimed, 7, 5)
    cv2.imshow("noiseReducedImg",noiseReducedImg)
    cv2.waitKey(0)

    hsvImg = cv2.cvtColor(noiseReducedImg, cv2.COLOR_BGR2HSV)

    beige = np.uint8([[[61,91,146]]])
    hsv_beige = cv2.cvtColor(beige,cv2.COLOR_BGR2HSV)
    print(hsv_beige)
    lower_beige = np.array([10,50,50])
    upper_beige = np.array([30,255,255])

    mask_beige = cv2.inRange(hsvImg, lower_beige, upper_beige)
    cv2.imshow("mask_beige",mask_beige)
    cv2.waitKey(0)

    mask_negaposi = cv2.bitwise_not(mask_beige)
    cv2.imshow("mask_negaposi",mask_negaposi)
    cv2.waitKey(0)

    res = cv2.bitwise_and(trimed,trimed, mask= mask_negaposi)
    cv2.imshow("res",res)
    cv2.waitKey(0)

    resWithPointsImg = drawCrossPoints(res)
    cv2.imshow("resWithPointsImg",resWithPointsImg)
    cv2.waitKey(0)

    stonePosition = checkStonePosition(res)
    print("\n")
    print("stonePosition: \n" + str(stonePosition))

    print("\n")
    territoryTable = makeTerritoryTable(stonePosition)
    print("territoryTable: \n" + str(territoryTable))
    pyperclip.copy(str(territoryTable).replace("], [","], \n["))\
    
    with open("./stonePosition.csv","w") as f:
        writer = csv.writer(f)
        writer.writerows(stonePosition)

    resultImg = drawTerritoryColor(trimed,territoryTable)
    cv2.imshow("resultImg",resultImg)
    cv2.waitKey(0)

    split_image(trimed, 9, 9, 0)
