class Stat:

	vLikely = 5
	likely = 4
	possible = 3
	unlikely = 2
	vUnlikely = 1
	unknown = 0

	def __init__ (self):
		self.data = [0,0,0,0,0,0]
		self.total = 0;
		self.avg = 0;

	def calcAverage():
		i = 1
		for i in range 6:
			avg += data[i] * i
		avg /= (total - data[unknown])

	def add(input):
		if (input >= 0 and input < 6):
			data[input] += 1
			total += 1


