from sender import transmit_message
from receiver import listenForData
from convertUtility import bytesToMessage, messageToBytes
from dataProcessor import processData
from multiprocessing import Process, Queue

def listen(port, data):
    listenForData(port, data)

def broadcast(message, ports):
    transmit_message(messageToBytes(message), ports)

def receiveFrom(ports):
    data = Queue()

    createQueueThread(data)

    for port in ports:
        thread = Process(target=listen, args=(port, data))
        thread.start()

def broadcastTo(ports, message):
    b1 = Process(target=broadcast, args=(message, ports))
    b1.start()

def createQueueThread(queue):
    queueThread = Process(target=processData, args=(queue,))
    queueThread.start()
