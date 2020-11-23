#############################################################################
#
# Script for questions 3e) and 3f)
# 
# Author: Chris Francis, 18110041
#
# Usage: 
# 
# for 3e) run: sudo python3 3e_and_3f.py Bible.txt Ramayana.txt Anna_Karenina.txt War_and_Peace.txt Brothers_Karamazov.txt
#
# for 3f) run: sudo python3 3e_and_3f.py Bible.txt Bible.txt Bible.txt Bible.txt Bible.txt
#
#############################################################################

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.util import pmonitor
import sys
import time

popens = {}

# topology
net = Mininet()
h = {}
h[1] = net.addHost('h1')
h[2] = net.addHost('h2')
h[3] = net.addHost('h3')
h[4] = net.addHost('h4')
h[5] = net.addHost('h5')
h[6] = net.addHost('h6')
s1 = net.addSwitch('s1')
c0 = net.addController('c0')
net.addLink(h[1], s1)
net.addLink(h[2], s1)
net.addLink(h[3], s1)
net.addLink(h[4], s1)
net.addLink(h[5], s1)
net.addLink(h[6], s1)
net.start()

popens[h[1]] = h[1].popen("python3 server/TCPserver_thread_mn.py 32768 " + str(h[1].IP()))

time.sleep(0.1)

popens[h[2]] = h[2].popen("python3 TCPclient_mn.py 32768 " + str(h[1].IP()) + " " + sys.argv[1])

popens[h[3]] = h[3].popen("python3 TCPclient_mn.py 32768 " + str(h[1].IP()) + " " + sys.argv[2])

popens[h[4]] = h[4].popen("python3 TCPclient_mn.py 32768 " + str(h[1].IP()) + " " + sys.argv[3])

popens[h[5]] = h[5].popen("python3 TCPclient_mn.py 32768 " + str(h[1].IP()) + " " + sys.argv[4])

popens[h[6]] = h[6].popen("python3 TCPclient_mn.py 32768 " + str(h[1].IP()) + " " + sys.argv[5])


# monitoring output of scripts
for h, line in pmonitor(popens, timeoutms=500):
    if h:
        print(str(h.name) +": " + str(line), end = '')
    else:
        break

# stopping
net.stop()