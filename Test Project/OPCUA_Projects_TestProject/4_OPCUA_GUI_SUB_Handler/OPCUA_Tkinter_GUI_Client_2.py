
# https://www.google.com/search?q=tkinter+and+OPCUA&rlz=1C1GCEU_enIN987IN987&ei=DINVY6DEF-K44t4P_vmowAY&ved=0ahUKEwig-o73-Pb6AhVinNgFHf48CmgQ4dUDCA8&uact=5&oq=tkinter+and+OPCUA&gs_lcp=Cgdnd3Mtd2l6EAMyBwghEKABEAoyBwghEKABEAo6CggAEEcQ1gQQsAM6BQgAEIAEOggILhCABBDUAjoFCAAQkQI6BggAEBYQHjoICAAQFhAeEA86BQghEKABSgQITRgBSgQIQRgASgQIRhgAUJ0lWPFEYP1VaAFwAXgAgAGpBIgB-yqSAQkyLTkuNS4xLjKYAQCgAQHIAQjAAQE&sclient=gws-wiz
# https://www.youtube.com/watch?v=xPYBmh2v6r4

from tkinter import Label, Frame , Tk ,PhotoImage
from opcua import Client

# Creat GUI
tk = Tk()
mainframe = Frame(tk)
mainframe.pack()
# Off.bmp
# On.bmp

button_states = [PhotoImage(file=""),PhotoImage(file="")]
# button_states = [PhotoImage(file=r"D:\Projects\Python\OPC\Off.png"), PhotoImage(file=r"D:\Projects\Python\OPC\On.png")]
my_button = Label(mainframe , image= button_states[0])
my_button.pack()
Label(mainframe ,text= "States of the button").pack()

# Classes for the Subscription handler
class ButtonHandler(object):
    def datachange_notification(self , node, val, data):
        print("New States : " + str(val))
        if val == True:
            my_button.configure(image= button_states[1])
        else:
            my_button.configure(image=button_states[0])

#Connect to Server
client = Client("opc.tcp://localhost:4840")
try:
    client.connect()
except:
    print("Could not connect to Server")
else:
    button_var = client.get_node("ns = 1;s=my_button")
    handler = ButtonHandler()
    sub = client.create_subscription(500, handler)
    handle = sub.subscribe_data_change(button_var)

# Start TK mainloop
tk.mainloop()
sub.unsubscribe(handle)
print("Disconnect Client")
client.disconnect()

