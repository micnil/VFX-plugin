import maya.cmds as cmds

class Boid():
		
	_velocity = [0,0,0]
	_object = ""
	_position = [0,0,0]
	_name = ""
	_keyframe = []
	
	def __init__(self, n):
		self._object = cmds.polyCone(name = n)
		_name = n
	

	def setPosition(self, x, y, z):
		self._position = [x, y, z]

	def getPosition():
		return self._position

	def move(self, dt):
		self._position = self._velocity*dt
		
	def addVelocity(self, vel):
		self._velocity += vel
		
	def setKeyFrame(self, t):
		cmds.setKeyFrame(self._object, time = t, v = self._position[0], at = "translateX")
		cmds.setKeyFrame(self._object, time = t, v = self._position[1], at = "translateY")
		cmds.setKeyFrame(self._object, time = t, v = self._position[2], at = "translateZ")
		
	def delete(self):
		cmds.delete(at = self._name)