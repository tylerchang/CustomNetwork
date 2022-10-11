import pigpio
import time
import constants
from multiprocessing import Process

wake = "10"

def send_sequence(pi, message, GPIO_TRANSMITTER_NUMBERS):
    for bit in message:
        for number in GPIO_TRANSMITTER_NUMBERS:
            pi.write(number, int(bit))
        time.sleep(constants.CLOCKSPEED)

def add_bit_stuffing(message, n):
    # n is the length of a repeating bit sequence before adding in a stuff bit
    answer = ""
    n_buffer = " "
    for bit in message:
        if bit != n_buffer[-1]:
            n_buffer = bit
            answer += bit
        else:
            n_buffer += bit
            answer += bit
            if len(n_buffer) == n:
                answer += str(1-int(bit))
                n_buffer = str(1-int(bit))
    return answer

def wave_send(pi, message, GPIO_TRANSMITTER_NUMBERS):
        for number in GPIO_TRANSMITTER_NUMBERS:
            pi.set_mode(number, pigpio.OUTPUT)

        pi.wave_clear()
        pi.wave_add_new()

        for number in GPIO_TRANSMITTER_NUMBERS:
            pi.wave_add_serial(number, constants.BIT_RATE, message)
    
        wave_output = pi.wave_create()

        pi.wave_send_once(wave_output)
            
def transmit_message(message, ports):
    GPIO_TRANSMITTER_NUMBERS = [constants.GPIO_TRANSMITTER_NUMBER(port) for port in ports]

    pi = pigpio.pi()

    if constants.LINK_MODE == "WAVE":
        wave_send(pi, message, GPIO_TRANSMITTER_NUMBERS)
    else:
        sequence = wake + constants.START_SEQUENCE + message + constants.STOP_SEQUENCE
        bit_stuffed_sequence = add_bit_stuffing(sequence, constants.BIT_STUFF_RUN_LENGTH)
        send_sequence(pi, bit_stuffed_sequence, GPIO_TRANSMITTER_NUMBERS)
