from random import choice, randint
import os
from validadores import Validador, ValidarMontoPositivo, ValidarNumeroRuleta, ValidarNumerosDado
from colores import Colors
import data

def ApostarRojoNegro(Jugador):
    print("\t Has seleccionado apostar a rojo o negro")
    Monto = Validador(input("\t Ingrese el monto de la apuesta -> "), "decimal", "\t Monto invalido, debe ser un numero positivo", ValidarMontoPositivo)
    
    if not Jugador.TieneSaldoSuficiente(Monto):
        print(f"{Colors.RED}\t Saldo insuficiente{Colors.RESET}")
        return

    Eleccion = input(f"\t Elija '{Colors.RED}rojo{Colors.RESET}' o '{Colors.PLOMO}negro{Colors.RESET}' -> ").lower()
    if Eleccion not in ["rojo", "negro"]:
        print("\t Elección no válida.")
        return

    Resultado = choice(["rojo", "negro"])
    
    if Eleccion == Resultado:
        Jugador.ActualizarSaldo(Monto)
        print(f"{Colors.GREEN}\t Ganaste. Resultado {Resultado}{Colors.RESET}")
    else:
        Jugador.ActualizarSaldo(-Monto)
        print(f"{Colors.RED}\t Perdiste. Resultado {Resultado}{Colors.RESET}")

    Apuesta = {
        "Jugador": Jugador.Usuario,
        "Monto": Monto,
        "Eleccion": Eleccion,
        "Resultado": Resultado,
        "SaldoRestante": Jugador.ConsultarSaldo()
    }
    input(f"\t{Colors.BLUE}Presiona Enter para continuar...{Colors.RESET}")
    os.system('cls' if os.name == 'nt' else 'clear')
    data.AddApuesta(Apuesta)
    

def Ruleta(Jugador):
    print("\t Has seleccionado apostar en la ruleta")
    Monto = Validador(input("\t Ingrese el monto de la apuesta -> "), "decimal", "\t Monto invalido, debe ser un numero positivo", ValidarMontoPositivo)
    
    if not Jugador.TieneSaldoSuficiente(Monto):
        print("\t Saldo insuficiente")
        return

    Eleccion = Validador(input("\t Elija un numero del 1 al 36 -> "), "numero", "\t Eleccion no valida", ValidarNumeroRuleta)
    Resultado = choice(range(1, 37))
    
    if Eleccion == Resultado:
        Bono = Monto * 6
        Jugador.ActualizarSaldo(Bono)
        print(f"\t Ganaste. Bono {Bono:.2f} Saldo {Jugador.ConsultarSaldo():.2f}")
    else:
        Jugador.ActualizarSaldo(-Monto)
        print(f"\t Perdiste. Resultado {Resultado} Saldo {Jugador.ConsultarSaldo():.2f}")

    Apuesta = {
        "Jugador": Jugador.Usuario,
        "Monto": Monto,
        "Eleccion": Eleccion,
        "Resultado": Resultado,
        "SaldoRestante": Jugador.ConsultarSaldo()
    }
    data.AddApuesta(Apuesta)
    input(f"\t{Colors.BLUE}Presiona Enter para continuar...{Colors.RESET}")
    os.system('cls' if os.name == 'nt' else 'clear')
    
def VerHistorial(Jugador):
    print(f"\t Historial apuestas de {Jugador.Usuario}")
    HistorialJugador = Jugador.ObtenerHistorial()
    if HistorialJugador:
        for Apuesta in HistorialJugador:
            if "NumerosElegidos" in Apuesta:
                print(f"\t Dado - Monto {Apuesta['Monto']:.2f} Numeros {Apuesta['NumerosElegidos']} Resultado {Apuesta['Resultado']} Bono {Apuesta['Bono']:.2f} Saldo {Apuesta['SaldoRestante']:.2f}")
            else:
                TipoApuesta = "Rojo/Negro" if Apuesta['Eleccion'] in ["rojo", "negro"] else "Ruleta"
                print(f"\t {TipoApuesta} - Monto {Apuesta['Monto']:.2f} Eleccion {Apuesta['Eleccion']} Resultado {Apuesta['Resultado']} Saldo {Apuesta['SaldoRestante']:.2f}")
    else:
        print("\t No hay historial de apuestas")
    input("\tPresiona Enter para continuar...")
    os.system('cls' if os.name == 'nt' else 'clear')
def LanzaElDado(Jugador):
    print("\t LANZA EL DADO")
    print("\t Has seleccionado lanzar el dado")
    Monto = Validador(input("\t Ingrese el monto de la apuesta -> "), "decimal", "\t Monto invalido, debe ser un numero positivo", ValidarMontoPositivo)
    
    if not Jugador.TieneSaldoSuficiente(Monto):
        print("\t Saldo insuficiente")
        return

    print("\t Elija tres numeros distintos entre 1 y 6 separados por espacio")
    while True:
        Numeros = input("\t Ingrese sus tres numeros -> ").split()
        if ValidarNumerosDado(Numeros):
            N1 = int(Numeros[0])
            N2 = int(Numeros[1])
            N3 = int(Numeros[2])
            break
        else:
            print("\t Numeros invalidos")

    Resultado = randint(1, 6)
    print(f"\t Dado: {Resultado}")
    Bono = 0
    
    if Resultado == N1:
        Bono = Monto * 3
        print(f"\t Primer numero. Bono {Bono:.2f}")
    elif Resultado == N2:
        Bono = Monto * 1.5
        print(f"\t Segundo numero. Bono {Bono:.2f}")
    elif Resultado == N3:
        Bono = Monto * 0.5
        print(f"\t Tercer numero. Bono {Bono:.2f}")
    else:
        Bono = -Monto
        print("\t No hubo aciertos. Pierdes")

    Jugador.ActualizarSaldo(Bono)
    print(f"\t Saldo: {Jugador.ConsultarSaldo():.2f}")

    Apuesta = {
        "Jugador": Jugador.Usuario,
        "Monto": Monto,
        "NumerosElegidos": [N1, N2, N3],
        "Resultado": Resultado,
        "Bono": Bono,
        "SaldoRestante": Jugador.ConsultarSaldo()
    }
    data.AddApuesta(Apuesta)
    input(f"\t{Colors.BLUE}Presiona Enter para continuar...{Colors.RESET}")
    os.system('cls' if os.name == 'nt' else 'clear')
