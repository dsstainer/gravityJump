import math
import time
class Test:
    def __init__(self) -> None:
        self.player_xPos = 200
        self.player_yPos = 200
        self.PLAYER_WIDTH = 50
        self.PLAYER_HEIGHT = 60
        self.angle = 50
        self.sin_theta = math.sin(self.angle)
        self.cos_theta = math.cos(self.angle)
    def player_pointA(self):
        w = self.PLAYER_WIDTH/2
        h = self.PLAYER_HEIGHT/2
        return (self.player_xPos - w*self.cos_theta - h*self.sin_theta, 
                self.player_yPos - w*self.sin_theta + h*self.cos_theta)

    def player_pointB(self):
        w = self.PLAYER_WIDTH/2
        h = self.PLAYER_HEIGHT/2
        return (self.player_xPos + w*self.cos_theta - h*self.sin_theta, 
                self.player_yPos + w*self.sin_theta + h*self.cos_theta)

    def player_pointC(self):
        w = self.PLAYER_WIDTH/2
        h = self.PLAYER_HEIGHT/2
        return (self.player_xPos + w*self.cos_theta + h*self.sin_theta, 
                self.player_yPos + w*self.sin_theta - h*self.cos_theta)

    def player_pointD(self):
        w = self.PLAYER_WIDTH/2
        h = self.PLAYER_HEIGHT/2
        return (self.player_xPos - w*self.cos_theta + h*self.sin_theta, 
                self.player_yPos - w*self.sin_theta - h*self.cos_theta)

    def is_intersect(self, yp, ya, yb, xp, xa, xb, rad):
        if yb-ya == 0:
            py = ya
            px = xp
        elif xb-xa == 0:
            py = yp
            px = ya
        else:
            w1 = (yp-ya)*(yb-ya)*(xb-xa) + xa*(yb-ya)**2 + xp*(xb-xa)**2
            w2 = ((yb-ya)**2 + (xb-xa)**2)
            px = w1/w2
            py = ((-1*(xb-xa)*(px-xp))/(yb-ya))+yp
        distance = math.sqrt((py-yp)**2 + (px-xp)**2)
        print(distance)
        dist_rad = (distance <= rad)
        print(dist_rad)
        between_x = max(xa,xb) >= px and px >=  min(xa,xb)
        between_y = max(ya,yb) >= py and py >=  min(ya,yb)
        return dist_rad and between_x and between_y

def milisecs_to_secs( ms):
    return ms/1000

def calculate_time_in_secs(start_time, current_time):
    time_elapsed = current_time-start_time
    return time_elapsed

def set_text():
    start_time = time.time()
    time.sleep(5)
    current_time = time.time()
    print(f"{calculate_time_in_secs(start_time, current_time)}")

#t = Test()
#print("Point A: ", t.player_pointA())
#print("Point B: ", t.player_pointB())
#print("Point C: ", t.player_pointC())
#print("Point D: ", t.player_pointD())
#print("----------------------------------------------")
#print(t.is_intersect(450, 408.749999, 408.749999, 300, 260, 340, 100))

set_text()
