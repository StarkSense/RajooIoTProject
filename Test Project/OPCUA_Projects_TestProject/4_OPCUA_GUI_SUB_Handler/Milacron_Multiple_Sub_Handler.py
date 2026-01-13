
# https://github.com/FreeOpcUa/python-opcua/issues/791
# import sys
# import time
#
#
# sys.path.insert(0, "..")
#
# from opcua import Client
#
# class SubHandler(object):
#     def __init__(self, obj):
#         self.obj = obj
#
#     def datachange_notification(self, node, val, data):
#         setattr(self.obj, self.obj.browse_name, data.monitored_item.Value.Value.Value)
#
# class value(object):
#
#     def __setattr__(self, key, value):
#         print(key, value)
#         super().__setattr__(key, value)
#
#     def __init__(self, opcua_server, ua_node):
#         self.ua_node = ua_node
#         self.MyVariable = 0
#         self.browse_name = ua_node.get_browse_name().Name
#
#         handler = SubHandler(self)
#         sub = opcua_server.create_subscription(500, handler)
#         handle = sub.subscribe_data_change(self.ua_node)
#
#
# if __name__ == "__main__":
#     url = "opc.tcp://127.0.0.1:4840"
#     client = Client(url)
#     try:
#         client.connect()
#         root = client.get_root_node()
#         objNode = client.get_objects_node()
#         # myvar = root.get_child(["0:Objects", "2:MyObject", "2:MyVariable"])
#         myvar = root.get_child(["0:Object", "7:GlobalVars"])
#         variableObj = value(client, myvar)
#         print(variableObj.MyVariable)
#         time.sleep(10)
#
#     finally:
#         client.disconnect()





# https://stackoverflow.com/questions/70005210/how-to-access-the-data-when-using-opc-ua-subscriptions-with-the-python-opc-ua-im
from opcua import Client
import time

class SubHandler(object):
    """
    Client to subscription. It will receive events from server
    """

    def datachange_notification(self, node, val, data):
        print("Python: New data change event", node, val)
        x = f"Hardik: New data change event {node} and {val}"
        print(x)
        # pass

    def event_notification(self, event):
        print("Python: New event", event)


if __name__ == "__main__":

    # configure client
    url = "opc.tcp://127.0.0.1:4840"
    client = Client(url)

    try:
        # connect client
        client.connect()
        # map the nodes of the informaiton model to Pyhton
        # e.g. node1, node2
        # Note: AS4.8 have ns = 6 and AS4.12 have ns = 11
        node1= client.get_node("ns = 11;s=::AsGlobalPV:FEATURE.Set.CoreMasEnable")
        node2= client.get_node("ns = 11;s=::AsGlobalPV:FEATURE.Set.Ejtenable")
        node3= client.get_node("ns = 11;s=::AsGlobalPV:FEATURE.Set.Injenable")
        node4= client.get_node("ns = 11;s=::AsGlobalPV:FEATURE.Set.Insertmold")

        handler = SubHandler()
        sub = client.create_subscription(500, handler)

        handle1 = sub.subscribe_data_change(node1)
        handle2 = sub.subscribe_data_change(node2)
        handle3 = sub.subscribe_data_change(node3)
        handle4 = sub.subscribe_data_change(node4)
        # handle5 = sub.subscribe_events(node4)

    # use the data of the read-nodes ?

    except:
         client.disconnect()