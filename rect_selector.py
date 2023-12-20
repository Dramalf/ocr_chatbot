import cv2
import time

class RectangleSelector:
    def __init__(self, image_path,screen_dpi):
        self.screen_dpi=screen_dpi
        self.reset(image_path)

    # 鼠标事件处理函数
    def draw_rectangle(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.top_left_pt = (x, y)

        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            self.completed = True
        if self.drawing :
            self.bottom_right_pt = (x, y)
    
    def reset(self,image_path):
        self.image_path = image_path
        self.top_left_pt = None
        self.bottom_right_pt = None
        self.drawing = False
        self.completed = False
        self.area = None
        self.callback = None
        # 加载图片
        self.image = cv2.imread(image_path)

        # 创建窗口并绑定鼠标事件处理函数
        cv2.namedWindow("Image")
        cv2.setMouseCallback("Image", self.draw_rectangle)
        
    
    # 获取矩形坐标
    def get_rectangle_coordinates(self):

        while True:
            # 在图像上绘制矩形
            temp_image = self.image.copy()
            cv2.resizeWindow("Image", (600, 600))
            cv2.rectangle(temp_image, self.top_left_pt,self.bottom_right_pt, (0, 255, 0), 2)
            
            # 显示图像

            cv2.imshow("Image", temp_image)
            key = cv2.waitKey(1) & 0xFF
            # 退出循环
            if self.completed and key == 27:
                cv2.destroyAllWindows()
                cv2.waitKey(1)
                x_min = min(self.top_left_pt[0], self.bottom_right_pt[0])
                y_min = min(self.top_left_pt[1], self.bottom_right_pt[1])
                x_max = max(self.top_left_pt[0], self.bottom_right_pt[0])
                y_max = max(self.top_left_pt[1], self.bottom_right_pt[1])
                screen_dpi=self.screen_dpi
                origin = (x_min, y_min, x_max, y_max)
                self.area=tuple(int(value/screen_dpi) for value in origin)
                if self.callback:
                    self.callback(self.area)
                break

        
        # 获取矩形坐标
        
        if self.completed:
            return self.area
        else:
            return None
        
    def after_close(self, callback):
        print(callback,'callback')
        self.callback = callback