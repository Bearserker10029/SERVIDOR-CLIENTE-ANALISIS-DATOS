import sys
import csv

def find_and_print_next_match(csv_reader, target_severity):
    """
    Busca desde la posición actual del lector e imprime la siguiente
    fila que coincida con la severidad. Devuelve True si la encuentra,
    False si llega al final del archivo sin encontrarla.
    """
    for row in csv_reader:
        # La severidad es la 3ra columna (índice 2)
        if len(row) > 2 and row[2].strip() == target_severity:
            # Imprime la fila unida por ';' para simular la línea original
            print(";".join(row))
            return True
    return False

def main():
    """
    Función principal del programa.
    """
    # 1. Validar los argumentos de la línea de comandos
    valid_args = ['-WARN', '-INFO', '-ERROR']
    if len(sys.argv) != 2 or sys.argv[1] not in valid_args:
        print("Error: Argumento de severidad inválido o faltante.", file=sys.stderr)
        print(f"Uso: python {sys.argv[0]} <{'|'.join(valid_args)}>", file=sys.stderr)
        sys.exit(1)

    # Extrae la severidad sin el guion inicial '-'
    target_severity = sys.argv[1][1:]

    try:
        # 2. Abrir el archivo CSV de forma segura
        with open('Log_de_medidores.csv', 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            
            # 3. Buscar e imprimir la primera coincidencia
            if not find_and_print_next_match(reader, target_severity):
                print(f"No se encontraron eventos con severidad '{target_severity}'.")
                return

            # 4. Bucle interactivo para buscar las siguientes coincidencias
            while True:
                try:
                    # Espera la entrada del usuario
                    user_input = input()
                    if user_input.lower() == 'p':
                        break
                    elif user_input.lower() == 's':
                        # Si el usuario pide la siguiente y no se encuentra, el bucle termina
                        if not find_and_print_next_match(reader, target_severity):
                            break
                except (EOFError, KeyboardInterrupt):
                    # Termina limpiamente si el usuario presiona Ctrl+C o Ctrl+D
                    break
    
    except FileNotFoundError:
        print("Error: El archivo 'Log_de_medidores.csv' no fue encontrado.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}", file=sys.stderr)
        sys.exit(1)

# Ejecutar la función principal solo si el script es llamado directamente
if __name__ == "__main__":
    main()