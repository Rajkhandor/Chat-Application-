# mysql.connector installed only on python2.7 
# Won't compile on python3

#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from mysql.connector import MySQLConnection,Error
from python_mysql_dbconfig import read_db_config

clients = {}
addresses = {}

HOST = '127.0.0.1'
PORT = 8000
BUFSIZ = 1024
ADDR = (HOST, PORT)
#print(ADDR)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

def connect_to_database():

	db_config = read_db_config()
	try:
		conn = MySQLConnection(**db_config)
		
		if conn.is_connected():
			print("Connected to mysql database")
		else:
			print("Failed to connect to the database")

	except Error as e:
		print(e)
	
	return conn

def display_query(conn,query_stmt):
	
	c = conn.cursor()
	c.execute(query_stmt)
	row = c.fetchall()
	for r in row:
		print(r)

def accept_incoming_connections(conn):

    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Please enter your name", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,conn,)).start()

def broadcast(msg, prefix=""):
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

def handle_client(client,conn):  # Takes client socket as argument.

    name = client.recv(BUFSIZ).decode("utf8")
    #welcome = 'Welcome %s! You are connected to the chat .' % name
    #client.send(bytes(welcome, "utf8"))
    #msg = "%s has joined the chat!" % name
    #broadcast(bytes(msg, "utf8"))
    clients[client] = name
    c = conn.cursor()
    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("\q", "utf8"):
            query1 = "INSERT INTO message VALUES('" + name + "', NOW(),'" +  msg.decode("utf8") + "' )"
            c.execute(query1)
            print(query1)
            conn.commit()
            broadcast(msg, name+": ")
        else:
            client.send(bytes("\q", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break

if __name__ == "__main__":
    conn = connect_to_database()
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections, args=(conn,))
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()


