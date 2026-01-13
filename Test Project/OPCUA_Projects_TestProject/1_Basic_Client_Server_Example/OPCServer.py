
#Reference : https://www.youtube.com/watch?v=NbKeBfK3pfk&list=PLWw98q-Xe7iGf-c4b6zF0bnJA9avEN_mF&index=2

from opcua import ua, uamethod, Server
from random import randint
import datetime
import time

server = Server()

# url = "opc.tcp://0.0.0.0:4840"
# url = "opc.tcp://0.0.0.0:4840/freeopcua/server/"
# url = "opc.tcp://192.168.72.182:4841" #IP when i connected with WIFI
url = "opc.tcp://192.168.111.99:4841"   #Must have to configure Ethernet ,Currently Ethernet 3 set with this IP.

#you must connect those network IP in which you use in url

server.set_endpoint(url)

name = "OPCUA_SIMULATION_SERVER"

# set all possible endpoint policies for clients to connect through
# server.set_security_policy([
#     ua.SecurityPolicyType.NoSecurity,
#     ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
#     ua.SecurityPolicyType.Basic256Sha256_Sign])
# server.set_security_policy([ua.SecurityPolicyType.NoSecurity])

addspace = server.register_namespace(name)


node = server.get_objects_node()
Param = node.add_object(addspace, "Parameters")

Temp = Param.add_variable(addspace, "Temperature", 0)
Press = Param.add_variable(addspace, "Pressure", 0)
Time = Param.add_variable(addspace, "CurrentTime", 0)

Temp.set_writable()
Press.set_writable()
Time.set_writable()

server.start()
print("Server started at {}".format(url))

while True:
    Temperature = randint(10,50)
    Pressure = randint(200,999)
    CurrentTime = datetime.datetime.now()

    print(Temperature, Pressure, CurrentTime)
    Temp.set_value(Temperature)
    Press.set_value(Pressure)
    Time.set_value(CurrentTime)


    time.sleep(1)