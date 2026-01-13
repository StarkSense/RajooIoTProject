
from opcua import Client
import time

url = "opc.tcp://192.168.111.99:4841"

client = Client(url)

client.connect()
print("Client connected {}".format(url))


while True:
    Temp = client.get_node("ns=2;i=2")
    Temperature = Temp.get_value()
    print(Temperature)

    Prs = client.get_node("ns=2;i=3")
    Pressure = Prs.get_value()
    print(Pressure)

    ActTime = client.get_node("ns=2;i=4")
    CurrentTime = ActTime.get_value()
    print(CurrentTime)

    time.sleep(1)



