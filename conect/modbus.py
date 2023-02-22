import struct
import socket


class Modbus:

    def __init__(self, ip='127.0.0.1'):
        self.client_soscket = socket.create_connection((ip, 502))

    @staticmethod
    def get_pack_package(params: dict):
        """
        "Tx_Transaction_ID": 1,
        "Tx_Protocol_ID": 0,
         # 03 Read Holding Registers
        # 06 Write Holding Registers
        Tx_MODBUS_function = 3

        # адрес регистра (тега)
        Tx_Register_address = 0

        # Количество регистров от номера регистра(тега)
        # Работает Если теги одного типа.
        Tx_Register_count = 4
        """

        return struct.pack(*params.values())

    @staticmethod
    def unpack(unpack_format: str, data: bytes) -> tuple:
        """Конвертирует данные"""
        return struct.unpack(unpack_format, data)

    def send_request(self, pack: struct) -> None:
        """Метод отправляет запрос GKR"""
        self.client_soscket.send(pack)

    def get_response(self) -> bytes:
        """Метод возвращает ответ от ПЛК"""
        return self.client_soscket.recv(1500)

    def read_write_teg(self, params: dict):
        """Метод читает теги"""
        unpack_format = params.pop('unpack_format')
        pack = self.get_pack_package(params)
        self.send_request(pack)
        request = self.get_response()
        params['unpack_format'] = unpack_format
        return self.unpack(unpack_format, request)
