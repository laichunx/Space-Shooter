import sys, logging, os, random, math, open_color, arcade

#check to make sure we are running the right version of Python
version = (3,7)
assert sys.version_info >= version, "This script requires at least Python {0}.{1}".format(version[0],version[1])

#turn on logging, in case we have to leave ourselves debugging messages
logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MARGIN = 30
SCREEN_TITLE = "Space Shooter"

NUM_ENEMIES = 5
STARTING_LOCATION = (400,100)
BULLET_DAMAGE = 10
ENEMY_HP = 100
HIT_SCORE = 10
KILL_SCORE = 100


class Bullet(arcade.Sprite):
    def __init__(self, position, velocity, damage):
        ''' 
        initializes the bullet
        Parameters: position: (x,y) tuple
            velocity: (dx, dy) tuple
            damage: int (or float)
        '''
        super().__init__("assets/bullet.png", 0.5)
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity
        self.damage = damage

    def update(self):
        '''
        Moves the bullet
        '''
        self.center_x += self.dx
        self.center_y += self.dy


    
class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("assets/SpaceShip.png", 0.5)
        (self.center_x, self.center_y) = STARTING_LOCATION

class Enemy(arcade.Sprite):
    def __init__(self, position):
        '''
        initializes an enemy
        Parameter: position: (x,y) tuple
        '''
        super().__init__("assets/EnemySpaceShip.png", 0.5)
        self.hp = ENEMY_HP
        (self.center_x, self.center_y) = position
        #(self.dx, self.dy) = velocity #This is defined to make enemies move on their own

class EnemyBullet(arcade.Sprite):
    def __init__(self, position, velocity, damage):
        super().__init__("assets/bullet_enemy.png", 0.5)
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity
        self.damage = damage
        #Figure out how to match the shooting enemy bullets up with the enemy's positions
        #def update(self):
            #self.center_x += 
            #self.center_y += 


        


class Window(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.set_mouse_visible(True)
        self.background = None
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player = Player()
        self.score = 0

    def setup(self):
        '''
        Set up enemies
        '''
        for i in range(NUM_ENEMIES):
            x = 120 * (i+1) + 40 
            y = random.randrange(300,500)
            enemy = Enemy((x,y))
            self.enemy_list.append(enemy)       

        self.background = arcade.load_texture("assets/SpaceShooterBackground.jpg") 

    def update(self, delta_time):
        self.bullet_list.update()
        #The lines below should make enemies move around on their own FIGURE OUT VELOCITY
        #self.enemy_list.update()
        #for e in self.enemy_list:
           # e.center_x = e.center_x + e.dx
            #e.center_y = e.center_y + e.dy
            #if e.center_x <= 0:
                #e.dx = abs(e.dx)
            #if e.center_x >= SCREEN_WIDTH:
                #e.dx = abs(e.dx) * -1
            #if e.center_y <= 750:
                #e.dy = abs(e.dy)
            #if e.center_y >= SCREEN_HEIGHT:
                #e.dy = abs(e.dy) * 1
        for e in self.enemy_list:

            damage = arcade.check_for_collision_with_list(e, self.bullet_list)
            for d in damage:
                e.hp = e.hp - d.damage
                d.kill()
                if e.hp < 0:
                    e.kill()
                    self.score = self.score + KILL_SCORE
                else:
                    self.score = self.score + HIT_SCORE
           
    def on_draw(self):
        arcade.start_render()

        arcade.draw_texture_rectangle(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        self.player.draw()
        self.bullet_list.draw()
        self.enemy_list.draw()

        arcade.draw_text(f"Score: {self.score}", 20, SCREEN_HEIGHT - 40, (255, 255, 255), 16)

    def on_mouse_motion(self, x, y, dx, dy):
        '''
        The player moves left and right and up and down with the mouse
        '''
        self.player.center_x = x
        self.player.center_y = y

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            x = self.player.center_x
            y = self.player.center_y + 15
            bullet = Bullet((x,y),(0,10),BULLET_DAMAGE)
            self.bullet_list.append(bullet)
            #fires a bullet when the mouse is clicked
           

def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()