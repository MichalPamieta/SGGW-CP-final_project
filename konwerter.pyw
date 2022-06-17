from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from os import path

class NegativeNumberError(Exception):
    pass

class TooMuchNumberError(Exception):
    pass

class TooLittleNumberError(Exception):
    pass

class Converter(object):
    
    def __init__(self, master):
        frame = Frame(master)
        frame.grid()
        master.wm_attributes("-transparentcolor", 'grey')
        self.options = {"Łyżki stołowe" : "Tablespoons", "Szklanki" : "Cups", "Litry" : "Liters",
                        "Łyżeczki do herbaty" : "Teaspoons", "Galony" : "Gallons", 
                        "Pinty" : "Pints", "Kwarty" : "Quarts", "Uncje płynu" : "Fluid Ounces"}
        self.create_widgets()

    def create_widgets(self):
        #tło
        if path.isfile("./convert.png"):
            self.bg = PhotoImage(file="convert.png")
            self.label = Label(root, image=self.bg)
        else:
            self.bg="#ddc7a0"
            self.label = Label(root, background=self.bg)
        
        self.label.place(x=0, y=0, relwidth=1, relheight=1)
        
        #wybór jednostki objętości do zmiany na mililitry
        self.volume = ttk.Combobox(root, values=list(self.options.keys()), state="readonly", width=16, justify="center", font="helvetica 12")
        self.volume.place(x=230, y=150, anchor="center")
        self.volume.current(0)
        
        #pole input
        self.amount_entry = Entry(root, width=18, justify="center", font="helvetica 12")
        self.amount_entry.place(x=430, y=150, anchor="center")
        
        #jednostka wyjściowa -> mililitry
        self.amount_label = Label(root, text="Mililitry", width=18, font="helvetica 12")
        self.amount_label.place(x=230, y=200, anchor="center")
        
        #pole output z wynikiem
        self.result_label = Label(root, text=f"", width=16, justify="center", font="helvetica 12 bold")
        self.result_label.place(x=430, y=200, anchor="center")
        
        #przycisk Konwertuj
        self.convert_button = Button(root, text="Konwertuj", command=self.converter, width=12, font="helvetica 12 bold")
        self.convert_button.place(x=330, y=250, anchor="center")
    
    def converter(self):
        
        value = self.amount_entry.get()
        
        if "," in value:
            value = value.replace(",", ".")
        if ":" in value:
            value = value.replace(":", "/")
        
        try:
      
            if "/" in value:
                temp = self.convert(value)
                if not 0 == temp:
                    value = temp

            value = float(value)
                
            if value < 0.0:
                raise NegativeNumberError

            if value > 100000000.0:
                raise TooMuchNumberError   
                
            if value != 0 and value < 0.001:
                raise TooLittleNumberError 

            result_amount = 0
            
            if self.options.get(self.volume.get()) == "Tablespoons":
                result_amount = value * 14.786765
                
            elif self.options.get(self.volume.get()) == "Cups":
                result_amount = value * 236.588236

            elif self.options.get(self.volume.get()) == "Liters":
                result_amount = value * 1000

            elif self.options.get(self.volume.get()) == "Teaspoons":
                result_amount = value * 4.928922

            elif self.options.get(self.volume.get()) == "Gallons":
                result_amount = value * 3785.411784

            elif self.options.get(self.volume.get()) == "Pints":
                result_amount = value * 473.176473

            elif self.options.get(self.volume.get()) == "Quarts":
                result_amount = value * 946.352946

            elif self.options.get(self.volume.get()) == "Fluid Ounces":
                result_amount = value * 29.57353
            
            result_amount = float("{:.2f}".format(round(result_amount, 4)))
            self.result_label.configure(text=f"{result_amount}")

        except ValueError:
            messagebox.showerror("Błąd wartości", "Wprowadź liczbę!")
            self.amount_entry.delete(0, END)
            self.result_label.configure(text="")

        except NegativeNumberError:
            messagebox.showerror("Błąd wartości", "Wprowadź liczbę dodatnią!")
            self.amount_entry.delete(0, END)
            self.result_label.configure(text="")

        except TooMuchNumberError:
            messagebox.showinfo("Błąd wartości", "Wprowadzono za dużą liczbę!\nMaksymalna dostępna liczba to 100000000 (sto milionów).")
            self.amount_entry.delete(0, END)
            self.result_label.configure(text="")
            
        except TooLittleNumberError:
            messagebox.showinfo("Błąd wartości", "Wprowadzono za małą liczbę!\nMinimalna dostępna liczba to 0.001 (jedna tysięczna).")
            self.amount_entry.delete(0, END)
            self.result_label.configure(text="")  

    def convert(self, v):
        try:
            return float(v)
        except ValueError:
            tmp = v.rsplit("/", 1)
            v = tmp[0]
            try:
                if not (len(tmp) == 1 and isinstance(float(tmp[0]),float)):
                    denominator = float(tmp[1])
                if denominator == 0:
                    raise ValueError
            except ValueError:
                v = 0.0
                return v
            else:
                try:
                    if not (len(tmp) == 1 and isinstance(float(tmp[0]),float)):
                        nominator = float(tmp[0])
                except ValueError:
                    if "/" in tmp[0]:
                        nominator = self.convert(v)
                    else:
                        v = 0.0
                        return v
            return nominator / denominator

if __name__ == "__main__":
    root = Tk()
    root.title("Konwerter różnych objętości do mililitrów")
    root.resizable(False, False)
    root.geometry("640x420")
    konwerter = Converter(root)
    root.mainloop()