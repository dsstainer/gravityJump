import tkinter as tk
from tkinter import ttk
import time
from datetime import timedelta
from PIL import ImageTk, Image
import math
import random
"""
Add items to board
--> images:
    load in image using Pillow
    a sprite which is a red bloack
--> object:
    create objects (i.e. a rectangle)

create objects in canvas
Add objects to canvas (pack)
Gameloop:
    change velocities based on gravity
    change positions based on velocities
    collision detection
    check for user input- 
        if user pressed u, implement a button press
    re-align position based on collision
    re-render all items

gravity - have a constant g
velocity changes based on g and position of item on surface?: new_velocity = initial_velocity + g


position changes based on velocity


Task 2 -> get circle -
player can run around circle with arrow keys
Circle has gravitational pull
player jumps in direction perpendicular to surface when space pressed
Circle + square collision detection
implement camera -> do this first because it influences the MAth
"""

def setup_window():
    """
    Initialises the tkinter window
    Returns: tkinter_window
    """
    #Initialise window
    root_window = tk.Tk()
    root_window.title("Gravity jump")
    root_window.maxsize(1440, 900)
    root_window.resizable(False, False)
    return root_window

class Planet:
    def __init__(self, xPos, yPos, rad, M, numItems):
        self.xPos = xPos
        self.yPos = yPos
        self.rad = rad
        self.M = M
        self.items = self.generate_items(numItems)
        
    def load_items(self, items):
        self.items = items

    def generate_items(self, numItems):
        items = []
        item_angle = math.floor(360/numItems)
        current_angle = 0
        for i in range(numItems):
            angle = random.randint(current_angle, current_angle+item_angle-1)
            xPos = self.xPos + (self.rad+Item.WIDTH)*math.cos(math.radians(angle))
            yPos = self.yPos + (self.rad+Item.HEIGHT)*math.sin(math.radians(angle))
            items.append(Item(xPos,yPos,angle, False))
            current_angle += item_angle
        return items

class Item:
    WIDTH = 20
    HEIGHT = 20
    RADIUS = 20
    POINT_COUNT = 1
    ITEM_IMAGE_PATH = "placeholder_item.png"
    def __init__(self, xPos, yPos, angle, is_hidden):
        self.xPos = xPos
        self.yPos = yPos
        self.rotation = angle
        self.hidden = is_hidden
    
        

class GravityJump(tk.Canvas):
    def __init__(self, master, keybindings, is_load):
        #Initialize variables
        self.keybindings = keybindings
        self.init_window()
        super().__init__(
            master=master,
            width=self.WINDOW_WIDTH,
            height=self.WINDOW_HEIGHT
        )
        self.init_camera()
        if is_load:
            self.load()
        else:
            self.init_player()
            self.init_platform()

        #Bind keys
        self.bind_all('<Key>', self.on_key_press)
        
        #Create text
        self.create_labels()

        #Create game objects and put onto canvas
        self.create_images()
        self.create_objects()
        self.grid(row=0, column=0, sticky="nsew")

        #Start game
        self.after(self.DELTA_TIME, self.game_loop)

    def quit_game(self):
        global game, menu, is_load
        game = False
        menu = True
        is_load = False
        main_menu_frame.tkraise()
        start_game_button['state'] = 'normal'
        self.destroy()

    def create_labels(self):
        self.score_label_xPos = 40
        self.score_label_yPos = 20
        self.timer_label_xPos = 40
        self.timer_label_yPos = 40
        self.score_label = self.create_text((self.score_label_xPos,self.score_label_yPos),fill="darkblue",font="Times 20 italic bold")
        self.timer_label = self.create_text((self.timer_label_xPos,self.timer_label_yPos),fill="darkblue",font="Times")
        self.save_button = ttk.Button(self, text="SAVE", command=self.save)
        self.quit_button = ttk.Button(self, text="QUIT", command=self.quit_game)
        self.save_button_window = self.create_window(700,400, window=self.save_button, state='hidden')
        self.quit_button_window = self.create_window(700,300, window=self.quit_button, state='hidden')
        self.itemconfigure(self.save_button_window,state='hidden')
        self.paused_label = self.create_text((720, 450), fill="darkblue",font="Times 40 bold", text="PAUSED" ,state="hidden")

    def save(self):
        #flush out any pausing time
        with open('save.txt', 'w') as f:
            f.write(str(self.score)+"\n")
            f.write(str(self.timer)+"\n")

            f.write(str(self.player_jumping)+"\n")
            f.write(str(self.player_action)+"\n")
            f.write(str(self.player_xPos)+"\n")
            f.write(str(self.player_yPos)+"\n")
            f.write(str(self.player_xVelocity)+"\n")
            f.write(str(self.player_yVelocity)+"\n")
            f.write(str(self.player_rotation)+"\n")

            for planet in self.planets:
                f.write("New Planet\n")
                f.write(str(planet.xPos)+"\n")
                f.write(str(planet.yPos)+"\n")
                f.write(str(planet.rad)+"\n")
                f.write(str(planet.M)+"\n")
                for item in planet.items:
                    f.write("New Item\n")
                    f.write(str(item.xPos)+"\n")
                    f.write(str(item.yPos)+"\n")
                    f.write(str(item.rotation)+"\n")
                    f.write(str(item.hidden)+"\n")

        
            f.write("End of file"+"\n")

    def load(self):
        with open('save.txt', 'r') as f:
            self.score = int(f.readline().strip())
            self.timer  = int(f.readline().strip())
            

            self.player_jumping = f.readline().strip() == 'True'
            self.player_action = f.readline().strip()
            self.player_xPos = float(f.readline().strip())
            self.player_yPos = float(f.readline().strip())
            self.player_xVelocity = float(f.readline().strip())
            self.player_yVelocity = float(f.readline().strip())
            self.player_rotation = float(f.readline().strip())

            self.planets = []
            while f.readline().strip() == "New Planet":
                xPos = float(f.readline().strip())
                yPos = float(f.readline().strip())
                rad = int(f.readline().strip())
                M = int(f.readline().strip())
                items = []
                file_pointer = f.tell()
                while f.readline().strip() == "New Item":
                    item_xPos = float(f.readline().strip())
                    item_yPos = float(f.readline().strip())
                    item_rotation = float(f.readline().strip())
                    item_hidden = f.readline().strip() == "True"
                    item = Item(item_xPos, item_yPos, item_rotation, item_hidden)
                    item.hidden = item_hidden
                    items.append(item)
                    file_pointer = f.tell()
                p = Planet(xPos, yPos, rad, M, len(items))
                p.load_items(items)
                self.planets.append(p)
                f.seek(file_pointer)


            #print(self.planets)

                

        self.game_state = "Running"
        self.m  = 100
        self.player_left = False
        self.player_right = False
        self.PLAYER_JUMP_VELOCITY = 500
        self.PLAYER_IMAGE_PATH = "./placeholder_item.png"
        self.PLAYER_HEIGHT = 40
        self.PLAYER_WIDTH = 40

        self.NUM_ITEMS = 20
        self.G = 100


    def init_camera(self):
        self.CAMERA_WORLD_LEFT = 0
        self.CAMERA_WORLD_RIGHT = self.WINDOW_WIDTH
        self.CAMERA_WORLD_TOP = self.WINDOW_HEIGHT
        self.CAMERA_WORLD_BOTTOM = 0
        self.CAMERA_SCREEN_LEFT = 0
        self.CAMERA_SCREEN_RIGHT = self.WINDOW_WIDTH
        self.CAMERA_SCREEN_TOP = 0
        self.CAMERA_SCREEN_BOTTOM = self.WINDOW_HEIGHT

    def screen_to_world(self, screenX, screenY):
        worldX =   screenX
        worldY =   self.WINDOW_HEIGHT - screenY
        return worldX, worldY

    def world_to_screen(self, worldX, worldY):
        screenX =   worldX
        screenY =   self.WINDOW_HEIGHT - worldY
        return screenX, screenY

    def init_platform(self):
        self.planets = [
            Planet(200, 700, 100, -3000, 2),
            Planet(400, random.randint(300,400), 200,-5000, 5),
            Planet(800, 200, 100, -3000, 2),
            Planet(1000, random.randint(500, 700), 200, -5000, 7),
            Planet(1200, 200, 100, -3000, 4)
        ]
        self.NUM_ITEMS = 20
        self.G = 100


    def init_window(self):
        self.WINDOW_WIDTH = 1440
        self.WINDOW_HEIGHT = 900
        self.DELTA_TIME = 10 #seconds

    def init_player(self):
        self.timer = 0
        self.score = 0
        self.game_state = "Running"
        self.m  = 100
        self.player_left = False
        self.player_right = False
        self.PLAYER_JUMP_VELOCITY = 500
        self.PLAYER_IMAGE_PATH = "./placeholder_item.png"
        self.player_xPos = 0
        self.player_rotation = 90
        self.player_yPos = 900
        self.PLAYER_HEIGHT = 40
        self.PLAYER_WIDTH = 40
        self.player_action = "None"
        self.player_yVelocity = 0
        self.player_xVelocity = 0

    def milisecs_to_secs(self, ms):
        return ms/1000

    def on_key_press(self, event):
        key_pressed = event.keysym
        if key_pressed == keybindings["Jump"].get(): 
            self.player_jumping = True
        if key_pressed == keybindings["Left"].get():
            self.player_action = "Left"
        if key_pressed == keybindings["Right"].get():
            self.player_action = "Right"
        if key_pressed == "r":
            self.timer = 0
        if key_pressed == "p":
            if self.game_state == "Paused":
                self.itemconfig(self.paused_label, state='hidden')
                self.save_button['state']  = 'disabled'
                self.quit_button['state'] = 'disabled'
                self.itemconfig(self.save_button_window, state='hidden')
                self.itemconfig(self.quit_button_window, state='hidden')
                self.game_state = "Running"
            elif self.game_state == "Running":
                self.itemconfig(self.paused_label, state='normal')
                self.itemconfig(self.quit_button_window, state='normal')
                self.itemconfig(self.save_button_window, state='normal')
                self.save_button['state']  = 'normal'
                self.quit_button['state'] = 'normal'
                self.game_state = "Paused"


    def pointA(self, w, h, x, y, cos_theta, sin_theta):
        return (x - w*cos_theta - h*sin_theta, 
                y - w*sin_theta+ h*cos_theta)

    def pointB(self, w, h, x, y, cos_theta, sin_theta):
        return (x + w*cos_theta - h*sin_theta, 
                y + w*sin_theta + h*cos_theta)

    def pointC(self, w, h, x, y, cos_theta, sin_theta):
        return (x + w*cos_theta + h*sin_theta, 
                y + w*sin_theta - h*cos_theta)

    def pointD(self, w,h,x,y,cos_theta,sin_theta):
        return (x - w*cos_theta + h*sin_theta, 
                y - w*sin_theta - h*cos_theta)

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
        dist_rad = (distance <= rad)
        between_x = max(xa,xb) >= px and px >=  min(xa,xb)
        between_y = max(ya,yb) >= py and py >=  min(ya,yb)
        return dist_rad and between_x and between_y
    
    def player_planet_collision(self, new_player_xPos, new_player_yPos, new_cos_theta, new_sin_theta, planet_xPos, planet_yPos, planet_radius):
        
        #Equations to calculate individual coordinates of player's hitbox
        new_a = self.pointA(self.PLAYER_WIDTH/2, self.PLAYER_HEIGHT/2, new_player_xPos, new_player_yPos, new_cos_theta, new_sin_theta)
        new_b = self.pointB(self.PLAYER_WIDTH/2, self.PLAYER_HEIGHT/2, new_player_xPos, new_player_yPos, new_cos_theta, new_sin_theta)
        new_c = self.pointC(self.PLAYER_WIDTH/2, self.PLAYER_HEIGHT/2, new_player_xPos, new_player_yPos, new_cos_theta, new_sin_theta)
        new_d = self.pointD(self.PLAYER_WIDTH/2, self.PLAYER_HEIGHT/2, new_player_xPos, new_player_yPos, new_cos_theta, new_sin_theta)
        p = (planet_xPos, planet_yPos)

        #Vector equations to check if the centre of circle is inside the rectangle 
        ap = (p[0]-new_a[0],p[1]-new_a[1])
        ab = (new_b[0]-new_a[0],new_b[1]-new_a[1])
        ad = (new_d[0]-new_a[0],new_d[1]-new_a[1])
        ap_dot_ab = (ap[0]*ab[0]+ap[1]*ab[1])
        ab_dot_ab = 2*(ab[0]*ab[0])
        ap_dot_ad = (ap[0]*ad[0]+ap[1]*ad[1])
        ad_dot_ad = 2*(ad[0]*ad[0])

        planet_center_in_player = (
            0 <= ap_dot_ab
            and ap_dot_ab <= ab_dot_ab
            and 0 <= ap_dot_ad
            and ap_dot_ad <= ad_dot_ad
        )

        #bools confirming if planets intersects player
        intersect_check = [
            self.is_intersect(planet_yPos, new_a[1], new_b[1], planet_xPos, new_a[0], new_b[0], planet_radius),
            self.is_intersect(planet_yPos, new_a[1], new_d[1], planet_xPos, new_a[0], new_d[0], planet_radius),
            self.is_intersect(planet_yPos, new_c[1], new_d[1], planet_xPos, new_c[0], new_d[0],planet_radius),
            self.is_intersect(planet_yPos, new_b[1], new_c[1], planet_xPos, new_b[0], new_c[0],planet_radius)
        ]
        
        return planet_center_in_player or any(intersect_check)


    def set_text(self):
        self.itemconfig(self.score_label, text=f"{self.score}/{self.NUM_ITEMS}")
        self.itemconfig(self.timer_label, text=f"{self.timer}")
    
    def game_loop(self):
        if self.game_state == "Paused":
            self.after(10, self.game_loop)
            return
        dt = self.milisecs_to_secs(self.DELTA_TIME)
        """       

        if sin_theta >= 0 and cos_theta >= 0:
            self.player_rotation = math.degrees(math.acos(cos_theta))
        elif sin_theta > 0 and cos_theta < 0:
            self.player_rotation = math.degrees(math.acos(sin_theta))
        elif sin_theta < 0 and cos_theta > 0:
            self.player_rotation = math.degrees(math.acos(cos_theta))
        else:
            self.player_rotation = math.degrees(math.acos(sin_theta))
        """

        #print("Direct distance: " ,direct_distance)
        #print("cos_theta: ", self.cos_theta)
        #print("sin_theta: ", self.sin_theta)
        #print("YPos: ", self.player_yPos)
        #print("XPos: ", self.player_xPos)
        #print("XVelocity: ", self.player_xVelocity)
        #print("YVelocity: ", self.player_yVelocity)
        #print("Angle: " ,self.player_rotation)
        
        #collision with platfom
        #circle centre in the rectangle prep
        #Calculate new position based on all planet's gravitational pull...
        
        gravitational_pullX = 0
        gravitational_pullY = 0
        planet_player_cos_thetas = []
        planet_player_sin_thetas = []
        for planet in self.planets:
            planet_player_distance = (math.sqrt((self.player_xPos-planet.xPos)**2 + (self.player_yPos-planet.yPos)**2))
            planet_player_sin_theta = (self.player_yPos - planet.yPos)/planet_player_distance
            planet_player_cos_theta = (self.player_xPos - planet.xPos)/planet_player_distance
            F = (self.G * self.m * planet.M)/(planet_player_distance**2)
            gravitational_pullX += planet_player_cos_theta*F
            gravitational_pullY += planet_player_sin_theta*F
            planet_player_cos_thetas.append(planet_player_cos_theta)
            planet_player_sin_thetas.append(planet_player_sin_theta)
            #print(F)
        #print(planet_player_cos_thetas)
        #print(planet_player_sin_thetas)
        
        new_player_yPos = self.player_yPos + self.player_yVelocity*dt + 0.5*gravitational_pullY*(dt**2)
        new_player_yVelocity = self.player_yVelocity + (gravitational_pullY*(dt))
        new_player_xPos = self.player_xPos + self.player_xVelocity*dt + 0.5*gravitational_pullX*(dt**2)
        new_player_xVelocity = self.player_xVelocity + (gravitational_pullX*(dt))
        
        closest_distance_to_surface = math.inf
        collision_occured = False
        for index, planet in enumerate(self.planets):
            new_direct_distance = (math.sqrt((new_player_xPos-planet.xPos)**2 + (new_player_yPos-planet.yPos)**2))
            new_cos_theta = (new_player_xPos - planet.xPos)/new_direct_distance
            new_sin_theta = (new_player_yPos - planet.yPos)/new_direct_distance
            if closest_distance_to_surface > (new_direct_distance-planet.rad):
                closest_planet = planet
                closest_distance_to_surface = new_direct_distance-planet.rad
            if self.player_planet_collision(new_player_xPos, new_player_yPos, new_cos_theta, new_sin_theta, planet.xPos, planet.yPos, planet.rad):
                #print("Collision!")
                collision_occured = True
                #find component going at angle theta, '
                #accel = self.G * self.m * planet.M / (planet.rad+self.PLAYER_HEIGHT/2)**2
                
                #yAccel = -1 *accel*planet_player_sin_thetas[index]
                #xAccel = -1 *accel*planet_player_cos_thetas[index]
                #self.player_yVelocity = self.player_yVelocity + (yAccel*(dt))
                #self.player_xVelocity = self.player_xVelocity + (xAccel*(dt))
                self.player_xVelocity = 0
                self.plaxer_yVelocity = 0
                #print("Old position: ", (self.player_xPos, self.player_yPos))
                #print("Collided position:", (new_player_xPos, new_player_yPos))
                self.player_yPos = planet.yPos + (self.PLAYER_HEIGHT/2 + planet.rad)*planet_player_sin_thetas[index]
                self.player_xPos = planet.xPos  + (self.PLAYER_HEIGHT/2 + planet.rad)*planet_player_cos_thetas[index]
                #print(self.player_yPos, self.player_xPos)
                #print("New position: ", (self.player_xPos, self.player_yPos))
                #print("A: ", new_a)
                #print("B: ", new_b)
                #print("C: ", new_c)
                #print("D: ", new_d)

                #print("Distance: ",end="" )
                #self.is_intersect(self.PLATFORM_YPOS, new_a[1], new_d[1], self.PLATFORM_XPOS, new_a[0], new_d[0],self.PLATFORM_RADIUS),
                self.player_rotation = math.degrees(math.atan2(self.player_yPos-closest_planet.yPos, self.player_xPos-closest_planet.xPos))
                if self.player_jumping:
                    self.player_xVelocity = self.PLAYER_JUMP_VELOCITY*planet_player_cos_thetas[index]
                    self.player_yVelocity = self.PLAYER_JUMP_VELOCITY*planet_player_sin_thetas[index]
                    self.player_jumping = None
                if self.player_action == "Left":
                    rotation_angle = 3
                    angle = self.player_rotation
                    angle += rotation_angle
                    self.player_xPos = planet.xPos + (planet.rad+self.PLAYER_HEIGHT/2)*math.cos(math.radians(angle))
                    self.player_yPos = planet.yPos + (planet.rad+self.PLAYER_HEIGHT/2)*math.sin(math.radians(angle))
                    self.player_action = None
                if self.player_action == "Right":
                    #print("Right button pressed!")
                    rotation_angle = 3
                    angle = self.player_rotation
                    angle -= rotation_angle
                    self.player_xPos = planet.xPos + (planet.rad+self.PLAYER_HEIGHT/2)*math.cos(math.radians(angle))
                    self.player_yPos = planet.yPos + (planet.rad+self.PLAYER_HEIGHT/2)*math.sin(math.radians(angle))
                    self.player_action = None

        if not collision_occured:
            #Update player position and velocity
            #print("No Collision")
            #print("Position: ",new_player_xPos, new_player_yPos)
            self.player_xPos = new_player_xPos
            self.player_yPos = new_player_yPos
            #self.sin_theta = new_sin_theta
            #self.cos_theta = new_cos_theta
            self.player_xVelocity = new_player_xVelocity
            self.player_yVelocity = new_player_yVelocity
            self.player_rotation = math.degrees(math.atan2(new_player_yPos-closest_planet.yPos, new_player_xPos-closest_planet.xPos))
            #print(closest_planet.xPos, closest_planet.yPos)
            self.action = None
        
        self.player_jumping = False

        #self.player_jumping = False
        self.action = None
        #Left+Right -> not based on collision

        #player gets items...
        for planet_number, planet in enumerate(self.planets):
            for item_number, item in enumerate(planet.items):
                if not self.planets[planet_number].items[item_number].hidden:
                    if self.player_planet_collision(new_player_xPos, new_player_yPos, new_cos_theta, new_sin_theta, item.xPos, item.yPos, Item.RADIUS):
                        self.score += Item.POINT_COUNT
                        #print(self.planets, planet.items)
                        #print(planet_number, item_number)
                        #print(self.item_handles)
                        self.delete(self.item_handles[planet_number][item_number])
                        self.planets[planet_number].items[item_number].hidden = True
            

        """"
        #Collision with floor
        if self.player_bottom() >= self.platform_yPos():
            self.player_yVelocity = 0
            self.player_yPos = (self.platform_yPos()) - (self.PLAYER_HEIGHT/2)
            #Jumping action (only if player is touching the floor)
            if self.player_action == "Jump":
                self.player_yVelocity = self.PLAYER_JUMP_VELOCITY
        else:
            #player has no action (because it's falling)
            self.player_action = "none"
        """""
        #update player stats - coords and rotation
        self.delete(self.player)
        self.player_image = Image.open(self.PLAYER_IMAGE_PATH).rotate(self.player_rotation)
        self.resized_player = self.player_image.resize((self.PLAYER_WIDTH, self.PLAYER_HEIGHT))
        self.photo_image = ImageTk.PhotoImage(self.resized_player)
        self.player = self.create_image(
            *self.world_to_screen(self.player_xPos, self.player_yPos) ,image=self.photo_image, tag="player"
        )
        self.set_text()
        #run game loop again
        if self.score != self.NUM_ITEMS:
            self.after(self.DELTA_TIME, self.game_loop)
            self.timer += 1
        else:
            #time_taken = self.current_time - self.start_time
            #initials = self.game_over(time_taken)
            #self.writeToLeaderboard(initials, time_taken)
            #self.displayLeaderboard()
            #All the stuff to finish the game
            self.game_over()
    


    def game_over(self):
        global time_elapsed, is_load, game_over_time
        time_elapsed = self.timer
        is_load = False
        game_over_frame.tkraise()
        game_over_time['text'] = time_elapsed
        start_game_button['state'] = 'normal'

        self.destroy()

    def create_images(self):
        self.player_image = Image.open(self.PLAYER_IMAGE_PATH)
        self.resized_player = self.player_image.resize((self.PLAYER_WIDTH, self.PLAYER_HEIGHT))
        self.photo_image = ImageTk.PhotoImage(self.resized_player)
        self.player = self.create_image(
            *self.world_to_screen(self.player_xPos, self.player_yPos) ,image=self.photo_image, tag="player"
        )

    def create_objects(self):
        self.planet_handles = []
        self.item_handles = []
        #in order to not get garbage collected
        self.item_image_hadnles = []
        for planet in self.planets:
            self.planet_handles.append(self.create_oval(
                *self.world_to_screen(planet.xPos-planet.rad, planet.yPos-planet.rad), 
                *self.world_to_screen(planet.xPos+planet.rad, planet.yPos+planet.rad),
                tag="platform",
                fill='black'
            ))
            planet_items = []
            for item in planet.items:
                item_image = Image.open(Item.ITEM_IMAGE_PATH).rotate(item.rotation)
                resized_item = item_image.resize((Item.HEIGHT, Item.WIDTH))
                item_image = ImageTk.PhotoImage(resized_item)
                item_state = 'hidden' if item.hidden else 'normal'
                self.item_image_hadnles.append(item_image)
                planet_items.append(
                    self.create_image(
                        *self.world_to_screen(item.xPos, item.yPos),
                        image=item_image,
                        tag="item",
                        state = item_state
                    )
                )
            self.item_handles.append(planet_items)            


menu = True
game = False
boss_key = False
game_frame = None
main_menu_frame = None
time_elapsed = 0
game_over_time = 0
boss_key_frame = None
keybindings_page = None
is_load = False
root_window = None
load = False
jump_keybinding = 'Jump'
right_keybinding = 'Right'
left_keybinding = 'Left'
keybindings = {'Left': None , 'Right':None, 'Jump':None}

def start():
    global game, menu, main_menu_frame, is_load
    game = True
    menu = False
    game_frame.tkraise()
    start_game_button["state"] = "disabled"
    GravityJump(game_frame, keybindings, is_load)

def flip(*args):
    global game, game_frame, boss_key_frame, root_window, boss_key, menu
    if boss_key:
        if game:
            game_frame.tkraise()
        elif menu:
            main_menu_frame.tkraise()
        root_window.title("Gravity Jump")
        boss_key = False
    else:
        boss_key_frame.tkraise()
        root_window.title("Excel [1]")
        boss_key = True

def update_jump_keybinding(e):
    keybindings["Jump"] = keybindings["Jump"]
    #print(keybindings["Jump"])

def update_right_keybinding(e):
    keybindings["Right"] = keybindings["Right"]
    #print(keybindings["Right"])

def update_left_keybinding(e):
    keybindings["Left"] = keybindings["Left"]
    #print(keybindings["Left"])

def set_load():
    global is_load
    is_load = True
    start()

def build_main_menu(main_menu_frame):
    global keybindings, start_game_button, keybindings_page, main_page, jump_keybinding, left_keybinding, right_keybinding

    keybindings_page = ttk.Frame(main_menu_frame, height=1440, width=900)
    keybindings_page.grid(row=0, column=0, sticky="nsew")
    keybindings_page_title = ttk.Label(keybindings_page, text="Keybindings", font="Times 80 bold")
    keybindings_back_button = ttk.Button(keybindings_page, text="Back", command=move_to_start)
    keybindings_jump = ttk.Frame(keybindings_page)
    keybindings_jump_text = ttk.Label(keybindings_jump, text="Jump")
    keybindings["Jump"] = tk.StringVar(keybindings_jump, 'Up')
    keybindings_jump_combobox = ttk.Combobox(keybindings_jump, textvariable=keybindings["Jump"])
    keybindings_jump_combobox['values'] = ('space', 'Up', 'w')
    keybindings_jump_combobox.bind('<<ComboboxSelected>>', update_jump_keybinding)

    keybindings_left = ttk.Frame(keybindings_page)
    keybindings_left_text = ttk.Label(keybindings_left, text="Left")
    keybindings["Left"] = tk.StringVar(keybindings_left, 'Left')
    keybindings_left_combobox = ttk.Combobox(keybindings_left, textvariable=keybindings['Left'])
    keybindings_left_combobox['values'] = ('Left', 'a')
    keybindings_left_combobox.bind('<<ComboboxSelected>>', update_left_keybinding)
    
    keybindings_right = ttk.Frame(keybindings_page)
    keybindings_right_text = ttk.Label(keybindings_right, text="Right")
    keybindings["Right"] = tk.StringVar(keybindings_right, 'Right')
    keybindings_right_combobox = ttk.Combobox(keybindings_right, textvariable=keybindings['Right'])
    keybindings_right_combobox['values'] = ('Right', 'd')
    keybindings_right_combobox.bind('<<ComboboxSelected>>', update_right_keybinding)

    keybindings_page_title.pack()
    keybindings_back_button.pack()
    keybindings_jump.pack()
    keybindings_jump_text.pack()
    keybindings_jump_combobox.pack()

    keybindings_left.pack()
    keybindings_left_text.pack()
    keybindings_left_combobox.pack()

    keybindings_right.pack()
    keybindings_right_text.pack()
    keybindings_right_combobox.pack()

    main_page = ttk.Frame(main_menu_frame, height=1440, width = 900)
    main_page.grid(row=0, column=0, sticky="nsew")
    main_page_title = ttk.Label(main_page, text="Gravity Jump", font="Times 80 bold")
    main_page_title.pack()
    main_page_button_controller = ttk.Frame(main_page, height=400, width=300)
    main_page_button_controller.pack()
    start_game_button = ttk.Button(main_page_button_controller,text="Start Game",command=start)
    start_game_button.pack()
    keybindings_button = ttk.Button(main_page_button_controller,text="Keybindings", command=move_to_keybindings)
    keybindings_button.pack()
    load_game_button = ttk.Button(main_page_button_controller,text="Load Game",command=set_load)
    load_game_button.pack()

def move_to_keybindings():
    keybindings_page.tkraise()

def move_to_start_menu():
    main_menu_frame.tkraise()

def move_to_start():
    main_page.tkraise()

def display_leaderboard():
    global leaderboard, leaderboard_page
    leaderboard_contents = []
    with open('leaderboard.txt', 'r') as f:
        file_contents = f.readlines()
    for x in range(0,len(file_contents)-1,2):
        user_data =[]
        user_data.append(file_contents[x])
        user_data.append(int(file_contents[x+1].strip()))
        leaderboard_contents.append(user_data)
    leaderboard_contents.sort(key=lambda data: data[1])
        
    for row in leaderboard.get_children(): 
        leaderboard.delete(row)
    for record in leaderboard_contents:
        leaderboard.insert("", "end", text="row", values=(record[0], record[1]))
    leaderboard_page.tkraise()
    

def write_to_leaderboard():
    global time_elapsed
    with open('leaderboard.txt', 'a+') as f:
        f.write(user_initials.get()+'\n')
        f.write(str(time_elapsed)+'\n')
    user_initials.set('')
    display_leaderboard()

def build_game_frame():
    global game_frame, user_initials, time_elapsed, game_over_frame, leaderboard, leaderboard_page, game_over_time
    game_frame = ttk.Frame(root_window, height=1440, width=900)
    game_frame.grid(row=0, column=0, sticky="nsew")
    user_initials = tk.StringVar()
    game_over_frame = ttk.Frame(game_frame, width=1440, height=900)
    game_over_frame.grid(row=0,column=0,sticky="nsew")
    game_over_label = ttk.Label(game_over_frame, text='GAME OVER', font='Times 40 bold')
    game_over_label.pack()
    game_over_time = ttk.Label(game_over_frame, text=time_elapsed)
    game_over_time.pack()
    game_over_initials = ttk.Entry(game_over_frame, textvariable=user_initials)
    game_over_initials.pack()
    game_over_submit_button = ttk.Button(game_over_frame, text="To leaderboard",command=write_to_leaderboard)
    game_over_submit_button.pack()

    leaderboard_page = ttk.Frame(game_frame, width=1440, height=900)
    leaderboard_page.grid(row=0, column=0, sticky="nsew")
    leaderboard_frame = ttk.Frame(leaderboard_page, width=1440, height=900)
    leaderboard_frame.grid(row=0, column=0, sticky='nsew')
    #leaderboard_scrollbar = ttk.Scrollbar(leaderboard_frame)
    leaderboard = ttk.Treeview(leaderboard_frame,columns=('Initials', 'Time'),show='headings')
    leaderboard.heading('# 1', text="Initials")
    leaderboard.heading('# 2', text="Time")




    #leaderboard_scrollbar.configure(command=leaderboard.yview)
    leaderboard_button = ttk.Button(leaderboard_page, text="Back to main menu",command=move_to_start_menu)

    #leaderboard_scrollbar.pack(side='right', fill='y')
    leaderboard.pack(side='left', fill='both', expand=True)
    leaderboard_button.grid(row=1, column=0)

def start_game():
    global boss_key_frame, root_window, main_menu_frame
    root_window = setup_window()
    boss_key_frame = ttk.Frame(root_window, height=1440, width=900)
    boss_key_frame.grid(row=0, column=0, sticky="nsew")
    build_game_frame()
    excel_image = Image.open("excel_spreadsheet.png").resize((1440, 900))
    excel_tkImage = ImageTk.PhotoImage(excel_image)
    excel_spreadsheet = ttk.Label(boss_key_frame,image=excel_tkImage)
    excel_spreadsheet.pack()
    root_window.bind('<c>', flip)
    main_menu_frame = ttk.Frame(root_window, height=1440, width=900)
    main_menu_frame.grid(row=0, column=0, sticky="nsew")
    build_main_menu(main_menu_frame)
    root_window.mainloop()
    

def test_camera():
    obj = GravityJump()
    #print(obj.screen_to_world(100, 150))
    #print(obj.world_to_screen(100, 150))

start_game()
#test_camera()
    