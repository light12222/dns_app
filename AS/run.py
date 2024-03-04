#!/usr/bin/env python
# coding: utf-8

from socket import *

server_port = 53533

# Create a socket (UDP)
server_socket = socket(AF_INET, SOCK_DGRAM)
# Bind to port
server_socket.bind(('', server_port))
dns_records = {}
# Now listen
print('The server is ready to receive message.')

while True:
    # Receive message
    message, client_address = server_socket.recvfrom(2048)
    msg_decoded = message.decode()
    print("Got the message: " + msg_decoded)

    lines = msg_decoded.splitlines()
    record = {line.split('=')[0]: line.split('=')[1] for line in lines}

    # Check if it's a registration request or a query
    if 'VALUE' in record:
        # Registration
        print("Registration request is taken")
        # Assuming TYPE is always provided in registration
        dns_records[record['NAME']] = {
            'TYPE': record['TYPE'],
            'VALUE': record['VALUE'],
            'TTL': record['TTL']
        }
        # You might want to save to file here
        server_socket.sendto("Success".encode(), client_address)
    else:
        # Query
        print("Query request is taken")
        response_name = record['NAME']
        if response_name in dns_records:
            queried_record = dns_records[response_name]
            if queried_record['TYPE'] == record['TYPE']:
                response = f"TYPE={queried_record['TYPE']}\nNAME={response_name}\nVALUE={queried_record['VALUE']}\nTTL={queried_record['TTL']}\n"
                server_socket.sendto(response.encode(), client_address)
            else:
                server_socket.sendto("Record type mismatch".encode(), client_address)
        else:
            server_socket.sendto("No such name".encode(), client_address)
