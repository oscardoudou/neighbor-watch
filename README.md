# neighbor-watch
Actively control traffic based on currrent congestion level implemented in both traditional and SDN way
# Overview
* Emulated network congestion by redirecting traffic to IFB and applied traffic control discipline on Linux
* Implemented daemon with configparser and logger which enable communication within among daemons using Zmq 
* Designed congestion control algorithm based on Randomly Early Detection and Active Queue Management
* Automated script including nodes(VM) setup and route configuration of 8 router and 7 hosts on GENI
* Improved latency, dropped packet rate of router by notifying current congestion level to upstream
