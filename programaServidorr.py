import socket
import select

HEADER_LENGTH = 10
IP = "localhost"
PORT = 50000
def recibe_mensaje(client_socket):
    try:
        encabezado = client_socket.recv(HEADER_LENGTH)
        if not len(encabezado):
            return False
        lon_mensaje = int(encabezado.decode('utf-8').strip())
        m = client_socket.recv(lon_mensaje)
        return{"header":encabezado,"data":m}
    except:
        return False

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
server_socket.bind( (IP,PORT))
server_socket.listen()
lista_sockets =[server_socket]
clients = {}

while True:
    read_socket, _,exception_sockets = select.select(lista_sockets,[],
                                        lista_sockets)
    for notified_socket in read_socket:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            user = recibe_mensaje(client_socket)
            if user is False:
                continue
            lista_sockets.append(client_socket)

            clients[client_socket] = user
            cod_cliente = user['data'].decode('utf-8')
            print(f"Desde {client_address[0]}):\
                {client_address[1]} CodigoCliente: {cod_cliente}")
        else:
            message = recibe_mensaje(notified_socket)
            if message is False:
                print(f"closed:{clients[notified_socket]['data'].decode('utf-8')}")
                lista_sockets.remove(notified_socket)
                del clients[notified_socket]
                continue

            user = clients[notified_socket]
            cod_cliente = user['data'].decode('utf-8')
            mensaje_cli = message['data'].decode('utf-8')
            print(f"recibe desde {cod_cliente}:{mensaje_cli}")
            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header']+\
                        user['data']+\
                        message['header']+ message['data'])
    for notified_socket in exception_sockets:
        lista_sockets.remove(notified_socket)
        del clients[notified_socket]