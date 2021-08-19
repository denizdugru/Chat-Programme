#!/usr/bin/env python3


from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread
import tkinter #---FOR GUI----
import datetime


def receive_online_users():
    #TO READ FROM TXT FILE AND DELETE EXCESS INFOS
    online_users = {}
    file_object = open(r"online_users.txt", "r")

    for x in range(50):
        username = (file_object.readline()).strip('\n')
        ip_addr = (file_object.readline()).strip('\n')
        online_users[username] = ip_addr

    for x in online_users:
        user_list.insert(tkinter.END, x)

    user_list.insert(tkinter.END, "---------------------")

def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
            file_object = open('CHAT_LOG.txt', "a")
            currentDT = datetime.datetime.now()
            file_object.writelines(str(currentDT))
            file_object.writelines(" - ")
            file_object.writelines(msg)
            file_object.writelines("\n")

        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # event is passed by binders.
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "/quit":
        client_socket.close()
        top.quit()


def on_closing(event=None):  # event is passed by binders.
    #This function is to be called when the window is closed.
    my_msg.set("/quit")
    send()

top = tkinter.Tk()
top.title("Chatter")


   #-------FRAMING--------
users_frame = tkinter.Frame(top)
messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("Type your messages here.")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
scrollbar_2= tkinter.Scrollbar(users_frame)

# Following will contain the messages, and user list.
user_list= tkinter.Listbox(users_frame, width=70, yscrollcommand=scrollbar_2.set)
msg_list = tkinter.Listbox(messages_frame, height=30, width=70, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
user_list.pack(side=tkinter.RIGHT, fill=tkinter.X)
scrollbar_2.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack()
user_list.pack()
messages_frame.pack()
users_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
show_button = tkinter.Button(top, text="Show Users", command=receive_online_users)
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()
show_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

#----Now comes the sockets part----
print("PLEASE LOOK UP YOUR IP ADDRESS IN WONDOWS :ipconfig --- IN UNIX/LINUX :ifconfig ")
HOST = input("Enter your IP:")
PORT = 5001
BUFSIZ = 1024
ADDR = (HOST, PORT) #----AS THIS METHOD WE CAN CONNECT OTHER USERS EASILY

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
top.mainloop()  # Starts GUI execution.




