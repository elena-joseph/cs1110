"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game.  Instances of Wave represent a single wave. Whenever
you move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or
models.py. Whether a helper method belongs in this module or models.py is
often a complicated issue.  If you do not know, ask on Piazza and we will
answer.

# Carly Hu (ch862) and Elena Joseph (esj34)
# 12/7/21
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you  should create a NEW instance of
    Wave (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.  This
    class will be similar to than one in how it interacts with the main class
    Invaders.

    All of the attributes of this class ar to be hidden. You may find that
    you want to access an attribute in class Invaders. It is okay if you do,
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter
    and/or setter for any attribute that you need to access in Invaders.
    Only add the getters and setters that you need for Invaders. You can keep
    everything else hidden.

    """
    # HIDDEN ATTRIBUTES:
    # Attribute _ship: the player ship to control
    # Invariant: _ship is a Ship object or None
    #
    # Attribute _aliens: the 2d list of aliens in the wave
    # Invariant: _aliens is a rectangular 2d list containing Alien objects or None
    #
    # Attribute _bolts: the laser bolts currently on screen
    # Invariant: _bolts is a list of Bolt objects, possibly empty
    #
    # Attribute _dline: the defensive line being protected
    # Invariant : _dline is a GPath object
    #
    # Attribute _lives: the number of lives left
    # Invariant: _lives is an int >= 0
    #
    # Attribute _time: the amount of time since the last Alien "step"
    # Invariant: _time is a float >= 0s
    #
    # You may change any attribute above, as long as you update the invariant
    # You may also add any new attributes as long as you document them.
    #
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    # Attribute _right_mov: whether aliens are moving right or left.
    # Invariant: _right_mov is a boolean
    #
    # Attribute _last: the number of keys pressed last frame
    # Invariant: _last is an int >= 0
    #
    # Attribute _rate: the number of alien steps taken between bolts
    # Invariant: _rate is an int between 1 and BOLT_RATE
    #
    # Attribute _step: the number of alien steps taken
    # Invariant: _step is an int >= 0
    #
    # Attribute _animator: the animation coroutine.
    # Invariant: _animator is either None or a coroutine
    #
    # Attribute _dead: whether the ship is dead or not
    # Invariant: _dead is a boolean
    #
    # Attribute _dipped: if an alien has dipped below the defense line
    # Invariant: _dipped is a boolean
    #
    # Attribute _win: if the player has won the game
    # Invariant: _win is a boolean


    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    def getDead(self):
        """
        Returns True if the ship is dead, due to getting shot by the aliens.
        """
        return self._dead

    def getLives(self):
        """
        Returns the amount of lives left to play until the game ends.
        """
        return self._lives

    def getWin(self):
        """
        Returns True if the player had won the game.
        """
        return self._win

    def getDipped(self):
        """
        Returns True if the alien has dipped below the defense line.
        """
        return self._dipped

    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS

    def __init__(self):
        """
        Initializes aliens, ship, and defense line.
        """
        self.alien_init()
        self._ship = Ship()
        self._dline = GPath(points=[0, DEFENSE_LINE, GAME_WIDTH, DEFENSE_LINE],\
            linewidth = 2, linecolor = 'dark grey')

        self._time = 0
        self._right_mov = True
        self._bolts = []
        self._last = 0
        self._rate = random.randint(1, BOLT_RATE)
        self._step = 0
        self._animator = None
        self._dead = False
        self._lives = 3
        self._dipped = False
        self._win = False


    #HELPER METHOD FOR CREATING ALIEN
    def alien_init(self):
        """
        A wave of aliens is created with the image alternating every two rows.
        """
        width = ALIEN_WIDTH
        height = ALIEN_HEIGHT
        y = GAME_HEIGHT-ALIEN_CEILING - (ALIEN_HEIGHT/2)

        self._aliens = []
        for rownum in range(ALIEN_ROWS):
            row = []
            x = ALIEN_H_SEP + (ALIEN_WIDTH/2)
            if rownum % 6 == 5 or rownum % 6 == 0:
                source = 'alien3.png'
            elif rownum % 6 == 3 or rownum % 6 == 4:
                source = 'alien1.png'
            elif rownum % 6 == 1 or rownum % 6 == 2:
                source= 'alien2.png'
            for alien in range(ALIENS_IN_ROW):
                x = x + ALIEN_WIDTH + ALIEN_H_SEP
                row.append(Alien(x, y, source))
            self._aliens.append(row)
            y = y - ALIEN_HEIGHT - ALIEN_V_SEP

    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self, input, dt):
        """
        Moves the ship, aliens and laser bolts as necessary.

        Parameter input: The user keyboard input
        Precondition: Input is a GInput object

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        self.movealiens(dt)
        self.shipbolt(input)
        self.alienbolt(dt)
        self.movebolts()
        self.collisionupdate(dt)
        self.respawn(input)
        self.runanimator(dt,input)
        self.death(input)

    # HELPER METHODS BELOW
    def movealiens(self, dt):
        """
        Moves the wave of aliens across the screen in the pattern of right, down,
        and left movements from the top of the window screen until the defense
        line.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        if self._time > ALIEN_SPEED:
            for row in self._aliens:
                for alien in row:
                    if alien != None:
                        if self._right_mov:
                            alien.x = alien.x + ALIEN_H_WALK
                        else:
                            alien.x = alien.x - ALIEN_H_WALK
            self._time = 0
            self._step = self._step + 1
        self._time = self._time + dt

        self.down()

    def down(self):
        """
        Handles the downward alien step and the step to turn back around.
        """

        for row in self._aliens:
            for alien in row:
                if alien != None:
                    if GAME_WIDTH - alien.right < ALIEN_H_SEP:
                        self._right_mov = False
                        rightdist = GAME_WIDTH - alien.right
                        distance = ALIEN_H_SEP - rightdist
                        for row in self._aliens:
                            for alien in row:
                                if alien != None:
                                    alien.y = alien.y - ALIEN_V_WALK
                                    alien.right = alien.right - distance
                    elif alien.left < ALIEN_H_SEP:
                        leftdist = alien.left
                        distance = ALIEN_H_SEP - leftdist
                        for row in self._aliens:
                            for alien in row:
                                if alien != None:
                                    alien.y = alien.y - ALIEN_V_WALK
                                    alien.left = alien.left + distance
                        self._right_mov = True

    def shipbolt(self, input):
        """
        Handles the creation of a bolt shot by the ship, triggered by the player
        clicking the spacebar.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        pewSound = Sound('pew1.wav')

        if self._ship != None:
            x = self._ship.x
            y = SHIP_HEIGHT + SHIP_BOTTOM
            velocity = BOLT_SPEED
            exists = False

        if input.is_key_down('spacebar') and self._last == 0:
            for bolt in self._bolts:
                if bolt.isPlayerBolt():
                    exists = True
            if not exists:
                self._bolts.append(Bolt(x,y,velocity))
                pewSound.play()
                exists = True
        self._last = input.is_key_down('spacebar')

    def alienbolt(self, dt):
        """
        Handles the creation of a bolt shot by a randomly selected alien. A
        bolt is shot after a random number of steps after the last bolt.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        column = random.randint(0, ALIENS_IN_ROW-1)
        velocity = -BOLT_SPEED

        minbottom = GAME_HEIGHT
        bottom = GAME_HEIGHT
        shootalien = 0
        for row in self._aliens:
            if row != None and row[column] != None:
                shootalien = row[column]
                bottom = shootalien.bottom
        if bottom != None:
            minbottom = min(minbottom,bottom)

        x = 0
        y = 0
        for row in self._aliens:
            for alien in row:
                if alien != None:
                    if alien == shootalien:
                        x = alien.x
                        y = alien.y - ALIEN_HEIGHT/2

        if self._step == self._rate:
            self._bolts.append(Bolt(x,y,velocity))
            self._rate = random.randint(1, BOLT_RATE)
            self._step = 0

    def movebolts(self):
        """
        Handles the movement of a bolt shot by either an alien or ship, and
        removes the bolt once it leaves the screen.
        """
        for bolt in self._bolts:
            bolt.y = bolt.y + bolt.getVelocity()
            if bolt.bottom > GAME_HEIGHT:
                self._bolts.remove(bolt)
                exists = False
            if bolt.top < 0:
                self._bolts.remove(bolt)

    def collisionupdate(self,dt):
        """
        Removes the object, the respective ship or alien, hit by the bolt

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        for bolt in self._bolts:
            for row in self._aliens:
                for alien in row:
                    if alien != None:
                        if alien.collides(bolt):
                            column = row.index(alien)
                            row[column] = None
                            self._bolts.remove(bolt)
        for bolt in self._bolts:
            if self._ship != None:
                if self._ship.collides(bolt):
                    self._bolts.remove(bolt)
                    self._animator = self._ship.animates(dt)
                    next(self._animator)

    def respawn(self,input):
        """
        Respawns ship and resumes game if the player presses r
        """
        if input.is_key_down('r'):
            self._dead = False
            self._ship = Ship()

    def runanimator(self, dt, input):
        """
        The driver for the animation coroutine

        Parameter dt: The number of seconds since the last animation frame
        Precondition: dt is an number >= 0
        """
        if not self._animator is None:
            try:
                self._animator.send(dt)
            except:
                self._animator = None
                self._ship = None
                for bolt in self._bolts:
                    self._bolts.remove(bolt)
                self._dead = True
        else:
            if self._ship != None:
                self._ship.moveship(input)
            self.shipbolt(input)

    def death(self, input):
        """
        Handles scenarios involving the ship's death (counting lives left), ship win
        (all aliens destroyed), or ship loss (alien dips below line).
        """
        # Count lives
        if self._dead == True:
            self._lives -= 1

        # Check for win (all aliens gone)
        win = True
        for row in self._aliens:
            for alien in row:
                if alien != None:
                    win = False
        if win == True:
            self._win = True

        # Check for loss (alien below line)
        for row in self._aliens:
            for alien in row:
                if alien != None:
                    if alien.bottom < DEFENSE_LINE:
                        self._dipped = True

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self, view):
        """
        Draws the ship, aliens, defensive line, and bolts as neccesary.

        Parameter view: The view window
        Precondition: view is a GView object
        """
        for row in self._aliens:
             for alien in row:
                 if alien != None:
                     alien.draw(view)

        if self._ship != None:
            self._ship.draw(view)
        self._dline.draw(view)

        for bolt in self._bolts:
            if bolt != None:
                bolt.draw(view)

    # HELPER METHODS FOR COLLISION DETECTION
