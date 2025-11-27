from random import choice, randint
from console import Console
from validadores import Validador, ValidarMontoPositivo, ValidarNumeroRuleta, ValidarNumerosDado
from colores import Colors
import data

def ApostarRojoNegro(Jugador):
    print(f"{Colors.CYAN}\t Has seleccionado apostar a rojo o negro{Colors.RESET}")
    Monto = Validador(input(f"{Colors.YELLOW}\t Ingrese el monto de la apuesta -> {Colors.RESET}"), "decimal", f"{Colors.RED}\t Monto invalido, debe ser un numero positivo{Colors.RESET}", ValidarMontoPositivo)
    
    if not Jugador.TieneSaldoSuficiente(Monto):
        print(f"{Colors.RED}\t Saldo insuficiente{Colors.RESET}")
        return

    Eleccion = input(f"{Colors.MAGENTA}\t Elija '{Colors.RED}rojo{Colors.RESET}{Colors.MAGENTA}' o '{Colors.PLOMO}negro{Colors.RESET}{Colors.MAGENTA}' -> {Colors.RESET}").lower()
    if Eleccion not in ["rojo", "negro"]:
        print(f"{Colors.RED}\t Elección no válida.{Colors.RESET}")
        return

    Resultado = choice(["rojo", "negro"])
    
    if Eleccion == Resultado:
        Jugador.ActualizarSaldo(Monto)
        print(f"{Colors.GREEN}\t ¡Ganaste! Resultado: {Resultado}{Colors.RESET}")
    else:
        Jugador.ActualizarSaldo(-Monto)
        print(f"{Colors.RED}\t ¡Perdiste! Resultado: {Resultado}{Colors.RESET}")

    Apuesta = {
        "Jugador": Jugador.Usuario,
        "Monto": Monto,
        "Eleccion": Eleccion,
        "Resultado": Resultado,
        "SaldoRestante": Jugador.ConsultarSaldo()
    }
    input(f"{Colors.BLUE}\t Presiona Enter para continuar...{Colors.RESET}")
    # limpiar pantalla usando la implementación de consola
    Console.clear()
    data.AddApuesta(Apuesta)
    

def Ruleta(Jugador):
    print(f"{Colors.GREEN}\t Has seleccionado apostar en la ruleta{Colors.RESET}")
    Monto = Validador(input(f"{Colors.YELLOW}\t Ingrese el monto de la apuesta -> {Colors.RESET}"), "decimal", f"{Colors.RED}\t Monto invalido, debe ser un numero positivo{Colors.RESET}", ValidarMontoPositivo)
    
    if not Jugador.TieneSaldoSuficiente(Monto):
        print(f"{Colors.RED}\t Saldo insuficiente{Colors.RESET}")
        return

    Eleccion = Validador(input(f"{Colors.MAGENTA}\t Elija un numero del 1 al 36 -> {Colors.RESET}"), "numero", f"{Colors.RED}\t Eleccion no valida{Colors.RESET}", ValidarNumeroRuleta)
    Resultado = choice(range(1, 37))
    
    if Eleccion == Resultado:
        Bono = Monto * 6
        Jugador.ActualizarSaldo(Bono)
        print(f"{Colors.GREEN}\t ¡Ganaste! Bono: {Bono:.2f} | Saldo: {Jugador.ConsultarSaldo():.2f}{Colors.RESET}")
    else:
        Jugador.ActualizarSaldo(-Monto)
        print(f"{Colors.RED}\t ¡Perdiste! Resultado: {Resultado} | Saldo: {Jugador.ConsultarSaldo():.2f}{Colors.RESET}")

    Apuesta = {
        "Jugador": Jugador.Usuario,
        "Monto": Monto,
        "Eleccion": Eleccion,
        "Resultado": Resultado,
        "SaldoRestante": Jugador.ConsultarSaldo()
    }
    data.AddApuesta(Apuesta)
    input(f"{Colors.BLUE}\t Presiona Enter para continuar...{Colors.RESET}")
    Console.clear()
    
def VerHistorial(Jugador):
    print(f"{Colors.CYAN}\t Historial apuestas de {Jugador.Usuario}{Colors.RESET}")
    HistorialJugador = Jugador.ObtenerHistorial()
    if HistorialJugador:
        for Apuesta in HistorialJugador:
            # mostrar apuestas del dado
            if "NumerosElegidos" in Apuesta:
                print(f"{Colors.WHITE}\t Dado{Colors.RESET} - {Colors.YELLOW}Monto:{Colors.RESET} {Apuesta['Monto']:.2f} {Colors.YELLOW}Numeros:{Colors.RESET} {Apuesta['NumerosElegidos']} {Colors.YELLOW}Resultado:{Colors.RESET} {Apuesta['Resultado']} {Colors.YELLOW}Bono:{Colors.RESET} {Apuesta['Bono']:.2f} {Colors.YELLOW}Saldo:{Colors.RESET} {Apuesta['SaldoRestante']:.2f}")
            # mostrar apuestas con tipo especifico (ruleta europea, blackjack)
            elif "Tipo" in Apuesta:
                print(f"{Colors.BLUE}\t {Apuesta['Tipo']}{Colors.RESET} - {Colors.YELLOW}Monto:{Colors.RESET} {Apuesta['Monto']:.2f} {Colors.YELLOW}Resultado:{Colors.RESET} {Apuesta['Resultado']} {Colors.YELLOW}Ganancia:{Colors.RESET} {Apuesta.get('Ganancia', 0):.2f} {Colors.YELLOW}Saldo:{Colors.RESET} {Apuesta['SaldoRestante']:.2f}")
            # mostrar apuestas de rojo negro y ruleta basica
            elif "Eleccion" in Apuesta:
                TipoApuesta = "Rojo/Negro" if Apuesta.get('Eleccion', "") in ["rojo", "negro"] else "Ruleta"
                ColorTipo = Colors.RED if Apuesta.get('Eleccion', "") in ["rojo", "negro"] else Colors.GREEN
                print(f"{ColorTipo}\t {TipoApuesta}{Colors.RESET} - {Colors.YELLOW}Monto:{Colors.RESET} {Apuesta['Monto']:.2f} {Colors.YELLOW}Eleccion:{Colors.RESET} {Apuesta['Eleccion']} {Colors.YELLOW}Resultado:{Colors.RESET} {Apuesta['Resultado']} {Colors.YELLOW}Saldo:{Colors.RESET} {Apuesta['SaldoRestante']:.2f}")
            else:
                # caso generico para apuestas no reconocidas
                print(f"{Colors.PLOMO}\t Apuesta desconocida - {Colors.YELLOW}Monto:{Colors.RESET} {Apuesta.get('Monto', 0):.2f} {Colors.YELLOW}Saldo:{Colors.RESET} {Apuesta.get('SaldoRestante', 0):.2f}{Colors.RESET}")
    else:
        print(f"{Colors.RED}\t No hay historial de apuestas{Colors.RESET}")
    input(f"{Colors.BLUE}\t Presiona Enter para continuar...{Colors.RESET}")
    Console.clear()
def LanzaElDado(Jugador):
    print(f"{Colors.MAGENTA}\t LANZA EL DADO{Colors.RESET}")
    print(f"{Colors.WHITE}\t Has seleccionado lanzar el dado{Colors.RESET}")
    Monto = Validador(input(f"{Colors.YELLOW}\t Ingrese el monto de la apuesta -> {Colors.RESET}"), "decimal", f"{Colors.RED}\t Monto invalido, debe ser un numero positivo{Colors.RESET}", ValidarMontoPositivo)
    
    if not Jugador.TieneSaldoSuficiente(Monto):
        print(f"{Colors.RED}\t Saldo insuficiente{Colors.RESET}")
        return

    print(f"{Colors.CYAN}\t Elija tres numeros distintos entre 1 y 6 separados por espacio{Colors.RESET}")
    while True:
        Numeros = input(f"{Colors.MAGENTA}\t Ingrese sus tres numeros -> {Colors.RESET}").split()
        if ValidarNumerosDado(Numeros):
            N1 = int(Numeros[0])
            N2 = int(Numeros[1])
            N3 = int(Numeros[2])
            break
        else:
            print(f"{Colors.RED}\t Numeros invalidos{Colors.RESET}")

    Resultado = randint(1, 6)
    print(f"{Colors.YELLOW}\t Dado: {Resultado}{Colors.RESET}")
    Bono = 0
    
    if Resultado == N1:
        Bono = Monto * 3
        print(f"{Colors.GREEN}\t ¡Primer numero! Bono: {Bono:.2f}{Colors.RESET}")
    elif Resultado == N2:
        Bono = Monto * 1.5
        print(f"{Colors.GREEN}\t ¡Segundo numero! Bono: {Bono:.2f}{Colors.RESET}")
    elif Resultado == N3:
        Bono = Monto * 0.5
        print(f"{Colors.GREEN}\t ¡Tercer numero! Bono: {Bono:.2f}{Colors.RESET}")
    else:
        Bono = -Monto
        print(f"{Colors.RED}\t No hubo aciertos. ¡Pierdes!{Colors.RESET}")

    Jugador.ActualizarSaldo(Bono)
    print(f"{Colors.BLUE}\t Saldo: {Jugador.ConsultarSaldo():.2f}{Colors.RESET}")

    Apuesta = {
        "Jugador": Jugador.Usuario,
        "Monto": Monto,
        "NumerosElegidos": [N1, N2, N3],
        "Resultado": Resultado,
        "Bono": Bono,
        "SaldoRestante": Jugador.ConsultarSaldo()
    }
    data.AddApuesta(Apuesta)
    input(f"{Colors.BLUE}\t Presiona Enter para continuar...{Colors.RESET}")
    Console.clear()
