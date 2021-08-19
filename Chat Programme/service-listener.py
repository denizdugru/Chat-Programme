import socket
import json

UDP_IP = ""
UDP_PORT = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
t_dict = {}
while True:
    data, addr = sock.recvfrom(1024)
    decoded_json = data.decode("utf-8")
    dict = json.loads(decoded_json)
    File_object1= open(r"trash.txt", "a") #OPEN A FILE
    username = dict['username']
    ip = dict['ip_addr']
    t_dict[username]=ip
    File_object1.write(username)
    File_object1.write("\n")
    File_object1.write(t_dict[username])
    File_object1.write("\n")
    lines_seen = set()
    outfile = open('online_users.txt', "w")
    infile = open('trash.txt', "r")
    for line in infile:
        if line not in lines_seen:  # not a duplicate
            outfile.write(line)
            lines_seen.add(line)
    outfile.close()
