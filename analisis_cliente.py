import socket
import time


SOCK_BUFFER = 1024


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ("localhost", 5000)
    print(f"Conectando a servidor: {server_address[0]}:{server_address[1]}")

    sock.connect(server_address)
    while True:
        msg = input("Ingrese la consulta a realizar: ")

        inicio = time.perf_counter()
        sock.sendall(msg.encode("utf-8"))
        data = sock.recv(SOCK_BUFFER)
        fin = time.perf_counter()

        print(f"Recibi: {data.decode()}")
        if msg=="salir":
            break
    sock.close()
    
    print(f"Tiempo total de operacion de E/S: {(fin - inicio):.6f} segundos")