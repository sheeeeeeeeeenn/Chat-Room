import socket
import threading
from tkinter import *
from tkinter import scrolledtext
from tkinter import simpledialog
from tkinter import messagebox

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Application")

        self.init_ui()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.setup_connection()
        self.running = True
        self.thread = threading.Thread(target=self.receive, daemon=True)
        self.thread.start()

    def init_ui(self):
        frame = Frame(self.root)
        frame.pack(padx=20, pady=20)

        self.txt_area = scrolledtext.ScrolledText(frame, state=DISABLED, height=15, width=70)
        self.txt_area.grid(row=0, column=0, columnspan=2)

        self.msg_entry = Entry(frame, width=58)
        self.msg_entry.grid(row=1, column=0, pady=10)
        self.msg_entry.bind("<Return>", self.send)

        send_button = Button(frame, text="Send", command=self.send)
        send_button.grid(row=1, column=1, padx=10)

    def setup_connection(self):
        try:
            self.client_socket.connect(('localhost', 12345))
            self.username = simpledialog.askstring("Name", "Enter your name", parent=self.root)
            if self.username is None:
                self.username = 'Anonymous'
            self.client_socket.send(f"{self.username} has joined the chat.".encode('utf-8'))
        except Exception as e:
            messagebox.showerror("Connection Error", f"Unable to connect to server: {e}")
            self.root.destroy()

    def receive(self):
        while self.running:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                self.txt_area.config(state=NORMAL)
                self.txt_area.insert(END, message + "\n")
                self.txt_area.yview(END)
                self.txt_area.config(state=DISABLED)
            except OSError:
                break

    def send(self, event=None):
        message = f"{self.username}: {self.msg_entry.get()}"
        if message.strip() == ":":
            return
        self.msg_entry.delete(0, END)
        self.client_socket.send(message.encode('utf-8'))

    def on_closing(self, event=None):
        self.running = False
        self.client_socket.send(f"{self.username} has left the chat.".encode('utf-8'))
        self.root.after(500, self.root.destroy)  # Give time to send the message

def main():
    root = Tk()
    app = ChatApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
