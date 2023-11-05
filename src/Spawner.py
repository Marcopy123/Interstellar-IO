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
        return player.radius * 20 + 100

    def spawnParticle(self, player: Body, uid: int) -> Body:
        # spawn a particle within the size, random mass, random x y pos within radius, initial velocity of 0
        # make sure the particle is smaller than the player body mass

        massAlgorithm = random.random()
        if massAlgorithm < 0.1:
            massOfParticle = random.randint(int(player.mass/20), int(player.mass/10))
        elif massAlgorithm < 0.15:
            massOfParticle = random.randint(int(player.mass/30), int(player.mass/10))
        else:
            massOfParticle = random.randint(10, int(6 * math.sqrt(player.mass)))

        minX = int(player.pos[0] - self.size)
        maxX = int(player.pos[0] + self.size)
        randX = random.randint(minX + 1, maxX - 1)

        yPos = math.sqrt(self.size**2 - (player.pos[0] - randX)**2)
        randY = player.pos[1] + random.choice([yPos, -yPos])

        # Update size
        self.size = self.newRadius(player)

        return Body.Body(massOfParticle, np.array([float(randX + random.random() * 50), float(randY + random.random() * 50)]), np.array([0.0, 0.0]), uid)
