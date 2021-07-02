#!/user/bin/env python3
# -*- coding: utf-8 -*-


print("out of complex share variable")
g_v = 1
class Complex:
	x = 100
	print("Complex share variable")


	def __init__(self, realpart, imagpart):
		print("__init__")
		self.r = realpart
		self.i = imagpart

	def printAll(self):
		print("print", self.r, self.i)

class Warehouse:
	test = 200
	print("Warehouse share variable")
	purpose = 'storage'
	region = 'west'

# w1 = Warehouse()
# print(w1.purpose, w1.region)
# w2 = Warehouse()
# w2.region = 'east'
# print(w2.purpose, w2.region)
# print(w1.purpose, w1.region)