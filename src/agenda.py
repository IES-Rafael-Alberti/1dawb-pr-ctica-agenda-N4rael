"""
27/11/2023

Práctica del examen para realizar en casa
-----------------------------------------

* El programa debe estar correctamente documentado.

* Debes intentar ajustarte lo máximo que puedas a lo que se pide en los comentarios TODO.

* Tienes libertad para desarrollar los métodos o funciones que consideres, pero estás obligado a usar como mínimo todos los que se solicitan en los comentarios TODO.

* Además, tu programa deberá pasar correctamente las pruebas unitarias que se adjuntan en el fichero test_agenda.py, por lo que estás obligado a desarrollar los métodos que se importan y prueban en la misma: pedir_email(), validar_email() y validar_telefono()

"""

import os
import pathlib
from os import path

# Constantes globales
RUTA = pathlib.Path(__file__).parent.absolute() 

NOMBRE_FICHERO = 'contactos.csv'

RUTA_FICHERO = path.join(RUTA, NOMBRE_FICHERO)

#TODO: Crear un conjunto con las posibles opciones del menú de la agenda
OPCIONES_MENU = {'1', '2', '3', '4', '5', '6', '7', '8'}
#TODO: Utiliza este conjunto en las funciones agenda() y pedir_opcion()


def borrar_consola():
    """ Limpia la consola
    """
    if os.name == "posix":
        os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system ("cls")


def cargar_contactos(contactos: list):

    """ Carga los contactos iniciales de la agenda desde un fichero
    ...
    """
    try:
        with open(RUTA_FICHERO, 'r') as fichero:
            for linea in fichero:
                valores = linea.strip().split(';')
                nombre, apellido, email = valores[:3]
                telefonos = valores[3:] if len(valores) > 3 else []
                contactos.append({
                    'nombre': nombre,
                    'apellido': apellido,
                    'email': email,
                    'telefonos': telefonos
                })
        print("Contactos cargados correctamente.")
    except Exception as e:
        print(f"**Error** {e}")
        print("No se cargaron los contactos correctamente.")

def validar_telefono(telefono: str) -> bool:
    """
    Valida la corrección de un número de teléfono.

    Parameters:
    - telefono (str): Número de teléfono a validar.

    Returns:
    - bool: True si el número de teléfono es válido, False de lo contrario.
    """
    try:
        # Elimina espacios y guiones del número de teléfono
        telefono = telefono.replace(" ", "").replace("-", "")
        
        # Verifica si el número de teléfono tiene la longitud correcta
        if len(telefono) == 9:
            return True
    
    except Exception as e:
        # Captura y maneja errores genéricos
        print(f"**Error** {e}")
        print("No se cargaron los teléfonos correctamente.")
        return False




def eliminar_contacto(contactos: list, email: str):
    """ Elimina un contacto de la agenda
    ...
    """
    try:
        pos = buscar_contacto(contactos, email)
        if pos is not None:
            del contactos[pos]
            print("Se eliminó 1 contacto")
        else:
            print("No se encontró el contacto para eliminar")
    except Exception as e:
        print(f"**Error** {e}")
        print("No se eliminó ningún contacto")

def mostrar_contactos(contactos: list):
    """ Muestra todos los contactos de la agenda ordenados por nombre
    ...
    """
    print("\nAGENDA ({})\n------".format(len(contactos)))
    
    # Obtener los nombres en una lista
    nombres = [contacto['nombre'] for contacto in contactos]
    
    # Ordenar la lista de nombres
    nombres_ordenados = sorted(nombres)
    
    # Iterar sobre los nombres ordenados
    for nombre in nombres_ordenados:
        # Encontrar el contacto correspondiente al nombre
        contacto = next(c for c in contactos if c['nombre'] == nombre)
        
        # Imprimir la información del contacto
        print("Nombre: {} {} ({})".format(contacto['nombre'], contacto['apellido'], contacto['email']))
        if not contacto['telefonos']:
            print("Teléfonos: ninguno")
        else:
            telefonos = ' / '.join(['{}'.format(t) for t in contacto['telefonos']])
            print("Teléfonos: {}".format(telefonos))
        print("......")


def pedir_email():
    """
    Simplemente pide el email.
    """
    email = input("Ingrese el email: ")
    return email
    
def validar_email(contactos: list, email: str) -> bool:
    """
    Valida la corrección de un email.

    Parameters:
    - contactos (list): Lista de contactos existentes para verificar si el email ya existe.
    - email (str): La dirección de correo electrónico a validar.

    Returns:
    - bool: True si el email es válido y no existe en la lista de contactos, False de lo contrario.
    """
    try:
        # Verifica si el email es una cadena vacía
        if email == "":
            raise ValueError("El email no puede ser una cadena vacía.")
        
        # Divide el email en usuario y dominio
        usuario, dominio = email.split('@')

        # Verifica que ni el usuario ni el dominio sean cadenas vacías
        if usuario == "" or dominio == "":
            raise Exception("El email debe contener un usuario y un dominio.")

        # Verifica si el email ya existe en la lista de contactos
        if email in [contacto['email'] for contacto in contactos]:
            print("Email ya existe. Inténtelo de nuevo.")
            return False

    except ValueError as ve:
        # Captura y maneja errores de tipo ValueError
        print(f"**Error de Valor** {ve}")
        print("El email no puede ser una cadena vacía.")
        return False

    except Exception as e:
        # Captura y maneja otros errores genéricos
        print(f"**Error** {e}")
        print("Ese email no es válido.")
        return False

    else:
        # Si no hay excepciones, el email es válido
        return True



def agregar_contacto(contactos: list):
    """ Agrega un nuevo contacto a la agenda
    ...
    """
    try:
        nombre = input("Ingrese el nombre: ").strip().title()
        apellido = input("Ingrese el apellido: ").strip().title()

        email = pedir_email()
        
        if validar_email( contactos, email) is False:
                raise Exception
            
        telefonos = []
        telefono = input("Ingrese un teléfono (deje en blanco para finalizar): ").strip().replace(" ", "")
        while telefono:
            if validar_telefono(telefono):
                telefonos.append(telefono)
            else:
                print("Teléfono no válido. Inténtelo de nuevo.")
            telefono = input("Ingrese un teléfono (deje en blanco para finalizar): ").strip().replace(" ", "")

        contactos.append({
            'nombre': nombre,
            'apellido': apellido,
            'email': email,
            'telefonos': telefonos
        })

        print("Contacto agregado correctamente.")
    except Exception as e:
        print(f"**Error** {e}")
        print("No se agregó el contacto correctamente.")

def mostrar_contactos_criterio(contactos: list):
    """
    Muestra la información de contacto según el criterio seleccionado por el usuario.

    Parameters:
    - contactos (list): Lista de contactos.

    Returns:
    - None
    """
    # Extrae los datos básicos del contacto
    nombre, apellido, email = contactos[:3]
    telefonos = contactos[3:] if len(contactos) > 3 else []

    # Muestra las opciones de búsqueda al usuario
    print("\nElige el criterio de búsqueda.\n------")
    print("1. Nombre")
    print("2. Apellido")
    print("3. Email")
    print("4. Teléfonos")
    
    # Solicita la elección del usuario
    eleccion = input("\n>> Seleccione una opción: ")

    if eleccion == "1":
        nombre = input("Escriba el nombre: ")
        pos = buscar_contacto_nombre(contactos, nombre)
        if pos is not None:
            print(contactos[pos])
        else:
            print("El contacto no está en la lista.")

    elif eleccion == "2":
        apellido = input("Escriba el apellido: ")
        pos = buscar_contacto_apellido(contactos, apellido)
        if pos is not None:
            print(contactos[pos])
        else:
            print("El contacto no está en la lista.")

    elif eleccion == "3":
        email = input("Escriba el email: ")
        pos = buscar_contacto(contactos, email)
        if pos is not None:
            print(contactos[pos])
        else:
            print("El contacto no está en la lista.")

    elif eleccion == "4":
        telefonos = input("Escriba uno de los teléfonos: ")
        pos = buscar_contacto_telefono(contactos, telefonos)
        if pos is not None:
            print(contactos[pos])
        else:
            print("El contacto no está en la lista.")
    else: 
        print("Opción inválida.")
    
    pulse_tecla_para_continuar()
    borrar_consola()


def buscar_contacto(contactos: list, email: str):
    """
    Busca un contacto por su email en la lista de contactos.

    Parameters:
    - contactos (list): Lista de contactos.
    - email (str): Email a buscar.

    Returns:
    - int or None: Devuelve el índice del contacto si se encuentra, None si no se encuentra.
    """
    for i, contacto in enumerate(contactos):
        if contacto['email'] == email:
            return i
    return None

def buscar_contacto_nombre(contactos: list, nombre: str):
    """
    Busca un contacto por su nombre en la lista de contactos.

    Parameters:
    - contactos (list): Lista de contactos.
    - nombre (str): Nombre a buscar.

    Returns:
    - int or None: Devuelve el índice del contacto si se encuentra, None si no se encuentra.
    """
    for i, contacto in enumerate(contactos):
        if contacto['nombre'] == nombre:
            return i
    return None

def buscar_contacto_apellido(contactos: list, apellido: str):
    """
    Busca un contacto por su apellido en la lista de contactos.

    Parameters:
    - contactos (list): Lista de contactos.
    - apellido (str): Apellido a buscar.

    Returns:
    - int or None: Devuelve el índice del contacto si se encuentra, None si no se encuentra.
    """
    for i, contacto in enumerate(contactos):
        if contacto['apellido'] == apellido:
            return i
    return None

def buscar_contacto_telefono(contactos: list, telefonos: str):
    """
    Busca un contacto por su número de teléfono en la lista de contactos.

    Parameters:
    - contactos (list): Lista de contactos.
    - telefonos (str): Número de teléfono a buscar.

    Returns:
    - int or None: Devuelve el índice del contacto si se encuentra, None si no se encuentra.
    """
    for i, contacto in enumerate(contactos):
        if telefonos in contacto['telefonos']:
            return i
    return None


def vaciar_agenda(contactos: list):
    """
    Elimina todos los contactos de la agenda.

    Parameters:
    - contactos (list): Lista de contactos.

    Returns:
    - None
    """
    print(" /!\ **ESTA ACCIÓN ELIMINARÁ TODOS LOS CONTACTOS DE LA AGENDA** /!\ ")
    eleccion = si_o_no()
    
    if eleccion == "s":
        contactos.clear()
        borrar_consola()
        print("Operación realizada correctamente.")
        pulse_tecla_para_continuar()
        borrar_consola()
        
    else:
        borrar_consola()
        print("Operación cancelada.")
        pulse_tecla_para_continuar()
        borrar_consola()
        
def modificar_contacto(contactos: list):
    """
    Modifica un contacto en la lista de contactos.

    Parameters:
    - contactos (list): Lista de contactos.

    Returns:
    - None
    """
    email = input("Escribe el email del contacto que desea modificar: ")
    eliminar_contacto(contactos, email)
    borrar_consola()
    print(f"Escriba la nueva información del contacto ({email}): ")
    agregar_contacto(contactos)



def mostrar_menu():
    """
    Muestra el menú al usuario.
    """

    print("\nAGENDA\n------")
    print("1. Nuevo contacto")
    print("2. Modificar contacto")
    print("3. Eliminar contacto")
    print("4. Vaciar agenda")
    print("5. Cargar agenda inicial")
    print("6. Mostrar contactos por criterio")
    print("7. Mostrar la agenda completa")
    print("8. Salir")
    print("\n>> Seleccione una opción: ")

def pedir_opcion():
    opcion = input("Ingrese la opción: ").strip()
    return opcion

def agenda(contactos: list):
    """ Ejecuta el menú de la agenda con varias opciones
    ...
    """
    opcion = None
    while opcion != '8':
        mostrar_menu()
        opcion = pedir_opcion()

        #TODO: Se valorará que utilices la diferencia simétrica de conjuntos para comprobar que la opción es un número entero del 1 al 8
        if opcion not in OPCIONES_MENU:
            print("Opción no válida. Inténtelo de nuevo.")
            continue

        if opcion == '1':
            # TODO: Llamada a la función agregar_contacto
            borrar_consola()
            agregar_contacto(contactos)
            pulse_tecla_para_continuar()
            
        elif opcion == '2':
            # TODO: Llamada a la función modificar_contacto
            borrar_consola()
            modificar_contacto(contactos)
            pulse_tecla_para_continuar()
            
        elif opcion == '3':
            email_eliminar = input("Ingrese el email del contacto a eliminar: ").strip()
            borrar_consola()
            eliminar_contacto(contactos, email_eliminar)
            pulse_tecla_para_continuar()
            
        elif opcion == '4':
            # TODO: Llamada a la función vaciar_agenda
            borrar_consola()
            vaciar_agenda(contactos)
            pulse_tecla_para_continuar()
            
        elif opcion == '5':
            # TODO: Llamada a la función cargar_contactos
            borrar_consola()
            cargar_contactos(contactos)
            pulse_tecla_para_continuar()
            
        elif opcion == '6':
            # TODO: Llamada a la función mostrar_contactos_criterio
            borrar_consola()
            mostrar_contactos_criterio(contactos)
            pulse_tecla_para_continuar()
            
        elif opcion == '7':
            # TODO: Llamada a la función mostrar_contactos
            borrar_consola()
            mostrar_contactos(contactos)
            pulse_tecla_para_continuar()

    borrar_consola()
    print("Saliendo de la agenda.")
    pulse_tecla_para_continuar()
    borrar_consola()



def pulse_tecla_para_continuar():
    """ Muestra un mensaje y realiza una pausa hasta que se pulse una tecla
    """
    print("\n")
    # os.system("pause")  esta funcion no funciona en Linux
    tecla = input("Pulse enter para continuar: ")

def si_o_no() -> str:
    """
    Pide al usuario que escriba s o n y se asegura de que lo haga bien.
    """
    eleccion = input("¿Desea continuar? s/n: ")
    if eleccion is "s" or "n":
        return eleccion

    else:
        while eleccion is not "s" or "n":
            print("Elección inválida.")
            eleccion = input("¿Desea continuar? s/n: ")
        return eleccion
def main():
    """ Función principal del programa
    """
    borrar_consola()

    #TODO: Asignar una estructura de datos vacía para trabajar con la agenda
    contactos = []

    #TODO: Modificar la función cargar_contactos para que almacene todos los contactos del fichero en una lista con un diccionario por contacto (claves: nombre, apellido, email y telefonos)
    #TODO: Realizar una llamada a la función cargar_contacto con todo lo necesario para que funcione correctamente.
    cargar_contactos(contactos)

    pulse_tecla_para_continuar()
    borrar_consola()
    #TODO: Crear función para agregar un contacto. Debes tener en cuenta lo siguiente:
    # - El nombre y apellido no pueden ser una cadena vacía o solo espacios y se guardarán con la primera letra mayúscula y el resto minúsculas (ojo a los nombre compuestos)
    # - El email debe ser único en la lista de contactos, no puede ser una cadena vacía y debe contener el carácter @.
    # - El email se guardará tal cuál el usuario lo introduzca, con las mayúsculas y minúsculas que escriba. 
    #  (CORREO@gmail.com se considera el mismo email que correo@gmail.com)
    # - Pedir teléfonos hasta que el usuario introduzca una cadena vacía, es decir, que pulse la tecla <ENTER> sin introducir nada.
    # - Un teléfono debe estar compuesto solo por 9 números, aunque debe permitirse que se introduzcan espacios entre los números.
    # - Además, un número de teléfono puede incluir de manera opcional un prefijo +34.
    # - De igual manera, aunque existan espacios entre el prefijo y los 9 números al introducirlo, debe almacenarse sin espacios.
    # - Por ejemplo, será posible introducir el número +34 600 100 100, pero guardará +34600100100 y cuando se muestren los contactos, el telófono se mostrará como +34-600100100. 
    #TODO: Realizar una llamada a la función agregar_contacto con todo lo necesario para que funcione correctamente.
    agregar_contacto(contactos)
    pulse_tecla_para_continuar()
    borrar_consola()

    #TODO: Realizar una llamada a la función eliminar_contacto con todo lo necesario para que funcione correctamente, eliminando el contacto con el email rciruelo@gmail.com
    eliminar_contacto(contactos, email = "rciruelo@gmail.com")
    pulse_tecla_para_continuar()

    #TODO: Crear función mostrar_contactos para que muestre todos los contactos de la agenda con el siguiente formato:
    # ** IMPORTANTE: debe mostrarlos ordenados según el nombre, pero no modificar la lista de contactos de la agenda original **
    #
    # AGENDA (6)
    # ------
    # Nombre: Antonio Amargo (aamargo@gmail.com)
    # Teléfonos: niguno
    # ......
    # Nombre: Daniela Alba (danalba@gmail.com)
    # Teléfonos: +34-600606060 / +34-670898934
    # ......
    # Nombre: Laura Iglesias (liglesias@gmail.com)
    # Teléfonos: 666777333 / 666888555 / 607889988
    # ......
    # ** resto de contactos **
    #
    #TODO: Realizar una llamada a la función mostrar_contactos con todo lo necesario para que funcione correctamente.
    mostrar_contactos(contactos)

    pulse_tecla_para_continuar()
    borrar_consola()
    #TODO: Crear un menú para gestionar la agenda con las funciones previamente desarrolladas y las nuevas que necesitéis:
    # AGENDA
    # ------
    # 1. Nuevo contacto
    # 2. Modificar contacto
    # 3. Eliminar contacto
    # 4. Vaciar agenda
    # 5. Cargar agenda inicial
    # 6. Mostrar contactos por criterio
    # 7. Mostrar la agenda completa
    # 8. Salir
    #
    # >> Seleccione una opción: 
    #
    #TODO: Para la opción 3, modificar un contacto, deberás desarrollar las funciones necesarias para actualizar la información de un contacto.
    #TODO: También deberás desarrollar la opción 6 que deberá preguntar por el criterio de búsqueda (nombre, apellido, email o telefono) y el valor a buscar para mostrar los contactos que encuentre en la agenda.
    agenda(contactos)


if __name__ == "__main__":
    main()