class dataPoint():
    def __init__(self, x, y, prevColour):
       self.x = x
       self.y = y
       self.prevColour = prevColour


previousActions = []
previousActions.append(dataPoint(-1,-1,-1))
print(f'x:{previousActions[-1].x} ,y: {previousActions[-1].y}, prevColour: {previousActions[-1].prevColour}')

