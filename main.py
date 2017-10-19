import cv2
import numpy as np

'''
비디오스탑,플레이 버튼 : space    32
현재 프레임부터 선택된 영역의 영상을 저장 : s 83
다음 프레임으로 넘어가기 : ->  39

'''

#Button
global s_Button, space_Button
global ix, iy, dx, dy, img, img2, rectangle, rect

DRAW_BG = {'color':(255,0,0), 'val':0}
DRAW_FG = {'color':(255,255,255), 'val':1}

#전역변수 초기값들 입력
s_Button = False
space_Button = False
rect = (0, 0, 0, 1)
rectangle = False
value = DRAW_FG
thickness = 3

font = cv2.FONT_HERSHEY_SIMPLEX


#바운딩박스, 녹화표시,
def display(mouseX=0,mouseY=0):
    global ix, iy, img, img2, rectangle, rect

    if rectangle:
        img = img2.copy()
        cv2.rectangle(img, (ix, iy), (mouseX, mouseY), (0, 0, 255), 2)
        rect = (min(ix, iy), min(iy, mouseY), abs(ix-mouseX), abs(iy-mouseY))
        cv2.imshow('output', img)
    else:
        cv2.imshow('output',img)


    return


def keyInput(t):
    global s_Button, space_Button
    global dx, dy
    k = cv2.waitKey(t) & 0xFF

    if k == 27: #ESC
        return 0
    elif k == 32: #SpaceBar
        space_Button = False
    elif k == ord('s'): #s버튼 눌러진 이후부터 사각형부분을 저장
        print('record start')
        if s_Button:
            s_Button = False
        else:
            s_Button = True

    elif k == ord('x'):
        print('next frame')
        ret, frame = cap.read()
        frame2 = frame.copy()
        if s_Button:
            out.write(frame)

    else:
        print('else')

    display(mouseX=dx, mouseY=dy)

def onMouse(event, x, y, flags, param):
    global ix, iy, img, img2, rectangle, rect, dx, dy

    #img = param[0]
    #img2 = param[1]

    if event == cv2.EVENT_RBUTTONDOWN:
        rectangle = True
        ix, iy = x, y
        print("마우스눌림")
    elif event == cv2.EVENT_MOUSEMOVE:
        #print('mouse moving')
        dx, dy = x, y
        if rectangle:
            #img = img2.copy()
            display(mouseX=x,mouseY=y)

    elif event == cv2.EVENT_RBUTTONUP:
        rectangle = False
        #cv2.rectangle(img, (ix, iy), (x, y), (0,0,255), 2)
        #rect = (min(ix, iy), min(iy, y), abs(ix-x), abs(iy-y))

        print('n:적용하기')

    return


#main
if __name__=="__main__":

    cv2.namedWindow('output')
    cv2.moveWindow('output', 0, 0)

    videoName = 'sample.mp4'
    out = None

    cap = cv2.VideoCapture(videoName)

    space_Button = False
    s_Button = False


    width = int(cap.get(3))
    height = int(cap.get(4))
    fcc = cv2.VideoWriter_fourcc('D','I','V','X')
    fps = 20.0

    saveName = 'trans_'+videoName
    out = cv2.VideoWriter(saveName, fcc, fps, (width, height))

    while True:

        ret, frame = cap.read()
        if not ret:
            print('비디오 읽기 오류')
            break

        img = frame
        img2 = frame.copy()   #기존이미지를 복사함

        #마우스콜백 등록
        cv2.setMouseCallback('output', onMouse)

        #프레임 display
        display()

        #키입력 등록
        if keyInput(0) == 0:
            break;





    cap.release()
    if out != None:
        out.release()
    cv2.destroyAllWindows()
