from Objects import *






if __name__ == '__main__':
    source = './busy_day.in'
    reader = DBReader(source=source)
    reader.read()
    
    print("Warehouse Amount: ", reader.getWarehouseAmount())
    print("Customer Order Amount: ", reader.getOrderAmount())
    print("Product Type Amount: ", reader.getProductTypeAmount())
    
    warehouses = reader.getWarehouseList()
    orders = reader.getOrderList()
    drones = reader.getDroneList()
    weights = reader.getProductWeights()

    commander = Commander(warehouses, orders, drones, weights)
    print(drones[0])
    #print(warehouses[1].getProductAmountOf(2))
    commander.command('0 L 1 2 2')
    #print(warehouses[1].getProductAmountOf(2))
    print(drones[0])
    drones[0].wait(3)
    print(drones[0])
    print(orders[1])
    commander.command('0 D 1 0 163')
    print(drones[0])
    print(orders[1])
    print("Distance from drone 0 to order 1: ", commander.getDistance(drones[0], orders[1]))

    