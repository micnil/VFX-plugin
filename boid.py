import maya.cmds as cmds

class Boid():
		
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

	def setPosition(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

	def getPosition():
		return self.x, self.y, self.z

	def move():
		pass