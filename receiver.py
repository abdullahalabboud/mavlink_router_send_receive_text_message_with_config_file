import sys
import time
from pymavlink import mavutil


from time import sleep

OWN_COMP_ID = 1

# python3 examples/receiver.py 127.0.0.1:14553 22

if len(sys.argv) != 3:
    print("Usage : %s <ip:udp_port> <system_id>" % (sys.argv[0]))
    print(
        "Receive mavlink heartbeats on specified interface. "
        "Respond with a ping message"
    )
    sys.exit()


srcSystem = int(sys.argv[2])

mav = mavutil.mavlink_connection(
    "udpin:" + sys.argv[1],
    source_system=srcSystem,
    source_component=OWN_COMP_ID,
)
mav.wait_heartbeat()

print(
    "Heartbeat from system id : %u , component id : %u"
    % (mav.target_system, mav.target_component)
)
while True:
    # print("\n\n\n\n", srcSystem, "\n\n\n\n")
    msg = mav.recv_match(blocking=True)
    print("Message from %d %s " % (msg.get_srcSystem(), msg))
    if hasattr(msg, "target_system"):
        if msg.target_system == 0:
            print("\tMessages send to all ")
        elif msg.target_system == srcSystem:
            print("\tMessages send to me ")
        else:
            print("\tMessages send to other")
    else:
        print("\tMessages without target system")

    # mav.mav.ping_send(
    #     int(time.time() * 1000), msg.seq, msg.get_srcSystem(), msg.get_srcComponent()
    # )
    # mav.mav.status_text(mavutil.mavlink.MAV_SEVERITY_INFO, msg)

    sleep(1)
