{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "64308ff3",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * Serving Flask app '__main__'\n",
      " * Debug mode: off\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.\n",
      " * Running on all addresses (0.0.0.0)\n",
      " * Running on http://127.0.0.1:9090\n",
      " * Running on http://10.0.0.139:9090\n",
      "Press CTRL+C to quit\n"
     ]
    }
   ],
   "source": [
    "from flask import Flask, request, jsonify\n",
    "import json\n",
    "import socket\n",
    "\n",
    "app = Flask(__name__)\n",
    "\n",
    "# Global variable to store registration information\n",
    "registration_info = {}\n",
    "\n",
    "@app.route('/register', methods=['PUT'])\n",
    "def register():\n",
    "    \"\"\"\n",
    "    Register FS information to an authoritative server (AS)\n",
    "    \"\"\"\n",
    "    data = request.get_json()\n",
    "    if not data or 'hostname' not in data or 'ip' not in data or 'as_ip' not in data or 'as_port' not in data:\n",
    "        return jsonify({\"error\": \"Registration data is incomplete\"}), 400\n",
    "\n",
    "    # Store registration information in the global variable\n",
    "    registration_info['hostname'] = data['hostname']\n",
    "    registration_info['ip'] = data['ip']\n",
    "    registration_info['as_ip'] = data['as_ip']\n",
    "    registration_info['as_port'] = int(data['as_port'])\n",
    "\n",
    "    # Send UDP message to AS for registration\n",
    "    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)\n",
    "    registration_message = f\"TYPE=A\\nNAME={registration_info['hostname']}\\nVALUE={registration_info['ip']}\\nTTL=10\\n\"\n",
    "    udp_socket.sendto(registration_message.encode(), (registration_info['as_ip'], registration_info['as_port']))\n",
    "    udp_socket.close()\n",
    "\n",
    "    return jsonify({\"message\": \"Registration successful\"}), 201\n",
    "\n",
    "@app.route('/fibonacci', methods=['GET'])\n",
    "def fibonacci_number():\n",
    "    \"\"\"\n",
    "    Calculate and return the Fibonacci number for the given sequence number X\n",
    "    \"\"\"\n",
    "    number = request.args.get('number')\n",
    "    try:\n",
    "        number = int(number)\n",
    "    except (ValueError, TypeError):\n",
    "        return jsonify({\"error\": \"Invalid input, number must be an integer\"}), 400\n",
    "\n",
    "    # Calculate the Fibonacci number\n",
    "    def fib(n):\n",
    "        a, b = 0, 1\n",
    "        for _ in range(n):\n",
    "            a, b = b, a + b\n",
    "        return a\n",
    "\n",
    "    fib_number = fib(number)\n",
    "    return jsonify({\"fibonacci_number\": fib_number}), 200\n",
    "\n",
    "if __name__ == '__main__':\n",
    "    app.run(host='0.0.0.0', port=9090)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "b8007d0e",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
