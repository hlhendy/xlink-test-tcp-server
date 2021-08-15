#!/usr/bin/env python3
import selectors
import socket
import re
import csv

HOST = ''  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print("SOCKET NAME: ", s.getsockname())
    print("Creating conn")
    all_data = []
    end_indicators = 0
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if end_indicators >= 5:
                break
            if data == b'\r\n':
                end_indicators += 1
            if data == None or data == b'':
                break
            data_str = data.decode('utf-8')
            data_splt = data_str.splitlines()
            for d in data_splt:
                all_data.append(d)
            conn.sendall(data)
        with open('output/output.csv', 'a', newline='') as csvfile:
            w = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            for row in all_data:
                row = row.split(",")
                print("ROW: ", row)
                w.writerow(row)
