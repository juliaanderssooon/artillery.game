from gamemodel import *
from graphics import *

class GameGraphics:
    def __init__(self, game):
        self.game = game

        self.win = GraphWin("Cannon game" , 640, 480, autoflush=False)
        self.win.setCoords(-110, -10, 110, 155)

        p1 = Point(-110, 0)
        p2 = Point(110, 0)

        line = Line(p1, p2)
        line.draw(self.win)

        self.draw_cannons = [self.drawCanon(0), self.drawCanon(1)]
        self.draw_scores  = [self.drawScore(0), self.drawScore(1)]
        self.draw_projs   = [None, None]

    def drawCanon(self,playerNr):

        players = self.game.getPlayers()
        player = players[playerNr]

        player_xPos = player.getX()

        cannonSize = self.game.getCannonSize()

        p1 = Point(0, 0)
        p2 = Point(cannonSize, cannonSize)

        cannon = Rectangle(p1, p2)

        cannon.setFill(player.getColor())
        cannon.move(player_xPos - cannonSize/2, 0)

        cannon.draw(self.win)

        return cannon

    def drawScore(self,playerNr):
        players = self.game.getPlayers()
        player = players[playerNr]
        x = player.getX()
        score = Text(Point(x, -5), f"Score: {player.getScore()}" )

        score.draw(self.win)
        return score

    def fire(self, angle, vel):
        playerNr = self.game.getCurrentPlayerNumber()
        player = self.game.getCurrentPlayer()

        if self.draw_projs[playerNr] != None:
            self.draw_projs[playerNr].undraw()

        proj = player.fire(angle, vel)

        ballRadius = (self.game.getBallSize())/2

        circle_X = proj.getX()
        circle_Y = proj.getY()

        circle = Circle(Point(circle_X, circle_Y), ballRadius)

        self.draw_projs[playerNr] = circle.draw(self.win)

        while proj.isMoving():
            proj.update(1/50)

            circle.move(proj.getX() - circle_X, proj.getY() - circle_Y)

            circle_X = proj.getX()
            circle_Y = proj.getY()

            update(50)

        return proj

    def updateScore(self,playerNr):
        self.draw_scores[playerNr].undraw()
        self.draw_scores[playerNr] = self.drawScore(playerNr)
        return self.draw_scores[playerNr]

    def explode(self):
        other_player = self.game.getOtherPlayer()
        current_player = self.game.getCurrentPlayer()
        cannonSize = self.game.getCannonSize()
        ballSize = self.game.getBallSize()
        x = other_player.getX()
        color = current_player.getColor()

        explosion = Circle(Point(x, 0), ballSize)
        increased_size = ballSize

        while increased_size <= 2*cannonSize:
            explosion = Circle(Point(x, 0), increased_size)
            explosion.setFill(color)
            explosion.draw(self.win)
            update(50)
            explosion.undraw()
            increased_size += 1

    def play(self):
        while True:
            player = self.game.getCurrentPlayer()
            oldAngle,oldVel = player.getAim()
            wind = self.game.getCurrentWind()

            inp = InputDialog(oldAngle,oldVel,wind)
            if inp.interact() == "Fire!": 
                angle, vel = inp.getValues()
                inp.close()
            elif inp.interact() == "Quit":
                exit()
            
            player = self.game.getCurrentPlayer()
            other = self.game.getOtherPlayer()
            proj = self.fire(angle, vel)
            distance = other.projectileDistance(proj)

            if distance == 0.0:
                player.increaseScore()
                self.explode()
                self.updateScore(self.game.getCurrentPlayerNumber())
                self.game.newRound()

            self.game.nextPlayer()


class InputDialog:
    def __init__ (self, angle, vel, wind):
        self.win = win = GraphWin("Fire", 200, 300)
        win.setCoords(0,4.5,4,.5)
        Text(Point(1,1), "Angle").draw(win)
        self.angle = Entry(Point(3,1), 5).draw(win)
        self.angle.setText(str(angle))
        
        Text(Point(1,2), "Velocity").draw(win)
        self.vel = Entry(Point(3,2), 5).draw(win)
        self.vel.setText(str(vel))
        
        Text(Point(1,3), "Wind").draw(win)
        self.height = Text(Point(3,3), 5).draw(win)
        self.height.setText("{0:.2f}".format(wind))
        
        self.fire = Button(win, Point(1,4), 1.25, .5, "Fire!")
        self.fire.activate()
        self.quit = Button(win, Point(3,4), 1.25, .5, "Quit")
        self.quit.activate()

    def interact(self):
        while True:
            pt = self.win.getMouse()
            if self.quit.clicked(pt):
                return "Quit"
            if self.fire.clicked(pt):
                return "Fire!"

    def getValues(self):
        a = float(self.angle.getText())
        v = float(self.vel.getText())
        return a,v

    def close(self):
        self.win.close()


class Button:

    def __init__(self, win, center, width, height, label):

        w,h = width/2.0, height/2.0
        x,y = center.getX(), center.getY()
        self.xmax, self.xmin = x+w, x-w
        self.ymax, self.ymin = y+h, y-h
        p1 = Point(self.xmin, self.ymin)
        p2 = Point(self.xmax, self.ymax)
        self.rect = Rectangle(p1,p2)
        self.rect.setFill('lightgray')
        self.rect.draw(win)
        self.label = Text(center, label)
        self.label.draw(win)
        self.deactivate()

    def clicked(self, p):
        return self.active and \
               self.xmin <= p.getX() <= self.xmax and \
               self.ymin <= p.getY() <= self.ymax

    def getLabel(self):
        return self.label.getText()

    def activate(self):
        self.label.setFill('black')
        self.rect.setWidth(2)
        self.active = 1

    def deactivate(self):
        self.label.setFill('darkgrey')
        self.rect.setWidth(1)
        self.active = 0


GameGraphics(Game(11,3)).play()
