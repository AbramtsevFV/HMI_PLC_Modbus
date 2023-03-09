import sys
from tkinter import *
from tkinter.ttk import Combobox

from conect.modbus import Modbus

params_read = {
    "unpack_format": ">HHHBBBHHH",
    "format_string": ">HHHBBHH",
    "Tx_Transaction_ID": 1,
    "Tx_Protocol_ID": 0,
    "Tx_Message_length": 6,
    "Tx_MODBUS_address": 1,
    "Tx_MODBUS_function": 3,
    "Tx_Register_address": 0,
    "Tx_Register_count": 3
}

params_write = {
    "unpack_format": ">HHHBBHH",
    "format_string": ">HHHBBHH",
    "Tx_Transaction_ID": 1,
    "Tx_Protocol_ID": 0,
    "Tx_Message_length": 6,  # Количество параметров
    "Tx_MODBUS_address": 1,
    "Tx_MODBUS_function": 6,
    "Tx_Register_address": 1,  # int(Register_address) & 0xFFFF  # Limit address
    "Tx_Register_count": 1,

}
""""Данный класс описывает работу всего приложения"""

class App:
    def __init__(self, width=500, height=350, title='MB', resizable=(False, False)):

        self.front = Tk()
        self.front.title(title)
        self.front.geometry(f'{width}x{height}+200+200')
        self.front.resizable(*resizable)
        # self.check_os()

        self.combox_list = ['True', 'False']
        self.label_r0 = Label(self.front)
        self.label_r1 = Label(self.front)
        self.label_r2 = Label(self.front)
        self.entry_r0 = Entry()
        self.entry_r1 = Entry()
        self.entry_r2 = Combobox(values=self.combox_list, state='readonly')
        self.modbus = Modbus()

        self.err_con = None

    def check_os(self):
        """Метод проверяет оs и формирует """
        if (sys.platform.startswith('win')):
            # Favico для windows
            self.front.iconbitmap(default='./gui/images/favico.ico')
        else:
            # Favico для linux
            logo = PhotoImage(file='./gui/images/favico.gif')

            self.front.tk.call('wm', 'iconphoto', self.front._w, logo)


    def update_and_run(self, new=True):
        """Метод обновляет выводимве данные и добавляет кнопки"""

        widgets_lst = [self.label_r0, self.label_r1, self.label_r2]
        entry_lst = [self.entry_r0, self.entry_r1, self.entry_r2]
        tags_list = self.modbus.read_write_teg(params_read)[6:]

        for num, value in enumerate(zip(tags_list, widgets_lst, entry_lst)):
            data, widget, entry = value
            self.draw_widget(widget=widget, num=num, data=data)
            entry.delete(0, END)
            entry.insert(1, data)
            if new:
                self.draw_input_field(entry)
                func = lambda x=entry, y=widget, z=num: self.write_teg(x, y, z)
                self.draw_button(text='Записать', func=func)

    def reconnect(self):
        "Перезапуск программы "
        self.front.destroy()
        m = App()
        m.run()



    def run(self):
        """ Метод собирает приложение"""

        if self.modbus.client_socket:
            self.update_and_run()
            self.draw_button(text='Считать  значение всех тегов', func=lambda x=False: self.update_and_run(x))
        else:
            self.err_con = Label(foreground='red', text= 'Подключение к устройству ModBus не выполнено', )
            self.err_con.pack(anchor=NW, padx=20, pady=5)
            self.draw_button(text='Подключить', func=self.reconnect, anchor=SE, padx=10, pady=5)

        self.draw_button(text='Выход', func=self.front.destroy, anchor=SE, padx=10, pady=5)
        self.front.mainloop()

    @staticmethod
    def draw_input_field(entry, anchor=NW, padx=20, pady=0):
        "Метод создаёт поля ввода"
        entry.pack(anchor=anchor, padx=padx, pady=pady)

    def write_teg(self, data, lable: Label, num):
        """Метод записывает данные в теги"""
        d = data.get()
        if d and d.isdigit() or d in self.combox_list:
            if d in self.combox_list:
                d = eval(d)
            params_write["Tx_Register_count"] = int(d)
            params_write["Tx_Register_address"] = num
            response = self.modbus.read_write_teg(params_write)[-1]
            lable['foreground'] = "black"
            lable['text'] = f"Текущее значение тега № {num}: {response}"
        else:
            lable['text'] = "Данные должны быть числовые"
            lable['foreground'] = "red"

    def draw_button(self, text: str, func, anchor=NW, padx=20, pady=5):
        """Создаём кнопку"""
        Button(self.front, text=text, command=func).pack(anchor=anchor, padx=padx, pady=pady)

    @staticmethod
    def draw_widget(widget, num: int, data: str, anchor=NW, padx=20, pady=0):
        """Создаёт виджет и вставляет текст"""
        text = f"Текущее значение тега № {num}: {data}"
        widget.config(text=text)
        widget.pack(anchor=anchor, padx=padx, pady=pady)
