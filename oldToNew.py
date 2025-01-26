import json
newFilePath = 'convertedSitePlan.json'
originalFilePath = 'SitePlan.json'
newMatrix = [[{'base': 1} for _ in range(120)] for _ in range(80)]
with open(originalFilePath, 'r') as file:
    oldMatrix = json.load(file)

for y in range(len(oldMatrix)):
            for x in range(len(oldMatrix[y])):
                newMatrix[y][x]['base'] = oldMatrix[y][x]

with open(newFilePath, 'w') as file:
    json.dump(newMatrix, file, indent=None)
