Project 2 README
Chris Kenyon & Eric Su

The objective of this project was to implement a bridged network that implemented the Spanning Tree Protocol for packet
routing and to avoid loops. To accomplish this, we defined a bridge class with a BPDU subclass, as well as a timer class to handle
timeouts for old BPDUs and forwarding table entries.

The bridge class handles the receipt and transmission of BPDUs and data packets, as well as the implementation of the spanning tree protocol. The
spanning tree protocol is implemented by checking the BPDU for a different root with lower IDs and bridges with lower costs to root.
When receiving a BPDU and updating its root, a bridge may designate a port as a root port or a designated port. These
indicate the need for the port to forward packets to the root or to other bridges in the network. Ports that are not designated will be disabled
in order to prevent loops.

When a bridge receives a data message, it will populate its forwarding table with the source host and the port the
message was seen on in order to better forward packets in the future. However, a forwarding table entry older than
5 seconds will be timed out and flushed from the table. With the implementation of the spanning tree protocol
and the forwarding table, the bridge transmits the message directly to a bridge if the destination is known, or the message is broadcasted
by the bridge in an attempt to find a route for the packet's destination.

We implemented our timer class on a threaded timer in order to run timeout checks and BPDU broadcasts on a separate thread.
Every 500ms, a bridge is tasked with broadcasting its BPDU to the network to keep the spanning tree updated. In addition,
we implement a timer to check and expire bridge messages if BPDUs haven't been received in the last 750ms.