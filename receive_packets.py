import socket
import json
import os
from dotenv import load_dotenv

load_dotenv()

JSON_FILE_NAME = "door-state.json"

# Define the IP and port to listen on
UDP_IP = "0.0.0.0"  # Listen on all adresses
UDP_PORT = os.getenv("PORT") # Port to listen for packets on

# Create the UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the given IP and adress
sock.bind((UDP_IP, UDP_PORT))

def updateJson(doorState):
    with open(JSON_FILE_NAME, "r") as file:
        json_data = json.load(file)
    json_data["door_status"] = doorState
    with open(JSON_FILE_NAME, "w") as file:
        json.dump(json_data, file, indent=4)
    
    print("Json file updated")


print(f"Listening for UDP packets on port {UDP_PORT}...")
# Infinite loop to keep listening on the socket. Only stops if there is a keyboard interupt
try:
    while True:
        # Receive data from the socket
        # recvfrom returns the data in bytes and the return adress
        rawData, addr = sock.recvfrom(2048)  # Buffer size is 1 byte because Esp will only ever send 1 bit.
        data = rawData[0] # Data will only ever be 1 bit, so just take the first (and only) bit.
        print(f"Packet recived from {addr} on port {UDP_PORT}: {data}") # Print the data to the console
        updateJson(data) # change the doorState in the json file to whatever was sent so that the discord bot can see the change

# If there is a keyboard interrupt close the socket and exit
except KeyboardInterrupt as e:
    print("Keyboard Interrupt, Exiting")
    sock.close()
    exit()