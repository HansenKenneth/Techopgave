import socket

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 10000)

# https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
client_ip = socket.gethostbyname(socket.gethostname())

# find ud af om keep alive is true
f = open("opt.conf", "r")
print(f.read())

# https://stackoverflow.com/questions/3393612/run-certain-code-every-n-seconds

import threading


def heartbeat():
    threading.Timer(3.0, heartbeat).start()
    print("Kan man løse dette uden at bruge threads?")

    message = b'con-h 0x00'
    sent = sock.sendto(message, server_address)


# Dette skal kun gøres hvis keep alive is true
# heartbeat()

sequence_counter = 0

try:
    ok = False

    # pakker som bliver sendt til serveren for at etablerer en forbindelse
    message = b'com-0 ' + client_ip.encode()
    sent = sock.sendto(message, server_address)

    # responese er en pakke der bliver sendt tilbage til client med en accept
    response, server = sock.recvfrom(4096)
    # if (b'com-0 accept' in data):
    if response.startswith(b'com-0 accept'):
        # clienten bekræfter at have modtaget pakken
        message = b'com-0 accept'
        sent = sock.sendto(message, server_address)
        ok = True

    print('Handshake successful')

    while ok:
        # Ask for input
        text_message = input()
        message = 'msg-' + str(sequence_counter) + '=' + text_message
        data = message.encode()

        # Send data
        print('sending {!r}'.format(data))
        sent = sock.sendto(data, server_address)
        sequence_counter += 1

        # Receive response
        print('waiting to receive')
        data, server = sock.recvfrom(4096)
        print('received {!r}'.format(data))

        message = data.decode()

        if message.startswith('overload'):
            ok = False
        else:
            header_message, body_message = message.split("=")
            potato, counter_message = header_message.split('-')
            counter_to_number = int(counter_message)

            if counter_to_number == sequence_counter:
                sequence_counter += 1
            else:
                ok = False
finally:
    print('closing socket')
    sock.close()