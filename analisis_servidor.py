import socket
import numpy as np

SOCK_BUFFER = 1024

def promedio(dato:str):
    valor=list()
    for fila in filas[1:]:
        if dato in fila:
            columnas = fila.split(",")
            valor.append(float(columnas[5]))


    promedio= sum(valor)/len(valor)
    return f"El promedio de ventas de {dato} es {promedio:.2f}."

def canal():
    ventas_online = 0
    ventas_offline = 0
    valor_on=list()
    valor_off=list()
    for fila in filas[1:]:
        if "Online" in fila:
            columnas_on = fila.split(",")
            ventas_online+=1
            valor_on.append(float(columnas_on[8]))
        elif "Offline" in fila:
            columnas_off = fila.split(",")
            valor_off.append(float(columnas_off[8]))
            ventas_offline+=1


    if ventas_online>ventas_offline:  
        canal_venta= "Online"
        numero_ventas= ventas_online
        total_ventas=sum(valor_on)
    else:
        canal_venta= "Offline"
        numero_ventas= ventas_offline
        total_ventas=sum(valor_off)
    return(f"El mejor canal de venta fue {canal_venta} con {numero_ventas} ventas y con un total de {total_ventas} soles.")

def desviacion(dato:str):
    valor=list()
    for fila in filas[1:]:
        if dato in fila:
            columnas = fila.split(",")
            valor.append(float(columnas[8]))

    valores_np = np.array(valor)
    desviacion_estandar=np.std(valores_np)
    return f"La desviación estándar de {dato} es {desviacion_estandar:.2f}."

def cantclient():

    cantidad_clientes=0
    for fila in filas[1:]:
        if "High" in fila:
            cantidad_clientes+=1

    return f"Los clientes con ventas superiores al promedio son: {cantidad_clientes}."

def distribucion_venta(dato:str):
    valor=list()
    for fila in filas[1:]:
        if dato in fila:
            columnas=fila.split(",")
            valor.append(float(columnas[8]))

    valores_np = np.array(valor)
    media = np.mean(valores_np)
    mediana = np.median(valores_np)
    mínimo = np.min(valores_np)
    máximo = np.max(valores_np)

    return f"Distribución de ventas de {dato}: media {media:.2f}, mediana {mediana:.2f}, mínimo {mínimo:.2f}, máximo {máximo:.2f}."

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ("localhost", 5000)

    print(f"Iniciando servidor en {server_address[0]}:{server_address[1]}")

    sock.bind(server_address)

    sock.listen(5)

    with open ("orders_data_large.csv","r") as f:
        contenido=f.read()
    
    filas = contenido.split("\n")
    
    while True:
        print("Esperando conexiones...")
        
        conn, client = sock.accept()

        print(f"Conexion de {client[0]}:{client[1]}")

        try:
            consultas=list()
            while True:
                data = conn.recv(SOCK_BUFFER)
                
                if data:
                    consulta=None
                    print(f"Recibi: {data}")
                    data=data.decode("utf-8")
                    if "promedio de ventas de" in data:
                        lista=[valor for valor in data.split(" ")]
                        dato= ' '.join(lista[4:])
                        print(f"El dato es {dato}")
                        consulta= promedio(dato)
                        
                    if "mejor canal de venta"  in data:
                        consulta=canal()

                    if "desviación estándar de ventas de" in data:
                        lista=[valor for valor in data.split(" ")]
                        dato= ' '.join(lista[5:])
                        consulta=desviacion(dato)

                    if "cantidad de clientes con ventas superiores al promedio" in data:
                        consulta= cantclient()

                    if "distribución de ventas de" in data:
                        lista=[valor for valor in data.split(" ")]
                        dato= ' '.join(lista[4:])
                        consulta=distribucion_venta(dato)

                    if "salir" in data:
                        print("Cerrando la conexion")
                        conn.close()
                        with open ("reporte.txt","a") as f:
                            f.write("\n".join(consultas))
                    consultas.append(consulta)
                    
                    if consulta:
                        conn.sendall(consulta.encode("utf-8"))
                else:
                    print(f"No hay mas datos")
                    break

            
        except ConnectionResetError:
            print("El cliente cerro la conexion de manera abrupta")
        except KeyboardInterrupt:
            print("El usuario termino el programa")
        