{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "b8c0c17e",
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
      " * Running on http://127.0.0.1:8080\n",
      " * Running on http://10.0.0.139:8080\n",
      "Press CTRL+C to quit\n"
     ]
    }
   ],
   "source": [
    "from flask import Flask, request, jsonify\n",
    "import socket\n",
    "\n",
    "app = Flask(__name__)\n",
    "\n",
    "@app.route('/fibonacci', methods=['GET'])\n",
    "def get_fibonacci():\n",
    "    \"\"\"\n",
    "    Handle GET requests for Fibonacci number calculation\n",
    "    \"\"\"\n",
    "    # Extract parameters from the request URL\n",
    "    hostname = request.args.get('hostname')\n",
    "    fs_port = request.args.get('fs_port')\n",
    "    number = request.args.get('number')\n",
    "    as_ip = request.args.get('as_ip')\n",
    "    as_port = request.args.get('as_port')\n",
    "\n",
    "    # Check if any parameter is missing\n",
    "    if not (hostname and fs_port and number and as_ip and as_port):\n",
    "        return jsonify({\"error\": \"Bad request, missing parameters\"}), 400\n",
    "\n",
    "    try:\n",
    "        # Resolve hostname to IP address by querying the authoritative DNS server\n",
    "        fs_ip = resolve_hostname(hostname, as_ip, int(as_port))\n",
    "    except Exception as e:\n",
    "        return jsonify({\"error\": str(e)}), 500\n",
    "\n",
    "    try:\n",
    "        # Send a request to the Fibonacci Server (FS) to get the Fibonacci number\n",
    "        fibonacci_number = get_fibonacci_from_fs(fs_ip, int(fs_port), int(number))\n",
    "        return jsonify({\"fibonacci_number\": fibonacci_number}), 200\n",
    "    except Exception as e:\n",
    "        return jsonify({\"error\": str(e)}), 500\n",
    "\n",
    "def resolve_hostname(hostname, as_ip, as_port):\n",
    "    \"\"\"\n",
    "    Resolve hostname to IP address by querying the authoritative DNS server (AS)\n",
    "    \"\"\"\n",
    "    # Send a DNS query to the authoritative DNS server (AS)\n",
    "    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)\n",
    "    query_message = f\"TYPE=A\\nNAME={hostname}\\n\"\n",
    "    udp_socket.sendto(query_message.encode(), (as_ip, as_port))\n",
    "\n",
    "    # Receive and parse the response\n",
    "    data, _ = udp_socket.recvfrom(1024)\n",
    "    response = data.decode().splitlines()\n",
    "    for line in response:\n",
    "        if line.startswith(\"VALUE=\"):\n",
    "            return line.split('=')[1]\n",
    "\n",
    "    raise Exception(\"Failed to resolve hostname to IP address\")\n",
    "\n",
    "def get_fibonacci_from_fs(fs_ip, fs_port, number):\n",
    "    \"\"\"\n",
    "    Get Fibonacci number from Fibonacci Server (FS)\n",
    "    \"\"\"\n",
    "    # Send a GET request to the Fibonacci Server (FS)\n",
    "    response = requests.get(f\"http://{fs_ip}:{fs_port}/fibonacci?number={number}\")\n",
    "    if response.status_code == 200:\n",
    "        return response.json()['fibonacci_number']\n",
    "    else:\n",
    "        raise Exception(\"Failed to get Fibonacci number from Fibonacci Server\")\n",
    "\n",
    "if __name__ == '__main__':\n",
    "    app.run(host='0.0.0.0', port=8080)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "14decc5e",
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
