import pigpio
import time
import constants

switch_time = None

def switch_callback(a, b, c):
    global switch_time
    switch_time = time.time()

def sleep_correction():
    if switch_time is None:
        time.sleep(constants.CLOCKSPEED)
    else:
        difference = time.time() - switch_time
        if difference <= constants.CLOCKSPEED:
            time.sleep(constants.CLOCKSPEED + (constants.CLOCKSPEED / 2 - difference))
        else:
            time.sleep(constants.CLOCKSPEED)

def listen(pi, GPIO_RECEIVER_NUMBER, data):

    state = "readingStart"

    buffer = ""

    message_buffer = ""

    run_value = None

    run_length = 0

    while True:
        bit = str(pi.read(GPIO_RECEIVER_NUMBER))

        if (run_length == constants.BIT_STUFF_RUN_LENGTH):
            run_length = 1
            run_value = bit
            sleep_correction()
            continue

        run_length = (run_length + 1) if (bit == run_value) else 1

        run_value = bit

        if state == "readingStart":
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
        sleep_correction()

def listen_for_data(port, data):

    GPIO_RECEIVER_NUMBER = constants.GPIO_RECEIVER_NUMBER(port)

    pi = pigpio.pi()

    pi.callback(GPIO_RECEIVER_NUMBER, pigpio.EITHER_EDGE, switch_callback)

    listen(pi, GPIO_RECEIVER_NUMBER, data)