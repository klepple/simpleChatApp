# Client who wants to connect and chat with EVERYONE!
from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread
import tkinter as tk


def receive():
    """Handling receiving messages"""
    while True:
        try:
            msg = client_sock.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tk.END, msg)
        except OSError:  # the client might have left the chat
            break


def send(event=None):  # event passed tkinter when send button on GUI is pressed
    """Handling sending messages"""
    msg = my_msg.get()  # gets the text that was entered in the input field
    my_msg.set("")  # clears the input field
    client_sock.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_sock.close()
        top.quit()


def on_close(event=None):
    """This function gets called when the window is closed"""
    my_msg.set("{quit}")
    send()


# GUI stuff
top = tk.Tk()
top.title("The best chat app EVER!")

messages_frame = tk.Frame(top)
my_msg = tk.StringVar()  # for sending messages
my_msg.set("Type your messages here.")
scrollbar = tk.Scrollbar(messages_frame)  # to navigate through the list of messages

msg_list = tk.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tk.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tk.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_close)

# Socket stuff
HOST = input('Enter host: ')
PORT = input('Enter port: ')

if not PORT:
    PORT = 33000  # default val
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_sock = socket(AF_INET, SOCK_STREAM)
client_sock.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tk.mainloop()  # Starts GUI
