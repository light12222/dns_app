#!/usr/bin/env python
# coding: utf-8

from flask import Flask, request, jsonify
import socket

app = Flask(__name__)

@app.route('/fibonacci', methods=['GET'])
def get_fibonacci():
    """
    Handle GET requests for Fibonacci number calculation
    """
    # Extract parameters from the request URL
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    # Check if any parameter is missing
    if not (hostname and fs_port and number and as_ip and as_port):
        return jsonify({"error": "Bad request, missing parameters"}), 400

    try:
        # Resolve hostname to IP address by querying the authoritative DNS server
        fs_ip = resolve_hostname(hostname, as_ip, int(as_port))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    try:
        # Send a request to the Fibonacci Server (FS) to get the Fibonacci number
        fibonacci_number = get_fibonacci_from_fs(fs_ip, int(fs_port), int(number))
        return jsonify({"fibonacci_number": fibonacci_number}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def resolve_hostname(hostname, as_ip, as_port):
    """
    Resolve hostname to IP address by querying the authoritative DNS server (AS)
    """
    # Send a DNS query to the authoritative DNS server (AS)
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    query_message = "TYPE=A\nNAME={}\n".format(hostname)
    udp_socket.sendto(query_message.encode(), (as_ip, as_port))

    # Receive and parse the response
    data, _ = udp_socket.recvfrom(1024)
    response = data.decode().splitlines()
    for line in response:
        if line.startswith("VALUE="):
            return line.split('=')[1]

    raise Exception("Failed to resolve hostname to IP address")

def get_fibonacci_from_fs(fs_ip, fs_port, number):
    """
    Get Fibonacci number from Fibonacci Server (FS)
    """
    # Send a GET request to the Fibonacci Server (FS)
    response = requests.get("http://{}:{}/fibonacci?number={}".format(fs_ip, fs_port, number))
    if response.status_code == 200:
        return response.json()['fibonacci_number']
    else:
        raise Exception("Failed to get Fibonacci number from Fibonacci Server")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
