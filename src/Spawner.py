import numpy as np
import random
import Body
import math
import pygame as pg

class Spawner:
    def __init__(self, player: Body) -> None:
        self.size = self.newRadius(player) # make the size of the spawner dependent on the mass
        self.currentParticles = 0
        return
    
    def newRadius(self, player: Body):
        return player.radius * 100 + 100

    def spawnParticle(self, player: Body, uid: int) -> Body:
        # spawn a particle within the size, random mass, random x y pos within radius, initial velocity of 0
        # make sure the particle is smaller than the player body mass
        massOfParticle = random.randint(10, int(player.mass / 2))
        minX = int(player.pos[0] - self.size)
        maxX = int(player.pos[0] + self.size)
        
        randX = random.randint(minX, maxX)
        print("maxX:" + str(maxX))
        print("randx"+ str(randX - player.pos[0]))
        minY = int(player.pos[1] - math.sqrt(abs((self.size + player.pos[0]) ** 2 - randX ** 2)))
        maxY = int(player.pos[1] + math.sqrt(abs((self.size + player.pos[0]) ** 2 - randX ** 2)))
        randY = random.randint(minY, maxY)

        # Update size
        self.size = self.newRadius(player)

        return Body.Body(massOfParticle, np.array([float(randX), randY]), np.array([0.0, 0.0]), uid)
