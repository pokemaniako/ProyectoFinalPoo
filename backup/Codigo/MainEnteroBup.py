from random import choice  # Elegir uno al azar de la secuencia, choice es para agarrar uno aleatorio entre rojo y negro
jugadores = []
apuestas = []

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

def MenuDeInicio():
    print("\n\t|" + "-" * 50 + "|")
    print("""\t|           Bienvenido Adicto al gambling            |
\t|           ¿Que desea realizar?                    |
\t|           (1) Registrarme                          |
\t|           (2) Iniciar sesion                       |
\t|           (3) Irse a la mrd                        |""")
    print("\t|" + "-" * 50 + "|")
    rpta = input("\t| Ingrese su rpta. -> ")
    match rpta:
        case "1":
            RegistrarJugador()
        case "2":
            IniciarSesion()
        case "3":
            print("\t Vuelve cuando tengas plata bab:bear:son")
        case _:
            print("\t Ingresa bien tu rpta hermanito lindo :v ")
            MenuDeInicio()

def RegistrarJugador():
    print("\t Has seleccionado REGISTRAR")
    nombre = validador(input("\t Ingrese su nombre -> "), "texto", "\t Nombre inválido, solo letras y espacios permitidos.")
    apellido_paterno = validador(input("\t Ingrese su apellido paterno -> "), "texto", "\t Apellido paterno inválido, solo letras y espacios permitidos.")
    apellido_materno = validador(input("\t Ingrese su apellido materno -> "), "texto", "\t Apellido materno inválido, solo letras y espacios permitidos.")
    sexo = validador(input("\t Ingrese su genero (M: masculino, F: Femenino) -> "), "genero", "\t Género inválido, solo M o F.")
    edad = validador(input("\t Ingrese su edad -> "), "numero", "\t Edad inválida, debe ser un número mayor a 18.", lambda x: x >= 18)
    usuario = input("\t Cree un nombre de usuario -> ")
    contraseña = input("\t Cree una contraseña -> ")
    saldo = validador(input("\t Ingrese su saldo en soles -> "), "decimal", "\t Saldo inválido, debe ser un número no negativo.", lambda x: x >= 0)
    
    jugador = {
        "nombre": nombre,
        "apellido_paterno": apellido_paterno,
        "apellido_materno": apellido_materno,
        "genero": sexo,
        "edad": edad,
        "usuario": usuario,
        "contraseña": contraseña,
        "saldo": saldo
    }
    jugadores.append(jugador)  # Almacenar todos los valores de arriba y ya pe
    print(f"\t Usuario {usuario} registrado con exito. Saldo inicial: {saldo:.2f} solsitos")
    MenuDeInicio()

def IniciarSesion():
    print("\t Has seleccionado INICIAR SESIÓN")
    usuario = input("\t Usuario -> ")
    contraseña = input("\t Contraseña -> ")
    for jugador in jugadores:
        if jugador["usuario"] == usuario and jugador["contraseña"] == contraseña:
            print(f"\t Bienvenido de nuevo, {jugador['nombre']}!")
            MenuJugador(jugador)  # Ejecuta la wbd de abajo para validar los datos del adicto q ta entrando
            return
    print("\t Usuario o contraseña incorrecto")
    MenuDeInicio()

def ConsultarSaldo(jugador):
    print("\t Has seleccionado CONSULTAR SALDO")
    print(f"\t Jugador: {jugador['nombre']} {jugador['apellido_paterno']}")
    print(f"\t Saldo actual: {jugador['saldo']:.2f} soles")
    MenuJugador(jugador)

def MenuJugador(jugador):
    print("\n\t|" + "*" * 50 + "|")  # Modificable para hacer el cuadro mas grande o mas pequenio
    print(f"""\t|           Jugador: {jugador['nombre']}                      
\t|           Saldo actual: {jugador['saldo']:.2f} soles                
\t|           ¿DONDE donde quieres apostar adicto?                         
\t|           (1) ROJO O NEGRO
\t|           (2) Ruletita MANO                          
\t|           (3) Ver historial           
\t|           (4) Consultar saldo           
\t|           (5) Largarse a la magno mrd                         |""")
    print("\t|" + "_" * 50 + "|")
    opcion = input("\t| Seleccione una opcion -> ")
    match opcion:
        case "1":
            RealizarApuestaRojoONegro(jugador)
        case "2":
            Ruletita(jugador)
        case "3":
            VerHistorial(jugador)
        case "4":
            ConsultarSaldo(jugador)
        case "5":
            print("\t Sesion cerrada")
            MenuDeInicio()
        case _:
            print("\t Opcion incorrecta hermanito lindo")
            MenuJugador(jugador)

def RealizarApuestaRojoONegro(jugador):
    print("\t Has seleccionado REALIZAR APUESTA ADICTO DE MRD")
    monto = validador(input("\t Ingrese monto de la apuesta -> "), "decimal", "\t Monto inválido, debe ser un número positivo.", lambda x: x > 0)
    if monto > jugador["saldo"]:
        print("\t No hay sencillo hijo")
        MenuJugador(jugador)
        return
    
    eleccion = input("\t Elija 'rojo' o 'negro' -> ").lower()
    if eleccion not in ["rojo", "negro"]:  # not in pa verificar q alguna otra wbd ademas de rojo o negro este en la lista
        print("\t Eleccion no valida")
        MenuJugador(jugador)
        return
    
    resultado = choice(["rojo", "negro"])
    if eleccion == resultado:
        jugador["saldo"] += monto  # Modificar el saldo del jugador dependiendo del diccionario de abajito : AUMENTAR
        print(f"\t Ganaste! El resultado fue {resultado}. \n\t Nuevo saldo: {jugador['saldo']:.2f}")
    else:
        jugador["saldo"] -= monto  # Modificar el saldo del jugador dependiendo del diccionario de abajito : DESCONTAR
        print(f"\t Perdiste! El resultado fue {resultado}. \n\t Nuevo saldo: {jugador['saldo']:.2f}")
    
    apuesta = {
        "jugador": jugador["usuario"],  # Diccionario de la apuesta y de los jugadores
        "monto": monto,
        "eleccion": eleccion,
        "resultado": resultado,
        "saldo_restante": jugador["saldo"]
    }
    apuestas.append(apuesta)  # almacena la wbd >v
    MenuJugador(jugador)

def Ruletita(jugador):
    print("\t Has seleccionado RULETA ADICTO DE MRD")
    monto = validador(input("\t Ingrese monto de la apuesta -> "), "decimal", "\t Monto inválido, debe ser un número positivo.", lambda x: x > 0)
    if monto > jugador["saldo"]:
        print("\t No hay sencillo hijo")
        MenuJugador(jugador)
        return
    
    eleccion = validador(input("\t Elija un numero del '1' al '36' -> "), "numero", "\t Eleccion no valida.", lambda x: 1 <= x <= 36)
    
    resultado = choice(range(1, 37))
    if eleccion == resultado:
        jugador["saldo"] += monto  # Modificar el saldo del jugador dependiendo del diccionario de abajito : AUMENTAR
        print(f"\t Ganaste! El resultado fue {resultado}. \n\t Nuevo saldo: {jugador['saldo']:.2f}")
    else:
        jugador["saldo"] -= monto  # Modificar el saldo del jugador dependiendo del diccionario de abajito : DESCONTAR
        print(f"\t Perdiste! El resultado fue {resultado}. \n\t Nuevo saldo: {jugador['saldo']:.2f}")
    
    apuesta = {
        "jugador": jugador["usuario"],  # Diccionario de la apuesta y de los jugadores
        "monto": monto,
        "eleccion": eleccion,
        "resultado": resultado,
        "saldo_restante": jugador["saldo"]
    }
    apuestas.append(apuesta)  # almacena la wbd >v
    MenuJugador(jugador)

def VerHistorial(jugador):  # ESCUCHAME, ya mano ya me escuchaste, chevere
    print(f"\t Historial de apuestas para {jugador['usuario']}")
    historial_encontrado = False
    for apuesta in apuestas:
        if apuesta["jugador"] == jugador["usuario"]:
            historial_encontrado = True
            print(f"\t Apostó {apuesta['monto']:.2f} a {apuesta['eleccion']} - Resultado: {apuesta['resultado']} - Saldo: {apuesta['saldo_restante']:.2f}")
    if not historial_encontrado:
        print("\t No existe historial de apuestas.")
    MenuJugador(jugador)

MenuDeInicio()