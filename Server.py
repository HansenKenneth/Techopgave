import socket

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the port
server_address = ('localhost', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# https://kite.com/python/examples/5615/socket-handle-a-socket-timeout
sock.settimeout(4)

# https://docs.python.org/2.3/lib/node304.html
import logging

logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('handshakes.txt')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

# https://stackoverflow.com/questions/13733552/logger-configuration-to-log-to-file-and-print-to-stdout
# logging.getLogger().addHandler(logging.StreamHandler())

# https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
server_ip = socket.gethostbyname(socket.gethostname())

# maskimale pakker tilladt
f = open("opt.conf", "r")
print(f.read())

max_number_package = 2
package_received_counter = 0

# https://stackoverflow.com/questions/7370801/how-to-measure-elapsed-time-in-python
import time

start = time.time()
print("Start counting")

client_address = 'client address'
sequence_counter = -1

while True:
    try:
        print('\nwaiting to receive message')
        message_request, address = sock.recvfrom(4096)
        print('received {} bytes from {}'.format(len(message_request), address))
        print(message_request)

        # kontroller om et sekundt er passeret !!!!
        end = time.time()
        print(end - start)

        if end - start > 1:
            package_received_counter = 0
            start = time.time()
            print("Start counting")

        # Hvis max antal pakker overskrides lukkes socket
        package_received_counter += 1
        if package_received_counter > max_number_package:
            print('Die please')
            response_message = 'overload Please kill yourself'
            print(response_message)
            data = response_message.encode()

            sent = sock.sendto(data, address)

        message_request_string = message_request.decode()
        print(message_request_string)

        # if message_request_string.startswith('com-0'):
        if message_request.startswith(b'com-0'):
            # https://stackoverflow.com/questions/3462784/check-if-a-string-matches-an-ip-address-pattern-in-python
            def validate_ip(s):
                a = s.split('.')
                if len(a) != 4:
                    return False
                for x in a:
                    if not x.isdigit():
                        return False
                    i = int(x)
                    if i < 0 or i > 255:
                        return False
                return True


            ip_or_accept = message_request_string[6:]
            print(ip_or_accept)
            #         print(validate_ip(ip_or_accept))

            if validate_ip(ip_or_accept):
                # hvis pakken starter med com-0 så accepterer serveren og sender respons tilbage
                response = b'com-0 accept ' + server_ip.encode()
                sent = sock.sendto(response, address)
                client_address = ip_or_accept
                sequence_counter = -1
                logger.info('Handshake successful')
                # importer logger i toppen af koden

        elif message_request:
            header_message, body_message = message_request_string.split("=")
            potato, counter_message = header_message.split('-')
            counter_to_number = int(counter_message)

            if counter_to_number == sequence_counter + 1:
                sequence_counter = counter_to_number + 1

                print(counter_to_number)
                print(sequence_counter)

                response_message = 'res-' + str(sequence_counter) + '=I am server'
                print(response_message)
                data = response_message.encode()

                sent = sock.sendto(data, address)
                print('sent {} bytes back to {}'.format(sent, address))

    except socket.timeout:
        print("Timeout raised and caught.")

#         # https://stackoverflow.com/questions/3462784/check-if-a-string-matches-an-ip-address-pattern-in-python
#         def validate_ip(s):
#             a = s.split('.')
#             if len(a) != 4:
#                 return False
#             for x in a:
#                 if not x.isdigit():
#                     return False
#                 i = int(x)
#                 if i < 0 or i > 255:
#                     return False
#             return True

#         #
#         if validate_ip(client_address):
#             response_message = 'con-res 0xFE'
#             print(response_message)

#             data = response_message.encode()

#             # https://stackoverflow.com/questions/13999393/python-socket-sendto/28790238
#             sent = sock.sendto(data, client_address)
