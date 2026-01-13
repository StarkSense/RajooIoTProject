
from opcua import Client
import time

# Classes for the Subscription handler
class CoreMasEnableHandler(object):
    def datachange_notification(self , node, val, data):
        print("New States : " + str(val))
        if val == True:
            print("Enable Core Operation Selection :  True")
        else:
            print("Enable Core Operation Selection :  False")

class InjectionEnableHandler(object):
    def datachange_notification(self , node, val, data):
        print("New States : " + str(val))
        if val == True:
            print("Enable Injection Selection :  True")
        else:
            print("Enable Injection Selection :  False")

#Connect to Server
url = "opc.tcp://127.0.0.1:4840"
client = Client(url)

try:
    client.connect()
    print("Connect to Server")
except:
    print("Could not connect to Server")

else:
    # Note: AS4.8 have ns = 6 and AS4.12 have ns = 11
    CoreMasEnable_var = client.get_node("ns = 11;s=::AsGlobalPV:FEATURE.Set.CoreMasEnable")
    root = client.get_root_node()
    print("Objects node is: ", root.get_browse_name())
    print("Children of root are: ", root.get_children())
    handler = CoreMasEnableHandler()
    sub = client.create_subscription(500, handler)
    handle = sub.subscribe_data_change(CoreMasEnable_var)


    InjectionEnable_var = client.get_node("ns = 11;s=::AsGlobalPV:FEATURE.Set.Injenable")
    root = client.get_root_node()
    print("Objects node is: ", root.get_browse_name())
    print("Children of root are: ", root.get_children())
    handler1 = InjectionEnableHandler()
    sub = client.create_subscription(500, handler1)
    handle1 = sub.subscribe_data_change(InjectionEnable_var)