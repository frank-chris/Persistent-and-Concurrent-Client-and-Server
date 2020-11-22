from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.util import pmonitor
import sys
import time

popens = {}

no_of_switches = int(sys.argv[1])

# topology
net = Mininet()
h = {}
h[1] = net.addHost('h1')
h[2] = net.addHost('h2')
s = {}
for i in range(no_of_switches):
    s[i+1] = net.addSwitch('s'+str(i+1))

c0 = net.addController('c0')

for i in range(1, no_of_switches):
    net.addLink(s[i], s[i+1])

net.addLink(h[1], s[1])
net.addLink(h[2], s[no_of_switches])
net.start()

# run scripts on hosts
popens[h[1]] = h[1].popen("python3 server/TCPserver_thread_mn.py 8 " + str(h[1].IP()))

popens[h[2]] = h[2].popen("python3 TCPclient_mn.py 8 " + str(h[1].IP()) + " Bible.txt")

time.sleep(3)

# monitoring 
for h, line in pmonitor(popens, timeoutms=500):
    if h:
        print(str(h.name) +": " + str(line), end = '')
    else:
        break

# stopping
net.stop()