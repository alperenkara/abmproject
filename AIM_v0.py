from random import randint
import time
import math


class Vehicle:
    def __init__(self, idno, value):
        self.directions = ["N", "S", "E", "W"]
        self.idno = idno
        self.travelDirection = self.directions[randint(0, 3)]
        self.speed = 20     # meters/sec
        self.distanceFromIntersection = 100     # meters
        self.isActive = True
        self.canPass = True
        self.value = value
        self.timeThroughIntersection = 0
        self.madeItThrough = False

    def adjustSpeed(self, value):
        self.speed += value

    def adjustDistanceFromIntersection(self, timePassed):
        self.distanceFromIntersection -= (self.speed * timePassed)
        # distance between intersections 100m
        if self.distanceFromIntersection < -100:
            self.isActive = False

    def checkIfThroughIntersection(self, currentTime):
        if self.distanceFromIntersection <= 0 and self.madeItThrough == False:
            self.timeThroughIntersection = currentTime - self.idno
            self.madeItThrough = True
    # useful info for the collision time
    def printVehicleData(self):
        print("Vehicle " + str(self.idno) + " -")
        print("Travel direction: " + str(self.travelDirection))
        print("Speed: " + str(self.speed))
        print("Distance from intersection: " +
              str(self.distanceFromIntersection))
        print("Active? " + str(self.isActive))
        print("-----------------------")


    # avoid collisions when two cars are approaching intersection at same time in different directions
    def avoidIntersectionCollisions(self, activeVehicles):
        for v1 in activeVehicles:
            for v2 in activeVehicles:
                if v1 != v2:
                    # math.fabs(x) return the absolute value of x.
                    if math.fabs(v1.distanceFromIntersection - v2.distanceFromIntersection) < 10:
                        if v1.distanceFromIntersection < 20 and v1.distanceFromIntersection > 0:
                            if oncomingDirections(v1.travelDirection, v2.travelDirection):
                                if v1.speed == v2.speed:
                                    print("Collision avoided!")
                                    v1.printVehicleData()
                                    v2.printVehicleData()
                                    v1.adjustSpeed(10)

def oncomingDirections(d1, d2):
    if d1 == "N" and d2 == "E":
        return True
    elif d1 == "N" and d2 == "W":
        return True
    elif d1 == "S" and d2 == "E":
        return True
    elif d1 == "S" and d2 == "W":
        return True
    elif d1 == "W" and d2 == "N":
        return True
    elif d1 == "W" and d2 == "S":
        return True
    elif d1 == "E" and d2 == "N":
        return True
    elif d1 == "E" and d2 == "S":
        return True
    else:
        return False


def printIntersectionData(time, allVehicles):
    print("Time: " + str(time))
    for vehicle in allVehicles:
        vehicle.printVehicleData()
    print("~~~~~~~~~~~~~~~~~~~~~~~")

def runCollisionCheck(allVehicles):
    # check for collision of vehicles travelling in the same direction
    for vehicle1 in allVehicles:
        for vehicle2 in allVehicles:
            if vehicle1 != vehicle2:
                if math.fabs(vehicle1.distanceFromIntersection - vehicle2.distanceFromIntersection) < 3:
                    if vehicle1.distanceFromIntersection > 0:
                        if vehicle1.travelDirection == vehicle2.travelDirection:
                            if vehicle1.canPass == vehicle2.canPass:
                                print("Collision: V1 ID:" + str(vehicle1.idno) +
                                      "-" + str(vehicle1.distanceFromIntersection),)
                                print(" V2 ID:" + str(vehicle2.idno) + "-" +
                                      str(vehicle2.distanceFromIntersection))


def main():
    RUNTIME = 100
    TIMEINCREMENT = 1
    percentiles = []

    t0 = time.time()
    # initialize a single vehicle with idno 0
    allVehicles = []
    allVehicles.append(Vehicle(0, 75))
    # a = Auctioneer()

    print("Running Simulation...")
    # main simulation loop
    t = 0
    #printIntersectionData(t, allVehicles)
    while t < RUNTIME:
        t += TIMEINCREMENT
        for vehicle in allVehicles:
            vehicle.adjustDistanceFromIntersection(TIMEINCREMENT)
            vehicle.checkIfThroughIntersection(t)

        allVehicles.append(Vehicle(t, randint(1, 100)))

        runCollisionCheck(allVehicles)

    tf = time.time()
    print("Simulation complete. Run time: " + str(tf - t0) + " sec")

    allTimes = []
    for v in allVehicles:
        if v.timeThroughIntersection != 0:
            allTimes.append(v.timeThroughIntersection)

    avgTimeThru = (float)(sum(allTimes)) / len(allTimes)
    print("# of cars that passed thru intersection (out of " +
          str(len(allVehicles)) + " vehicles spawned): " + str(len(allTimes)))
    print("Average time to get through intersection: " + str(avgTimeThru) + " sec")

    
if __name__ == '__main__':
    main()
