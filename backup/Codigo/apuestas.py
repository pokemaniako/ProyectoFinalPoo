from random import choice
import validadores as vt
import data

def ApostarRojoNegro(jugador):
    print("\t Has seleccionado realizar una apuesta a Rojo o Negro")
    monto = vt.validador(input("\t Ingrese el monto de la apuesta -> "), "decimal", "\t Monto inválido, debe ser un número positivo.", lambda x: x > 0)
    if monto > jugador["saldo"]:
        print("\t Saldo insuficiente para realizar la apuesta.")
        return

    eleccion = input("\t Elija 'rojo' o 'negro' -> ").lower()
    if eleccion not in ["rojo", "negro"]:
        print("\t Elección no válida.")
        return

    resultado = choice(["rojo", "negro"])
    if eleccion == resultado:
        jugador["saldo"] += monto
        print(f"\t ¡Ganaste! El resultado fue {resultado}. \n\t Nuevo saldo: {jugador['saldo']:.2f}")
    else:
        jugador["saldo"] -= monto
        print(f"\t Perdiste. El resultado fue {resultado}. \n\t Nuevo saldo: {jugador['saldo']:.2f}")

    apuesta = {
        "jugador": jugador["usuario"],
        "monto": monto,
        "eleccion": eleccion,
        "resultado": resultado,
        "saldo_restante": jugador["saldo"]
    }
    data.AddApuesta(apuesta)

def Ruleta(jugador):
    print("\t Has seleccionado apostar en la Ruleta")
    monto = vt.validador(input("\t Ingrese el monto de la apuesta -> "), "decimal", "\t Monto inválido, debe ser un número positivo.", lambda x: x > 0)
    if monto > jugador["saldo"]:
        print("\t Saldo insuficiente para realizar la apuesta.")
        return

    eleccion = vt.validador(input("\t Elija un número del '1' al '36' -> "), "numero", "\t Elección no válida.", lambda x: 1 <= x <= 36)
    resultado = choice(range(1, 37))
    if eleccion == resultado:
        bono = monto * 6
        jugador["saldo"] += bono
        print(f"\t ¡Ganaste! El resultado fue {resultado}. Bono del 600%: {bono:.2f} soles. \n\t Nuevo saldo: {jugador['saldo']:.2f}")
    else:
        jugador["saldo"] -= monto
        print(f"\t Perdiste. El resultado fue {resultado}. \n\t Nuevo saldo: {jugador['saldo']:.2f}")

    apuesta = {
        "jugador": jugador["usuario"], 
        "monto": monto,
        "eleccion": eleccion,
        "resultado": resultado,
        "saldo_restante": jugador["saldo"]
    }
    data.AddApuesta(apuesta)
    
def VerHistorial(jugador):
    print(f"\t Historial de apuestas para {jugador['usuario']}")
    historial_encontrado = False
    for apuesta in data.apuestas:
        if apuesta["jugador"] == jugador["usuario"]:
            historial_encontrado = True
            # Si es apuesta de dado
            if "numeros_elegidos" in apuesta:
                print(f"\t Dado: Apostó {apuesta['monto']:.2f} a {apuesta['numeros_elegidos']} - Resultado: {apuesta['resultado']} - Bono: {apuesta['bono']:.2f} - Saldo: {apuesta['saldo_restante']:.2f}")
            # Si es apuesta normal
            else:
                print(f"\t Ruleta: Apostó {apuesta['monto']:.2f} a {apuesta['eleccion']} - Resultado: {apuesta['resultado']} - Saldo: {apuesta['saldo_restante']:.2f}")
    if not historial_encontrado:
        print("\t No existe historial de apuestas.")

def LanzaElDado(jugador):
    print("\t" + "*" * 36)
    print("\t*         ¡LANZA EL DADO!         *")
    print("\t" + "*" * 36)
    print("\tHas seleccionado lanzar el dado")
    monto = vt.validador(input("\tIngrese el monto de la apuesta -> "), "decimal", "\tMonto inválido, debe ser un número positivo.", lambda x: x > 0)
    if monto > jugador["saldo"]:
        print("\tSaldo insuficiente para realizar la apuesta.")
        return

    print("\tElija tres números distintos entre 1 y 6 (separados por espacio):")
    while True:
        numeros = input("\tIngrese sus tres números -> ").split()
        if len(numeros) != 3:
            print("\tDebe ingresar exactamente tres números.")
            continue
        try:
            n1, n2, n3 = map(int, numeros)
            if len(set([n1, n2, n3])) != 3 or not all(1 <= x <= 6 for x in [n1, n2, n3]):
                print("\tLos números deben ser distintos y estar entre 1 y 6.")
                continue
            break
        except ValueError:
            print("\tEntrada inválida. Ingrese solo números.")

    from random import randint
    resultado = randint(1, 6)
    print(f"\tEl dado cayó en: {resultado}")
    bono = 0
    if resultado == n1:
        bono = monto * 3
        print(f"\t¡Felicidades! Coincidió tu primer número. Ganaste un bono del 300%: {bono:.2f} soles")
    elif resultado == n2:
        bono = monto * 1.5
        print(f"\t¡Bien! Coincidió tu segundo número. Ganaste un bono del 150%: {bono:.2f} soles")
    elif resultado == n3:
        bono = monto * 0.5
        print(f"\tCoincidió tu tercer número. Ganaste un bono del 50%: {bono:.2f} soles")
    else:
        bono = -monto
        print(f"\tNo coincidió ningún número. Perdiste la apuesta.")

    jugador["saldo"] += bono
    print(f"\tNuevo saldo: {jugador['saldo']:.2f} soles")

    apuesta = {
        "jugador": jugador["usuario"],
        "monto": monto,
        "numeros_elegidos": [n1, n2, n3],
        "resultado": resultado,
        "bono": bono,
        "saldo_restante": jugador["saldo"]
    }
    data.AddApuesta(apuesta)