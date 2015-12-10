import maya.cmds as cmds
from boid import Boid
from boundary import Boundary
import vectors ; from vectors import *
import random
import math

boids = []
boundary = Boundary()
dt=1/100.0

cWeight = 1.0
aWeight = 1.0
sWeight = 2.0

def createBoids(numBoids):
	'''create numboids boids and randomize position'''
	boundaryPos = boundary.getPosition()
	boundaryDim = boundary.getSpawnDimensions()
	for i in range(numBoids):
		b = Boid("boid{0}".format(i))

		x = random.uniform(boundaryPos[0]-boundaryDim[0]/2 , boundaryPos[0]+boundaryDim[0]/2)
		y = random.uniform(boundaryPos[1]-boundaryDim[1]/2 , boundaryPos[1]+boundaryDim[1]/2)
		z = random.uniform(boundaryPos[2]-boundaryDim[2]/2 , boundaryPos[2]+boundaryDim[2]/2)
		b.setPosition(x, y, z)
		boids.append(b)

	print 'creating boids done'

def clear():
	'''cleanup'''
	while boids:
		b = boids.pop()
		b.delete()

def createKeyFrames(numFrames, boundary):
	'''create the keyframes for the animation'''
	for frame in range(numFrames):
		cmds.currentTime( frame, edit=True )
		for b in boids:
			alignment(b)
			separation(b)
			cohesion(b)
			followPath(b)
			avoidWalls(b)
			b.move(dt)
			b.setKeyFrame(frame)


def run():
	'''run the simulation'''
	nFrames = 2000

	boundary.setFromName('boundary')
	createBoids(20)
	createKeyFrames(nFrames, boundary)

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
	boundaryTranslation = (0, 0, 0)
	if cmds.objExists("boundary"):
		boundaryTranslation = cmds.getAttr("boundary.translate")[0]
		boundaryScale = cmds.getAttr("boundary.scale")[0]
		w = cmds.polyCube("boundary", query=True, width=True) * boundaryScale[0]
		h = cmds.polyCube("boundary", query=True, height=True) * boundaryScale[1]
		d = cmds.polyCube("boundary", query=True, depth=True) * boundaryScale[2]


	if position[0] > boundaryTranslation[0] + w/2:
		boid.addForce(V(-2.0, 0.0, 0.0))
	elif position[0] < boundaryTranslation[0] - w/2:
		boid.addForce(V(2.0, 0.0, 0.0))

	if position[1] > boundaryTranslation[1] + h/2:
		boid.addForce(V(0.0, -2.0, 0.0))
	elif position[1] < boundaryTranslation[1] - h/2:
		boid.addForce(V(0.0, 2.0, 0.0))

	if position[2] > boundaryTranslation[2] + d/2:
		boid.addForce(V(0.0, 0.0, -2.0))
	elif position[2] < boundaryTranslation[2] - h/2:
		boid.addForce(V(0.0, 0.0, 2.0))
		
def followPath(boid):
	if cmds.objExists("locator"):
		pathPoint = cmds.getAttr("locator.translate")[0]
		for b in boids:
			seekForce = V(pathPoint) - b.getPosition()
			b.addForce(seekForce)
			
		#boid.addForce(cohesionForce * cWeight)

