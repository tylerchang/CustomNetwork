import pigpio
import time
from convertUtility import bytesToMessage
from dataProcessor import processChat
from constants import CLOCKSPEED, BIT_STUFF_RUN_LENGTH
import constants

switch_time = None

def switch_callback(a, b, c):
    global switch_time
    switch_time = time.time()

def sleepCorrection():
    if switch_time is None:
        time.sleep(CLOCKSPEED)
    else:
        difference = time.time() - switch_time
        if difference <= CLOCKSPEED:
            time.sleep(CLOCKSPEED + (CLOCKSPEED / 2 - difference))
        else:
            time.sleep(CLOCKSPEED)

def listen(pi, GPIO_RECEIVER_NUMBER, data):

    state = "readingStart"

    buffer = ""

    message_buffer = ""

    runValue = None

    runLength = 0

    while True:
        bit = str(pi.read(GPIO_RECEIVER_NUMBER))

        if (runLength == BIT_STUFF_RUN_LENGTH):
            runLength = 1
            runValue = bit
            sleepCorrection()
            continue

        runLength = (runLength + 1) if (bit == runValue) else 1

        runValue = bit

        if state == "readingStart":
            #print(buffer)
            if len(buffer) >= len(constants.START_SEQUENCE):
                buffer = buffer[1:]

            buffer += bit

            if buffer == constants.START_SEQUENCE:
                buffer = ""
                state = "readingMessage"

        elif state == "readingMessage":
            message_buffer += bit

            if len(buffer) >= len(constants.STOP_SEQUENCE):
                buffer = buffer[1:]

            buffer += bit

            if buffer == constants.STOP_SEQUENCE:
                buffer = ""
                state = "readingStart"

                message_buffer = message_buffer[:-1 * len(constants.STOP_SEQUENCE)]
                data.put(message_buffer)
                message_buffer = ""
        sleepCorrection()

def listenForData(port, data):

    GPIO_RECEIVER_NUMBER = constants.GPIO_RECEIVER_NUMBER(port)

    pi = pigpio.pi()

    pi.callback(GPIO_RECEIVER_NUMBER, pigpio.EITHER_EDGE, switch_callback)

    listen(pi, GPIO_RECEIVER_NUMBER, data)
