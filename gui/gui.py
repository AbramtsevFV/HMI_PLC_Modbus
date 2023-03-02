import os
import sys
from tkinter import *
from conect.modbus import Modbus

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

params_write = {
    "unpack_format": ">HHHBBHH",
    "format_string": ">HHHBBHH",
    "Tx_Transaction_ID": 1,
    "Tx_Protocol_ID": 0,
    "Tx_Message_length": 6, # Количество параметров
    "Tx_MODBUS_address":1,
    "Tx_MODBUS_function": 6,
    "Tx_Register_address": 1 ,#int(Register_address) & 0xFFFF  # Limit address
    "Tx_Register_count": 1,

}

class App:
    def __init__(self, width=300, height=120, title='MB', resizable=(False, False)):
        self.lable_r0 = None
        self.front = Tk()
        self.front.title(title)
        self.front.geometry(f'{width}x{height}+200+200')
        self.front.resizable(*resizable)
        if (sys.platform.startswith('win')):
            # Favico для windows
            self.front.iconbitmap(default='./gui/images/favico.ico')
        else:
            print(sys.platform.startswith('linux'))
            # Favico для linux
            logo = PhotoImage(file='./gui/images/favico.gif')
            self.front.call('wm', 'iconphoto',  self.front._w, logo)


        self.entry_r0 = Entry()
        self.modbus = Modbus()

    def run(self):
        teg = self.modbus.read_write_teg(params_read)[-1]
        self.draw_widgets(teg)
        self.draw_input_field()
        self.draw_button()
        self.front.mainloop()

    def draw_input_field(self, anchor=NW, padx=20, pady=0):
        self.entry_r0.pack(anchor=anchor, padx=padx, pady=pady)

    def get_data(self, data, lable):
        d = data.get()
        if d and d.isdigit():
            params_write["Tx_Register_count"] = int(d)
            response = self.modbus.read_write_teg(params_write)[-1]
            lable['foreground'] = "black"
            lable['text'] = f"Текущее значение тега № {params_write['Tx_MODBUS_address']}: {response}"
        else:
            lable['text'] = "Данные должны быть числовые"
            lable['foreground'] = "red"


    def write_read(self):
        self.modbus.read_write_teg()

    def draw_button(self, anchor=NW, padx=20, pady=5):
        Button(self.front, text='Записать', command=lambda: self.get_data(self.entry_r0, self.lable_r0)).pack(anchor=anchor, padx=padx, pady=pady)
        Button(self.front, text='Выход', command=self.front.destroy).pack(anchor=SE, padx=10, pady=0)

    def draw_widgets(self, data: str, anchor=NW, padx=20, pady=0):
        text = f"Текущее значение тега: {data}"
        self.lable_r0 = Label(self.front, text=text)
        self.lable_r0.pack(anchor=anchor, padx=padx, pady=pady)



