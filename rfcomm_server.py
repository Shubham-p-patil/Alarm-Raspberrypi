from bluetooth import *

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]
                 
print("Waiting for connection on RFCOMM channel %d" % port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)

try:
    while True:
        data = client_sock.recv(1024)
        print("Received [%s]" % data)
        command,value = data.split(":")
        if command == 'light' :
            if value == 'on':
                print("Light Is Turned On")
            else:
                print("Light Is Turned Off")
            
except IOError:
    pass

print("Disconnected")

client_sock.close()
server_sock.close()
print("All done")
