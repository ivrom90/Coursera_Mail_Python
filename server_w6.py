import asyncio


class ClientServerProtocol(asyncio.Protocol):
    def __init__(self):
        self.vault = {}


    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = self._process_data(data.decode())
        self.transport.write(resp.encode())

    def _process_data(self, data):
        data = data.strip()
        if data:
            answer = ''
            status, payload = data.split(" ", 1)
            # Вставка метрик по ключу
            if status == 'put':
                try:
                    name, metric, timestamp = payload.split()
                    if name not in self.vault:
                        self.vault[name] = []
                    self.vault[name].append((float(metric), int(timestamp)))
                except:
                    return 'error\nwrong command\n\n'
                return 'ok\n\n'

            # Запрос метрик по ключу
            elif status == 'get':
                try:
                    key = payload
                    if key == '*':
                        # Вывод всех метрик
                        for key, tupl  in self.vault.items():
                            tupl = sorted(tupl, key=lambda x: x[1])
                            for metr, tms in tupl:
                                answer += (' '.join((key, str(metr), str(tms))) + '\n')
                        return f'ok\n{answer}\n\n'

                    elif key in self.vault:
                        # Вывод конкретной метрики
                        self.vault[key] = sorted(self.vault[key], key=lambda x: x[1])
                        for item in self.vault[key]:
                            metr, tms = item
                            answer += (' '.join((key, str(metr), str(tms))) + '\n')
                        return f'ok\n{answer}\n\n'

                    else:
                        return 'ok\n\n'
                except:
                    return 'error\nwrong command\n\n'
            else:
                return 'error\nwrong command\n\n'


def run_server(host, port):
    # функция запуска сервера
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

# Запуск проверки сервера на локальной станции
if __name__ == "__main__":
    run_server("127.0.0.1", 10001)
