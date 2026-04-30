from tkinter import *

def calculate():
    miles = mile_input.get()
    km = float(miles) * 1.609
    km_value_label.config(text=f"{km}")


window = Tk()
window.title("Miles to Kilometer Converter")

mile_input = Entry(width=20)
mile_input.grid(row=0, column=1)

miles_label = Label(text="Miles")
miles_label.grid(row=0, column=2)

equals_label = Label(text="is equal to")
equals_label.grid(row=1, column=0)

km_value_label = Label(text="0")
km_value_label.grid(row=1, column=1)

km_label = Label(text="Km")
km_label.grid(row=1, column=2)

button = Button(text="Calculate", command=calculate)
button.grid(row=2, column=1)


window.mainloop()