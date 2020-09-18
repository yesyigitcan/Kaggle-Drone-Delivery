import math
from copy import deepcopy
import matplotlib.pyplot as plt
import random
from drawnow import drawnow

def calculateDistance(x1, y1, x2, y2):
    euclidean_distance = ( (x1 - x2)**2 + (y1 - y2)**2 ) ** 0.5
    return math.ceil(euclidean_distance)

class DBReader:
    # source busy_day.in
    def __init__(self, source):
        self.source = source
        self.orderAmount = 0
        self.warehouseAmount = 0
        self.warehouseList = list()
        self.productTypeAmount = 0
        self.orderList = list()
        self.droneAmount = 0
        self.droneList = list()
        self.turn = 0
        self.maxPayload = 0
        self.productWeightList = list()
        self.mapSize = {'x': 0, 'y': 0}
    def read(self):
        with open(self.source, 'r') as sourceFile:
            # 100 rows, ​100 columns, 3 drones, 50 turns, max payload is 500
            headerLineList = sourceFile.readline().split(' ')
            self.mapSize['x']   =    int(headerLineList[0])
            self.mapSize['y']   =    int(headerLineList[1])
            self.droneAmount    =    int(headerLineList[2])
            self.turn           =    int(headerLineList[3])
            self.maxPayload     =    int(headerLineList[4])
            del headerLineList

            

            # There are 3 different product types
            self.productTypeAmount = int(sourceFile.readline()) # Skip number of products line
            
            for i in range(self.droneAmount):
                self.droneList.append(Drone(self.productTypeAmount, self.maxPayload))

            # The product types weigh: 100u, 5u, 450u
            self.productWeightList = [int(weight) for weight in sourceFile.readline().split(' ')]

            # There are 2 warehouses.
            self.warehouseAmount = int(sourceFile.readline())

            for k in range(self.warehouseAmount):
                # First warehouse is located at [0, 0].
                location = [int(i) for i in sourceFile.readline().split(' ')]
                warehouse = Warehouse()
                warehouse.setLocation(location[0], location[1])

                # It stores 5 items of product 0 and 1 of product 1.
                warehouse.setProductAmount( [int(i) for i in sourceFile.readline().split(' ')] )
                self.warehouseList.append(warehouse)
            
            # There are 3 orders
            self.orderAmount = int(sourceFile.readline())

            for k in range(self.orderAmount):
                # First order to be delivered to [1, 1].
                location = [int(i) for i in sourceFile.readline().split(' ')]
                order = Order()
                order.setTargetLocation(location[0], location[1])

                # First order contains 2 items.
                orderProductTypeAmount = int(sourceFile.readline())

                # Items of product types: 2, 0.
                orderProductTypes = sourceFile.readline().split(' ')
                for amount in orderProductTypes:
                    order.addProductType(int(amount))
                for amount in range(self.productTypeAmount - orderProductTypeAmount):
                    order.addProductType(0)

                self.orderList.append(order)
    def printWarehouseList(self):
        for warehouse in self.warehouseList:
            print(warehouse)
    def printOrderList(self):
        for order in self.orderList:
            print(order)
    def getWarehouseAmount(self):
        return self.warehouseAmount
    def getOrderAmount(self):
        return self.orderAmount
    def getProductTypeAmount(self):
        return self.productTypeAmount
    def getDroneAmount(self):
        return self.droneAmount
    def getWarehouseList(self):
        return self.warehouseList
    def getOrderList(self):
        return self.orderList
    def getDroneList(self):
        return self.droneList
    def getProductWeights(self):
        return self.productWeightList
    def getTurnLimit(self):
        return self.turn  

class Warehouse:
    def __init__(self):
        self.locationDict = {'x': 0, 'y':0}
        self.productAmountList = None
    def setLocation(self, x, y):
        self.locationDict['x'] = x
        self.locationDict['y'] = y
    def setProductAmount(self, productAmountList):
        self.productAmountList = productAmountList
    def unload(self, productType, amount):
        if self.productAmountList[productType] < amount:
            raise Exception('Not enough product in warehouse') 
        #print(self.productAmountList[productType])
        #print(amount)
        self.productAmountList[productType] -= amount
    def getLocation(self):
        return self.locationDict
    def getX(self):
        return self.locationDict['x']
    def getY(self):
        return self.locationDict['y']
    def getProductAmountOf(self, index):
        return self.productAmountList[index]
    def getProductAmountList(self):
        return self.productAmountList
    def __str__(self):
        productAmount = 0
        for amount in self.productAmountList:
            productAmount += amount
        return "Wareh | X: " + str(self.locationDict['x']) + "\tY: " + str(self.locationDict['y']) + "\tProduct Amount: " + str(productAmount) 


class Order:
    def __init__(self):
        self.targetLocationDict = {'x': 0, 'y': 0}
        self.productTypesList = list()
        self.isDoneFlag = False
    def setTargetLocation(self, x, y):
        self.targetLocationDict['x'] = x
        self.targetLocationDict['y'] = y
    def getLocation(self):
        return self.targetLocationDict
    def getX(self):
        return self.targetLocationDict['x']
    def getY(self):
        return self.targetLocationDict['y']
    def addProductType(self, productType):
        self.productTypesList.append(productType)
    def unload(self, productType, amount):
        if self.isDone():
            raise Exception('Order is already done')
        elif len(self.productTypesList) < productType:
            raise Exception('Order has no that product type ' + str(productType))
        elif self.productTypesList[productType] == 0:
            raise Exception('Order has not the product specified')
        elif self.productTypesList[productType] - amount < 0:
            raise Exception('Order product amount cannot be negative')
        
        self.productTypesList[productType] -= amount
        self.setIfDone()
    def isDone(self):
        return self.isDoneFlag
    def setIfDone(self):
        for i in self.productTypesList:
            if i != 0:
                return 
        self.isDoneFlag = True
    def __str__(self):
        productAmount = 0
        for amount in self.productTypesList:
            productAmount += amount
        productString = ""
        for i in range(len(self.productTypesList)):
            if self.productTypesList[i] != 0:
                productString += "P" + str(i) + "x" + str(self.productTypesList[i]) + "\t" 
        return "Order | X: " + str(self.targetLocationDict['x']) + "\tY: " + str(self.targetLocationDict['y']) + "\tProduct Amount: " + str(productAmount) + "\t" + productString 

class Drone:
    def __init__(self, productTypeAmount, maxPayload):
        self.waitDuration = 0
        self.currentPayLoad = 0
        self.productAmount = 0
        self.maxPayload = maxPayload
        self.productTypesList = [0 for i in range(productTypeAmount)]
        self.currentPosition = {'x': 0, 'y': 0}
        self.targetDestination = {'x': 0, 'y': 0}
        self.actionType = 'N' # 'W' wait, 'F' fly 'L', 'N' null
        self.step_x = 0.0
        self.step_y = 0.0
    def getLocation(self):
        return self.currentPosition
    def getX(self):
        return self.currentPosition['x']
    def getY(self):
        return self.currentPosition['y']
    def getWait(self):
        return self.waitDuration
    def wait(self, time):
        self.waitDuration += time
    def load(self, warehouse, productType, amount, payload):
        if self.currentPayLoad + amount * payload > self.maxPayload:
            raise Exception('Drone cannot carry more products')
        warehouse.unload(productType, amount)
        self.currentPayLoad += amount * payload
        self.productAmount += amount
    '''
    def fly(self, x, y):
        distance = calculateDistance(self.currentPosition['x'], self.currentPosition['y'], x, y)
        self.currentPosition['x'] = x
        self.currentPosition['y'] = y
        return distance
    '''
    def getActionType(self):
        return self.actionType
    def setFly(self, x, y):
        distance = calculateDistance(self.currentPosition['x'], self.currentPosition['y'], x, y)
        if distance == 0:
            self.actionType = 'N'
            return
        self.targetDestination['x'] = x
        self.targetDestination['y'] = y
        self.step_x = (self.targetDestination['x'] - self.currentPosition['x']) / distance
        self.step_y = (self.targetDestination['y'] - self.currentPosition['y']) / distance
        self.actionType = 'F'
        
    def action(self):
        if self.actionType == 'W':
            self.waitDuration += 1
        elif self.actionType == 'F':
            self.currentPosition['x'] += self.step_x
            self.currentPosition['y'] += self.step_y
            if int(self.currentPosition['x']) == self.targetDestination['x'] and int(self.currentPosition['y']) == self.targetDestination['y']:
                self.currentPosition = deepcopy(self.targetDestination)
                self.actionType = 'N'

    def unload(self, order, productType, amount, payload):
        order.unload(productType, amount)
        if self.currentPayLoad - payload < 0:
            self.currentPayLoad = 0
        else:
            self.currentPayLoad -= payload
    def __str__(self):
        return "Drone | X: " + str(self.currentPosition['x']) + "\tY: " + str(self.currentPosition['y']) +  "\tPayload: " + str(self.currentPayLoad) + "/" + str(self.maxPayload) + "\tProduct Amount: " + str(self.productAmount) + "\tWait: " + str(self.waitDuration)
        

class Commander:
    def __init__(self, warehouses, orders, drones, weights, turnLimit):
        self.warehouses = warehouses
        self.orders = orders
        self.drones = drones
        self.productTypeWeights = weights
        self.turnLimit = turnLimit
        self.score = 0
        self.turn = 0
    def command(self, commandString):
        commandList = commandString.split(' ')
        droneIndex = int(commandList[0])
        droneAction = commandList[1].upper()
        if len(commandList) == 3:
            # 0 W 3 Command to drone 0, wait for three turns
            droneWait = commandList[2]
            self.drones[droneIndex].wait(droneWait)
        elif len(commandList) == 5:
            # 0 D 1 2 3 Command to drone 0, deliver for order 1 items of product type 2, three of them.
            dronePType = int(commandList[3])
            dronePAmount = int(commandList[4])
            if droneAction == 'D':
                droneOrder = int(commandList[2])
                # Drone 0: fly to customer 0 and ​deliver​ one product 0
                self.drones[droneIndex].unload(self.orders[droneOrder], dronePType, dronePAmount, self.productTypeWeights[dronePType])
            elif droneAction == 'L':
                droneWarehouse = int(commandList[2])
                # Drone 0: fly to warehouse 1 and ​load​ one product 2
                self.drones[droneIndex].load(self.warehouses[droneWarehouse], dronePType, dronePAmount, self.productTypeWeights[dronePType])
            else:
                raise Exception('Invalid Action Type')
        else:
            raise Exception('Invalid Command Length')
    def getDistance(self, drone, target):
        return calculateDistance(drone.getX(), drone.getY(), target.getX(), target.getY())
    def plotMap(self, showWarehouses = True, showOrders = True, showDrones = True):
        if showWarehouses:
            plt.scatter([warehouse.getX() for warehouse in self.warehouses], [warehouse.getY() for warehouse in self.warehouses], c='b', label="Warehouse")
        if showOrders:
            plt.scatter([order.getX() for order in self.orders], [order.getY() for order in self.orders], c='r', label="Order")
        if showDrones:
            plt.scatter([drone.getX() for drone in self.drones], [drone.getY() for drone in self.drones], c='g', label="Drone")
        plt.legend()
        plt.grid()
        plt.show()
    def setDroneFly(self, i, x, y):
        self.drones[i].setFly(x, y)
    def loadDrone(self, i_d, i_w, p_type, amount):
        self.drones[i_d].load(self.warehouses[i_w], p_type, amount, self.productTypeWeights[p_type])
    def deliverProduct(self, i_d, i_o, p_type, amount):
        self.drones[i_d].unload(self.orders[i_o], p_type, amount, self.productTypeWeights[p_type])
    def make_fig(self):
        plt.scatter([warehouse.getX() for warehouse in self.warehouses], [warehouse.getY() for warehouse in self.warehouses], c='b', label="Warehouse")
        plt.scatter([order.getX() for order in self.orders], [order.getY() for order in self.orders], c='r', label="Order")
        plt.scatter([drone.getX() for drone in self.drones], [drone.getY() for drone in self.drones], c='g', label="Drone")
    def checkOrderExist(self):
        for order in self.orders:
            if not order.isDone():
                return False
        return True
    def startSimulation(self):
        
        for i in range(self.turnLimit + 1):
            if self.turn == self.turnLimit:
                raise Exception('Exceed turn limit. Simulation terminated')
            
            for j in range(len(self.drones)):
                if self.drones[j].getActionType() == 'N':
                    self.setDroneFly(j, random.randint(0,350), random.randint(0,350))
            for drone in self.drones:
                drone.action()
            drawnow(self.make_fig)
            self.turnLimit += 1
            
        plt.show()