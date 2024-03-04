#!/usr/bin/env python
# coding: utf-8

from flask import Flask, request, jsonify
import json
import socket

app = Flask(__name__)

# Global variable to store registration information
registration_info = {}

@app.route('/register', methods=['PUT'])
def register():
    """
    Register FS information to an authoritative server (AS)
    """
    data = request.get_json()
    if not data or 'hostname' not in data or 'ip' not in data or 'as_ip' not in data or 'as_port' not in data:
        return jsonify({"error": "Registration data is incomplete"}), 400

    # Store registration information in the global variable
    registration_info['hostname'] = data['hostname']
    registration_info['ip'] = data['ip']
    registration_info['as_ip'] = data['as_ip']
    registration_info['as_port'] = int(data['as_port'])

    # Send UDP message to AS for registration
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    registration_message = "TYPE=A\nNAME={}\nVALUE={}\nTTL=10\n".format(registration_info['hostname'], registration_info['ip'])
    udp_socket.sendto(registration_message.encode(), (registration_info['as_ip'], registration_info['as_port']))
    udp_socket.close()

    return jsonify({"message": "Registration successful"}), 201

@app.route('/fibonacci', methods=['GET'])
def fibonacci_number():
    """
    Calculate and return the Fibonacci number for the given sequence number X
    """
    number = request.args.get('number')
    try:
        number = int(number)
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid input, number must be an integer"}), 400

    # Calculate the Fibonacci number
    def fib(n):
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        return a

    fib_number = fib(number)
    return jsonify({"fibonacci_number": fib_number}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)
