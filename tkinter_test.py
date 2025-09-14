import tkinter as tk

window = tk.Tk()
window.title('my window')
window.geometry('250x350')

e = tk.Entry(window, show=None)
e.pack()

def insert_point():
    var = e.get()
    # Use tk.INSERT to insert at current cursor position
    t.insert(tk.INSERT, var)

def insert_end():
    var = e.get()
    # Use tk.END to insert at the end
    t.insert(tk.END, var)

def insert_newline():
    # Insert a newline character at cursor position
    t.insert(tk.INSERT, '\n')

def insert_point_with_newline():
    var = e.get()
    # Insert text followed by a newline at cursor position
    t.insert(tk.INSERT, var + '\n')

def insert_end_with_newline():
    var = e.get()
    # Insert text followed by a newline at the end
    t.insert(tk.END, var + '\n')

# Create all five buttons
b1 = tk.Button(window, text='insert_point', width=15, height=1, command=insert_point)
b2 = tk.Button(window, text='insert_end', width=15, height=1, command=insert_end)
b3 = tk.Button(window, text='newline', width=15, height=1, command=insert_newline)
b4 = tk.Button(window, text='insert + newline', width=15, height=1, command=insert_point_with_newline)
b5 = tk.Button(window, text='end + newline', width=15, height=1, command=insert_end_with_newline)

# Create Text widget
t = tk.Text(window, height=8)

# Pack all components
b1.pack()
b2.pack()
b3.pack()
b4.pack()
b5.pack()
t.pack()

window.mainloop()