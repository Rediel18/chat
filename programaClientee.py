import socket
import select
import errno
import sys

HEADER_LENGH = 10
IP = "localhost"
PORT = 50000
nombre_u = input("usuario:")
client_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP,PORT))
client_socket.setblocking(False)

id_cliente = nombre_u.encode("utf-8")
encabezado =f"{len(id_cliente):<{HEADER_LENGH}}".encode('utf_8')

print(id_cliente," ",encabezado)
client_socket.send(encabezado +id_cliente)

while True:
    mensaje = input(f"{nombre_u}")
    if mensaje:
        mensaje = mensaje.encode("utf-8")
        lon_mensaje = f"{len(mensaje):<{HEADER_LENGH}}".encode("utf-8")
        client_socket.send( lon_mensaje + mensaje)

        try:
            while True:
                encabezado = client_socket.recv(HEADER_LENGH)
                if not len(encabezado):
                    print("conexion cerrada por el servidor")
                    sys.exit()
                longitud = int(encabezado.decode("utf-8").strip())
                id_cliente = client_socket.recv(longitud).decode("utf-8")
                m_encabezado = client_socket.recv(HEADER_LENGH)
                m_longitud = int(m_encabezado.decode("utf-8").strip())
                mensaje = client_socket.recv(m_longitud).decode("utf-8")
                print(f"{id_cliente}>{mensaje}")
        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print("error leyendo", str(e))
                sys.exit()
            continue
        except Exception as e:
            print("error general ", str(e))
            sys.exit()