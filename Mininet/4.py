from mininet.net import Mininet
from mininet.cli import CLI
from mininet.util import pmonitor
from mininet.link import TCLink
import sys
import time

question_number = sys.argv[1]
BW = int(sys.argv[2]) 

popens = {}

# topology
net = Mininet(link=TCLink)

# hosts
S = net.addHost('h1')
H = net.addHost('h2')
I = net.addHost('h3')
J = net.addHost('h4')
K = net.addHost('h5')
L = net.addHost('h6')
M = net.addHost('h7')
N = net.addHost('h8')
O = net.addHost('h9')

if question_number in ["la", "lb", "ma", "mb"]:
    S1 = net.addHost('h10')
    S2 = net.addHost('h11')

# switches
A = net.addSwitch('s1')
B = net.addSwitch('s2')
C = net.addSwitch('s3')
D = net.addSwitch('s4')
E = net.addSwitch('s5')
F = net.addSwitch('s6')
G = net.addSwitch('s7')

# controller
c0 = net.addController('c0')

# links
net.addLink(H, D, bw=BW/4)
net.addLink(I, D, bw=BW/4)
net.addLink(J, E, bw=BW/4)
net.addLink(K, E, bw=BW/4)
net.addLink(L, F, bw=BW/4)
net.addLink(M, F, bw=BW/4)
net.addLink(N, G, bw=BW/4)
net.addLink(O, G, bw=BW/4)
net.addLink(D, B, bw=BW/2)
net.addLink(E, B, bw=BW/2)
net.addLink(F, C, bw=BW/2)
net.addLink(G, C, bw=BW/2)
net.addLink(B, A, bw=BW)
net.addLink(C, A, bw=BW)
net.addLink(A, S, bw=BW)

if question_number in ["la", "lb", "ma", "mb"]:
    net.addLink(S1, F, bw=BW)
    net.addLink(S2, G, bw=BW)

if question_number == 'ma' or question_number == 'mb':
    net.addLink(B, C, bw=BW)

net.start()

# run scripts on hosts
if question_number == "ka":
    popens[S] = S.popen("python3 server/TCPserver_thread_mn.py 8 " + str(S.IP()))
    time.sleep(0.2)
    popens[H] = H.popen("python3 TCPclient_mn.py 8 " + str(S.IP()) + " Ramayana.txt")
    popens[I] = I.popen("python3 TCPclient_mn.py 8 " + str(S.IP()) + " Anna_Karenina.txt")
    popens[J] = J.popen("python3 TCPclient_mn.py 8 " + str(S.IP()) + " War_and_Peace.txt")
    popens[K] = K.popen("python3 TCPclient_mn.py 8 " + str(S.IP()) + " Brothers_Karamazov.txt")
elif question_number == "kb":
    popens[S] = S.popen("python3 server/TCPserver_thread_mn.py 8 " + str(S.IP()))
    time.sleep(0.2)
    popens[H] = H.popen("python3 TCPclient_mn.py 8 " + str(S.IP()) + " Ramayana.txt")
    popens[K] = K.popen("python3 TCPclient_mn.py 8 " + str(S.IP()) + " Anna_Karenina.txt")
    popens[M] = M.popen("python3 TCPclient_mn.py 8 " + str(S.IP()) + " War_and_Peace.txt")
    popens[N] = N.popen("python3 TCPclient_mn.py 8 " + str(S.IP()) + " Brothers_Karamazov.txt")
elif question_number == "la" or question_number == "ma":
    popens[S] = S.popen("python3 server/TCPserver_thread_mn.py 8 " + str(S.IP()))
    popens[S1] = S1.popen("python3 server/TCPserver_thread_mn.py 8 " + str(S1.IP()))
    popens[S2] = S2.popen("python3 server/TCPserver_thread_mn.py 8 " + str(S2.IP()))
    time.sleep(0.2)
    popens[H] = H.popen("python3 TCPclient_mn.py 8 " + str(S.IP()) + " Ramayana.txt")
    popens[I] = I.popen("python3 TCPclient_mn.py 8 " + str(S.IP()) + " Anna_Karenina.txt")
    popens[J] = J.popen("python3 TCPclient_mn.py 8 " + str(S1.IP()) + " War_and_Peace.txt")
    popens[K] = K.popen("python3 TCPclient_mn.py 8 " + str(S2.IP()) + " Brothers_Karamazov.txt")
elif question_number == "lb" or question_number == "mb":
    popens[S] = S.popen("python3 server/TCPserver_thread_mn.py 8 " + str(S.IP()))
    popens[S1] = S1.popen("python3 server/TCPserver_thread_mn.py 8 " + str(S1.IP()))
    popens[S2] = S2.popen("python3 server/TCPserver_thread_mn.py 8 " + str(S2.IP()))
    time.sleep(0.2)
    popens[H] = H.popen("python3 TCPclient_mn.py 8 " + str(S.IP()) + " Ramayana.txt")
    popens[K] = K.popen("python3 TCPclient_mn.py 8 " + str(S.IP()) + " Anna_Karenina.txt")
    popens[M] = M.popen("python3 TCPclient_mn.py 8 " + str(S1.IP()) + " War_and_Peace.txt")
    popens[N] = N.popen("python3 TCPclient_mn.py 8 " + str(S2.IP()) + " Brothers_Karamazov.txt")
else:
    print("Invalid argument.")
    exit()


time.sleep(13)

# monitoring 
for h, line in pmonitor(popens, timeoutms=500):
    if h:
        print(str(h.name) +": " + str(line), end = '')
    else:
        break

# stopping
net.stop()