import socket
import sys
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from colorama import init
import tkinter.font as tkFont

# DECLARING CONSTANTS
PORT = 5050 # Here goes the port you want to connect to
SERVER = "ngrok server" # Here goes the ip address/tcp connection you want to connect to
FORMAT = "utf-8"
ADDRESS = (SERVER, PORT)

# DECLARING VARIABLES
name = ""
run = True

# INITIALIZING COLORAMA
init()


# NEEDED FUNCTIONS
def send(msg):
    client_socket.send(msg.encode(FORMAT))


def handle_username():
    global name
    name = name_input.get()
    root.destroy()


def handle_message():
    global run
    msg = message_input.get()
    message_input.delete(0, "end")
    send(msg)


def stop_receiving():
    global run
    send("!1!2!3!")
    message_input.destroy()
    send_button.destroy()
    exit_button.destroy()
    tk.Label(root1, bg="white", text="THANKS FOR JOINING OUR CHAT !", width=800, justify="center", font=font7).pack()
    run = False


def receive():
    global run
    while run:
        try:
            message = client_socket.recv(512).decode(FORMAT)
            if message:
                if "has connected" in message:
                    tk.Label(scrollable_frame, font=font8, text=message, fg="green", bg="black", anchor="w",
                             width=82).pack(ipady=12)
                    canvas.update_idletasks()  # Updating idle tasks always as yview_move to may not work sometimes
                    canvas.yview_moveto(1.0)

                elif "has left the chat" in message:
                    tk.Label(scrollable_frame, font=font8, text=message, fg="red", bg="black", anchor="w",
                             width=82).pack(ipady=12)
                    canvas.update_idletasks()  # Updating idle tasks always as yview_move to may not work sometimes
                    canvas.yview_moveto(1.0)

                else:
                    tk.Label(scrollable_frame, font=font8, text=message, fg="white", bg="black", anchor="w",
                             width=82).pack(ipady=12)
                    canvas.update_idletasks()  # Updating idle tasks always as yview_move to may not work sometimes
                    canvas.yview_moveto(1.0)

        except Exception as e:
            pass


# ACCEPTING CLIENT'S USERNAME FOR THE FIRST TIME
root = tk.Tk()
root.title("ChatApp")
root.geometry("900x500")
root.resizable(False, False)
background_image = tk.PhotoImage(file="./images/background1.png")
trans = tk.PhotoImage(file="./images/final2.png")
background = tk.Label(root, image=background_image).place(x=-2)

font1 = tkFont.Font(family="Lucida Grande", size=20)
font2 = tkFont.Font(family="Calisto MT", size=20)
font3 = tkFont.Font(family="Calisto MT", size=13)
name_label = tk.Label(root, text="Username: ", font=font3, bg="white")
name_label.place(x = 300, y=324)
name_input = tk.Entry(root, width=12, font=font2, justify="center")
name_input.place(x=385, y=320)
join_button = tk.Button(command=handle_username, image=trans)
join_button.place(x=340, y=380)

def on_closing():
    root.destroy()
    sys.exit()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()


# CONNECTING AND SENDING TO THE SOCKET AFTER ENTERING A USERNAME
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(ADDRESS)
send(name)


# INFINITE LOOP FOR ACCEPTING MESSAGES
root1 = tk.Tk()


root1.title("ChatApp")
root1.geometry("900x578")
root1.resizable(False, False)
black_background = tk.PhotoImage(file="./images/black_background.png")
font4 = tkFont.Font(family="Calisto MT", size=17)
font5 = tkFont.Font(family="Calisto MT", size=12)
font6 = tkFont.Font(family="Century Gothic", size=20)
font7 = tkFont.Font(family="Century Gothic", size=18)
font8 = tkFont.Font(family="Century Gothic", size=12)
tk.Label(root1, text="KnownymousChat", bg="white", width=800, height=2, justify="center", font=font6).pack()
exit_button = tk.Button(root1, bg="red", text="Exit Chat", command=stop_receiving, font=font5, width=8)
exit_button.place(x=780,  y=21)
message_input = tk.Entry(root1, width=67, font=font4)
message_input.place(x=4, y=545)
send_button = tk.Button(text="Send", command=handle_message, borderwidth=1, width=7, font=font5, bg="blue")
send_button.place(x=814, y=545)
container = ttk.Frame(root1)
canvas = tk.Canvas(container, width=870, height=470, bg="black")
scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)
container.pack()
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")
x = threading.Thread(target=receive)
x.start()
root1.mainloop()

