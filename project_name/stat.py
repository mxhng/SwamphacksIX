class Statistic(object):

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

    def calcAverage(self):
        i = 1
        for i in range (6):
            self.avg += self.data[i] * i
        self.avg /= (self.total - self.data[unknown])
        return self.avg

    def add(self, input):
        if (input >= 0 and input < 6):
            self.data[input] += 1
            self.total += 1