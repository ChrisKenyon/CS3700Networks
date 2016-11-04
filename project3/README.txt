Project 2 README
Chris Kenyon & Eric Su

The objective of this project was to implement a transport protocol that provides reliable datagram service. The program consists of a sender and receiver module.

The sender is contained within a PacketSender class with attributes to track its congestion window, sequence number, RTT and so forth. The sender is responsible for estimating RTT using time samples from requests. The sender is also primarily responsible for the initial handshake to establish the connection between sender and receiver. We've established these methods within the class.

When the sender script is invoked, the start() method will set up the socket, perform the handshake, load a packet into its buffer, and then send the packet to the receiver. Once the initial data packet is sent, the sender goes into a loop of receiving ACKs, adjusting its congestion window, queueing and sending new packets. RTT and a dictionary of timestamps for each packet allows the sender to enable timeouts for packets still in transit.

The receiver is initialized to listen for inbound connection and will decode the CRC code from the message to verify that the data arrived uncorrupted. Once this is done it will respond appropriately for SYN/ACK handshake, an EOF, and so forth. The receiver also maintains a buffer of messages in transit.

For large packets, data compression has been used to reduce data size.