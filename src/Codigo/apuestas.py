from random import choice, randint
import validadores as vt
import data

def ValidarMontoPositivo(Monto):
    return Monto > 0

def ValidarNumeroRuleta(Numero):
    return 1 <= Numero <= 36


def ValidarNumerosDado(Numeros):
    if len(Numeros) != 3:
        return False
    try:
        N1, N2, N3 = map(int, Numeros)
        if len(set([N1, N2, N3])) != 3:
            return False
        if not all(1 <= X <= 6 for X in [N1, N2, N3]):
            return False
        return True
    except ValueError:
        return False

def ApostarRojoNegro(Jugador):
    print("\t Has seleccionado realizar una apuesta a Rojo o Negro")
    Monto = vt.Validador(input("\t Ingrese el monto de la apuesta -> "), "decimal", "\t Monto inválido, debe ser un número positivo.", ValidarMontoPositivo)
    
    if not Jugador.TieneSaldoSuficiente(Monto):
        print("\t Saldo insuficiente para realizar la apuesta.")
        return

    Eleccion = input("\t Elija 'rojo' o 'negro' -> ").lower()
    if Eleccion not in ["rojo", "negro"]:
        print("\t Elección no válida.")
        return

    Resultado = choice(["rojo", "negro"])
    
    if Eleccion == Resultado:
        Jugador.ActualizarSaldo(Monto)
        print(f"\t ¡Ganaste! El resultado fue {Resultado}. \n\t Nuevo saldo: {Jugador.ConsultarSaldo():.2f}")
    else:
        Jugador.ActualizarSaldo(-Monto)
        print(f"\t Perdiste. El resultado fue {Resultado}. \n\t Nuevo saldo: {Jugador.ConsultarSaldo():.2f}")

    Apuesta = {
        "Jugador": Jugador.Usuario,
        "Monto": Monto,
        "Eleccion": Eleccion,
        "Resultado": Resultado,
        "SaldoRestante": Jugador.ConsultarSaldo()
    }
    data.AddApuesta(Apuesta)

def Ruleta(Jugador):
    print("\t Has seleccionado apostar en la Ruleta")
    Monto = vt.Validador(input("\t Ingrese el monto de la apuesta -> "), "decimal", "\t Monto inválido, debe ser un número positivo.", ValidarMontoPositivo)
    
    if not Jugador.TieneSaldoSuficiente(Monto):
        print("\t Saldo insuficiente para realizar la apuesta.")
        return

    Eleccion = vt.Validador(input("\t Elija un número del '1' al '36' -> "), "numero", "\t Elección no válida.", ValidarNumeroRuleta)
    Resultado = choice(range(1, 37))
    
    if Eleccion == Resultado:
        Bono = Monto * 6
        Jugador.ActualizarSaldo(Bono)
        print(f"\t ¡Ganaste! El resultado fue {Resultado}. Bono del 600%: {Bono:.2f} soles. \n\t Nuevo saldo: {Jugador.ConsultarSaldo():.2f}")
    else:
        Jugador.ActualizarSaldo(-Monto)
        print(f"\t Perdiste. El resultado fue {Resultado}. \n\t Nuevo saldo: {Jugador.ConsultarSaldo():.2f}")

    Apuesta = {
        "Jugador": Jugador.Usuario,
        "Monto": Monto,
        "Eleccion": Eleccion,
        "Resultado": Resultado,
        "SaldoRestante": Jugador.ConsultarSaldo()
    }
    data.AddApuesta(Apuesta)

def VerHistorial(Jugador):
    print(f"\t Historial de apuestas para {Jugador.Usuario}")
    HistorialEncontrado = False
    
    HistorialJugador = Jugador.ObtenerHistorial()
    
    if HistorialJugador:
        HistorialEncontrado = True
        for Apuesta in HistorialJugador:
            if "NumerosElegidos" in Apuesta:
                print(f"\t Dado: Apostó {Apuesta['Monto']:.2f} a {Apuesta['NumerosElegidos']} - Resultado: {Apuesta['Resultado']} - Bono: {Apuesta['Bono']:.2f} - Saldo: {Apuesta['SaldoRestante']:.2f}")
            else:
                TipoApuesta = "Rojo/Negro" if Apuesta['Eleccion'] in ["rojo", "negro"] else "Ruleta"
                print(f"\t {TipoApuesta}: Apostó {Apuesta['Monto']:.2f} a {Apuesta['Eleccion']} - Resultado: {Apuesta['Resultado']} - Saldo: {Apuesta['SaldoRestante']:.2f}")
    
    if not HistorialEncontrado:
        print("\t No existe historial de apuestas.")

def LanzaElDado(Jugador):
    print("\t" + "*" * 36)
    print("\t*         ¡LANZA EL DADO!         *")
    print("\t" + "*" * 36)
    print("\tHas seleccionado lanzar el dado")
    Monto = vt.Validador(input("\tIngrese el monto de la apuesta -> "), "decimal", "\tMonto inválido, debe ser un número positivo.", ValidarMontoPositivo)
    
    if not Jugador.TieneSaldoSuficiente(Monto):
        print("\tSaldo insuficiente para realizar la apuesta.")
        return

    print("\tElija tres números distintos entre 1 y 6 (separados por espacio):")
    while True:
        Numeros = input("\tIngrese sus tres números -> ").split()
        if ValidarNumerosDado(Numeros):
            N1, N2, N3 = map(int, Numeros)
            break
        else:
            print("\tLos números deben ser distintos y estar entre 1 y 6.")

    Resultado = randint(1, 6)
    print(f"\tEl dado cayó en: {Resultado}")
    Bono = 0
    
    if Resultado == N1:
        Bono = Monto * 3
        print(f"\t¡Felicidades! Coincidió tu primer número. Ganaste un bono del 300%: {Bono:.2f} soles")
    elif Resultado == N2:
        Bono = Monto * 1.5
        print(f"\t¡Bien! Coincidió tu segundo número. Ganaste un bono del 150%: {Bono:.2f} soles")
    elif Resultado == N3:
        Bono = Monto * 0.5
        print(f"\tCoincidió tu tercer número. Ganaste un bono del 50%: {Bono:.2f} soles")
    else:
        Bono = -Monto
        print(f"\tNo coincidió ningún número. Perdiste la apuesta.")

    Jugador.ActualizarSaldo(Bono)
    print(f"\tNuevo saldo: {Jugador.ConsultarSaldo():.2f} soles")

    Apuesta = {
        "Jugador": Jugador.Usuario,
        "Monto": Monto,
        "NumerosElegidos": [N1, N2, N3],
        "Resultado": Resultado,
        "Bono": Bono,
        "SaldoRestante": Jugador.ConsultarSaldo()
    }
    data.AddApuesta(Apuesta)
