# neighbor-watch
Actively control traffic based on currrent congestion level implemented in both traditional and SDN way
# Overview
* Emulated network congestion by redirecting traffic to IFB and applied traffic control discipline on Linux
* Implemented daemon with configparser and logger which enable communication within among daemons using Zmq 
* Designed congestion control algorithm based on Randomly Early Detection and Active Queue Management
* Automated script including nodes(VM) setup and route configuration of 8 router and 7 hosts on GENI
* Improved latency, dropped packet rate of router by notifying current congestion level to upstream

# Introduction
In packet-switched network, bufferbloat occurs when a network buffer too much data resulting in high latency or network jitter. Rather than wait buffer being filled up, AQM(Active Queue Management) monitor on router's ingress queue and perform actions aimed on reducing network congestion before router's butter is full. Generally AQM provides two ways to alleviate congestion: drop packet(drop when ingress is completely full) and mark packet (Explicityly Congestion Notification ). The former one drops packet on ingress of congested router while the latter let end client directly notify the sender. Although ECN seems to be nicer than dropping packet, but it require the participation of end device. If end device ignore marked packet, there is no way to reduce congestion.

# High Level Proposal   
Unlike above approaches used by AQM, neighbor watch operates on previous hop's egress queue to conotrol ingress queue congestion on a give router. By reducing packet sending from previous hop, it allows a bufferbloat router to focus more on processing already queued packet rather than receiving and queueing incoming packet. Once a router has alleviated its congestion, the previuos router is notified and would allow more packets to flow by reduce its drop rate.

Congestion notification only notify immediate hop, never alert router two or more hop away. Will discuss this later.