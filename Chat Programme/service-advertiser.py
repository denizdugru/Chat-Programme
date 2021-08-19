
import socket
import asyncio
import json

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
name = input("Please enter your username :")

user_info = {"username" : name, "ip_addr" : IPAddr}
json_string=json.dumps(user_info)


UDP_PORT = 5000
MESSAGE = json_string



sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # this is a broadcast socket


async def work():       #-----TO TIME A LOOP
    while True:
        sock.sendto(bytes(json_string, "utf-8"), ('<broadcast>', UDP_PORT))
        await asyncio.sleep(60)

loop = asyncio.get_event_loop()
try:
    asyncio.ensure_future(work())
    loop.run_forever()      #----LOOP CONTINUES UNTIL ITS CUT
except KeyboardInterrupt:
    pass
finally:
    print("Closing Loop")
    loop.close()

