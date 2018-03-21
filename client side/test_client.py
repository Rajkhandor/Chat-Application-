import sqlite3
from sqlite3 import Error
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import tkinter.font as tkFont

conn = 0
name = 'Raj'
def create_connection(path):
	try: 
		global conn
		conn = sqlite3.connect(path)
		return conn
	except Error as e:
		print(e)

	return None

def execute_stmt(conn,query):
	try:
		c = conn.cursor()
		c.execute(query)
	except Error as e:
		print(e)

def insert_in_db(msg):
	global conn,name
	query = "INSERT INTO message VALUES('" + name + "', datetime('NOW','localtime'),'" +  msg + "' )"
	c = conn.cursor()
	c.execute(query)

def save_and_close(conn):
	conn.commit()
	conn.close()

def printAll(conn):
	c = conn.cursor()
	c.execute('SELECT * FROM message')
	row = c.fetchall()
	for r in row:
		print(r)

def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
            insert_in_db(msg)
			#msg_list.itemconfig(0, foreground="purple")
        except OSError:
            break

def send(event=None): 
    msg = my_msg.get()
    my_msg.set("")  
    client_socket.send(bytes(msg, "utf8"))
    if msg == "\q":
        client_socket.close()
        top.quit()
    else:
        insert_in_db(msg)

def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("\q")
    send()


if __name__ == "__main__":
	name = 'ex_db'
	conn = create_connection(name)
	#q1 = '''CREATE TABLE message( sender TEXT, dt DATETIME, mess TEXT)'''
	#if conn is not None:
	#	execute_stmt(conn,q1)
	#else:
	#	print('Cannot create the database connection')
	#q2 = '''INSERT INTO message VALUES ('Raj',datetime('NOW','localtime'),'Hii')'''
	#execute_stmt(conn,q2)
	#printAll(conn)
	top = tkinter.Tk()
	top.title("IRC Node")

	customFont = tkFont.Font(family="Helvetica", size=12)

	messages_frame = tkinter.Frame(top)
	my_msg = tkinter.StringVar()  # For the messages to be sent.
	my_msg.set("")
	scrollbar = tkinter.Scrollbar(messages_frame)  
	# For containing the messages.
	msg_list = tkinter.Listbox(messages_frame, height=20, width=80, yscrollcommand=scrollbar.set,font=customFont)
	scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
	msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
	msg_list.pack()
	messages_frame.pack()

	entry_field = tkinter.Entry(top, textvariable=my_msg,font=customFont)
	entry_field.bind("<Return>", send)
	entry_field.pack()
	send_button = tkinter.Button(top, text="Send", command=send, font=customFont)
	send_button.pack()

	top.protocol("WM_DELETE_WINDOW", on_closing)

	HOST = '127.0.0.1'#input('Enter host: ')
	PORT = 8000#input('Enter port: ')
	if not PORT:
		PORT = 8000
	else:
		PORT = int(PORT)

	BUFSIZ = 1024
	ADDR = (HOST, PORT)

	client_socket = socket(AF_INET, SOCK_STREAM)
	client_socket.connect(ADDR)

	receive_thread = Thread(target=receive)
	receive_thread.start()
	tkinter.mainloop()  # Starts GUI execution.
	save_and_close(conn)

