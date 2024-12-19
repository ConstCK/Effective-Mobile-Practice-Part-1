from __future__ import annotations
import random
import time


class Data:
    """Данные для передачи по локальной сети"""

    def __init__(self, data: str, ip: int) -> None:
        self.data = data
        self.ip = ip

    def __repr__(self) -> str:
        return f'Данные {self.data} для сервера с IP {self.ip}'


class Server:
    """Сервер в локальной сети для получения и передачи данных"""

    ip = 0

    def __new__(cls, *args, **kwargs):
        # Создание сквозной нумерации для экземпляров класса
        cls.ip += 1
        return super().__new__(cls, *args, **kwargs)

    def __init__(self) -> None:
        self.router = None
        self.ip = self._set_ip()
        self.buffer: list[Data] = list()

    def __repr__(self) -> str:
        return f'Сервер с IP {self.ip}'

    def get_ip(self) -> int:
        # Получение IP для экземпляра класса
        return self.ip

    @classmethod
    def _set_ip(cls) -> int:
        # Присвоение IP для экземпляра класса
        return cls.ip

    def send_data(self, data: Data) -> None:
        # Передача данных на связанный роутер
        if not self.router:
            print('Соединение не установленно...')
        else:
            print(f'Передача данных с {self}...')
            time.sleep(random.randint(1, 3))
            self.router.buffer.append(data)
            print('Данные успешно переданы...')

    def get_data(self) -> list[Data]:
        # Получение всех данных из буфера сервера с очисткой в завершении
        result = self.buffer.copy()
        [print(f'Данные №{n}:', x.data) for n, x in enumerate(result, 1)]
        self.buffer.clear()
        return result


class Router:
    """Роутер в локальной сети для связи серверов и передачи данных"""

    def __init__(self):
        self.buffer: list[Data] = list()
        self.name = 'Роутер: TP-Link Archer AX53'
        self.servers: set[Server] = set()

    def __repr__(self) -> str:
        return f'{self.name}'

    def link(self, server: Server) -> None:
        # Установка соединения с указанным сервером
        print(f'Соединение с {server} устанавливается...')
        time.sleep(1)
        server.router = self
        self.servers.add(server)
        print(f'Соединение с {server} установлено...')

    def unlink(self, server: Server) -> None:
        # Разрыв соединения с указанным сервером
        server.router = None
        self.servers.discard(server)
        print(f'Соединение с {server} разорвано...')

    def send_data(self) -> None:
        # Отправка данных на сервер при условии установленного соединения
        #  с последующей очисткой буфера
        for data in self.buffer:
            try:
                server = list(
                    filter(lambda x: x.ip == data.ip, self.servers))[0]
                server.buffer.append(data)
                time.sleep(0.5)
                print(f'Данные успешно переданы на сервер с IP {data.ip}')
            except IndexError:
                print(f'Ошибка передачи данных на сервер с IP {data.ip}')

        self.buffer.clear()
        print('Передача данных завершена...')
