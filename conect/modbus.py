import struct
import socket


class Modbus:

    def __init__(self, ip='192.168.0.19'):
        self.ip = ip
        self.client_socket = self.check_connect()

    def check_connect(self):
        """Проверяет подключение"""
        try:
            modbus = socket.create_connection((self.ip, 502))
        except:
            modbus = False
        return modbus

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
        self.client_socket.send(pack)

    def get_response(self) -> bytes:
        """Метод возвращает ответ от ПЛК"""
        return self.client_socket.recv(1500)

    def read_write_teg(self, params: dict):
        """Метод читает теги"""
        unpack_format = params.pop('unpack_format')
        pack = self.get_pack_package(params)
        self.send_request(pack)
        request = self.get_response()
        params['unpack_format'] = unpack_format
        return self.unpack(unpack_format, request)

# params_read = {
#     "unpack_format": ">HHHBBBHHH",
#     "format_string": ">HHHBBHH",
#     "Tx_Transaction_ID": 1,
#     "Tx_Protocol_ID": 0,
#     "Tx_Message_length": 6,
#     "Tx_MODBUS_address": 1,
#     "Tx_MODBUS_function": 3,
#     "Tx_Register_address": 0,
#     "Tx_Register_count": 3
# }
# mb = Modbus()
#
# print(mb.read_write_teg(params_read)[6:])
