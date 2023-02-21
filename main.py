
from conect.modbus import Modbus

modbus = Modbus()

params_read = {
    "unpack_format": ">HHHBBBH",
    "format_string": ">HHHBBHH",
    "Tx_Transaction_ID": 1,
    "Tx_Protocol_ID": 0,
    "Tx_Message_length": 6,
    "Tx_MODBUS_address": 1,
    "Tx_MODBUS_function": 3,
    "Tx_Register_address": 1,
    "Tx_Register_count": 1
}

print(f"Текущее значение тега 1: {modbus.read_write_teg(params_read)[-1]}")

n = int(input("новое значение: "))

params_write = {
    "unpack_format": ">HHHBBHH",
    "format_string": ">HHHBBHH",
    "Tx_Transaction_ID": 1,
    "Tx_Protocol_ID": 0,
    "Tx_Message_length": 6, # Количество параметров
    "Tx_MODBUS_address":1,
    "Tx_MODBUS_function": 6,
    "Tx_Register_address": 1 ,#int(Register_address) & 0xFFFF  # Limit address
    "Tx_Register_count": n,

}

print(f"Новое значение {modbus.read_write_teg(params_write)[-1]}")


