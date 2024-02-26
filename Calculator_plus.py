from numpy import arange
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox
from math import *
from tkinter import *


class Standard_Calculator:

    def __init__(self):
        self.calculator_std = Tk()
        self.calculator_std.geometry('410x550')
        self.calculator_std.resizable(0, 0)
        self.calculator_std.title('Standard Calculator')
        self.calculator_std.iconbitmap('calculator.ico')

        self.ans = 0  # Gan ans = 0
        self.var = StringVar()

        self.frame_screen = self.frame_screen()
        self.total_expression = ""  # Giá trị đầu của vùng nhập phép tính
        self.current_expression = ""  # Giá trị đầu của vùng hiển thị kết quả

        # total_label là vùng nhập, label là vùng hiện kết quả
        self.total_label, self.label = self.display_label()

        # Frame thanh công cụ:
        self.frame_tools = self.frame_tools()
        # Các nút trên thanh công cụ
        self.button_tools = self.button_tools()

        self.text_standard = {
            '(': (1, 1), ')': (1, 2), '\u221A': (1, 3), '\u00F7': (1, 4),  # \u unicode
            '7': (2, 1), '8': (2, 2), '9': (2, 3), '\u00D7': (2, 4),
            '4': (3, 1), '5': (3, 2), '6': (3, 3), '\u2212': (3, 4),
            '1': (4, 1), '2': (4, 2), '3': (4, 3), '\u002B': (4, 4),
            '0': (5, 1), '.': (5, 2), 'ans': (5, 3), '\u21A9': (5, 4)
        }
        # Frame Phím cơ bản cho máy tính
        self.frame_button_standard = self.frame_button_standard()
        # Tạo các phím cơ bản
        self.button_standard = self.button_standard()

        self.frame_history = self.frame_history()
        self.history = self.scrollbar_history()

        self.actualHistoryOperation = StringVar()
        self.actualHistoryOperation.trace('w', self.disable_clearall_button)
        self.input_from_keyboard()

    def frame_screen(self):
        frame = Frame(self.calculator_std, height=221, bg='#4781B9')
        frame.configure(relief='groove', padx=3, pady=2)
        frame.place(x=0, y=230)
        return frame

    def frame_history(self):
        frame = Frame(self.calculator_std, height=200)
        frame.configure(relief='groove', padx=0, pady=0)
        frame.place(x=0, y=0)
        return frame

    # Method tạo frame thanh công cụ
    def frame_tools(self):
        frame = Frame(self.calculator_std, height=221, bg='#EDEDED')
        frame.configure(relief='groove')
        frame.place(x=5, y=280)
        return frame

    def frame_button_standard(self):
        frame = Frame(self.calculator_std, height=221, bg='#EDEDED')
        frame.configure(relief='groove')
        frame.place(x=2, y=325)
        return frame

    def scrollbar_history(self):
        scrollbar = Scrollbar(self.frame_history, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)
        history = Text(self.frame_history, width=32, heigh=8, wrap=NONE,
                       font=("Times", 18),
                       state="disabled",
                       yscrollcommand=scrollbar.set)
        history.pack(side=TOP, fill=X)
        scrollbar.config(command=history.yview)
        return history

    # Method tạo hiển thị các label để nhập + hiện kết quả trong frame screen
    def display_label(self):
        total_label = Label(self.frame_screen, text=self.total_expression, width=24, heigh=2, bd=0, font=("Times", 14),
                            bg='white', anchor=W)
        total_label.pack(side=LEFT)

        label = Label(self.frame_screen, text=self.current_expression, width=16, heigh=2, bd=0, font=("Times", 14),
                      bg='white', anchor=E)
        label.pack(fill='both', side=RIGHT)
        return total_label, label

    def button_tools(self):
        global clear_button

        button1 = Button(self.frame_tools, text='StdCal', bd=1, bg='#EDEDED',
                         font=('tahoma', 10), width=8)
        button2 = Button(self.frame_tools, text='SciCal', bd=1, bg='#EDEDED',
                         font=('tahoma', 10), width=8, command=Scientific_Caculator)
        button3 = Button(self.frame_tools, text='Plot', bd=1, bg='#EDEDED',
                         font=('tahoma', 10), width=8, command=Plot)
        button1.pack(padx=2, pady=2, side=LEFT)
        button2.pack(padx=2, side=LEFT)
        button3.pack(padx=2, side=LEFT)

        clear_button = Button(self.frame_tools, text="clear all", bd=0, bg='#EDEDED',
                              font=("tahoma, 10"), width=10, state='disabled',
                              command=self.clear_all)
        clear_button.pack(padx=2, side=LEFT)

        AC_button = Button(self.frame_tools, text="C", bd=1, bg='#EDEDED',
                           font=("tahoma, 10"), width=5, heigh=2,
                           command=self.C)
        AC_button.pack(padx=3, side=LEFT)

        backspace_button = Button(self.frame_tools, text="\u232B", bd=1, bg='#EDEDED',
                                  font=("tahoma, 10"), width=4, heigh=2,
                                  command=self.backsapce)
        backspace_button.pack(padx=5, side=RIGHT)

    def disable_clearall_button(self, *args):
        global clear_button
        if self.actualHistoryOperation.get():
            clear_button.config(state='normal')
        else:
            clear_button.config(state='disabled')

    def button_standard(self):
        for text, location in self.text_standard.items():

            if location[1] == 4 or text == 'ans':
                button = Button(self.frame_button_standard, text=text, bg='white', bd=1,
                                width=9, heigh=1, font=('Times', 14, 'italic'),
                                command=lambda x=text: self.add_to_expression(x))
                # Hàm ẩn lambda để với mỗi lần nhấn phím thì biểu thức sẽ được add là vùng nhập
                button.grid(row=location[0],
                            column=location[1], padx=5, pady=5)
                if text == 'ans':
                    button['width'] = 8

                if text == '\u21A9':  # Nut Enter mau xanh
                    button = Button(self.frame_button_standard, text=text, bg='#4781B9', bd=1,
                                    width=9, heigh=1, font=('Times', 14, 'italic'),
                                    command=self.evaluate)
                    button.grid(row=location[0],
                                column=location[1], padx=5, pady=5)
            else:
                if location[0] == 1:
                    button = Button(self.frame_button_standard, text=text, bg='white', bd=1,
                                    width=8, heigh=1, font=('Times', 14),
                                    command=lambda x=text: self.add_to_expression(x))
                    button.grid(row=location[0],
                                column=location[1], padx=5, pady=5)
                else:
                    button = Button(self.frame_button_standard, text=text, bg='#CACACA', bd=1,
                                    width=8, heigh=1, font=('Times', 14),
                                    command=lambda x=text: self.add_to_expression(x))
                    button.grid(row=location[0],
                                column=location[1], padx=5, pady=5)

    # Phương thức để khi nhấn 1 phím thì text sẽ hiện lên trên màn hình hiển thị
    # value là chữ khi nhấn phím thì sẽ hiển thị lên
    def add_to_expression(self, value):
        if value == '\u221A':
            self.total_expression += str(value) + '('
        else:
            # Giá trị của vùng nhập phép tính
            self.total_expression += str(value)

        self.update_total_label()  # Update Label hiển thị phép tính

    # Method tính toán để gán vào phím enter
    def evaluate(self):
        operator = {'\u00F7': '/', '\u00D7': '*',
                    '\u2212': '-', '\u002B': '+', '\u221A': 'sqrt'}
        express = self.total_label['text']
        a = express.count('(') - express.count(')')
        if a > 0:
            express += ')' * a
            self.total_expression = express
            self.update_total_label()
        # Thay the ans bang gia tri da luu tru trong bien self.ans
        if 'ans' in express:
            express = express.replace('ans', str(self.ans))

        # VÒng lap thay the ky tu Unicode sang ky tu python hieu
        for i in express:
            if str(i) in list(operator.keys()):
                express = express.replace(i, operator[i])

        try:
            self.current_expression = "= " + str(eval(express))[:13] + ' '
        except Exception:
            self.current_expression = "Math Error "

        finally:
            self.update_label()

        if self.current_expression != "Math Error ":
            self.add_history()
            self.add_ans()

    # Method update Label hiện phép tính khi nhập
    def update_total_label(self):
        self.total_label.configure(text=self.total_expression)

    # Method update label kết quả
    def update_label(self):
        self.label.configure(text=self.current_expression)

    def clear_all(self):
        self.actualHistoryOperation.set("")
        self.history.config(state=NORMAL)
        self.history.delete(1.0, END)
        self.history.config(state=DISABLED)

        self.total_expression = ""
        self.current_expression = ""
        self.update_total_label()
        self.update_label()
        self.add_ans()
        return

    def C(self):
        self.total_expression = ""
        self.current_expression = ""
        self.update_total_label()
        self.update_label()
        return

    def backsapce(self):
        if self.total_expression != "":
            self.total_expression = self.total_expression[0:len(
                self.total_expression) - 1]
            self.current_expression = ""
            self.update_total_label()
            self.update_label()
        else:
            pass

    def add_history(self):
        self.actualHistoryOperation.set(
            '\n' + ' ' * 2 + self.total_expression + " \t" * 3 + self.current_expression + '\n\n')
        self.history.config(state=NORMAL)
        self.history.insert(INSERT, self.actualHistoryOperation.get())
        self.history.config(state=DISABLED)

    def add_ans(self):
        if self.current_expression == "":
            self.ans = '0'
        else:
            self.ans = self.current_expression[2::]

    def input_from_keyboard(self):
        self.calculator_std.bind('<Return>', lambda event: self.evaluate())
        self.calculator_std.bind('<BackSpace>', lambda event: self.backsapce())
        self.calculator_std.bind('<c>', lambda event: self.C())
        self.calculator_std.bind('<Delete>', lambda event: self.clear_all())
        self.calculator_std.bind(
            '<Key>', lambda event: self.add_to_expression(event.char))

        btn_std = ['(', ')', '.', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        btn_opr = {"/": "\u00F7", "*": "\u00D7",
                   "-": '\u2212', '+': '\u002B'
                   }

        for key in btn_std:
            self.calculator_std.bind(
                str(key), lambda event, digit=key: self.add_to_expression(digit))

        for key in btn_opr:
            self.calculator_std.bind(
                key, lambda event, operator=key: self.add_to_expression(operator))

    def run(self):
        self.calculator_std.mainloop()


bg_gray = '#EDEDED'
font_display = ('Times New Roman', 24, 'bold')
function_params = {'fg': 'black', 'bg': '#EDEDED',
                   'font': ('Times New Roman', 10)}
button_params = {'fg': 'black', 'bg': 'white', 'font': ('Times New Roman', 10)}
enter_button_params = {'fg': 'white',
                       'bg': '#4781B9', 'font': ('Times New Roman', 10)}
button_params_main = {'fg': 'black',
                      'bg': '#CBCBCB', 'font': ('Times New Roman', 10)}


class Scientific_Caculator:
    def __init__(self):
        self.tk_calc = Tk()
        self.tk_calc.geometry('600x588')
        self.tk_calc.resizable(0, 0)
        self.tk_calc.title("Scientific Calculator")
        self.tk_calc.iconbitmap('calculator.ico')
        self.total_expression = ""
        self.current_expression = ""
        self.Ans = "0"
        self.actualHistoryOperation = StringVar()
        self.switch_variable = StringVar(value="Deg")
        self.radians_switch_variable = "Deg"
        self.history_frame = self.create_history_frame()
        self.display_frame = self.create_display_frame()
        self.total_label, self.label = self.create_display_labels()
        self.function_frame = self.create_function_frame()
        self.history = self.scrollbar_history()
        self.create_all_functions()
        self.buttons_frame = self.create_buttons_frame()
        self.create_all_buttons()
        self.enter_from_keyboard()

    def create_history_frame(self):
        frame = Frame(self.tk_calc, height=284, bg=bg_gray)
        frame.pack(expand=True, fill='both')
        return frame

    def scrollbar_history(self):
        scrollbar = Scrollbar(self.history_frame, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)
        history = Text(self.history_frame, width=600, heigh=12, wrap=NONE,
                       font=("Times New Roman", 18),
                       state="disabled",
                       yscrollcommand=scrollbar.set)
        history.pack(side=TOP, fill=X)
        scrollbar.config(command=history.yview)
        return history

    # vẽ cái màn hình máy tính

    def create_display_labels(self):
        total_label = Label(self.display_frame, text=self.total_expression,
                            anchor=W, bg='white', fg='black', padx=24, font=font_display)
        total_label.pack(expand=True, fill='both')
        label = Label(self.display_frame, text=self.current_expression,
                      anchor=E, bg='white', fg='black', padx=24, font=font_display)
        label.pack(expand=True, fill='both')
        return total_label, label

    def create_display_frame(self):
        frame = Frame(self.tk_calc, height=92, bg=bg_gray)
        frame.pack(expand=True, fill='both')
        return frame

    # vẽ cái thanh công cụ

    def create_all_functions(self):
        self.function_frame.columnconfigure(0, weight=2)
        self.function_frame.columnconfigure(1, weight=2)
        self.function_frame.columnconfigure(2, weight=2)
        self.function_frame.columnconfigure(3, weight=1)
        self.function_frame.columnconfigure(4, weight=2)
        self.function_frame.columnconfigure(5, weight=2)
        self.function_frame.columnconfigure(6, weight=2)
        self.function_frame.columnconfigure(7, weight=2)
        self.function_frame.columnconfigure(8, weight=1)
        self.function_frame.columnconfigure(9, weight=2)
        self.function_frame.columnconfigure(10, weight=2)

        set_button = Button(self.function_frame,
                            function_params, text="Help input", command=lambda: self.help())
        set_button.grid(column=0, row=0,
                        sticky=NSEW, padx=2, pady=10)
        exit_button = Button(self.function_frame, function_params,
                             text="Exit", command=self.tk_calc.destroy)
        exit_button.grid(column=1, row=0, sticky=NSEW, padx=2, pady=10)

        blank = Label(self.function_frame, text="")
        blank.grid(column=3, row=0)

        plot_button = Button(self.function_frame, function_params,
                             text="Arc", command=lambda: self.button_click('a'))
        plot_button.grid(column=4, row=0, sticky=NSEW, padx=2, pady=10)

        rad_button = Checkbutton(self.function_frame, function_params,
                                 text="Radians", variable=self.switch_variable, onvalue="Rad", offvalue="Deg", command=lambda: self.check_radians())
        rad_button.grid(column=5, row=0, sticky=NSEW, padx=2, pady=10)

        round_button = Button(self.function_frame,
                              function_params, text="Round", command=lambda: self.button_click('round('))
        round_button.grid(column=6, row=0,
                          sticky=NSEW, padx=2, pady=10)

        blank = Label(self.function_frame, text="")
        blank.grid(column=8, row=0)

        del_button = Button(self.function_frame, enter_button_params,
                            text="Del", command=lambda: self.delete())
        del_button.grid(column=9, row=0, sticky=NSEW, padx=2, pady=10)
        clear_button = Button(
            self.function_frame, enter_button_params, text="AC", command=lambda: self.clear())
        clear_button.grid(column=10, row=0, sticky=NSEW, padx=2, pady=10)

    def create_function_frame(self):
        frame = Frame(self.tk_calc, height=44, bg=bg_gray)
        frame.pack(expand=True, fill='both')
        return frame

    # vẽ cái bàn phím máy tính

    def create_all_buttons(self):
        self.buttons_frame.columnconfigure(0, weight=2)
        self.buttons_frame.columnconfigure(1, weight=2)
        self.buttons_frame.columnconfigure(2, weight=2)
        self.buttons_frame.columnconfigure(3, weight=1)
        self.buttons_frame.columnconfigure(4, weight=2)
        self.buttons_frame.columnconfigure(5, weight=2)
        self.buttons_frame.columnconfigure(6, weight=2)
        self.buttons_frame.columnconfigure(7, weight=2)
        self.buttons_frame.columnconfigure(8, weight=1)
        self.buttons_frame.columnconfigure(9, weight=2)
        self.buttons_frame.columnconfigure(10, weight=2)
        self.buttons_frame.rowconfigure(0, weight=1)
        self.buttons_frame.rowconfigure(1, weight=1)
        self.buttons_frame.rowconfigure(2, weight=1)
        self.buttons_frame.rowconfigure(3, weight=1)

        second_button = Button(
            self.buttons_frame, button_params, text="x\u00B2", command=lambda: self.button_click('^2'))
        second_button.grid(column=0, row=0, sticky=NSEW, padx=2, pady=2)
        nth_power = Button(self.buttons_frame, button_params,
                           text="x^n", command=lambda: self.button_click('^'))
        nth_power.grid(column=1, row=0, sticky=NSEW, padx=2, pady=2)
        abs_button = Button(self.buttons_frame, button_params,
                            text="|x|", command=lambda: self.button_click('abs('))
        abs_button.grid(column=2, row=0, sticky=NSEW, padx=2, pady=2)

        sqrt_button = Button(self.buttons_frame, button_params,
                             text="\u00B2\u221A", command=lambda: self.button_click('\u221A'))
        sqrt_button.grid(column=0, row=1, sticky=NSEW, padx=2, pady=2)
        nth_root = Button(self.buttons_frame, button_params,
                          text="\u207F\u221A", command=lambda: self.button_click('^(1/'))
        nth_root.grid(column=1, row=1, sticky=NSEW, padx=2, pady=2)
        pi_button = Button(self.buttons_frame, button_params,
                           text="π", command=lambda: self.button_click('π'))
        pi_button.grid(column=2, row=1, sticky=NSEW, padx=2, pady=2)

        sin_button = Button(self.buttons_frame, button_params, text="sin",
                            command=lambda: self.button_click('sin(R('))
        sin_button.grid(column=0, row=2, sticky=NSEW, padx=2, pady=2)
        cos_power = Button(self.buttons_frame, button_params, text="cos",
                           command=lambda: self.button_click('cos(R('))
        cos_power.grid(column=1, row=2, sticky=NSEW, padx=2, pady=2)
        tan_button = Button(self.buttons_frame, button_params, text="tan",
                            command=lambda: self.button_click('tan(R('))
        tan_button.grid(column=2, row=2, sticky=NSEW, padx=2, pady=2)

        left_button = Button(self.buttons_frame, button_params,
                             text="(", command=lambda: self.button_click('('))
        left_button.grid(column=0, row=3, sticky=NSEW, padx=2, pady=2)
        right_power = Button(self.buttons_frame, button_params,
                             text=")", command=lambda: self.button_click(')'))
        right_power.grid(column=1, row=3, sticky=NSEW, padx=2, pady=2)
        factorial_button = Button(
            self.buttons_frame, button_params, text="x!", command=lambda: self.button_click('!('))
        factorial_button.grid(column=2, row=3, sticky=NSEW, padx=2, pady=2)

        blank = Label(self.buttons_frame, text="")
        blank.grid(column=3, row=0)

        button_7 = Button(self.buttons_frame, button_params_main,
                          text=" 7 ", command=lambda: self.button_click('7'))
        button_7.grid(column=4, row=0, sticky=NSEW, padx=2, pady=2)
        button_8 = Button(self.buttons_frame, button_params_main,
                          text=" 8 ", command=lambda: self.button_click('8'))
        button_8.grid(column=5, row=0, sticky=NSEW, padx=2, pady=2)
        button_9 = Button(self.buttons_frame, button_params_main,
                          text=" 9 ", command=lambda: self.button_click('9'))
        button_9.grid(column=6, row=0, sticky=NSEW, padx=2, pady=2)
        div_button = Button(self.buttons_frame, button_params,
                            text="\u00F7", command=lambda: self.append_operator('\u00F7'))
        div_button.grid(column=7, row=0, sticky=NSEW, padx=2, pady=2)

        button_4 = Button(self.buttons_frame, button_params_main,
                          text=" 4 ", command=lambda: self.button_click('4'))
        button_4.grid(column=4, row=1, sticky=NSEW, padx=2, pady=2)
        button_5 = Button(self.buttons_frame, button_params_main,
                          text=" 5 ", command=lambda: self.button_click('5'))
        button_5.grid(column=5, row=1, sticky=NSEW, padx=2, pady=2)
        button_6 = Button(self.buttons_frame, button_params_main,
                          text=" 6 ", command=lambda: self.button_click('6'))
        button_6.grid(column=6, row=1, sticky=NSEW, padx=2, pady=2)
        mul_button = Button(self.buttons_frame, button_params,
                            text="\u00D7", command=lambda: self.append_operator('\u00D7'))
        mul_button.grid(column=7, row=1, sticky=NSEW, padx=2, pady=2)

        button_1 = Button(self.buttons_frame, button_params_main,
                          text=" 1 ", command=lambda: self.button_click('1'))
        button_1.grid(column=4, row=2, sticky=NSEW, padx=2, pady=2)
        button_2 = Button(self.buttons_frame, button_params_main,
                          text=" 2 ", command=lambda: self.button_click('2'))
        button_2.grid(column=5, row=2, sticky=NSEW, padx=2, pady=2)
        button_3 = Button(self.buttons_frame, button_params_main,
                          text=" 3 ", command=lambda: self.button_click('3'))
        button_3.grid(column=6, row=2, sticky=NSEW, padx=2, pady=2)
        sub_button = Button(self.buttons_frame, button_params,
                            text="-", command=lambda: self.append_operator('-'))
        sub_button.grid(column=7, row=2, sticky=NSEW, padx=2, pady=2)

        button_0 = Button(self.buttons_frame, button_params_main,
                          text=" 0 ", command=lambda: self.button_click('0'))
        button_0.grid(column=4, row=3, sticky=NSEW, padx=2, pady=2)
        dot_button = Button(self.buttons_frame, button_params_main,
                            text=".", command=lambda: self.button_click('.'))
        dot_button.grid(column=5, row=3, sticky=NSEW, padx=2, pady=2)
        ans_button = Button(self.buttons_frame, button_params,
                            text="Ans", command=lambda: self.button_click('Ans'))
        ans_button.grid(column=6, row=3, sticky=NSEW, padx=2, pady=2)
        add_button = Button(self.buttons_frame, button_params,
                            text="+", command=lambda: self.append_operator('+'))
        add_button.grid(column=7, row=3, sticky=NSEW, padx=2, pady=2)

        blank = Label(self.buttons_frame, text="")
        blank.grid(column=8, row=0)

        percent_button = Button(self.buttons_frame, button_params,
                                text="%", command=lambda: self.button_click('%'))
        percent_button.grid(column=9, row=0, sticky=NSEW, padx=2, pady=2)
        ten_button = Button(self.buttons_frame, button_params,
                            text="10^x", command=lambda: self.button_click('10^'))
        ten_button.grid(column=10, row=0, sticky=NSEW, padx=2, pady=2)

        log_button = Button(self.buttons_frame, button_params_main,
                            text="log\u2081\u2080", command=lambda: self.button_click('log10('))
        log_button.grid(column=9, row=1, sticky=NSEW, padx=2, pady=2)
        ln_button = Button(self.buttons_frame, button_params_main,
                           text="ln", command=lambda: self.button_click('ln('))
        ln_button.grid(column=10, row=1, sticky=NSEW, padx=2, pady=2)

        e_button = Button(self.buttons_frame, button_params_main,
                          text="e", command=lambda: self.button_click('e'))
        e_button.grid(column=9, row=2, sticky=NSEW, padx=2, pady=2)
        exp_button = Button(self.buttons_frame, button_params_main,
                            text="e^x", command=lambda: self.button_click('e^'))
        exp_button.grid(column=10, row=2, sticky=NSEW, padx=2, pady=2)

        eval_button = Button(self.buttons_frame, enter_button_params,
                             text="=", command=lambda: self.evaluate())
        eval_button.grid(column=9, row=3, columnspan=2,
                         sticky=NSEW, padx=2, pady=2)

    def create_buttons_frame(self):
        frame = Frame(self.tk_calc, height=168, bg=bg_gray)
        frame.pack(expand=True, fill='both')
        return frame

    def check_radians(self):
        if self.radians_switch_variable == "Deg":
            self.radians_switch_variable = "Rad"
        else:
            self.radians_switch_variable = "Deg"

        # nhấn nút

    def button_click(self, char):
        self.current_expression = ""
        self.total_expression += str(char)
        if char == "\u221A":
            self.total_expression += '('
        if self.radians_switch_variable == 'Rad':
            if 'sin' in self.total_expression:
                self.total_expression = self.total_expression.replace(
                    'sin(R', 'sin')
            if 'cos' in self.total_expression:
                self.total_expression = self.total_expression.replace(
                    'cos(R', 'cos')
            if 'tan' in self.total_expression:
                self.total_expression = self.total_expression.replace(
                    'tan(R', 'tan')
        if self.radians_switch_variable == 'Deg':
            if 'asin' in self.total_expression:
                self.total_expression = self.total_expression.replace(
                    'asin(R', 'D(asin')
            if 'acos' in self.total_expression:
                self.total_expression = self.total_expression.replace(
                    'acos(R', 'D(acos')
            if 'atan' in self.total_expression:
                self.total_expression = self.total_expression.replace(
                    'atan(R', 'D(atan')
        self.update_total_label()
        self.update_label()

    # nhấn + - * /

    def append_operator(self, operator):
        if self.total_expression == "":
            self.current_expression += operator
            self.total_expression += self.current_expression
            self.current_expression = ""
        else:
            self.total_expression += operator
            self.current_expression = ""
        self.update_total_label()
        self.update_label()

    # AC

    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()

    # DEL

    def delete(self):
        self.current_expression = ""
        text = self.total_expression[:-1]
        self.total_expression = text
        self.update_total_label()
        self.update_label()

    # =

    def evaluate(self):
        operator = {'\u00F7': '/', '\u00D7': '*',
                    '\u2212': '-', '\u002B': '+', '\u221A': 'sqrt', 'π': str(pi), 'e': str(exp(1)), '^': '**', '%': '/100', '!': 'factorial'}
        express = self.total_label['text']
        a = express.count('(') - express.count(')')
        if a > 0:
            express += ')'*a
            self.total_expression = express
            self.update_total_label()
        for i in express:
            if str(i) in list(operator.keys()):
                express = express.replace(i, operator[i])
        other_operator = {'R': 'radians', 'D': 'degrees'}
        for i in express:
            if str(i) in list(other_operator.keys()):
                express = express.replace(i, other_operator[i])
        # Thay the Ans bang gia tri da luu tru trong bien self.ans
        if 'Ans' in express:
            express = express.replace('Ans', str(self.Ans))
        if 'ln' in express:
            express = express.replace('ln', 'log')
        a = express.count('(') - express.count(')')
        if a > 0:
            express += ')'*a
            # VÒng lap thay the ky tu Unicode sang ky tu python hieu
        try:
            self.current_expression += str(eval(express))
            self.add_history()
            self.add_Ans()
        except Exception:
            self.current_expression = "Math Error!"
        self.update_label()

    # ans

    def add_Ans(self):
        if self.current_expression == "":
            self.Ans = '0'
        else:
            self.Ans = self.current_expression

    # hiển thị lịch sử

    def add_history(self):
        self.actualHistoryOperation.set(
            '\n'+' '*2+self.total_expression + " \t"*3 + " = " + self.current_expression + '\n\n')
        self.history.config(state=NORMAL)
        self.history.insert(INSERT, self.actualHistoryOperation.get())
        self.history.config(state=DISABLED)

    def enter_from_keyboard(self):
        self.tk_calc.bind('<Return>', lambda event: self.evaluate())
        self.tk_calc.bind('<BackSpace>', lambda event: self.delete())
        self.tk_calc.bind('<Escape>', lambda event: self.clear())
        self.tk_calc.bind(
            '<Key>', lambda event: self.button_click(event.char))

        btn_std = ['(', ')', '.', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        btn_opr = {"/": "\u00F7", "*": "\u00D7",
                   "-": '\u2212', '+': '\u002B'
                   }

        for key in btn_std:
            self.tk_calc.bind(
                str(key), lambda event, digit=key: self.button_click(digit))

        for key in btn_opr:
            self.tk_calc.bind(
                key, lambda event, operator=key: self.append_operator(operator))
    # Settings

    def help(self):
        messagebox.showinfo("Help input from keyboard",
                            "Enter = Equal button" + '\n' + "Esc = AC button" + '\n' + "BackSpace = Delete button")

    # cập nhật hiển thị phép tính

    def update_total_label(self):
        self.total_label.configure(text=self.total_expression)

    # cập nhật hiển thị kết quả

    def update_label(self):
        self.label.configure(text=self.current_expression)

    # chạy chương trình

    def run(self):
        self.tk_calc.mainloop()


class Plot:
    def __init__(self, root=Tk()):
        self.root = root
        self.root.geometry('540x600')
        self.root.resizable(0, 0)
        self.root.title("Plot")
        self.root.iconbitmap('calculator.ico')
        self.frame = self.create_frame()

        Label(self.frame, text='Choose plot type?').pack()
        Button(self.frame, text='Plot 2D', command=self.plot2D).pack()
        Button(self.frame, text='Plot 3D', command=self.plot3D).pack()
        self.plot2D = Plot2D(master=self.root, app=self)
        self.plot3D = Plot3D(master=self.root, app=self)
        Button(self.frame, text='Exit', command=self.exit).pack()

    def create_frame(self):  # tạo frame chứa Choose Plot
        frame = Frame(self.root)
        frame.pack()
        return frame

    # tạo frame chính
    def main_page(self):
        self.frame.pack()

    # từ frame plot 2D quay về trang chính
    def plot2D(self):
        self.frame.pack_forget()
        self.plot2D.start_page()

    # từ frame plot 3D quay về trang chính
    def plot3D(self):
        self.frame.pack_forget()
        self.plot3D.start_page()
    # thoát chế độ vẽ

    def exit(self):
        self.frame.pack_forget()


class Plot2D:
    # dùng None để app vào nút Plot 2D sẽ được app vào root
    def __init__(self, master=None, app=None):
        self.master = master
        self.app = app
        self.frame = Frame(self.master)
        self.xmin = StringVar()
        self.xmax = StringVar()
        self.ymin = StringVar()
        self.ymax = StringVar()
        self.color = StringVar()
        self.style_lines = StringVar()
        self.maker = StringVar()
        self.var1 = IntVar()
        self.var2 = IntVar()
        self.var = StringVar()

        menu_color = ['b', 'r', 'm', 'g', 'c', 'k', 'y']
        menu_style_lines = ['None', '-', '--', '-.', ':']
        menu_maker = ['None', '.', ',', 'o', 'v', '^', '<', '>']

        # option color
        color = OptionMenu(self.frame, self.color, *menu_color)
        color.grid(row=5, column=1, columnspan=1, sticky=W)
        self.color.set(menu_color[0])
        # option lines
        style_lines = OptionMenu(
            self.frame, self.style_lines, *menu_style_lines)
        style_lines.grid(row=5, column=3, columnspan=1, sticky=W)
        self.style_lines.set(menu_style_lines[1])
        # option marker
        maker = OptionMenu(self.frame, self.maker, *menu_maker)
        maker.grid(row=5, column=5, columnspan=1, sticky=W)
        self.maker.set(menu_maker[1])

        Label(self.frame, text=' PLOT 2D ', bg='lightblue', font=(
            'Times', 14)).grid(row=0, column=2, columnspan=1)
        Label(self.frame, text='x_min ').grid(
            row=2, column=0, columnspan=1, sticky=E)
        Label(self.frame, text='x_max ').grid(
            row=3, column=0, columnspan=1, sticky=E)
        Label(self.frame, text='y_min ').grid(
            row=2, column=2, columnspan=1, sticky=E)
        Label(self.frame, text='y_max ').grid(
            row=3, column=2, columnspan=1, sticky=E)
        Label(self.frame, text='Color  ').grid(
            row=5, column=0, columnspan=1, sticky=E)
        Label(self.frame, text='Line_style ').grid(
            row=5, column=2, columnspan=1, sticky=E)
        Label(self.frame, text='Maker').grid(
            row=5, column=4, columnspan=1, sticky=E)
        Label(self.frame, text='Axis    ').grid(
            row=6, column=0, columnspan=1, sticky=E)
        Label(self.frame, text='Function').grid(
            row=7, column=0, columnspan=1, sticky=E)

        # tạo nút để chọn hiển thị trục toạ độ
        lstCheck = [('X', 1), ('Y', 2)]
        Checkbutton(self.frame, text=lstCheck[0][0], variable=self.var1, onvalue=1, offvalue=0, command=self.plot).grid(
            row=6, column=1, columnspan=1, sticky=W)

        Checkbutton(self.frame, text=lstCheck[1][0], variable=self.var2, onvalue=2, offvalue=0, command=self.plot).grid(
            row=6, column=3, columnspan=1, sticky=W)

        Button(self.frame, text='Go back', command=self.go_back).grid(
            row=1, column=4, columnspan=1, sticky=W)
        Button(self.frame, text='Plot', command=self.plot).grid(
            row=1, column=3, columnspan=1, sticky=E)

        Entry(self.frame, textvariable=self.xmin,
              width=16).grid(row=2, column=1)
        Entry(self.frame, textvariable=self.ymin,
              width=16).grid(row=2, column=3)
        Entry(self.frame, textvariable=self.xmax,
              width=16).grid(row=3, column=1)
        Entry(self.frame, textvariable=self.ymax,
              width=16).grid(row=3, column=3)
        Entry(self.frame, textvariable=self.var, width=20,
              font=('Times', 14)).grid(row=7, column=1)

    # gọi trang bắt đầu là trang plot 2D
    def start_page(self):
        self.frame.pack()

    # trở về trang chính choose plot
    def go_back(self):
        self.frame.pack_forget()
        self.app.main_page()

    # vẽ đồ thị
    def plot(self):
        try:
            # trường hợp người dùng nhập giá trị
            try:
                x1 = self.xmin.get()
                x2 = self.xmax.get()
                y1 = self.ymin.get()
                y2 = self.ymax.get()

                # lấy hàm vẽ có thể từ funtion hoặc từ label của máy tính, ưu tiên funtion
                funtion = self.var.get()

                # tạo giá trị cho x
                x = np.array(arange(float(x1), float(x2) + 1, 0.1))
                # chuyển từ người dùng nhập sang máy hiểu
                lg = {
                    'sin': 'np.sin',
                    'cos': 'np.cos',
                    'tan': 'np.tan',
                    'log': 'np.log',
                    'exp': 'np.exp'
                }
                for i in list(lg.keys()):
                    if i in funtion:
                        funtion = funtion.replace(i, lg[i])
                        if i == 'log':  # do log chỉ nhận giá trị x>0
                            x = np.linspace(0, 10 * 4, 10 * 6)
                            x = x[1::]

                y = eval(funtion)  # hàm sau khi đổi giá trị dùng để vẽ

            except:
                # trường hợp người dùng không nhập lim_x,y
                x1 = -10
                x2 = 10
                y1 = -10
                y2 = 10
                # lấy hàm vẽ có thể từ funtion hoặc từ label của máy tính, ưu tiên funtion
                funtion = self.var.get()

                # dùng dict để chuyển hàm lượng giác về numpy để máy tính hiểu
                lg = {
                    'sin': 'np.sin',
                    'cos': 'np.cos',
                    'tan': 'np.tan',
                    'log': 'np.log',
                    'exp': 'np.exp'
                }
                x = np.array(arange(float(x1), float(x2) + 1, 0.1))

                for i in list(lg.keys()):
                    if i in funtion:
                        funtion = funtion.replace(i, lg[i])
                        if i == 'log':
                            x = np.linspace(0, 10 * 4, 10 * 6)
                            x = x[1::]
                            x1 = 10 ** (-7)
                            x2 = 5
                            y1 = -5
                            y2 = 5

                y = eval(funtion)  # hàm sau khi đổi giá trị dùng để vẽ

            # tạo frame hiển thị đồ thị
            self.frame.plottingFrame = self.frame
            self.frame.functions2Plot = self.frame

            self.frame.firstPlot = False
            self.frame.myFigure = Figure(figsize=(3.5, 3.5), dpi=120)
            self.frame.a = self.frame.myFigure.add_subplot(111)

            # ẩn giá trị của trục toạ độ
            x_axis = self.frame.a.axes.get_xaxis()
            x_axis.set_visible(False)
            y_axis = self.frame.a.axes.get_yaxis()
            y_axis.set_visible(False)

            # ẩn trục toạ độ bên phải và phía trên
            self.frame.a.spines['right'].set_color('none')
            self.frame.a.spines['top'].set_color('none')

            # chuyển trục bên trái và bên dưới lên trung tâm
            self.frame.a.spines['left'].set_position('center')
            self.frame.a.spines['bottom'].set_position('center')

            # ẩn trục vừa chuyển về center
            self.frame.a.spines['left'].set_color('none')
            self.frame.a.spines['bottom'].set_color('none')

            # hiển thị trục toạ độ
            if self.var1.get() == 1:  # khi tick vào trục X
                self.frame.a.spines['bottom'].set_color('black')
                x_axis = self.frame.a.axes.get_xaxis()
                x_axis.set_visible(True)
                self.frame.a.set_xlabel('X Label', loc='right')

            if self.var2.get() == 2:  # khi tick vào trục y
                self.frame.a.spines['left'].set_color('black')
                y_axis = self.frame.a.axes.get_yaxis()
                y_axis.set_visible(True)
                self.frame.a.set_ylabel('Y Label', loc='top')

            # if self.var2.get() == 3:
            #     self.frame.a.grid(True)

            self.frame.canvas = FigureCanvasTkAgg(
                self.frame.myFigure, self.frame.plottingFrame)
            self.frame.canvas.draw()
            self.frame.canvas.get_tk_widget().grid(row=8, column=0, columnspan=10)
            self.frame.canvas._tkcanvas.grid(row=8, column=0, columnspan=10)

            # set x,y value
            self.frame.a.set_xlim([float(x1), float(x2)])
            self.frame.a.set_ylim([float(y1), float(y2)])
            self.frame.a.plot(x, y, color=self.color.get(
            ), linestyle=self.style_lines.get(), marker=self.maker.get())  # vẽ đồ thị

        except:
            self.root = Tk()
            self.root.geometry('200x50')
            self.root.resizable(0, 0)
            self.root.title('ERROR!')
            Label(self.root, text='ERROR!').pack()


class Plot3D:
    # dùng None để app vào nút Plot 2D sẽ được app vào root
    def __init__(self, master=None, app=None):
        self.master = master
        self.app = app
        self.frame = Frame(self.master)
        self.xmin = IntVar()
        self.xmax = IntVar()
        self.ymin = IntVar()
        self.ymax = IntVar()
        self.zmin = IntVar()
        self.zmax = IntVar()
        self.color_line = StringVar()
        self.color_surf = StringVar()
        self.style_lines = StringVar()
        self.maker = StringVar()
        self.var = StringVar()

        menu_color_line = ['b', 'r', 'm', 'g', 'c', 'k', 'y']
        menu_color_surf = ['viridis', 'spring', 'winter',
                           'cool', 'hsv', 'hot', 'summer', 'ocean']
        menu_style_lines = ['None', '-', '--', '-.', ':']
        menu_maker = ['None', '.', ',', 'o', 'v', '^', '<', '>']

        # màu hàm 1 biến
        color_line = OptionMenu(self.frame, self.color_line, *menu_color_line)
        color_line.grid(row=5, column=1, columnspan=1, sticky=E)
        self.color_line.set(menu_color_line[0])

        # màu  hàm 2 biến
        color_surf = OptionMenu(self.frame, self.color_surf, *menu_color_surf)
        color_surf.grid(row=5, column=2, columnspan=1, sticky=W)
        self.color_surf.set(menu_color_surf[0])

        style_lines = OptionMenu(
            self.frame, self.style_lines, *menu_style_lines)
        style_lines.grid(row=5, column=4, columnspan=1, sticky=W)
        self.style_lines.set(menu_style_lines[1])

        maker = OptionMenu(self.frame, self.maker, *menu_maker)
        maker.grid(row=5, column=6, columnspan=1, sticky=W)
        self.maker.set(menu_maker[1])

        Label(self.frame, text='PLOT 3D', bg='lightblue', font=(
            'Times', 14)).grid(row=0, column=3, columnspan=1)
        Button(self.frame, text='Plot', command=self.plot).grid(
            row=1, column=4, columnspan=1, sticky=E)
        Button(self.frame, text='Go back', command=self.go_back).grid(
            row=1, column=5, columnspan=1, sticky=W)
        Label(self.frame, text='x_min').grid(
            row=3, column=0, columnspan=1, sticky=E)
        Label(self.frame, text='x_max').grid(
            row=4, column=0, columnspan=1, sticky=E)
        Label(self.frame, text='y_min').grid(
            row=3, column=2, columnspan=1, sticky=E)
        Label(self.frame, text='y_max').grid(
            row=4, column=2, columnspan=1, sticky=E)
        Label(self.frame, text='z_min').grid(
            row=3, column=4, columnspan=1, sticky=E)
        Label(self.frame, text='z_max').grid(
            row=4, column=4, columnspan=1, sticky=E)
        Label(self.frame, text='Color').grid(
            row=5, column=0, columnspan=1, sticky=E)
        Label(self.frame, text='Line_style').grid(
            row=5, column=3, columnspan=1, sticky=E)
        Label(self.frame, text='Maker').grid(
            row=5, column=5, columnspan=1, sticky=E)
        Label(self.frame, text='Function').grid(
            row=6, column=0, columnspan=1, sticky=E)

        Entry(self.frame, textvariable=self.xmin, width=10).grid(
            row=3, column=1, columnspan=1)
        Entry(self.frame, textvariable=self.ymin, width=10).grid(
            row=3, column=3, columnspan=1)
        Entry(self.frame, textvariable=self.zmin, width=10).grid(
            row=3, column=5, columnspan=1)
        Entry(self.frame, textvariable=self.xmax, width=10).grid(
            row=4, column=1, columnspan=1)
        Entry(self.frame, textvariable=self.ymax, width=10).grid(
            row=4, column=3, columnspan=1)
        Entry(self.frame, textvariable=self.zmax, width=10).grid(
            row=4, column=5, columnspan=1)
        Entry(self.frame, textvariable=self.var, width=15, font=(
            'Times', 14)).grid(row=6, column=1, columnspan=1)

    def start_page(self):  # frame vẽ
        self.frame.pack()

    def go_back(self):  # về lại frame chọn loại đồ thị 2D or 3D
        self.frame.pack_forget()
        self.app.main_page()

    def plot(self):  # hàm vẽ đồ thị
        try:
            try:
                # get giá trị lim người dùng nhập vào
                x1 = self.xmin.get()
                x2 = self.xmax.get()
                y1 = self.ymin.get()
                y2 = self.ymax.get()
                z1 = self.zmin.get()
                z2 = self.zmax.get()

                # lấy hàm vẽ đồ thị
                funtion = self.var.get()

                # chuyển hàm lượng giác
                lg = {
                    'sin': 'np.sin',
                    'cos': 'np.cos',
                    'tan': 'np.tan',
                    'log': 'np.log',
                    'exp': 'np.exp'
                }
                try:
                    # hàm 1 ẩn
                    x = np.array(arange(float(x1), float(x2) + 1, 0.1))
                    for i in list(lg.keys()):
                        if i in funtion:
                            funtion = funtion.replace(i, lg[i])
                            if i == 'log':
                                x = np.linspace(0, 10 * 4, 10 * 6)
                                x = x[1::]

                    y = eval(funtion)

                except:
                    # hàm 2 ẩn ko cần chuyển hàm lượng giác mà nhập trực tiếp Ví dụ sin(x)--> np.sin(x)
                    # for i in list(lg.keys()):
                    #     if i in funtion:
                    #         funtion = funtion.replace(i, lg[i])
                    #         if i == 'log':
                    #             x1 = y1 = 10 ** (-7)

                    def fun(x, y):
                        return eval(self.var.get())

                    x = np.linspace(x1, x2, 50)
                    y = np.linspace(y1, y2, 50)
                    X, Y = np.meshgrid(x, y)
                    zs = np.array(fun(np.ravel(X), np.ravel(Y)))
                    Z = zs.reshape(X.shape)

            except:
                # người dùng ko nhập giá trị
                x1 = -10
                x2 = 10
                y1 = -10
                y2 = 10
                z1 = -10
                z2 = 10

                funtion = self.var.get()

                lg = {
                    'sin': 'np.sin',
                    'cos': 'np.cos',
                    'tan': 'np.tan',
                    'log': 'np.log',
                    'exp': 'np.exp'
                }
                try:
                    # hàm 1 ẩn
                    x = np.array(arange(float(x1), float(x2) + 1, 0.1))
                    for i in list(lg.keys()):
                        if i in funtion:
                            funtion = funtion.replace(i, lg[i])
                            if i == 'log':
                                x = np.linspace(0, 10 * 4, 10 * 6)
                                x = x[1::]
                                x1 = 10 ** (-7)
                                x2 = 5
                                y1 = -5
                                y2 = 5
                    y = eval(funtion)

                except:
                    # hàm 2 ẩn

                    # for i in list(lg.keys()):
                    #     if i in funtion:
                    #         funtion = funtion.replace(i, lg[i])
                    #         if i == 'log':
                    #             x1 = y1 = 10 ** (-7)
                    #             x2 = y2 = 5
                    #             z1 = -5
                    #             z2 = 5

                    def fun(x, y):
                        return eval(self.var.get())

                    x = np.linspace(x1, x2, 50)
                    y = np.linspace(y1, y2, 50)
                    X, Y = np.meshgrid(x, y)
                    # set giá trị cho Z
                    zs = np.array(fun(np.ravel(X), np.ravel(Y)))
                    Z = zs.reshape(X.shape)

            self.frame.plottingFrame = self.frame
            self.frame.functions3Plot = self.frame

            self.frame.firstPlot = False
            self.frame.myFigure = Figure(figsize=(3.5, 3.5), dpi=120)
            self.frame.a = self.frame.myFigure.add_subplot(
                111, projection="3d")

            self.frame.a.set_xlabel('X Label')
            self.frame.a.set_ylabel('Y Label')
            self.frame.a.set_zlabel('Z Label')

            self.frame.canvas = FigureCanvasTkAgg(
                self.frame.myFigure, self.frame.plottingFrame)
            self.frame.canvas.draw()
            self.frame.canvas.get_tk_widget().grid(row=7, column=0, columnspan=7)
            self.frame.canvas._tkcanvas.grid(row=7, column=0, columnspan=7)

            self.frame.a.set_xlim([float(x1), float(x2)])
            self.frame.a.set_ylim([float(y1), float(y2)])
            self.frame.a.set_zlim([float(z1), float(z2)])

            # vẽ đồ thị, ưu tiên vẽ 3D trước vì TH 2D trc thì máy bỏ qua Z
            try:
                self.frame.a.plot_surface(X, Y, Z, cmap=self.color_surf.get())

            except:
                self.frame.a.plot(x, y, color=self.color_line.get(), linestyle=self.style_lines.get(),
                                  marker=self.maker.get())

        except:
            self.root = Tk()
            self.root.geometry('200x30')
            self.root.resizable(0, 0)
            self.root.title('ERROR!')
            Label(self.root, text='ERROR!').pack()


cal = Standard_Calculator()
cal.run()
