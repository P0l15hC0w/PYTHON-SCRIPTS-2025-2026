import tkinter as tk

class calcApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("simple calculator")
        self.root.geometry("300x420")

        self.label = tk.Label(self.root, text='calculator', font=('Arial', 20))
        self.txtbx = tk.Label(self.root, text='', font=('Arial', 22))

        self.bttfr = tk.Frame(self.root)
        self.bttfr.columnconfigure(0, weight=1)
        self.bttfr.columnconfigure(1, weight=1)
        self.bttfr.columnconfigure(2, weight=1)

        self.btt1 = tk.Button(self.bttfr, text='1', font=('Arial', 15), command=lambda: self.insert_number('1'))
        self.btt2 = tk.Button(self.bttfr, text='2', font=('Arial', 15), command=lambda: self.insert_number('2'))
        self.btt3 = tk.Button(self.bttfr, text='3', font=('Arial', 15), command=lambda: self.insert_number('3'))

        self.btt4 = tk.Button(self.bttfr, text='4', font=('Arial', 15), command=lambda: self.insert_number('4'))
        self.btt5 = tk.Button(self.bttfr, text='5', font=('Arial', 15), command=lambda: self.insert_number('5'))
        self.btt6 = tk.Button(self.bttfr, text='6', font=('Arial', 15), command=lambda: self.insert_number('6'))

        self.btt7 = tk.Button(self.bttfr, text='7', font=('Arial', 15), command=lambda: self.insert_number('7'))
        self.btt8 = tk.Button(self.bttfr, text='8', font=('Arial', 15), command=lambda: self.insert_number('8'))
        self.btt9 = tk.Button(self.bttfr, text='9', font=('Arial', 15), command=lambda: self.insert_number('9'))

        self.btt0 = tk.Button(self.bttfr, text='0', font=('Arial', 15), command=lambda: self.insert_number('0'))

        self.btt_plus = tk.Button(self.bttfr, text='+', font=('Arial', 15), command=lambda: self.insert_operator('+'))
        self.btt_minus = tk.Button(self.bttfr, text='-', font=('Arial', 15), command=lambda: self.insert_operator('-'))
        self.btt_multi = tk.Button(self.bttfr, text='*', font=('Arial', 15), command=lambda: self.insert_operator('*'))
        self.btt_divide = tk.Button(self.bttfr, text='/', font=('Arial', 15), command=lambda: self.insert_operator('/'))
        self.btt_eq = tk.Button(self.bttfr, text='=', font=('Arial', 15), command=self.calculate)
        self.btt_reset = tk.Button(self.bttfr, text='CE', font=('Arial', 15), command=self.reset)

        self.label.pack(pady=5)
        self.txtbx.pack(pady=5)

        self.btt1.grid(row=0, column=0, padx=2, pady=2, sticky=tk.W+tk.E)
        self.btt2.grid(row=0, column=1, padx=2, pady=2, sticky=tk.W+tk.E)
        self.btt3.grid(row=0, column=2, padx=2, pady=2, sticky=tk.W+tk.E)

        self.btt4.grid(row=1, column=0, padx=2, pady=2, sticky=tk.W+tk.E)
        self.btt5.grid(row=1, column=1, padx=2, pady=2, sticky=tk.W+tk.E)
        self.btt6.grid(row=1, column=2, padx=2, pady=2, sticky=tk.W+tk.E)

        self.btt7.grid(row=2, column=0, padx=2, pady=2, sticky=tk.W+tk.E)
        self.btt8.grid(row=2, column=1, padx=2, pady=2, sticky=tk.W+tk.E)
        self.btt9.grid(row=2, column=2, padx=2, pady=2, sticky=tk.W+tk.E)

        self.btt0.grid(row=3, column=1, sticky=tk.W+tk.E)

        self.btt_plus.grid(row=4, column=0, padx=2, pady=(50,2), sticky=tk.W+tk.E)
        self.btt_minus.grid(row=4, column=1, padx=2, pady=(50,2), sticky=tk.W+tk.E)
        self.btt_eq.grid(row=4, column=2, padx=2, pady=(50,2), sticky=tk.W+tk.E)

        self.btt_multi.grid(row=5, column=0, padx=2, pady=(2), sticky=tk.W+tk.E)
        self.btt_divide.grid(row=5, column=1, padx=2, pady=(2), sticky=tk.W+tk.E)
        self.btt_reset.grid(row=5, column=2, padx=2, pady=(2), sticky=tk.W+tk.E)

        self.bttfr.pack(padx=4, pady=4, fill='x')

        self.current_text = ""
        self.root.mainloop()

    def insert_number(self, num):
        self.current_text += num
        self.txtbx.config(text=self.current_text)

    def insert_operator(self, op):
        if self.current_text and self.current_text[-1] not in '+-*/':
            self.current_text += op
            self.txtbx.config(text=self.current_text)

    def calculate(self):
        try:
            result = eval(self.current_text, {"__builtins__": None}, {})
            self.current_text = str(result)
            self.txtbx.config(text=self.current_text)
        except Exception:
            self.txtbx.config(text="Error")
            self.current_text = ""
    def reset(self):
        self.txtbx.config(text="")
        self.current_text = ""
calcApp()
