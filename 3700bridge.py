#!/usr/bin/python -u
# The -u makes output unbuffered, so it will show up immediately
import sys
import socket
import select
import time
import json


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
        for x in range(len(LAN)):
            s = socket.socket(socket.AF_UNIX, socket.SOCK_SEQPACKET)
            s.connect(pad(LAN[x]))
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

# pads the name with null bytes at the end
def pad(name):
        result = '\0' + name
        while len(result) < 108:
                result += '\0'
        return result

            #print(message)

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

