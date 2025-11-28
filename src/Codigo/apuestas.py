from random import choice, randint
from console import Console
from validadores import Validador, ValidarMontoPositivo, ValidarNumeroRuleta, ValidarNumerosDado
from colores import Colors
import data

def ValidarNumeroRangoRuleta(Numero):
    """Valida que un número esté en el rango 0-36 para ruleta europea"""
    return 0 <= Numero <= 36

def ValidarOpcionSiNo(Opcion):
    """Valida que la opción sea 's' o 'n'"""
    return Opcion.lower() in ['s', 'n']

def ValidarSeleccionDocena(Docena):
    """Valida selección de docena"""
    return Docena in ["1-12", "13-24", "25-36"]

def ValidarSeleccionColumna(Columna):
    """Valida selección de columna"""
    return Columna in ["1", "2", "3"]

def ValidarSeleccionColor(Color):
    """Valida selección de color rojo o negro"""
    return Color.lower() in ["rojo", "negro"]

def ValidarSeleccionParidad(Paridad):
    """Valida selección de par o impar"""
    return Paridad.lower() in ["par", "impar"]

def ValidarSeleccionAltoBajo(AltoBajo):
    """Valida selección de alto o bajo"""
    return AltoBajo.lower() in ["alto", "bajo"]

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

    RojosEuropeos = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    NegrosEuropeos = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
    
    NumeroResultado = choice(range(1, 37))
    ResultadoColor = "rojo" if NumeroResultado in RojosEuropeos else "negro"
    
    if Eleccion == ResultadoColor:
        Ganancia = Monto
        Jugador.ActualizarSaldo(Ganancia)
        print(f"{Colors.GREEN}\t ¡Ganaste! Número {NumeroResultado} es {ResultadoColor}. Ganancia: {Ganancia:.2f}{Colors.RESET}")
    else:
        Ganancia = -Monto
        Jugador.ActualizarSaldo(Ganancia)
        print(f"{Colors.RED}\t ¡Perdiste! Número {NumeroResultado} es {ResultadoColor}{Colors.RESET}")

    Apuesta = {
        "Jugador": Jugador.Usuario,
        "Tipo": "Rojo/Negro",
        "Monto": Monto,
        "Eleccion": Eleccion,
        "Resultado": f"{NumeroResultado} ({ResultadoColor})",
        "Ganancia": Ganancia,
        "SaldoRestante": Jugador.ConsultarSaldo()
    }
    data.AddApuesta(Apuesta)
    input(f"{Colors.BLUE}\t Presiona Enter para continuar...{Colors.RESET}")
    Console.clear()
    

def RuletaSimple(Jugador):
    print(f"{Colors.GREEN}\t Has seleccionado RULETA SIMPLE{Colors.RESET}")
    Monto = Validador(input(f"{Colors.YELLOW}\t Ingrese el monto de la apuesta -> {Colors.RESET}"), "decimal", f"{Colors.RED}\t Monto invalido, debe ser un numero positivo{Colors.RESET}", ValidarMontoPositivo)
    
    if not Jugador.TieneSaldoSuficiente(Monto):
        print(f"{Colors.RED}\t Saldo insuficiente{Colors.RESET}")
        return

    Eleccion = Validador(input(f"{Colors.MAGENTA}\t Elija un numero del 1 al 36 -> {Colors.RESET}"), "numero", f"{Colors.RED}\t Eleccion no valida{Colors.RESET}", ValidarNumeroRuleta)
    Resultado = choice(range(1, 37))
    
    if Eleccion == Resultado:
        Ganancia = Monto * 6
        Jugador.ActualizarSaldo(Ganancia)
        print(f"{Colors.GREEN}\t ¡Ganaste! Bono: {Ganancia:.2f} | Saldo: {Jugador.ConsultarSaldo():.2f}{Colors.RESET}")
    else:
        Ganancia = -Monto
        Jugador.ActualizarSaldo(Ganancia)
        print(f"{Colors.RED}\t ¡Perdiste! Resultado: {Resultado} | Saldo: {Jugador.ConsultarSaldo():.2f}{Colors.RESET}")

    Apuesta = {
        "Jugador": Jugador.Usuario,
        "Tipo": "Ruleta Simple",
        "Monto": Monto,
        "Eleccion": Eleccion,
        "Resultado": Resultado,
        "Ganancia": Ganancia,
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
            if "Tipo" in Apuesta:
                TipoApuesta = Apuesta.get("Tipo", "Desconocida")
                Monto = Apuesta.get("Monto", 0)
                Resultado = Apuesta.get("Resultado", "N/A")
                Ganancia = Apuesta.get("Ganancia", 0)
                SaldoRestante = Apuesta.get("SaldoRestante", 0)
                print(f"{Colors.BLUE}\t {TipoApuesta}{Colors.RESET} - {Colors.YELLOW}Monto:{Colors.RESET} {Monto:.2f} {Colors.YELLOW}Resultado:{Colors.RESET} {Resultado} {Colors.YELLOW}Ganancia:{Colors.RESET} {Ganancia:.2f} {Colors.YELLOW}Saldo:{Colors.RESET} {SaldoRestante:.2f}")
            else:
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
            Numero1 = int(Numeros[0])
            Numero2 = int(Numeros[1])
            Numero3 = int(Numeros[2])
            break
        else:
            print(f"{Colors.RED}\t Numeros invalidos{Colors.RESET}")

    Resultado = randint(1, 6)
    print(f"{Colors.YELLOW}\t Dado: {Resultado}{Colors.RESET}")
    Ganancia = 0
    
    if Resultado == Numero1:
        Ganancia = Monto * 3
        print(f"{Colors.GREEN}\t ¡Primer numero! Ganancia: {Ganancia:.2f}{Colors.RESET}")
    elif Resultado == Numero2:
        Ganancia = Monto * 1.5
        print(f"{Colors.GREEN}\t ¡Segundo numero! Ganancia: {Ganancia:.2f}{Colors.RESET}")
    elif Resultado == Numero3:
        Ganancia = Monto * 0.5
        print(f"{Colors.GREEN}\t ¡Tercer numero! Ganancia: {Ganancia:.2f}{Colors.RESET}")
    else:
        Ganancia = -Monto
        print(f"{Colors.RED}\t No hubo aciertos. ¡Pierdes!{Colors.RESET}")

    Jugador.ActualizarSaldo(Ganancia)
    print(f"{Colors.BLUE}\t Saldo: {Jugador.ConsultarSaldo():.2f}{Colors.RESET}")

    Apuesta = {
        "Jugador": Jugador.Usuario,
        "Tipo": "Lanza El Dado",
        "Monto": Monto,
        "NumerosElegidos": [Numero1, Numero2, Numero3],
        "Resultado": Resultado,
        "Ganancia": Ganancia,
        "SaldoRestante": Jugador.ConsultarSaldo()
    }
    data.AddApuesta(Apuesta)
    input(f"{Colors.BLUE}\t Presiona Enter para continuar...{Colors.RESET}")
    Console.clear()


def RuletaEuropea(Jugador):
    print(f"{Colors.GREEN}\t Has seleccionado RULETA EUROPEA (0-36){Colors.RESET}")
    Monto = Validador(input(f"{Colors.YELLOW}\t Ingrese el monto de la apuesta -> {Colors.RESET}"), "decimal", f"{Colors.RED}\t Monto invalido, debe ser un numero positivo{Colors.RESET}", ValidarMontoPositivo)
    
    if not Jugador.TieneSaldoSuficiente(Monto):
        print(f"{Colors.RED}\t Saldo insuficiente{Colors.RESET}")
        return

    RojosEuropeos = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    NegrosEuropeos = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
    
    print(f"{Colors.CYAN}\t Tipos de apuestas:")
    print(f"{Colors.YELLOW}\t 1. Directo (numero individual, 0-36) - Pago 35:1")
    print(f"{Colors.YELLOW}\t 2. Rojo o Negro - Pago 1:1")
    print(f"{Colors.YELLOW}\t 3. Par o Impar - Pago 1:1")
    print(f"{Colors.YELLOW}\t 4. Alto (19-36) o Bajo (1-18) - Pago 1:1")
    print(f"{Colors.YELLOW}\t 5. Docena (1-12, 13-24, 25-36) - Pago 2:1")
    print(f"{Colors.YELLOW}\t 6. Columna (1, 2 o 3) - Pago 2:1{Colors.RESET}")
    
    TipoApuesta = input(f"{Colors.MAGENTA}\t Seleccione tipo de apuesta (1-6) -> {Colors.RESET}")
    
    Resultado = choice(range(0, 37))
    Ganancia = 0
    Descripcion = ""
    
    if TipoApuesta == "1":
        Numero = Validador(input(f"{Colors.MAGENTA}\t Ingrese numero (0-36) -> {Colors.RESET}"), "numero", f"{Colors.RED}\t Numero invalido{Colors.RESET}", ValidarNumeroRangoRuleta)
        if Numero == Resultado:
            Ganancia = Monto * 35
            print(f"{Colors.GREEN}\t ¡Ganaste! {Resultado} es el numero ganador. Ganancia: {Ganancia:.2f}{Colors.RESET}")
        else:
            Ganancia = -Monto
            print(f"{Colors.RED}\t Perdiste. Resultado: {Resultado}{Colors.RESET}")
        Descripcion = f"Ruleta Europea - Directo ({Numero})"
        
    elif TipoApuesta == "2":
        Color = input(f"{Colors.MAGENTA}\t Elija '{Colors.RED}rojo{Colors.RESET}{Colors.MAGENTA}' o '{Colors.PLOMO}negro{Colors.RESET}{Colors.MAGENTA}' -> {Colors.RESET}").lower()
        if not ValidarSeleccionColor(Color):
            print(f"{Colors.RED}\t Elección no válida{Colors.RESET}")
            return
        
        ColorResultado = "rojo" if Resultado in RojosEuropeos else ("negro" if Resultado in NegrosEuropeos else "verde")
        if Color == ColorResultado:
            Ganancia = Monto
            print(f"{Colors.GREEN}\t ¡Ganaste! {Resultado} es {ColorResultado}. Ganancia: {Ganancia:.2f}{Colors.RESET}")
        else:
            Ganancia = -Monto
            print(f"{Colors.RED}\t Perdiste. Resultado: {Resultado} ({ColorResultado}){Colors.RESET}")
        Descripcion = f"Ruleta Europea - {Color.capitalize()}"
        
    elif TipoApuesta == "3":
        Paridad = input(f"{Colors.MAGENTA}\t Elija 'par' o 'impar' -> {Colors.RESET}").lower()
        if not ValidarSeleccionParidad(Paridad):
            print(f"{Colors.RED}\t Elección no válida{Colors.RESET}")
            return
        
        EsParResultado = (Resultado % 2 == 0) if Resultado != 0 else False
        EsParApuesta = Paridad == "par"
        if EsParResultado == EsParApuesta:
            Ganancia = Monto
            print(f"{Colors.GREEN}\t ¡Ganaste! {Resultado} es {Paridad}. Ganancia: {Ganancia:.2f}{Colors.RESET}")
        else:
            Ganancia = -Monto
            print(f"{Colors.RED}\t Perdiste. Resultado: {Resultado}{Colors.RESET}")
        Descripcion = f"Ruleta Europea - {Paridad.capitalize()}"
        
    elif TipoApuesta == "4":
        AltoBajo = input(f"{Colors.MAGENTA}\t Elija 'alto' (19-36) o 'bajo' (1-18) -> {Colors.RESET}").lower()
        if not ValidarSeleccionAltoBajo(AltoBajo):
            print(f"{Colors.RED}\t Elección no válida{Colors.RESET}")
            return
        
        EsAlto = (19 <= Resultado <= 36)
        if (AltoBajo == "alto" and EsAlto) or (AltoBajo == "bajo" and not EsAlto and Resultado != 0):
            Ganancia = Monto
            print(f"{Colors.GREEN}\t ¡Ganaste! {Resultado} es {AltoBajo}. Ganancia: {Ganancia:.2f}{Colors.RESET}")
        else:
            Ganancia = -Monto
            print(f"{Colors.RED}\t Perdiste. Resultado: {Resultado}{Colors.RESET}")
        Descripcion = f"Ruleta Europea - {AltoBajo.capitalize()}"
        
    elif TipoApuesta == "5":
        Docena = input(f"{Colors.MAGENTA}\t Elija docena (1-12, 13-24 o 25-36) -> {Colors.RESET}")
        if not ValidarSeleccionDocena(Docena):
            print(f"{Colors.RED}\t Docena inválida{Colors.RESET}")
            return
        
        if Docena == "1-12":
            RangoDocena = range(1, 13)
        elif Docena == "13-24":
            RangoDocena = range(13, 25)
        else:
            RangoDocena = range(25, 37)
        
        if Resultado in RangoDocena:
            Ganancia = Monto * 2
            print(f"{Colors.GREEN}\t ¡Ganaste! {Resultado} está en la docena. Ganancia: {Ganancia:.2f}{Colors.RESET}")
        else:
            Ganancia = -Monto
            print(f"{Colors.RED}\t Perdiste. Resultado: {Resultado}{Colors.RESET}")
        Descripcion = f"Ruleta Europea - Docena {Docena}"
        
    elif TipoApuesta == "6":
        Columna = input(f"{Colors.MAGENTA}\t Elija columna (1, 2 o 3) -> {Colors.RESET}")
        if not ValidarSeleccionColumna(Columna):
            print(f"{Colors.RED}\t Columna inválida{Colors.RESET}")
            return
        
        if Columna == "1":
            RangoColumna = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]
        elif Columna == "2":
            RangoColumna = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35]
        else:
            RangoColumna = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]
        
        if Resultado in RangoColumna:
            Ganancia = Monto * 2
            print(f"{Colors.GREEN}\t ¡Ganaste! {Resultado} está en la columna. Ganancia: {Ganancia:.2f}{Colors.RESET}")
        else:
            Ganancia = -Monto
            print(f"{Colors.RED}\t Perdiste. Resultado: {Resultado}{Colors.RESET}")
        Descripcion = f"Ruleta Europea - Columna {Columna}"
    else:
        print(f"{Colors.RED}\t Opción inválida{Colors.RESET}")
        return
    
    Jugador.ActualizarSaldo(Ganancia)
    print(f"{Colors.BLUE}\t Saldo: {Jugador.ConsultarSaldo():.2f}{Colors.RESET}")
    
    Apuesta = {
        "Jugador": Jugador.Usuario,
        "Tipo": Descripcion,
        "Monto": Monto,
        "Resultado": Resultado,
        "Ganancia": Ganancia,
        "SaldoRestante": Jugador.ConsultarSaldo()
    }
    data.AddApuesta(Apuesta)
    input(f"{Colors.BLUE}\t Presiona Enter para continuar...{Colors.RESET}")
    Console.clear()


def CalcularValorMano(Cartas):
    """Calcula el valor de una mano de blackjack, ajustando ases si es necesario"""
    Total = sum(Cartas)
    Ases = Cartas.count(11)
    while Total > 21 and Ases > 0:
        Total -= 10
        Ases -= 1
    return Total


def MostrarManoBlackjack(Nombre, Cartas, MostrarOculta=True):
    """Muestra la mano del jugador o crupier en blackjack"""
    if MostrarOculta and Nombre == "Crupier" and len(Cartas) > 1:
        print(f"{Colors.CYAN}\t {Nombre}: [{Cartas[0]}] [?] = {Cartas[0]}{Colors.RESET}")
    else:
        Valor = CalcularValorMano(Cartas)
        print(f"{Colors.CYAN}\t {Nombre}: {Cartas} = {Valor}{Colors.RESET}")


def Blackjack(Jugador):
    print(f"{Colors.MAGENTA}\t BIENVENIDO A BLACKJACK{Colors.RESET}")
    Monto = Validador(input(f"{Colors.YELLOW}\t Ingrese el monto de la apuesta -> {Colors.RESET}"), "decimal", f"{Colors.RED}\t Monto invalido, debe ser un numero positivo{Colors.RESET}", ValidarMontoPositivo)
    
    if not Jugador.TieneSaldoSuficiente(Monto):
        print(f"{Colors.RED}\t Saldo insuficiente{Colors.RESET}")
        return
    
    Mazo = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4
    
    ManoJugador = [choice(Mazo), choice(Mazo)]
    ManoCrupier = [choice(Mazo), choice(Mazo)]
    
    print(f"{Colors.YELLOW}\t --- INICIO DEL JUEGO ---{Colors.RESET}")
    MostrarManoBlackjack("Tu mano", ManoJugador, False)
    MostrarManoBlackjack("Crupier", ManoCrupier, True)
    
    ValorJugador = CalcularValorMano(ManoJugador)
    
    if ValorJugador == 21 and len(ManoJugador) == 2:
        print(f"{Colors.GREEN}\t ¡BLACKJACK! ¡Ganaste 3:2!{Colors.RESET}")
        Ganancia = Monto * 1.5
        Jugador.ActualizarSaldo(Ganancia)
        Apuesta = {
            "Jugador": Jugador.Usuario,
            "Tipo": "Blackjack",
            "Monto": Monto,
            "Resultado": "Blackjack",
            "Ganancia": Ganancia,
            "SaldoRestante": Jugador.ConsultarSaldo()
        }
        data.AddApuesta(Apuesta)
        input(f"{Colors.BLUE}\t Presiona Enter para continuar...{Colors.RESET}")
        Console.clear()
        return
    
    while True:
        Accion = input(f"{Colors.MAGENTA}\t ¿Pedir (h) o Plantarse (s)? -> {Colors.RESET}").lower()
        if Accion == "h":
            ManoJugador.append(choice(Mazo))
            ValorJugador = CalcularValorMano(ManoJugador)
            MostrarManoBlackjack("Tu mano", ManoJugador, False)
            if ValorJugador > 21:
                print(f"{Colors.RED}\t ¡Te pasaste de 21! Pierdes.{Colors.RESET}")
                Ganancia = -Monto
                break
        elif Accion == "s":
            break
        else:
            print(f"{Colors.RED}\t Acción no válida{Colors.RESET}")
    
    if ValorJugador <= 21:
        print(f"{Colors.YELLOW}\t --- TURNO DEL CRUPIER ---{Colors.RESET}")
        print(f"{Colors.CYAN}\t Crupier: {ManoCrupier}{Colors.RESET}")
        
        ValorCrupier = CalcularValorMano(ManoCrupier)
        while ValorCrupier < 17:
            ManoCrupier.append(choice(Mazo))
            ValorCrupier = CalcularValorMano(ManoCrupier)
            print(f"{Colors.CYAN}\t Crupier: {ManoCrupier} = {ValorCrupier}{Colors.RESET}")
        
        if ValorCrupier > 21:
            print(f"{Colors.GREEN}\t ¡El crupier se pasó! ¡Ganas!{Colors.RESET}")
            Ganancia = Monto
        elif ValorJugador > ValorCrupier:
            print(f"{Colors.GREEN}\t ¡Tu mano es mejor! ¡Ganas!{Colors.RESET}")
            Ganancia = Monto
        elif ValorJugador < ValorCrupier:
            print(f"{Colors.RED}\t La mano del crupier es mejor. Pierdes.{Colors.RESET}")
            Ganancia = -Monto
        else:
            print(f"{Colors.YELLOW}\t ¡Empate! Tu apuesta se devuelve.{Colors.RESET}")
            Ganancia = 0
    
    Jugador.ActualizarSaldo(Ganancia)
    print(f"{Colors.BLUE}\t Saldo: {Jugador.ConsultarSaldo():.2f}{Colors.RESET}")
    
    Apuesta = {
        "Jugador": Jugador.Usuario,
        "Tipo": "Blackjack",
        "Monto": Monto,
        "Resultado": f"Tu: {ValorJugador}",
        "Ganancia": Ganancia,
        "SaldoRestante": Jugador.ConsultarSaldo()
    }
    data.AddApuesta(Apuesta)
    input(f"{Colors.BLUE}\t Presiona Enter para continuar...{Colors.RESET}")
    Console.clear()
