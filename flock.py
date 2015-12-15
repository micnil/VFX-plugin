import maya.cmds as cmds
from boid import Boid
from boundary import Boundary
from obstacle import Obstacle
import vectors ; from vectors import *
import random
import math
import os.path
import sys

boids = []
obstacles = []
boundary = Boundary()
dt=1/100.0

cWeight = 1.0
aWeight = 2.0
sWeight = 2.0
oWeight = 5.0
pWeight = 1.0

def createBoids(numBoids):
	'''create numboids boids and randomize position'''
	boundaryPos = boundary.getPosition()
	boundaryDim = boundary.getSpawnDimensions()
	for i in range(numBoids):
		b = Boid("boid{0}".format(i))
		x = random.uniform(boundaryPos[0]-boundaryDim[0]/2, boundaryPos[0]+boundaryDim[0]/2)
		y = random.uniform(boundaryPos[1]-boundaryDim[1]/2, boundaryPos[1]+boundaryDim[1]/2)
		z = random.uniform(boundaryPos[2]-boundaryDim[2]/2, boundaryPos[2]+boundaryDim[2]/2)
		b.setPosition(x, y, z)
		boids.append(b)

	print 'creating boids done'

def createObstacles():
	obstacleNames = cmds.ls("obstacle*", transforms = True)
	for obstacleName in obstacleNames:
		obstacle = Obstacle(obstacleName)
		obstacles.append(obstacle)

def clear():
	'''cleanup'''
	cmds.select(cmds.ls("boid*"), r=True)
	cmds.delete()
	while boids:
		b = boids.pop()
		b.delete()
	while obstacles:
		o = obstacles.pop()
		o.delete()

def createKeyFrames(numFrames, boundary):
	'''create the keyframes for the animation'''
	for frame in range(numFrames):
		cmds.currentTime( frame, edit=True )
		for b in boids:

			# How to stop a running maya script:
			# When a script is running in maya, Everything
			# freezes and maya does not repond to input.
			# To get around this maya has to be stopped from
			# the outside. This if-statement looks for a empty file
			# named "stop.maya" anywhere you want in your filesystem.
			# If it is found, maya exits the script. To stop a script,
			# just add this file to your defined path and it exits. When
			# you want to start the script again, just rename it to something
			# else, eg: run.maya.
			if os.path.isfile('C:\\dev\\stop.maya'):
				sys.exit()

			neighborhood = getNeighborhood(b)
			alignment(b, neighborhood)
			separation(b, neighborhood)
			cohesion(b, neighborhood)
			boundary.avoidWalls(b)
			followPath(b)
			obstacleAvoidance(b)
			wander(b)
			b.move(dt)
			b.setKeyFrame(frame)

def limit(v, limit):
	#clamp vector if it exceeds magnitude limit.
	if (v.magnitude() > limit):
		v = v.magnitude(limit)

	return v;

def getNeighborhood(boid):
	neighborhood = []
	for b in boids:

		if b.getName() == boid.getName():
			continue

		distance = vectors.distance(b.getPosition(), boid.getPosition())
		if distance < boid.neighborhoodRadius:
			neighborhood.append(b)

	return neighborhood

def alignment(boid, neighborhood):
	'''flocking function'''
	velocities = []
	for b in neighborhood:
		velocities.append(b.getVelocity())

	if(len(neighborhood) > 0):
		avgVelocity = sum(velocities) / len(neighborhood)
		alignmentForce = avgVelocity.magnitude(boid._maxSpeed) - boid.getVelocity()
		alignmentForce = limit(alignmentForce * aWeight, 2.0)
		boid.addForce(alignmentForce)

def separation(boid, neighborhood):
	'''flocking function'''
	distances = []
	for b in neighborhood:
		distVector = boid.getPosition() - b.getPosition()
		distances.append(distVector)

	if(len(neighborhood) > 0):
		separationForce = (sum(distances) / len(neighborhood))
		separationForce = limit(separationForce * sWeight, 2.3)
		boid.addForce(separationForce)

def cohesion(boid, neighborhood):
	'''flocking function'''
	positions = []
	for b in neighborhood:
		positions.append(b.getPosition())

	if(len(neighborhood) > 0):
		centerPoint = sum(positions) / len(neighborhood)
		cohesionForce = centerPoint - boid.getPosition();
		cohesionForce = limit(cohesionForce * cWeight, 2.0)
		boid.addForce(cohesionForce)

def followPath(boid):
	if cmds.objExists("locator"):
		pathPoint = cmds.getAttr("locator.translate")[0]
		seekForce = V(pathPoint) - boid.getPosition()
		boid.addForce(seekForce * pWeight)
		seekForce = limit(seekForce, 3)
		

def wander(boid):
	velocity = boid.getVelocity()
	sphereCenter = boid.getPosition() + velocity.magnitude(3)

	randomVector = V.random()
	while randomVector ==  boid.wanderVector:
		randomVector = V.random()
	rotationAxis = boid.wanderVector.cross(randomVector)

	rotationAngle = random.uniform(-1, 1) * vectors.radians(5)
	rotatedVector = M.rotate(rotationAxis, rotationAngle) * boid.wanderVector
	boid.wanderVector = V(rotatedVector[0], rotatedVector[1], rotatedVector[2])
	wanderForce = (sphereCenter + boid.wanderVector) - boid.getPosition()
	limit(wanderForce, 1.0)
	boid.addForce(wanderForce)

# def obstacleAvoidance(boid):

# 	if cmds.objExists("pCylinderShape*"):
# 		objPos = V(cmds.getAttr("pCylinder1.translate")[0])

# 		avoidanceForce = oWeight * -(objPos - boid.getPosition())

# 		if(objPos.distance(boid.getPosition()) < 2.0):
# 			print avoidanceForce
# 			boid.addForce(avoidanceForce)
def obstacleAvoidance(boid):
	position = boid.getPosition()
	ahead = position + boid.getVelocity()
	ahead2 = ahead * 0.5
	closestObstacle = None

	#find closest obstacle
	for obstacle in obstacles:
		intersects1 = obstacle.intersects(ahead)
		intersects2 = obstacle.intersects(ahead2)
		if(intersects1 or intersects2):
			distance = obstacle.distanceFrom(boid.getPosition())
			if(closestObstacle is None or closestObstacle.distanceFrom(boid.getPosition()) > distance):
				closestObstacle = obstacle

	if closestObstacle is not None:
		avoidanceForce = obstacle.orthoProject(ahead) * (-1)
		avoidanceForce = limit(avoidanceForce, 6)
		avoidanceForce *= oWeight
		boid.addForce(avoidanceForce)



def run():
	'''run the simulation'''
	nFrames = 2000

	boundary.setFromName('boundary')
	createBoids(40)
	createObstacles()
	createKeyFrames(nFrames, boundary)

	cmds.playbackOptions(max=nFrames)
	cmds.playbackOptions(aet=nFrames)


	cmds.play()
