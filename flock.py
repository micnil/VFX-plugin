import maya.cmds as cmds
from boid import Boid
import vectors ; from vectors import *
import random
import math

boids = []
dt=1/100.0

cWeight = 1.0
aWeight = 1.5
sWeight = 2.0

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
			avoidWalls(b)
			b.move(dt)
			b.setKeyFrame(frame)


def run():
	'''run the simulation'''
	nFrames = 2000;
	createBoids(20)
	createKeyFrames(nFrames)

	cmds.playbackOptions(max=nFrames)
	cmds.playbackOptions(aet=nFrames)

	cmds.play()

def alignment(boid):
	'''flocking function'''
	neighborhood = []
	for b in boids:

		if b.getName() == boid.getName():
			continue

		distance = vectors.distance(b.getPosition(), boid.getPosition())

		if distance < boid.neighborhoodRadius:
			neighborhood.append(b.getVelocity())

	if(len(neighborhood) > 0):
		avgVelocity = sum(neighborhood) / len(neighborhood)
		alignmentForce = avgVelocity - boid.getVelocity()
		boid.addForce(alignmentForce * aWeight)

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

		distance = vectors.distance(b.getPosition(), boid.getPosition())

		if distance < boid.neighborhoodRadius:
			neighborhood.append(b.getPosition())

	if(len(neighborhood) > 0):
		centerPoint = sum(neighborhood) / len(neighborhood)
		cohesionForce = centerPoint - boid.getPosition();
		boid.addForce(cohesionForce * cWeight)

def avoidWalls(boid, w = 20, h = 20, d = 20):
	position = boid.getPosition()

	if position[0] > w/2:
		boid.addForce(V(-1.0, 0.0, 0.0))
	elif position[0] < -w/2:
		boid.addForce(V(1.0, 0.0, 0.0))

	if position[1] > h/2:
		boid.addForce(V(0.0, -1.0, 0.0))
	elif position[1] < -h/2:
		boid.addForce(V(0.0, 1.0, 0.0))

	if position[2] > d/2:
		boid.addForce(V(0.0, 0.0, -1.0))
	elif position[2] < -h/2:
		boid.addForce(V(0.0, 0.0, 1.0))