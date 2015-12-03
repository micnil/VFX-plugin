import maya.cmds as cmds
from boid import Boid
import vectors ; from vectors import *
import random
import math

boids = []
dt=1/100.0

cWeight = 5
aWeight = 5
sWeight = 5

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
		b = boids.pop()
		b.delete()

def createKeyFrames(numFrames):
	'''create the keyframes for the animation'''
	for frame in range(numFrames):
		cmds.currentTime( frame, edit=True )
		for b in boids:
			alignment(b)
			separation(b)
			cohesion(b)
			b.move(dt)
			b.setKeyFrame(frame)


def run():
	'''run the simulation'''
	nFrames = 5000;
	createBoids(5)
	createKeyFrames(nFrames)

	cmds.playbackOptions(max=nFrames)
	cmds.playbackOptions(aet=nFrames)

	cmds.play()

def alignment(boid):
	'''flocking function'''
	#c = [0,0,0]
	neighborhood = []
	for b in boids:

		if b.getName() == boid.getName():
			continue
			#c+= b.getPosition
		distVector = b.getPosition() - boid.getPosition()
		distance = distVector.magnitude()
		if distance < boid.neighborhoodRadius:
			neighborhood.append(b.getVelocity())
		#c /= len(boids) -1
	if(len(neighborhood) > 0):
		avgVelocity = sum(neighborhood) / len(neighborhood)
		alignmentForce = avgVelocity - boid.getVelocity()
		boid.addForce(alignmentForce * aWeight)

	#boid.addForce((c - b.getPosition)/100)

def separation(boid):
	'''flocking function'''
	neighborhood = []
	for b in boids:
		if b.getName() == boid.getName():
			continue
		distVector = b.getPosition() - boid.getPosition()
		distance = distVector.magnitude()
		if distance < boid.neighborhoodRadius:
			neighborhood.append(distVector)

	if(len(neighborhood) > 0):
		separationForce = (sum(neighborhood) / len(neighborhood)) * V(-1, -1, -1)
		boid.addForce(separationForce * sWeight)

def cohesion(boid):

	'''flocking function'''
	neighborhood = []
	for b in boids:
		if b.getName() == boid.getName():
			continue
		distVector = b.getPosition() - boid.getPosition()
		distance = distVector.magnitude()
		if distance < boid.neighborhoodRadius:
			neighborhood.append(b.getPosition())

	if(len(neighborhood) > 0):
		centerPoint = sum(neighborhood) / len(neighborhood)
		cohesionForce = centerPoint - boid.getPosition();
		boid.addForce(cohesionForce * cWeight)


