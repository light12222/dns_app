#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import socket
import json

# Simple database to store DNS records (in this example, a dictionary)
dns_records = {}

def load_dns_records():
    """
    Load previously saved DNS records
    """
    try:
        with open("dns_records.json", "r") as f:
            dns_records.update(json.load(f))
    except FileNotFoundError:
        pass

def save_dns_records():
    """
    Save DNS records to file
    """
    with open("dns_records.json", "w") as f:
        json.dump(dns_records, f)

def register_dns(data):
    """
    Handle registration requests and save the records to the dns_records dictionary
    """
    lines = data.splitlines()
    record = {line.split('=')[0]: line.split('=')[1] for line in lines}
    if 'NAME' in record and 'VALUE' in record and 'TYPE' in record and 'TTL' in record:
        # Save the record to dns_records
        dns_records[record['NAME']] = {
            'TYPE': record['TYPE'],
            'VALUE': record['VALUE'],
            'TTL': record['TTL']
        }
        save_dns_records()
        return True
    return False

def handle_dns_query(data):
    """
    Handle DNS queries and return record information
    """
    lines = data.splitlines()
    query = {line.split('=')[0]: line.split('=')[1] for line in lines}
    if 'NAME' in query and 'TYPE' in query:
        # Look up the record
        record = dns_records.get(query['NAME'])
        if record and record['TYPE'] == query['TYPE']:
            response = f"TYPE={record['TYPE']}\nNAME={query['NAME']}\nVALUE={record['VALUE']}\nTTL={record['TTL']}\n"
            return response.encode()
    return b""

print("Authoritative Server is running...")
load_dns_records()
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 53533))
    while True:
        data, addr = sock.recvfrom(1024)
        message = data.decode()
        
        # Process registration or query based on the received message type
        if message.startswith('TYPE=A\n'):
            if 'VALUE' in message:
                # This is a registration request
                if register_dns(message):
                    print(f"Registered: {message}")
                else:
                    print(f"Failed to register: {message}")
            else:
                # This is a query request
                response = handle_dns_query(message)
                if response:
                    sock.sendto(response, addr)
                    print(f"Responded to query: {message}")
                else:
                    print(f"No DNS record found for query: {message}")
except KeyboardInterrupt:
    print("Authoritative Server is shutting down...")
finally:
    sock.close()


# In[ ]:




