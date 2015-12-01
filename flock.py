import maya.cmds as cmds
from boid import Boid
from vectors import *
import random
import math

boids = []
dt=1/100.0

def createBoids(numBoids):
	'''create numboids boids and randomize position'''
	for i in range(numBoids):
		b = Boid("boid{0}".format(i))
		x = random.uniform(-5, 5);
		y = random.uniform(-5, 5);
		z = random.uniform(-5, 5);
		b.setPosition(x, y, z)
		boids.append(b)

	print 'creating boids done'

def clear():
	'''cleanup'''
	while boids:
		print boid._name
		b = boids.pop()
		b.delete()

def createKeyFrames(numFrames):
	'''create the keyframes for the animation'''
	for frame in range(numFrames):
		cmds.currentTime( frame, edit=True )
		for b in boids:
			# example force (just until we get the boid rules right)
			b.addForce(V(-1.0, math.sin(math.radians(frame)), 0.5))
			b.move(dt)
			b.setKeyFrame(frame)


def run():
	'''run the simulation'''
	nFrames = 500;
	createBoids(3)
	createKeyFrames(nFrames)

	cmds.playbackOptions(max=nFrames)
	cmds.playbackOptions(aet=nFrames)

	cmds.play()

def alignment():
	'''flocking function'''
	pass
def separation():
	'''flocking function'''
	pass
def cohesion():
	'''flocking function'''
	pass


