
from opcua import Client
import time
import paho.mqtt.client as mqtt
import json
# url = "opc.tcp://127.0.0.1:4840"
url = "opc.tcp://172.17.1.32:4840"



client = Client(url)

client.connect()
print("Client connected {}".format(url))

# z3fgMWUK8PcubfVVRo2H
iot_hub = "demo.thingsboard.io"
port = 1883         #This Port is reserved for MQTT communication
username = "z3fgMWUK8PcubfVVRo2H"
password = ""
topic = "v1/devices/me/telemetry"

iot_hub_client = mqtt.Client()
iot_hub_client.username_pw_set(username, password)
iot_hub_client.connect(iot_hub, port)
print("Connected to IOT hub")

data = dict()



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


    Milacron4 = client.get_node("ns=11;s=::AsGlobalPV:HEAT[0].Zone[0].Set.Temp")
    MilacronVar4 = Milacron4.get_value()
    print("Zone 1 Temperature {}".format(MilacronVar4))

    Milacron5 = client.get_node("ns=11;s=::AsGlobalPV:HEAT[0].Zone[1].Set.Temp")
    MilacronVar5 = Milacron5.get_value()
    print("Zone 2 Temperature {}".format(MilacronVar5))

    Milacron6 = client.get_node("ns=11;s=::AsGlobalPV:HEAT[0].Zone[2].Set.Temp")
    MilacronVar6 = Milacron6.get_value()
    print("Zone 3 Temperature {}".format(MilacronVar6))

    Milacron7 = client.get_node("ns=11;s=::AsGlobalPV:HEAT[0].Zone[3].Set.Temp")
    MilacronVar7 = Milacron7.get_value()
    print("Zone 4 Temperature {}".format(MilacronVar7))

    data['CLP Position'] = str(MilacronVar1)
    data['EJT Position'] = str(MilacronVar2)
    data['INJ Position'] = str(MilacronVar3)
    data['Zone 1 Temp'] = str(MilacronVar4)
    data['Zone 2 Temp'] = str(MilacronVar5)
    data['Zone 3 Temp'] = str(MilacronVar6)
    data['Zone 4 Temp'] = str(MilacronVar7)

    data_out = json.dumps(data)
    iot_hub_client.publish(topic, data_out, 0)

    time.sleep(0.1)



