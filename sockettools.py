import socket

class PriorityReceiver(object):
    def __init__(self, ip ="", port = 5004):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, # internet
                                    socket.SOCK_DGRAM) # udp
        self.socket.bind((self.ip, self.port))
        self.message_buffer = [[] for i in range(10)]

    def update(self):
        while True:
            try:
                data, addr = self.socket.recvfrom(1024, socket.MSG_DONTWAIT)
            except socket.error:
                break
            else:
                data = data.decode('utf-8').strip()
                with_priority = True
                try:
                    priority = int(data[0])
                except ValueError:
                    priority = 0
                    with_priority = False
                if with_priority:
                    message = data[1:].replace('\n', ' ')
                else:
                    message = data.replace('\n', ' ')
                self.message_buffer[priority].append(message)
                if len(self.message_buffer[priority]) > 1000:
                    message_buffer[priority] = message_buffer[priority][-1000:]

    def __bool__(self):
        empty = 1
        for el in self.message_buffer:
            if el:
                empty = 0
        return not empty

    def pop(self):
        for priority in range(len(self.message_buffer)):
            if self.message_buffer[priority]:
                return (self.message_buffer[priority].pop(), priority)
        return None

    
