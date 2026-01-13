import opcua
from opcua import Client
import time

url = "opc.tcp://172.17.1.32:4840"

client = Client(url)

client.connect()
print("Client connected {}".format(url))

while True:

    # Note: AS4.8 have ns = 6 and AS4.12 have ns = 11
    Milacron1 = client.get_node("ns=11;s=::AsGlobalPV:CLP.Cal.Actpos")
    MilacronVar1 = Milacron1.get_value()
    print("Clamp Position {}".format(MilacronVar1))

    Milacron2 = client.get_node("ns=11;s=::AsGlobalPV:EJT.Cal.Actpos")
    MilacronVar2 = Milacron2.get_value()
    print("Ejector Position {}".format(MilacronVar2))

    Milacron3 = client.get_node("ns=11;s=::AsGlobalPV:INJ[0].Cal.Actpos")
    MilacronVar3 = Milacron3.get_value()
    print("Injection Position {}".format(MilacronVar3))

    time.sleep(0.1)



