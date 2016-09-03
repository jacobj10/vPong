
from visual import *
import random

class Environment():
    def __init__(self):
        self.left_wall = box(color=color.green, pos = [-10,0,0], length=0.5, height=5, width=0.5)
        self.right_wall = box(color=color.green, pos = [10,0,0], length=0.5, height=5, width=0.5)
        self.x_min = self.left_wall.pos.x + self.left_wall.length
        self.x_max = self.right_wall.pos.x - self.right_wall.length
        self.y_min = -10
        self.y_max = 10

class MovingEngine():
    def __init__(self):
        self.p1keys = ['w','s']
        self.p2keys = ['up', 'down']
        self.score = [0,0]
        self.text = text(text="Pong by JJ\nP1: {0}   P2: {1}".format(self.score[0], self.score[1]), align='center', depth=-0.3, color=color.green)
        self.ball = sphere(color=color.green, pos=[0,0,0], radius=0.5)
        self.env = Environment()
        ev = scene.waitfor('keydown')
        self.render_new()

    def render_new(self):
        ball = self.ball
        ball.pos = vector(0,0,0)
        deltaT = 0.01
        xv = 3
        yv = int(random.random() * 10 % 12 - 6)
        if yv == 0:
            yv = 3
        ball.V = vector(xv,yv,0)
        scene.bind('keydown', self.keyInput)
        shutdown_frames = 0
        while shutdown_frames < 25:
            ball.pos = ball.pos + ball.V * deltaT
            if ball.pos.x < self.env.x_min or ball.pos.x > self.env.x_max:
                lHit = (ball.pos.y > self.env.left_wall.pos.y - 2.5 and ball.pos.y < self.env.left_wall.pos.y + 2.5)
                rHit = (ball.pos.y > self.env.right_wall.pos.y - 2.5 and ball.pos.y < self.env.right_wall.pos.y + 2.5)
                if lHit or rHit and shutdown_frames == 0:
                    ball.V.x = -ball.V.x
                else:
                    shutdown_frames += 1
            if ball.pos.y < self.env.y_min or ball.pos.y > self.env.y_max:
                 ball.V.y = -ball.V.y
            rate(500)
        if ball.pos.x > self.env.x_max:
            self.score[0] += 1
        elif ball.pos.x < self.env.x_min:
            self.score[1] += 1
        self.update_score()
        ev = scene.waitfor('keydown')
        self.render_new()
        
    def update_score(self):
        self.text.text = "Pong by JJ\nP1:  {0}   P2:  {1}".format(self.score[0], self.score[1])

    def keyInput(self, evt):
        key = evt.key
        if key in self.p1keys:
            self.handle_motion(key, self.env.left_wall)
        elif key in self.p2keys:
            self.handle_motion(key, self.env.right_wall)

    def handle_motion(self, direction, Obj):
        move = 1 if direction in ['up','w'] else -1
        if Obj.pos.y + move > self.env.y_max - 1 or Obj.pos.y + move < self.env.y_min + 1:
            return
        Obj.pos.y += move

x = MovingEngine()
