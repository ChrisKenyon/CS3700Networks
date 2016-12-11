Project 5 README
Chris Kenyon & Eric Su

NOTE: Eric Su was in the hospital Dec 4-5. Please refer to Christo concerning emails and accommodation for an extra day. Eric Su himself can provide his discharge form for reference.

The objective of this project was to implement a distributed key-value store by using the Raft consensus protocol.

The program was implemented in Python using sockets and threading. Alongside the AppendEntries RPC and RequestVote RPC methods laid out by the Raft protocol, handlers for GET and PUT requests were included, as well as handlers for the responses to the RPC requests. Two timeouts had to be implemented: election and heartbeat, in order to make sure there was always a leader.

Challenges include reducing latency and failures. Threading was used in order to help reduce latency, as well as the reduction of loops and unnecessary function calls while handling GET and PUT requests. For example, PUT requests originally included the logic to send  AppendEntries RPC messages when a new entry was given by the user, but this was cut out and left to the standard heartbeat mechanism to reduce latency in processing a PUT request.

Testing was done against the test.py script, as well as individual configurations for better debugging.