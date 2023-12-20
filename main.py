import time
import pyautogui
import pyperclip
import threading
from PIL import ImageGrab
from cnocr import CnOcr
from rect_selector import RectangleSelector
from request import send_post_request
from translate import Translator

pyautogui.FAILSAFE=False
pyautogui.PAUSE=1
fallscreen_path='fallscreen.png'

fullscreen_img = ImageGrab.grab()
fullscreen_img.save(fallscreen_path)
screenwidth,screenheight = pyautogui.size()
screen_dpi=int(fullscreen_img.size[0]/screenwidth)
rs = RectangleSelector(fallscreen_path,screen_dpi)
print('请圈选消息框区域，esc确认')
chat_window_position = rs.get_rectangle_coordinates()
print('消息框区域：',chat_window_position)
rs.reset(fallscreen_path);
print('请圈选文本框焦点，esc确认')
type_area_position=rs.get_rectangle_coordinates()
print(f'文本框焦点：({type_area_position[0]},{type_area_position[0]})')
rs.reset(fallscreen_path);
print('请圈选发送按钮焦点，esc确认')
send_btn_position=rs.get_rectangle_coordinates()
print(f'发送按钮焦点：({send_btn_position[0]},{send_btn_position[0]})')



# 所有参数都使用默认值
questions=[]
answered=[]
lock = threading.Lock()

def chat_monitor():
    global questions,chat_window_position,answered
    ocr = CnOcr() 
    def check_has_q(q):
        return q and q not in questions and q not in answered
    while True:
        with lock:
            chat_area = ImageGrab.grab(bbox=chat_window_position)
            chat_area.save('chat.png')
            out = ocr.ocr('chat.png')
            hasQ = False
            lastQY = None
            q=""
            for t in out:
                line:str=t['text']
                position=t['position']
                curY=position[0][1]
                if '#bot' in line:
                    if hasQ and check_has_q(q):
                        questions.append(q)
                        print('new question:',q)
                    hasQ= True
                    lastQY = curY
                    q=line
                elif hasQ :
                    if curY < lastQY +25 and curY > lastQY + 15:
                        q += line
                        lastQY = curY
                    elif check_has_q(q) :
                        questions.append(q)
                        print('new question:',q)
                        hasQ=False
                        q=None
                else:
                   hasQ=None 
            if hasQ and check_has_q(q):
                questions.append(q)
        time.sleep(5)

def question_handler():
    global questions,answered
    while True:
        with lock:
            if questions:
                while len(questions)>0:
                    q = questions.pop(0)
                    print(questions)
                    text=q.replace("#bot","")
                    print('text:',text)
                    
                    if len(answered)>10:
                        answered.pop()
                    answer=send_post_request(text)
                    if answer:
                        answered.append(q)
                        pyautogui.click(type_area_position[0], type_area_position[1])  # 点击聊天窗口
                        pyperclip.copy(answer)
                        pyautogui.hotkey('command','v')
                        pyautogui.click(send_btn_position[0], send_btn_position[1])
                    else:
                        questions.append(q)
                    print(answer)

        time.sleep(5)
producer_thread = threading.Thread(target=chat_monitor)
consumer_thread = threading.Thread(target=question_handler)

# 启动线程
producer_thread.start()
time.sleep(1)
consumer_thread.start()
