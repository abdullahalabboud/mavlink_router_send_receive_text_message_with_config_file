import sys
from pymavlink import mavutil
import time

from threading import Thread
from time import sleep


TARGET_COMP_ID = 1
# python3 examples/sender.py 127.0.0.1:14552 21 0
# argv[3] : means 0 value and that has used in ping_send method to indicates a PING request

if len(sys.argv) != 4:
    print("Usage : %s <ip:udp_port> <system_id> <target_system_id>" % (sys.argv[0]))
    print(
        "Send mavlink pings, using given <system-id> and <target-system-id>, "
        "to specified interface"
    )
    sys.exit()

srcSystem = int(sys.argv[2])

mav = mavutil.mavlink_connection("udp:" + sys.argv[1], source_system=srcSystem)
# print("mav try connection")
mav.wait_heartbeat()
# print("mav wait heartbeat ")


def pingloop():
    i = 0
    while True:
        # print("start while pind send")
        mav.mav.statustext_send(
            mavutil.mavlink.MAV_SEVERITY_INFO, "text message".encode()
        )

        # mav.mav.ping_send(
        #     int(time.time() * 1000),
        #     i,
        #     int(sys.argv[3]),
        #     TARGET_COMP_ID,
        # )


# print("try threading ")
pingthread = Thread(target=pingloop)
pingthread.daemon = True
pingthread.start()
# print("start threading ")


print(
    "Heartbeat from system id : %u , component id : %u"
    % (mav.target_system, mav.target_component)
)

while True:
    # print("\n\n\n\n", srcSystem, "\n\n\n\n")
    print("Sending ...!!")
    msg = mav.recv_match(blocking=True)
    # print("Message from %d: %s:" % (msg.get_srcSystem(), msg))
