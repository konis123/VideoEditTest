import cv2
import numpy as np

'''
비디오스탑,플레이 버튼 : space    32
현재 프레임부터 선택된 영역의 영상을 저장 : s 83
다음 프레임으로 넘어가기 : ->  39

'''

DRAW_BG = {'color':(255,0,0), 'val':0}
DRAW_FG = {'color':(255,255,255), 'val':1}

rect = (0, 0, 0, 1)
drawing = False
rectangle = False
rect_over = False
rect_or_mask = 100
value = DRAW_FG
thickness = 3

def onMouse(event, x, y, flags, param):
    global ix, iy, img, img2, rectangle
    global rect, rect_over

    img = param[0]
    img2 = param[1]

    if event == cv2.EVENT_RBUTTONDOWN:
        rectangle = True
        ix, iy = x, y
        print("마우스눌림")
    elif event == cv2.EVENT_MOUSEMOVE:
        print('mouse moving')
        if rectangle:
            img = img2.copy()
            cv2.rectangle(img, (ix, iy), (x, y), (0, 0, 255), 2)
            rect = (min(ix, iy), min(iy, y), abs(ix-x), abs(iy-y))
            cv2.imshow('output', img)


    elif event == cv2.EVENT_RBUTTONUP:
        rectangle = False
        rect_over = True

        cv2.rectangle(img, (ix, iy), (x, y), (0,0,255), 2)
        rect = (min(ix, iy), min(iy, y), abs(ix-x), abs(iy-y))
        #rect_or_mask = 0
        print('n:적용하기')

    '''
    if event == cv2.EVENT_LBUTTONDOWN:
        if not rect_over:
            print('마우스 왼쪽 버튼을 누른채로 전경부분 클릭')
        else:
            drawing = True
            cv2.circle(img, (x,y), thickness, value['color'], -1)
            cv2.circle(mask, (x,y), thickness, value['val'], -1)

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            cv2.circle(img, (x,y), thickness, value['color'], -1)
            cv2.circle(mask, (x,y), thickness, value['val'], -1)

    elif event == cv2.EVENT_LBUTTONUP:
        if drawing:
            drawing = False
            cv2.circle(img, (x,y), thickness, value['color'], -1)
            cv2.circle(mask, (x,y), thickness, value['val'], -1)
    '''

    return


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
fps = 60.0

saveName = 'trans_'+videoName
out = cv2.VideoWriter(saveName, fcc, fps, (width, height))

while True:
    if space_Button == True:
        k = cv2.waitKey(0) & 0xFF
        if k == 27: #ESC
            break
        elif k == 32: #SpaceBar
            space_Button = False
        elif k == ord('s'): #s버튼 눌러진 이후부터 사각형부분을 저장
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

            cv2.imshow('output', frame)


        else:
            print('else')

        #continue
    else:
        k = cv2.waitKey(1) & 0xFF


        ret, frame = cap.read()
        frame2 = frame.copy()
        cv2.setMouseCallback('output', onMouse, param=(frame, frame2))
        cv2.imshow('output', frame)

        if not ret:
            print('비디오 읽기 오류')
            break



        if k == 27: #ESC
            break
        elif k == 32: #SpaceBar
             space_Button = True
        # elif k == ord('s'): #s버튼 눌러진 이후부터 사각형부분을 저장
        #     s_Button = True
        #     width = int(cap.get(3))
        #     height = int(cap.get(4))
        #     fcc = cv2.VideoWriter_fourcc('D','I','V','X')
        #     fps = 60.0
        #
        #     saveName = 'trans_'+videoName
        #     out = cv2.VideoWriter(saveName, fcc, fps, (width, height))
        #     out.write(frame)
        #
        # elif k == ord('x'):
        #     print('next frame')
        # else:
        #     print('else')





cap.release()
if out != None:
    out.release()
cv2.destroyAllWindows()
