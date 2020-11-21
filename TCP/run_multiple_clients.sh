#!/bin/bash
python3 TCPclient.py 32768 n n Bible.txt & 
python3 TCPclient.py 32768 n n Ramayana.txt &
python3 TCPclient.py 32768 n n Anna_Karenina.txt &
python3 TCPclient.py 32768 n n War_and_Peace.txt &
python3 TCPclient.py 32768 n n Brothers_Karamazov.txt &

