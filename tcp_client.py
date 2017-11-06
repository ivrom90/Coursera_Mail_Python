import time
import socket


class Client:

    def __init__(self, adr, port, timeout=None):
        self.adr = adr
        self.port = port
        self.timeout = timeout

    def get(self, key):
        result = {}

        with socket.create_connection((self.adr, self.port), self.timeout) as sock:

            try:
                sock.send(f"get {key}\n".encode('utf8'))
            except socket.error:
                raise ClientError

            try:
                data = sock.recv(4096)
            except socket.timeout:
                raise ClientError

            if data:
                response = data.decode("utf8").split("\n")
                if response[0] == "ok":
                    response.remove("ok")
                    for line in response:

                        try:
                            if line != "":
                                name, metric_value, timestamp = line.split(" ")
                                if name in result:
                                    result[name].append((int(timestamp), float(metric_value)))
                                else:
                                    result[name] = [(int(timestamp), float(metric_value))]
                        except:
                            raise ClientError
                else:
                    raise ClientError
        return result

    def put(self, metric, value, timestamp=None):

        if not timestamp:
            timestamp = str(int(time.time()))

        with socket.create_connection((self.adr, self.port), self.timeout) as sock:

            try:
                sock.send(f"put {metric} {value} {timestamp}\n".encode('utf8'))
            except socket.error:
                raise ClientError

            try:
                data = sock.recv(4096)
            except socket.timeout:
                raise ClientError
            if data != b"ok\n\n":
                raise ClientError


class ClientError(Exception):
    pass
