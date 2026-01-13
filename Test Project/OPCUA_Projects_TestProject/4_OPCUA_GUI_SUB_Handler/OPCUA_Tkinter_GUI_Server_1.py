from opcua import Server
from time import sleep
server = Server()
root = server.get_objects_node()
my_button = root.add_variable("ns = 1;s=my_button","my_button",  50)
server.start()

# if True:
#     my_button.set_value(True)
#     sleep(1)
#     my_button.set_value(False)
#     sleep(1)
#     my_button.set_value(True)