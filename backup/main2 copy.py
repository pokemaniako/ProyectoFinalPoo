from random import choice

# Global data
jugadores = []
apuestas = []

# Validadores
def validador(dato, tipo, mensaje_error, restriccion=None):
    """Valida los datos ingresados según el tipo y restricciones especificadas."""
    while True:
        try:
            if tipo == "texto":
                # Validar solo letras (a-z, A-Z) y espacios
                if not all(c.isspace() or (c.lower() in 'abcdefghijklmnopqrstuvwxyz') for c in dato):
                    print(mensaje_error)
                    dato = input("\t Ingrese nuevamente -> ")
                    continue
            elif tipo == "numero":
                dato = int(dato)
                if restriccion and not restriccion(dato):
                    print(mensaje_error)
                    dato = input("\t Ingrese nuevamente -> ")
                    continue
            elif tipo == "decimal":
                dato = float(dato)
                if restriccion and not restriccion(dato):
                    print(mensaje_error)
                    dato = input("\t Ingrese nuevamente -> ")
                    continue
            elif tipo == "genero":
                dato = dato.upper()
                if dato not in ['M', 'F']:
                    print(mensaje_error)
                    dato = input("\t Ingrese nuevamente -> ")
                    continue
            return dato
        except ValueError:
            print(mensaje_error)
            dato = input("\t Ingrese nuevamente -> ")

# Data functions
def AddJugador(jugador):
    jugadores.append(jugador)

def FindPlayerByCredentials(usuario, contraseña):
    for j in jugadores:
        if j["usuario"] == usuario and j["contraseña"] == contraseña:
            return j
    return 0

def AddApuesta(apuesta):
    apuestas.append(apuesta)

# Registro e inicio
def RegistrarJugador():
    print("\t Has seleccionado REGISTRAR")
    Nombre = validador(input("\t Ingrese su nombre -> "), "texto", "\t Nombre inválido, solo letras y espacios permitidos.")
    ApellidoPaterno = validador(input("\t Ingrese su apellido paterno -> "), "texto", "\t Apellido paterno inválido, solo letras y espacios permitidos.")
    ApellidoMaterno = validador(input("\t Ingrese su apellido materno -> "), "texto", "\t Apellido materno inválido, solo letras y espacios permitidos.")
    Sexo = validador(input("\t Ingrese su genero (M: masculino, F: Femenino) -> "), "genero", "\t Género inválido, solo M o F.")
    Edad = validador(input("\t Ingrese su edad -> "), "numero", "\t Edad inválida, debe ser un número mayor a 18.", lambda x: x >= 18)
    Usuario = input("\t Cree un nombre de usuario -> ")
    Contraseña = input("\t Cree una contraseña -> ")
    Saldo = validador(input("\t Ingrese su saldo en soles -> "), "decimal", "\t Saldo inválido, debe ser un número no negativo.", lambda x: x >= 0)

    Jugador = {
        "nombre": Nombre,
        "apellido_paterno": ApellidoPaterno,
        "apellido_materno": ApellidoMaterno,
        "genero": Sexo,
        "edad": Edad,
        "usuario": Usuario,
        "contraseña": Contraseña,
        "saldo": Saldo
    }
    AddJugador(Jugador)
    print(f"\t Usuario {Usuario} registrado con exito. Saldo inicial: {Saldo:.2f} solsitos")
    return Jugador

def IniciarSesion():
    print("\t Has seleccionado INICIAR SESIÓN")
    Usuario = input("\t Usuario -> ")
    Contraseña = input("\t Contraseña -> ")
    Jugador = FindPlayerByCredentials(Usuario, Contraseña)
    if Jugador:
        print(f"\t\t\n Bienvenido de nuevo, {Jugador['nombre']}!") 
        return Jugador
    print("\t Usuario o contraseña incorrecto")
    return 0   

# Apuestas functions
def ApostarRojoNegro(jugador):
    print("\t Has seleccionado realizar una apuesta a Rojo o Negro")
    monto = validador(input("\t Ingrese el monto de la apuesta -> "), "decimal", "\t Monto inválido, debe ser un número positivo.", lambda x: x > 0 and x <= jugador['saldo'])
    if monto > jugador['saldo']:
        print("\t Saldo insuficiente")
        return
    color = input("\t Elija Rojo o Negro (R/N) -> ").upper()
    if color not in ['R', 'N']:
        print("\t Opción inválida")
        return
    resultado = choice(['Rojo', 'Negro'])
    print(f"\t El resultado es {resultado}")
    ganancia = 0
    if (color == 'R' and resultado == 'Rojo') or (color == 'N' and resultado == 'Negro'):
        ganancia = monto
        jugador['saldo'] += ganancia
        print(f"\t Ganaste! Ganancia: {ganancia:.2f} soles. Saldo actual: {jugador['saldo']:.2f}")
    else:
        jugador['saldo'] -= monto
        print(f"\t Perdiste. Saldo actual: {jugador['saldo']:.2f}")
    apuesta = {
        "jugador": jugador['usuario'],
        "tipo": "Rojo/Negro",
        "monto": monto,
        "resultado": "Ganó" if ganancia else "Perdió"
    }
    AddApuesta(apuesta)

def Ruleta(jugador):
    print("\t Has seleccionado Ruleta")
    monto = validador(input("\t Ingrese el monto de la apuesta -> "), "decimal", "\t Monto inválido, debe ser un número positivo.", lambda x: x > 0 and x <= jugador['saldo'])
    if monto > jugador['saldo']:
        print("\t Saldo insuficiente")
        return
    numero = validador(input("\t Elija un número del 0 al 36 -> "), "numero", "\t Número inválido", lambda x: 0 <= x <= 36)
    resultado = choice(range(0, 37))
    print(f"\t El resultado es {resultado}")
    if numero == resultado:
        ganancia = monto * 6
        jugador['saldo'] += ganancia
        print(f"\t Ganaste! Ganancia: {ganancia:.2f} soles. Saldo actual: {jugador['saldo']:.2f}")
    else:
        jugador['saldo'] -= monto
        print(f"\t Perdiste. Saldo actual: {jugador['saldo']:.2f}")
    apuesta = {
        "jugador": jugador['usuario'],
        "tipo": "Ruleta",
        "monto": monto,
        "resultado": "Ganó" if numero == resultado else "Perdió"
    }
    AddApuesta(apuesta)

def LanzaElDado(jugador):
    print("\t Has seleccionado Lanza el Dado")
    monto = validador(input("\t Ingrese el monto de la apuesta -> "), "decimal", "\t Monto inválido, debe ser un número positivo.", lambda x: x > 0 and x <= jugador['saldo'])
    if monto > jugador['saldo']:
        print("\t Saldo insuficiente")
        return
    num1 = validador(input("\t Elija primer número del 1 al 6 -> "), "numero", "\t Número inválido", lambda x: 1 <= x <= 6)
    num2 = validador(input("\t Elija segundo número del 1 al 6 -> "), "numero", "\t Número inválido", lambda x: 1 <= x <= 6)
    num3 = validador(input("\t Elija tercer número del 1 al 6 -> "), "numero", "\t Número inválido", lambda x: 1 <= x <= 6)
    resultado = choice(range(1, 7))
    print(f"\t El dado cayó en {resultado}")
    ganancia = 0
    if resultado == num1:
        ganancia = monto * 3
    elif resultado == num2:
        ganancia = monto * 1.5
    elif resultado == num3:
        ganancia = monto * 0.5
    if ganancia > 0:
        jugador['saldo'] += ganancia
        print(f"\t Ganaste! Ganancia: {ganancia:.2f} soles. Saldo actual: {jugador['saldo']:.2f}")
        resultado_str = "Ganó"
    else:
        jugador['saldo'] -= monto
        print(f"\t Perdiste. Saldo actual: {jugador['saldo']:.2f}")
        resultado_str = "Perdió"
    apuesta = {
        "jugador": jugador['usuario'],
        "tipo": "Dado",
        "monto": monto,
        "resultado": resultado_str
    }
    AddApuesta(apuesta)

def VerHistorial(jugador):
    print("\t Historial de apuestas:")
    for a in apuestas:
        if a["jugador"] == jugador['usuario']:
            print(f"\t Tipo: {a['tipo']}, Monto: {a['monto']:.2f}, Resultado: {a['resultado']}")

# Menus
def MenuDeInicio():
    while True:
        print("\t" + "=" * 52)
        print("\t Bienvenido al casino virtual")
        print("\t 1. Registrar jugador")
        print("\t 2. Iniciar sesión")
        print("\t 3. Salir")
        print("\t" + "=" * 52)
        opcion = input("\tSeleccione una opción: ")
        if opcion == "1":
            jugador = RegistrarJugador()
            if jugador:
                MenuDeJuego(jugador)
        elif opcion == "2":
            jugador = IniciarSesion()
            if jugador:
                MenuDeJuego(jugador)
        elif opcion == "3":
            print("\t Gracias por visitar el casino virtual. ¡Vuelve pronto!")
            break
        else:
            print("\t Opción incorrecta. Por favor, intente nuevamente.")

def MenuDeJuego(jugador):
    while True:
        print("\t" + "=" * 52)
        print("\t Menú de juego")
        print("""\t1.- Apostar Rojo o Negro:
              
                    Si aciertas el color:
                    Ganas el 100% de tu apuesta (te suman el monto apostado a tu saldo).
                    Si fallas:
                    Pierdes el monto apostado.
                    ************************************************
                    """)
        print("""\t2.- Ruleta:

                    Si aciertas el número:
                    Ganas el 600% de tu apuesta (te suman 6 veces el monto apostado a tu saldo).
                    Si fallas:
                    Pierdes el monto apostado.
                    ************************************************
                    """)
        print("""\t3.- Lanza el dado:
              
                    Si el dado cae en tu primer número elegido:
                    Ganas el 300% de tu apuesta (te suman 3 veces el monto apostado).
                    Si el dado cae en tu segundo número elegido:
                    Ganas el 150% de tu apuesta (te suman 1.5 veces el monto apostado).
                    Si el dado cae en tu tercer número elegido:
                    Ganas el 50% de tu apuesta (te suman 0.5 veces el monto apostado).
                    Si no cae en ninguno de tus números:
                    Pierdes el monto apostado.
                    ************************************************
                    """)        
        print("\t  4. Ver historial de apuestas")
        print("\t  5. Consultar saldo")
        print("\t  6. Cerrar sesión")
        print("\t" + "=" * 52)
        opcion = input("\tSeleccione una opción: ")
        if opcion == "1":
            ApostarRojoNegro(jugador)
        elif opcion == "2":
            Ruleta(jugador)
        elif opcion == "3":
            LanzaElDado(jugador)
        elif opcion == "4":
            VerHistorial(jugador)
        elif opcion == "5":
            print(f"\tJugador: {jugador['nombre']} {jugador['apellido_paterno']}")
            print(f"\tSaldo actual: {jugador['saldo']:.2f} soles")
        elif opcion == "6":
            print("\tSesión cerrada. ¡Hasta luego!")
            break
        else:
            print("\tOpción incorrecta. Por favor, intente nuevamente.")

if __name__ == "__main__":
    MenuDeInicio()