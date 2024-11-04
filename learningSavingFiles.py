import json

class matrixManagement:
    def __init__(self):
        self.matrix = [[1] * 20 for _ in range(10)]

    def saveMatrixToJson(self, filePath):
        with open(filePath, 'w') as file:
            json.dump(self.matrix, file, indent=None)

    def loadMatrixFromJson(self, filePath):
        with open(filePath, 'r') as file:
            self.matrix = json.load(file)
        print('loaded Matrix')
        return self.matrix
    
manager = matrixManagement()
manager.saveMatrixToJson('matrixdata.json')
manager.matrix[0][0] = 0
print(manager.matrix)
print(manager.loadMatrixFromJson('matrixdata.json'))
print(manager.matrix[0][0])