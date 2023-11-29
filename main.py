import time
import pyautogui
import win32gui
import os


def get_img_list(path):
    i = 0
    result = []
    while True:
        fileName = path + "\\"+ str(i+1) + ".png"
        i = i+1
        if(os.path.exists(fileName)):           
            result.append(fileName)
        else:
            break
    return result

def get_current_cusor():
     cursor_info = win32gui.GetCursorInfo()
     return cursor_info[1]

class AutoFish:
    #鼠标当前的指针样式
    cursor = None

    #水花检测区域, 为了提高性能,只检测鱼漂附近的水花
    splash_check_region = None
    
    # 本次钓鱼开始的时间戳
    start_fishing_timestamp = time.time()

    # 鱼漂检测图片列表
    float_imgs = get_img_list("float")

    # 水花检测图片列表
    splash_imgs = get_img_list("splash")

    # 等待当前鼠标指针为wow的鼠标指针
    def wait_start(self):
        while True:
            time.sleep(1)
            cursor = get_current_cusor()
            if(abs(cursor) > 100000):
                print("准备就绪,当前鼠标值:" + str(cursor))
                break
   
    #开始钓鱼,默认钓鱼的快捷键为F
    def start_fish(self):
        print("甩杆!")
        pyautogui.keyDown("F8")
        pyautogui.keyUp("F8") 
        self.start_fishing_timestamp = time.time()      
    

    #获取鱼漂坐标
    def Window_check():
        # 获取进程内指定标题窗口
        window = gw.getActiveWindowTitle('魔兽世界')
        print(window)
        windows = window[0]
        # 获取窗口左上角的坐标和窗口的大小
        x,y,width,height = windows.topleft[0],windows.topleft[1],windows.size[0],windows.size[1]




        # 获取屏幕图像
        screenshot = pyautogui.screenshot(region=(x,y,width,height))
        screenshot.save('.\wow_fishingtools\images\screenshot.png')
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        # 加载指定图像
        template = cv2.imread('.\wow_fishingtools\images\google.png', 0)
        w, h = template.shape[::-1]

        # 匹配图像并获取坐标
        time.sleep(1)
        res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)

    #寻找鱼漂
    def find_float(self):
        while True:
            time.sleep(0.3)
            
            #超过6秒没有找到鱼漂就重新甩杆
            if(time.time() - self.start_fishing_timestamp > 6):
                self.start_fish()
            
            for fileName in self.float_imgs:
                box = pyautogui.locateOnScreen(fileName,confidence=0.72)
                if(box):
                    x,y=pyautogui.center(box)
                    pyautogui.moveTo(x,y)
                    #pyautogui.click()
                    time.sleep(0.1)
                    current_cusor = get_current_cusor()
                    if(current_cusor != self.cursor):
                        # print("鼠标变化 原值: " + str(self.cursor) + " 新值: " + str(current_cusor))
                        self.cursor = current_cusor
                        self.splash_check_region = (box.left-box.width,box.top,box.width*2,box.height*2)                     
                        # pyautogui.screenshot('splash_check_region.png',region=self.splash_check_region)
                        print("找到鱼漂!" + fileName)
                        return
        
    def check_splash(self):
        while True:
            time.sleep(0.01)
            for fileName in self.splash_imgs:
                box =  pyautogui.locateOnScreen(fileName,confidence=0.6,region=self.splash_check_region)
                if(box):
                    pyautogui.rightClick()
                    print("起杆!" + fileName)
                current_cusor = get_current_cusor()
                if(current_cusor != self.cursor):
                    # print("鼠标变化 原值: " + str(self.cursor) + " 新值: " + str(current_cusor))
                    self.cursor = current_cusor
                    print("钓鱼结束!")
                    # pyautogui.click()
                    return           

    def run(self):
        self.wait_start()
        while True:
            self.find_float()
            self.check_splash()


auto_fish = AutoFish()
auto_fish.run()
