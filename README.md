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

# Test vm network in virtualbox
power off
`VBoxManage modifyvm VMNAME --nicN hostonly(type)` or config in GUI setting network tab, dont know how to specify nic card type
after reboot, `ip link show` would have one more interface 
use `sudo ip a a INTERFACE_IP dev DEV_NAME` to bring up interface
change broadcast addr`sudo inconfig INTERFACE_NAME broadcast 192.168.34.255` if it is 0.0.0.0 right after bringing up interface
turn on ip forwarding`sudo sysctl net.ipv4.ip_forward=1`
add ip route
`ip route add 192.168.34.100 via 192.168.33.100 [dev enp0s8]
`ip route add 192.168.34.0/24 via 192.168.33.100 [dev enp0s8]
Where 192.168.34.100 is the IP address of the host in dotted decimal notation, 192.168.33.100 is the next hop address and enp0s8 is the exit interface leading to the next hop.
Where 192.168.34.0/24 is a range of IP addresses
VM2 - VM1 - VM3
192.168.33.200/24(VM2) could ping 192.168.34.100/24(VM1), but when bring VM3 with 192.168.34.200/24, it can't even ping 192.168.34.100, suspect is because nic card mode is hostonly, other tuturials suggest internal network.   