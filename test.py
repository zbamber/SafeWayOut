import timeit

# Constants used in the simulation
WALKING_PACE = 1.4
DISTANCE_BETWEEN_PEOPLE = 0.6
PEOPLE_PER_METRE = 2
PEOPLE_PER_SECOND_PER_METRE = WALKING_PACE * PEOPLE_PER_METRE / DISTANCE_BETWEEN_PEOPLE

def calculateRequiredWidth(totalPeople, timeValue):
    desiredFlow = totalPeople / timeValue
    return desiredFlow / PEOPLE_PER_SECOND_PER_METRE

# Time slider simulation value (for example, 5 seconds)
timeValue = 5

def testSmall():
    return calculateRequiredWidth(300, timeValue)

def testHuge():
    return calculateRequiredWidth(8_000_000_000, timeValue)

runs = 100
small_times = [timeit.timeit('testSmall()', globals=globals(), number=1000000) for _ in range(runs)]
huge_times = [timeit.timeit('testHuge()', globals=globals(), number=1000000) for _ in range(runs)]

avgSmall = sum(small_times) / runs
avgHuge = sum(huge_times) / runs

print(f"Average time for small capacity (300 people): {avgSmall} seconds")
print(f"Average time for huge capacity (8 billion people): {avgHuge} seconds")
