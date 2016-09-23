#!/usr/bin/python -u
# The -u makes output unbuffered, so it will show up immediately
import json
import select
import socket
import sys
import time

# BPDU format:
#
# {"source": <bridge ID>, "dest": <ID or 'ffff'>, "type": <bpdu or data>, "message": <message data>}
# {"source":"02a1", "dest":"ffff", "type": "bpdu", "message":{"id":"02a1", "root":"02a1", "cost":0}}

# A BPDU class to keep the information about this bridge
class BPDU:
    def __init__(self, bridge_id, root_id, cost_to_root, dest='ffff'):
        self.bridge_id = bridge_id
        self.dest = dest
        self.root_id = root_id
        self.cost_to_root = cost_to_root
    def __str__(self):
        msg = {
            "source": self.bridge_id,
            "dest": self.dest,
            "type": "bpdu",
            "message": {
                "id": self.bridge_id,
                "root": self.root_id,
                "cost": self.cost_to_root
            }
        }
        return json.dumps(msg)

class Bridge:
    ports = []
    neighbors = []
    last_received = {}
    last_sent = None
    def __init__(self, bridge_id, LANs):
        self.bridge_id = bridge_id
        self.root_id = bridge_id
        self.cost_to_root = 0
        self.ports = range(len(LANs))
        self.sockets = []
        # creates sockets and connects to them
        for lan in LANs:
            s = socket.socket(socket.AF_UNIX, socket.SOCK_SEQPACKET)
            padded_lan = '\0' + lan
            while len(padded_lan) < 108:
                padded_lan += '\0'
            s.connect(padded_lan)
            self.sockets.append(s)
        print "Bridge " + id + " starting up\n"

    def broadcast(self):
        for sock in self.sockets:
            bpdu = BPDU(self.bridge_id, self.root_id, self.cost_to_root)
            sock.send(str(bpdu))

    def receive(self, port, bpdu):
        # TODO do we need port? Tracking which neighbor to which port?
        data = json.loads(bpdu)
        last_received[data.get("source")] = time.time()


if __name__ == "__main__":
        id = sys.argv[1]
        LAN = sys.argv[2:]

        bridge = Bridge(id, LAN)

        # Main loop
        while True:
                # Calls select with all the sockets; change the timeout value (1)
                ready, ignore, ignore2 = select.select(sockets, [], [], 1)

                # Reads from each fo the ready sockets
                for x in ready:
                        data = x.recv(1500)
                        print(data)

