#! /usr/bin/python
import pygame,sys,os,random,time,glob,math

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
cyan = (0,255,255)
grey = (90,90,90)
slate = (47,89,89)
silver = (200,200,200)
bblue = (0, 109, 160)

with open(os.path.join(os.path.dirname(sys.argv[0]),'data/res.dat')) as f:
    content = f.readlines()
    f.close()

width = content[1]
height = content[2]
width = int(width)
height = int(height)
WIN_WIDTH = width
WIN_HEIGHT = height
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 0

pygame.init()
try:
    pygame.font.init()
    font = pygame.font.SysFont('Georgia', 10)
except:
    pass

walls = pygame.sprite.Group()
entities = pygame.sprite.Group()
backgrounds = pygame.sprite.Group()
view_object = pygame.sprite.Group()

stars = []
levels = []

illyrians = []
igliders = []

devaris = []
dgliders = []

projectiles = []

total_level_width  = 0
total_level_height = 0

def build(level):

    total_level_width  = len(level[0])*200
    total_level_height = len(level)*200

    (total_level_width)
    (total_level_height)

    x = y = 0
    for row in level:
        for col in row:

            if col == "s":
                s = Star(x,y)
                stars.append(s)
                entities.add(s)

            if col == "o":
                v = Background(x,y,"#900C3F")
                backgrounds.add(v)
            if col == "v":
                v = Background(x,y,"#581845")
                backgrounds.add(v)
            if col == "p":
                p = Background(x,y,"#0000CD")
                backgrounds.add(p)
            if col == 's':
                s = Background(x,y,"#0000FF")
                backgrounds.add(s)
            if col == 'b':
                b = Background(x,y,"#000000")
                backgrounds.add(b)
            if col == 'q':
                q = Illyrian(x,y)
                illyrians.append(q)
                entities.add(q)
            if col == 'd':
                d = Devaris(x,y)
                devaris.append(d)
                entities.add(d)
            x += 200
        y += 200
        x = 0
    player = illyrians[0]
    entities.add(player)
    ('Lives: 5')

def clearall(l):
    entities.empty()
    del illyrians[:]
    del igliders[:]

    del devaris[:]
    del dgliders[:]

    del stars[:]

    del projectiles[:]

    backgrounds.empty()
    walls.empty()
    build(levels[l])
    level = levels[l]
    total_level_width  = len(level[0])*200
    total_level_height = len(level)*200
    camera = Camera(complex_camera, total_level_width, total_level_height)

def main():
    Game = True
    l = 0
    firstround = True
    try:
        pygame.mixer.music.load(os.path.join(os.path.dirname(sys.argv[0]),'resources/soundtrack.wav'))
        pygame.mixer.music.play()
    except:
        pass
    playing = True
    while Game:
        global cameraX, cameraY

        screen = pygame.display.set_mode(DISPLAY,FLAGS, DEPTH)

        timer = pygame.time.Clock()

        pygame.mouse.set_visible(False)

        up = down = left = right = glider = shooting = shielding = expand = mouse_button = False

        bg = pygame.Surface((32,32))
        bg.fill(pygame.Color("#000000"))

        bg.convert()
        #bg = pygame.image.load('block.png')

        for name in glob.glob(os.path.join(os.path.dirname(sys.argv[0]),'data/*.map')):
            with open(name) as f:
                level = f.readlines()
                levels.append(level)
                f.close()

        # build the level

        if firstround == True:
            build(levels[l])
            firstround = False
        else:
            pass

        level = levels[l]
        total_level_width  = len(level[0])*200
        total_level_height = len(level)*200
        camera = Camera(complex_camera, total_level_width, total_level_height)

        lastdir = 'right'

        Running = True

        player = illyrians[0]

        pause = False

        mouseblock = Background(0,0)

        with open(os.path.join(os.path.dirname(sys.argv[0]),'data/fps.dat')) as f:
            fpscontent = f.readlines()
            f.close()

        fps = fpscontent[0]

        while Running:

            timer.tick(float(fps))

            pygame.display.set_caption(str(player.rect.left)+' '+str(player.rect.top))

            mouse_button = False

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    Game = False
                    Running = False
                    pygame.quit()
                    sys.exit(0)
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    Game = False
                    Running = False
                    pygame.quit()
                    sys.exit(0)
                if e.type == pygame.KEYDOWN and e.key == pygame.K_UP:
                    up = True
                if e.type == pygame.KEYDOWN and e.key == pygame.K_DOWN:
                    down = True
                if e.type == pygame.KEYDOWN and e.key == pygame.K_LEFT:
                    lastdir = 'left'
                    left = True
                if e.type == pygame.KEYDOWN and e.key == pygame.K_RIGHT:
                    lastdir = 'right'
                    right = True
                if e.type == pygame.KEYDOWN and e.key == pygame.K_z:
                    shooting = True
                if e.type == pygame.KEYDOWN and e.key == pygame.K_x:
                    shielding = True

                if e.type == pygame.KEYDOWN and e.key == pygame.K_a:
                    expand = -1
                if e.type == pygame.KEYDOWN and e.key == pygame.K_s:
                    expand = 1

                if e.type == pygame.KEYUP and e.key == pygame.K_LEFT:
                    left = False

                if e.type == pygame.KEYUP and e.key == pygame.K_RIGHT:
                    right = False

                if e.type == pygame.KEYDOWN and e.key == pygame.K_e:
                    for x in range(0,2):
                        pro = Projectile(5,5,100)
                        projectiles.append(pro)
                        entities.add(pro)
                        g = IllyrianGlider(pro,player,player.rect.left+random.randint(-16,16),player.rect.top+random.randint(-16,16))
                        pro.owner = g
                        igliders.append(g)
                        entities.add(g)

                if e.type == pygame.KEYUP and e.key == pygame.K_z:
                    shooting = False
                if e.type == pygame.KEYUP and e.key == pygame.K_x:
                    shielding = False

                if e.type == pygame.KEYUP and e.key == pygame.K_a:
                    expand = 0
                if e.type == pygame.KEYUP and e.key == pygame.K_s:
                    expand = 0

                if e.type == pygame.KEYUP and e.key == pygame.K_ESCAPE:
                    try:
                        if playing:
                            playing = False
                            pygame.mixer.music.pause()
                        elif not playing:
                            playing = True
                            pygame.mixer.music.unpause()
                    except:
                        pass
                if e.type == pygame.KEYUP and e.key == pygame.K_UP:
                    up = False
                if e.type == pygame.KEYUP and e.key == pygame.K_DOWN:
                    down = False

                if e.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()

                if e.type == pygame.MOUSEBUTTONDOWN:
                    for ill in illyrians:
                        if pygame.Rect.colliderect(ill.rect,mouseblock.rect):
                            player = ill

            mouseblock.rect.left = mouse_pos[0] + player.rect.left - HALF_WIDTH
            mouseblock.rect.top = mouse_pos[1] + player.rect.top - HALF_HEIGHT

            # draw background
            for y in range(32):
                for x in range(32):
                    screen.blit(bg, (x * 32, y * 32))

            camera.update(player)

            # update player, draw everything else
            try:
                player.update(up, down, left, right, shooting, shielding, expand)
            except Exception as e:
                (e)

            playersgliders = 0


            for glider in igliders:
                glider.update()
                glider.orbit()
                glider.projectile.update()

            for glider in igliders:
                if glider.mothership == player:
                    playersgliders += 1

            for glider in dgliders:
                glider.update()
                glider.orbit()
                glider.projectile.update()

            for dev in devaris:
                dev.update(player)
                dev.checkdeath()

            for ill in illyrians:
                if player.lives <= 0:
                    player = illyrians[0]
                ill.checkdeath()
                if len(illyrians) == 0:
                    Running = False
                if ill != player:
                    ill.AIupdate(player)

            player.set_message(str(playersgliders))
            if (player.message != player.previous_message):
                player.set_message(player.previous_message)
            screen.blit(player.message,(HALF_WIDTH+6,HALF_HEIGHT+20))


            for b in backgrounds:
                screen.blit(b.image, camera.apply(b))

            for e in entities:
                screen.blit(e.image, camera.apply(e))

            View.update()

            pygame.display.update()

        screen.fill(black)

        pygame.display.update()

        time.sleep(0.25)
        with open(os.path.join(os.path.dirname(sys.argv[0]),'data/dif.dat'))as f:
            content = f.readlines()
            difficulty = content[1]
            f.close()

        if difficulty == 'norm':
            (difficulty)
            try:
                clearall(l)
                level = levels[l]
                total_level_width  = len(level[0])*32
                total_level_height = len(level)*32
                camera = Camera(complex_camera, total_level_width, total_level_height)
            except:
                ('ERROR IN: building_level')
        else:
            l = 0
            (difficulty)
            try:
                clearall(l)
                level = levels[l]
                total_level_width  = len(level[0])*32
                total_level_height = len(level)*32
                camera = Camera(complex_camera, total_level_width, total_level_height)
            except:
                ('ERROR IN: building_level')


class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class view(Entity):
    def __init__(self,image = "#0000C5"):
        Entity.__init__(self)
        self.color = image
        self.image = pygame.Surface((WIN_WIDTH,WIN_HEIGHT))
        self.image.fill(pygame.Color(self.color))

        try:
            self.image = pygame.image.load(image)
        except:
            pass

        self.rect = pygame.Rect(0, 0,WIN_WIDTH,WIN_HEIGHT)
        view_object.add(self)

View = view()

class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

def simple_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return pygame.Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)

def complex_camera(camera, target_rect):
    with open(os.path.join(os.path.dirname(sys.argv[0]),'data/os.dat')) as f:
        content = f.readlines()
        f.close()
        ostype = content[0]

    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h
    if ostype == 'mac':
        pass
#        l = min(0, l)                      # stop scrolling at the left edge
#        l = max(-(camera.width-WIN_WIDTH)+64, l)   # stop scrolling at the right edge
#        t = max(-(camera.height-WIN_HEIGHT), t) # stop scrolling at the bottom
#        t = min(0, t)                           # stop scrolling at the top
    if ostype == 'win':
        pass
#        l = min(0, l)                      # stop scrolling at the left edge
#        l = max(-(camera.width-WIN_WIDTH)+32, l)   # stop scrolling at the right edge
#        t = max(-(camera.height-WIN_HEIGHT), t) # stop scrolling at the bottom
#        t = min(0, t)                      # stop scrolling at the top
    View.rect.left, View.rect.top, _, _ = pygame.Rect(l, t, w, h)
    View.rect.left = -View.rect.left
    View.rect.top = -View.rect.top
    return pygame.Rect(l, t, w, h)

class Illyrian(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.total_level_width = 5000
        self.total_level_height = 3000
        self.lives = 15
        self.livestime = 3
        self.time = 0
        self.angle = 0
        self.forward = 0
        self.xvel = 0
        self.yvel = 0
        self.gravity = True
        self.onGround = False
        self.image = pygame.Surface((16,16))
        self.image.fill(pygame.Color("#00FFFF"))
        self.rect = pygame.Rect(x, y, 16, 16)
        self.timer = 0
        self.target = None
        self.turn = 0
        self.bumpx = 0
        self.bumpy = 0

    def set_message(self,text):
        try:
            self.message = None
            self.previous_message = None

            self.message = font.render(text,True, cyan)

            self.previous_message = self.message
        except:
            pass
    def AIupdate(self,player):

        self.y = self.rect.top
        if self.rect.left > (self.total_level_width):
            self.rect.left = 0
        if self.rect.left < 0:
            self.rect.left = (self.total_level_width)
        if self.y > (self.total_level_height):
            self.rect.top = 0
        if self.y < 0:
            self.rect.top = (self.total_level_height)

        self.shooting = True
        self.shielding = False
        self.forward = 6

        if self.target == None or self.target not in devaris and len(devaris)>0:
            try:
                for dev in devaris:
                    (dev)
                self.target = devaris[random.randint(0,len(devaris)-1)]
                (self.target)
                self.shooting = True
                self.shielding = False
            except Exception as e:
                (e)

        if len(devaris) == 0:
            self.forward = player.forward
            self.target = player
            self.shooting = False
            self.shielding = False

        if (((((self.target.rect.left-self.rect.left)**2)+((self.target.rect.top-self.rect.top)**2))**0.5) > 200):
            if ((self.target.rect.left-self.rect.left > 0) and (self.target.rect.top-self.rect.top < 0)):
                self.turn = -90-self.angle-math.degrees(math.atan2((self.rect.top-self.target.rect.top),(self.rect.left-self.target.rect.left)))
            if ((self.target.rect.left-self.rect.left < 0) and (self.target.rect.top-self.rect.top > 0)):
                self.turn = 180-self.angle+(90-(math.degrees(math.atan2((self.rect.top-self.target.rect.top),(self.rect.left-self.target.rect.left)))))
            if ((self.target.rect.left-self.rect.left > 0) and (self.target.rect.top-self.rect.top > 0)):
                self.turn = -90-self.angle-math.degrees(math.atan2((self.rect.top-self.target.rect.top),(self.rect.left-self.target.rect.left)))
            if ((self.target.rect.left-self.rect.left < 0) and (self.target.rect.top-self.rect.top < 0)):
                self.turn = 180-self.angle+(90-(math.degrees(math.atan2((self.rect.top-self.target.rect.top),(self.rect.left-self.target.rect.left)))))
            self.angle += self.turn

        if self.angle > 360:
            self.angle += -360
        if self.angle < 0:
            self.angle += 360

        self.timer += 1
        if self.timer == 100:
            ('glider made')
            pro = Projectile(5,5,100)
            projectiles.append(pro)
            entities.add(pro)
            d = IllyrianGlider(pro,self,self.rect.left+random.randint(-16,16),self.rect.top+random.randint(-16,16))
            pro.owner = d
            (pro.owner)
            igliders.append(d)
            entities.add(d)
            self.timer = 0

        if self.shooting:
            for glider in igliders:
                if glider.mothership == self:
                    if ((((glider.rect.left-glider.projectile.rect.left)**2)+((glider.rect.top-glider.projectile.rect.top)**2))**0.5) > 350:
                        glider.projectile.res(glider,glider.mothership)
                    else:
                        pass

        if self.shielding:
            for glider in igliders:
                if glider.mothership == self:
                    if ((((glider.rect.left-glider.projectile.rect.left)**2)+((glider.rect.top-glider.projectile.rect.top)**2))**0.5) > 1800:
                        glider.projectile.res(glider,glider)
                    else:
                        pass


        try:
            for ill in illyrians:
                if ill != self:
                    if pygame.Rect.colliderect(self.rect,ill.rect):
                        self.bumpx = random.randint(-20,20)
                        self.bumpy = random.randint(-20,20)
                        self.rect.left += self.bumpx
                        self.rect.top += self.bumpy
        except:
            pass

        # increment in x direction
        self.xvel = self.forward * math.sin(math.radians(abs(self.angle)))
        self.yvel = self.forward * math.cos(math.radians(abs(self.angle)))
        self.rect.left += self.xvel
        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air

    def update(self, up, down, left, right, shooting, shielding ,expand):

        self.y = self.rect.top
        if self.rect.left > (self.total_level_width):
            self.rect.left = 0
        if self.rect.left < 0:
            self.rect.left = (self.total_level_width)
        if self.y > (self.total_level_height):
            self.rect.top = 0
        if self.y < 0:
            self.rect.top = (self.total_level_height)

        if up:
            if self.forward < 10:
                self.forward += 0.15
        if down:
            if self.forward > -10:
                self.forward -= 0.15
        if left:
            self.angle+=2
            if self.angle > 360:
                self.angle += -360
            if self.angle < 0:
                self.angle += 360

        if right:
            self.angle-=2
            if self.angle > 360:
                self.angle += -360
            if self.angle < 0:
                self.angle += 360

        if not(up or down):
            if self.forward > 0:
                self.forward -= 0.05
            if self.forward < 0:
                self.forward += 0.05

        if shooting:
            for glider in igliders:
                if glider.mothership == self:
                    if ((((glider.rect.left-glider.projectile.rect.left)**2)+((glider.rect.top-glider.projectile.rect.top)**2))**0.5) > 350:
                        glider.projectile.res(glider,glider.mothership)
                    else:
                        pass

        if shielding:
            for glider in igliders:
                if glider.mothership == self:
                    if ((((glider.rect.left-glider.projectile.rect.left)**2)+((glider.rect.top-glider.projectile.rect.top)**2))**0.5) > 1500:
                        glider.projectile.res(glider,glider)
                    else:
                        pass

        if expand > 0:
            for glider in igliders:
                if glider.mothership == self:
                    glider.orbitradius += expand
                    glider.orbitangle = 95
                    if glider.orbitradius < 64:
                        glider.orbitradius = 64
                        glider.orbitangle = 95

        elif expand < 0:
            for glider in igliders:
                if glider.mothership == self:
                    glider.orbitradius += expand
                    glider.orbitangle = 85
                    if glider.orbitradius < 64:
                        glider.orbitradius = 64
                        glider.orbitangle = 95

        else:
            for glider in igliders:
                if glider.mothership == self:
                    glider.orbitangle = 95
                    if glider.orbitradius < 64:
                        glider.orbitradius = 64

        # increment in x direction
        self.xvel = self.forward * math.sin(math.radians(abs(self.angle)))
        self.yvel = self.forward * math.cos(math.radians(abs(self.angle)))
        self.rect.left += self.xvel
        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air

    def checkdeath(self):
        if self.lives <= 0:
            entities.remove(self)
            illyrians.remove(self)
            ('killed')

        try:
            for projectile in projectiles:
                if pygame.Rect.colliderect(self.rect,projectile.rect):
                    if projectile.owner.mothership != self:
                        self.lives -=1
                        ("player lives: "+str(self.lives))
        except:
            pass


class IllyrianGlider(Entity):
    def __init__(self,projectile,mothership, x, y):
        Entity.__init__(self)
        self.projectile = projectile
        self.mothership = mothership
        self.total_level_width = self.mothership.total_level_width
        self.total_level_height = self.mothership.total_level_height
        self.lives = 1
        self.livestime = 9
        self.time = 0
        self.angle = 0
        self.turn = 0
        self.forward = random.randint(18,25)
        self.xvel = 0
        self.yvel = 0
        self.gravity = True
        self.onGround = False
        self.image = pygame.Surface((8,8))
        self.image.fill(pygame.Color("#0000FF"))
        self.rect = pygame.Rect(x, y, 8, 8)
        self.orbitradius = 64
        self.orbitangle = 90
        self.player = None

    def orbit(self):
        if self.mothership in illyrians:
            if ((((self.mothership.rect.left-self.rect.left)**2)+((self.mothership.rect.top-self.rect.top)**2))**0.5) < self.orbitradius:
                if ((self.mothership.rect.left-self.rect.left > 0) and (self.mothership.rect.top-self.rect.top < 0)):
                    self.turn = -90-self.angle-math.degrees(math.atan2((self.rect.top-self.mothership.rect.top),(self.rect.left-self.mothership.rect.left)))+self.orbitangle
                if ((self.mothership.rect.left-self.rect.left < 0) and (self.mothership.rect.top-self.rect.top > 0)):
                    self.turn = 180-self.angle+(90-(math.degrees(math.atan2((self.rect.top-self.mothership.rect.top),(self.rect.left-self.mothership.rect.left)))))+self.orbitangle
                if ((self.mothership.rect.left-self.rect.left > 0) and (self.mothership.rect.top-self.rect.top > 0)):
                    self.turn = -90-self.angle-math.degrees(math.atan2((self.rect.top-self.mothership.rect.top),(self.rect.left-self.mothership.rect.left)))+self.orbitangle
                if ((self.mothership.rect.left-self.rect.left < 0) and (self.mothership.rect.top-self.rect.top < 0)):
                    self.turn = 180-self.angle+(90-(math.degrees(math.atan2((self.rect.top-self.mothership.rect.top),(self.rect.left-self.mothership.rect.left)))))+self.orbitangle
            else:
                if ((self.mothership.rect.left-self.rect.left > 0) and (self.mothership.rect.top-self.rect.top < 0)):
                    self.turn = -90-self.angle-math.degrees(math.atan2((self.rect.top-self.mothership.rect.top),(self.rect.left-self.mothership.rect.left)))
                if ((self.mothership.rect.left-self.rect.left < 0) and (self.mothership.rect.top-self.rect.top > 0)):
                    self.turn = 180-self.angle+(90-(math.degrees(math.atan2((self.rect.top-self.mothership.rect.top),(self.rect.left-self.mothership.rect.left)))))
                if ((self.mothership.rect.left-self.rect.left > 0) and (self.mothership.rect.top-self.rect.top > 0)):
                    self.turn = -90-self.angle-math.degrees(math.atan2((self.rect.top-self.mothership.rect.top),(self.rect.left-self.mothership.rect.left)))
                if ((self.mothership.rect.left-self.rect.left < 0) and (self.mothership.rect.top-self.rect.top < 0)):
                    self.turn = 180-self.angle+(90-(math.degrees(math.atan2((self.rect.top-self.mothership.rect.top),(self.rect.left-self.mothership.rect.left)))))
        else:
            if ((((self.rect.left-self.projectile.rect.left)**2)+((self.rect.top-self.projectile.rect.top)**2))**0.5) > 350:
                self.projectile.res(self,self)
            if self.player == None or self.player not in illyrians:
                self.player = illyrians[random.randint(0,len(illyrians)-1)]
            if (((((self.player.rect.left-self.rect.left)**2)+((self.player.rect.top-self.rect.top)**2))**0.5) > 200):
                if ((self.player.rect.left-self.rect.left > 0) and (self.player.rect.top-self.rect.top < 0)):
                    self.turn = -90-self.angle-math.degrees(math.atan2((self.rect.top-self.player.rect.top),(self.rect.left-self.player.rect.left)))
                if ((self.player.rect.left-self.rect.left < 0) and (self.player.rect.top-self.rect.top > 0)):
                    self.turn = 180-self.angle+(90-(math.degrees(math.atan2((self.rect.top-self.player.rect.top),(self.rect.left-self.player.rect.left)))))
                if ((self.player.rect.left-self.rect.left > 0) and (self.player.rect.top-self.rect.top > 0)):
                    self.turn = -90-self.angle-math.degrees(math.atan2((self.rect.top-self.player.rect.top),(self.rect.left-self.player.rect.left)))
                if ((self.player.rect.left-self.rect.left < 0) and (self.player.rect.top-self.rect.top < 0)):
                    self.turn = 180-self.angle+(90-(math.degrees(math.atan2((self.rect.top-self.player.rect.top),(self.rect.left-self.player.rect.left)))))

        self.angle += self.turn

    def update(self):

        self.y = self.rect.top
        if self.rect.left > (self.total_level_width):
            self.rect.left = 0
        if self.rect.left < 0:
            self.rect.left = (self.total_level_width)
        if self.y > (self.total_level_height):
            self.rect.top = 0
        if self.y < 0:
            self.rect.top = (self.total_level_height)

        if self.angle > 360:
            self.angle += -360
        if self.angle < 0:
            self.angle += 360

        self.xvel = self.forward * math.sin(math.radians(abs(self.angle)))
        self.yvel = self.forward * math.cos(math.radians(abs(self.angle)))

        self.rect.left += self.xvel
        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air

        try:
            for glider in igliders:
                if glider != self:
                    if pygame.Rect.colliderect(self.rect,glider.rect):
                        self.bumpx = random.randint(-20,20)
                        self.bumpy = random.randint(-20,20)
                        self.rect.left += self.bumpx
                        self.rect.top += self.bumpy
        except:
            pass

        try:
            for projectile in projectiles:
                if pygame.Rect.colliderect(self.rect,projectile.rect):
                    if projectile.owner.mothership != self.mothership:
                        entities.remove(self)
                        igliders.remove(self)
                        entities.remove(self.projectile)
                        projectiles.remove(self.projectile)
        except:
            pass




class Devaris(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.total_level_width = 5000
        self.total_level_height = 3000
        self.lives = 5
        self.livestime = 3
        self.time = 0
        self.angle = 0
        self.forward = 6
        self.xvel = 0
        self.yvel = 0
        self.gravity = True
        self.onGround = False
        self.image = pygame.Surface((8,8))
        self.image.fill(pygame.Color("#00FF00"))
        self.rect = pygame.Rect(x, y, 8, 8)
        self.timer = 0
        self.turn = 0
        self.bumpx = 0
        self.bumpy = 0

    def set_message(self,text):
        try:
            self.message = None
            self.previous_message = None

            self.message = font.render(text,True, cyan)

            self.previous_message = self.message
        except:
            pass
    def update(self,player):

        self.y = self.rect.top
        if self.rect.left > (self.total_level_width):
            self.rect.left = 0
        if self.rect.left < 0:
            self.rect.left = (self.total_level_width)
        if self.y > (self.total_level_height):
            self.rect.top = 0
        if self.y < 0:
            self.rect.top = (self.total_level_height)

        self.shooting = False
        self.shielding = True
        self.forward = 6

        if (((((player.rect.left-self.rect.left)**2)+((player.rect.top-self.rect.top)**2))**0.5) > 200):
            if ((player.rect.left-self.rect.left > 0) and (player.rect.top-self.rect.top < 0)):
                self.turn = -90-self.angle-math.degrees(math.atan2((self.rect.top-player.rect.top),(self.rect.left-player.rect.left)))
            if ((player.rect.left-self.rect.left < 0) and (player.rect.top-self.rect.top > 0)):
                self.turn = 180-self.angle+(90-(math.degrees(math.atan2((self.rect.top-player.rect.top),(self.rect.left-player.rect.left)))))
            if ((player.rect.left-self.rect.left > 0) and (player.rect.top-self.rect.top > 0)):
                self.turn = -90-self.angle-math.degrees(math.atan2((self.rect.top-player.rect.top),(self.rect.left-player.rect.left)))
            if ((player.rect.left-self.rect.left < 0) and (player.rect.top-self.rect.top < 0)):
                self.turn = 180-self.angle+(90-(math.degrees(math.atan2((self.rect.top-player.rect.top),(self.rect.left-player.rect.left)))))

            self.shooting = True
            self.shielding = False

            self.angle += self.turn

        if self.angle > 360:
            self.angle += -360
        if self.angle < 0:
            self.angle += 360

        self.timer += 1
        if self.timer == 100:
            ('glider made')
            pro = Projectile(5,5,100)
            projectiles.append(pro)
            entities.add(pro)
            d = DevarisGlider(pro,self,self.rect.left+random.randint(-16,16),self.rect.top+random.randint(-16,16))
            pro.owner = d
            (pro.owner)
            dgliders.append(d)
            entities.add(d)
            self.timer = 0

        if self.shooting:
            for glider in dgliders:
                if glider.mothership == self:
                    if ((((glider.rect.left-glider.projectile.rect.left)**2)+((glider.rect.top-glider.projectile.rect.top)**2))**0.5) > 350:
                        glider.projectile.res(glider,glider.mothership)
                    else:
                        pass

        if self.shielding:
            for glider in dgliders:
                if glider.mothership == self:
                    if ((((glider.rect.left-glider.projectile.rect.left)**2)+((glider.rect.top-glider.projectile.rect.top)**2))**0.5) > 1800:
                        glider.projectile.res(glider,glider)
                    else:
                        pass


        # increment in x direction
        self.xvel = self.forward * math.sin(math.radians(abs(self.angle)))
        self.yvel = self.forward * math.cos(math.radians(abs(self.angle)))
        self.rect.left += self.xvel
        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air

        try:
            for dev in devaris:
                if dev != self:
                    if pygame.Rect.colliderect(self.rect,dev.rect):
                        self.bumpx = random.randint(-20,20)
                        self.bumpy = random.randint(-20,20)
                        self.rect.left += self.bumpx
                        self.rect.top += self.bumpy
        except:
            pass

    def checkdeath(self):
        try:
            for projectile in projectiles:
                if pygame.Rect.colliderect(self.rect,projectile.rect):
                    if projectile.owner.mothership != self:
                        self.lives -=1
        except:
            pass

        if self.lives <= 0:
            entities.remove(self)
            devaris.remove(self)

class DevarisGlider(Entity):
    def __init__(self,projectile,mothership, x, y):
        Entity.__init__(self)
        self.projectile = projectile
        self.mothership = mothership
        self.total_level_width = self.mothership.total_level_width
        self.total_level_height = self.mothership.total_level_height
        self.lives = 1
        self.livestime = 9
        self.time = 0
        self.angle = 0
        self.forward = random.randint(12,20)
        self.xvel = 0
        self.turn = 0
        self.yvel = 0
        self.gravity = True
        self.onGround = False
        self.image = pygame.Surface((8,8))
        self.image.fill(pygame.Color("#00BB00"))
        self.rect = pygame.Rect(x, y, 8, 8)
        self.orbitradius = 128
        self.orbitangle = 90
        self.player = None

    def orbit(self):
        if self.mothership in devaris:
            if ((((self.mothership.rect.left-self.rect.left)**2)+((self.mothership.rect.top-self.rect.top)**2))**0.5) < self.orbitradius:
                if ((self.mothership.rect.left-self.rect.left > 0) and (self.mothership.rect.top-self.rect.top < 0)):
                    self.turn = -90-self.angle-math.degrees(math.atan2((self.rect.top-self.mothership.rect.top),(self.rect.left-self.mothership.rect.left)))+self.orbitangle
                if ((self.mothership.rect.left-self.rect.left < 0) and (self.mothership.rect.top-self.rect.top > 0)):
                    self.turn = 180-self.angle+(90-(math.degrees(math.atan2((self.rect.top-self.mothership.rect.top),(self.rect.left-self.mothership.rect.left)))))+self.orbitangle
                if ((self.mothership.rect.left-self.rect.left > 0) and (self.mothership.rect.top-self.rect.top > 0)):
                    self.turn = -90-self.angle-math.degrees(math.atan2((self.rect.top-self.mothership.rect.top),(self.rect.left-self.mothership.rect.left)))+self.orbitangle
                if ((self.mothership.rect.left-self.rect.left < 0) and (self.mothership.rect.top-self.rect.top < 0)):
                    self.turn = 180-self.angle+(90-(math.degrees(math.atan2((self.rect.top-self.mothership.rect.top),(self.rect.left-self.mothership.rect.left)))))+self.orbitangle
            else:
                if ((self.mothership.rect.left-self.rect.left > 0) and (self.mothership.rect.top-self.rect.top < 0)):
                    self.turn = -90-self.angle-math.degrees(math.atan2((self.rect.top-self.mothership.rect.top),(self.rect.left-self.mothership.rect.left)))
                if ((self.mothership.rect.left-self.rect.left < 0) and (self.mothership.rect.top-self.rect.top > 0)):
                    self.turn = 180-self.angle+(90-(math.degrees(math.atan2((self.rect.top-self.mothership.rect.top),(self.rect.left-self.mothership.rect.left)))))
                if ((self.mothership.rect.left-self.rect.left > 0) and (self.mothership.rect.top-self.rect.top > 0)):
                    self.turn = -90-self.angle-math.degrees(math.atan2((self.rect.top-self.mothership.rect.top),(self.rect.left-self.mothership.rect.left)))
                if ((self.mothership.rect.left-self.rect.left < 0) and (self.mothership.rect.top-self.rect.top < 0)):
                    self.turn = 180-self.angle+(90-(math.degrees(math.atan2((self.rect.top-self.mothership.rect.top),(self.rect.left-self.mothership.rect.left)))))

        else:
            if ((((self.rect.left-self.projectile.rect.left)**2)+((self.rect.top-self.projectile.rect.top)**2))**0.5) > 350:
                self.projectile.res(self,self)
            if self.player == None or self.player not in illyrians:
                self.player = illyrians[random.randint(0,len(illyrians)-1)]
            if (((((self.player.rect.left-self.rect.left)**2)+((self.player.rect.top-self.rect.top)**2))**0.5) > 200):
                if ((self.player.rect.left-self.rect.left > 0) and (self.player.rect.top-self.rect.top < 0)):
                    self.turn = -90-self.angle-math.degrees(math.atan2((self.rect.top-self.player.rect.top),(self.rect.left-self.player.rect.left)))
                if ((self.player.rect.left-self.rect.left < 0) and (self.player.rect.top-self.rect.top > 0)):
                    self.turn = 180-self.angle+(90-(math.degrees(math.atan2((self.rect.top-self.player.rect.top),(self.rect.left-self.player.rect.left)))))
                if ((self.player.rect.left-self.rect.left > 0) and (self.player.rect.top-self.rect.top > 0)):
                    self.turn = -90-self.angle-math.degrees(math.atan2((self.rect.top-self.player.rect.top),(self.rect.left-self.player.rect.left)))
                if ((self.player.rect.left-self.rect.left < 0) and (self.player.rect.top-self.rect.top < 0)):
                    self.turn = 180-self.angle+(90-(math.degrees(math.atan2((self.rect.top-self.player.rect.top),(self.rect.left-self.player.rect.left)))))

        self.angle += self.turn

    def update(self):

        self.y = self.rect.top
        if self.rect.left > (self.total_level_width):
            self.rect.left = 0
        if self.rect.left < 0:
            self.rect.left = (self.total_level_width)
        if self.y > (self.total_level_height):
            self.rect.top = 0
        if self.y < 0:
            self.rect.top = (self.total_level_height)

        if self.angle > 360:
            self.angle += -360
        if self.angle < 0:
            self.angle += 360

        self.xvel = self.forward * math.sin(math.radians(abs(self.angle)))
        self.yvel = self.forward * math.cos(math.radians(abs(self.angle)))

        self.rect.left += self.xvel
        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air

        try:
            for glider in dgliders:
                if glider != self:
                    if pygame.Rect.colliderect(self.rect,glider.rect):
                        self.bumpx = random.randint(-20,20)
                        self.bumpy = random.randint(-20,20)
                        self.rect.left += self.bumpx
                        self.rect.top += self.bumpy
        except:
            pass
        try:
            for projectile in projectiles:
                if pygame.Rect.colliderect(self.rect,projectile.rect):
                    if projectile.owner.mothership != self.mothership:
                        entities.remove(self)
                        dgliders.remove(self)
                        entities.remove(self.projectile)
                        projectiles.remove(self.projectile)
        except:
            pass





class Star(Entity):
    def __init__(self, x, y,):
        Entity.__init__(self)
        self.image = pygame.Surface((350,350))
        self.image.fill(pygame.Color("#FFFFFF"))
        self.image.convert()
        self.rect = pygame.Rect(x, y, 350, 350)

    def update(self):
        pass


class Projectile(Entity):

    def __init__(self, x, y,velocity):
        Entity.__init__(self)
        self.velocity = 30
        self.xvel = 0
        self.yvel = 0
        self.image = pygame.Surface((4,4))
        self.image.fill(pygame.Color("#FF0000"))
        self.image.convert()
        self.rect = pygame.Rect(x, y, 4, 4)
        self.owner = None

    def place(self,x,y):
        self.rect.left = x
        self.rect.top = y

    def res(self,var,varangle):
        self.rect.left = var.rect.left+16
        self.rect.top = var.rect.top+16
        self.xvel = self.velocity * math.sin(math.radians(abs(varangle.angle)))
        self.yvel = self.velocity * math.cos(math.radians(abs(varangle.angle)))

    def update(self):
        self.rect.left += self.xvel
        self.rect.top += self.yvel

    def collide_update(self):
        pass


class Background(Entity):
    def __init__(self, x, y,image = "#478989"):
        Entity.__init__(self)
        self.color = image
        self.image = pygame.Surface((8, 8))

        self.image.fill(pygame.Color(self.color))

        self.image.convert()
        self.rect = self.image.get_rect()
        try:
            entities.add(self)
        except Exception as e:
            (e)

    def update(self):
        pass

if __name__ == "__main__":
    main()
