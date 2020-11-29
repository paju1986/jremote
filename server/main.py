import socket
import uinput 
import json
import time

def createDevice(deviceData):
    buttons = deviceData["button_mapHex"]
    axes = deviceData["axis_mapHex"]
    
    arrayUinputButtons = []
    arrayUinputAxes = []
    for button in buttons:
        arrayUinputButtons.append((0x01,button))
        
    for axis in axes:
        arrayUinputAxes.append((0x03,axis) + (-32767, 32767, 0, 0))
    
    events = []
    events = events + arrayUinputButtons
    events = events + arrayUinputAxes
    return uinput.Device(tuple(events))
      

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 6666       # Port to listen on (non-privileged ports are > 1023)

device = None

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        print(uinput.BTN_JOYSTICK)
        buff = ""
        while True:
            data = conn.recv(1024)
            if not data:
                break
            buff = buff + data.decode()
           
            packets = buff.split("|")
            for packet in packets:
                #process packet
                if packet != "":
                    if packet != packets[-1]:
                        parsedData = json.loads(packet)
                        if "deviceName" in parsedData:
                            device = createDevice(parsedData)
                            time.sleep(2)
                        if "typ" in parsedData:
                            if parsedData["typ"] == "button":
                                print("button")
                                print(parsedData["index"])
                                button = (0x01,parsedData["cod"])
                                device.emit(button,parsedData["value"])
                            else:
                                axes = (0x03,parsedData["cod"])
                                device.emit(axes,parsedData["value"])
                    
                    
            buff = packets[-1]
            