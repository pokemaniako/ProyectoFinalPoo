from random import choice
from console import Console
from validadores import Validador, ValidarMontoPositivo
from colores import Colors
import data


def RuletaEuropea(Jugador):
    print(f"{Colors.GREEN}\t Has seleccionado RULETA EUROPEA (0-36){Colors.RESET}")
    Monto = Validador(input(f"{Colors.YELLOW}\t Ingrese el monto de la apuesta -> {Colors.RESET}"), "decimal", f"{Colors.RED}\t Monto invalido, debe ser un numero positivo{Colors.RESET}", ValidarMontoPositivo)
    
    if not Jugador.TieneSaldoSuficiente(Monto):
        print(f"{Colors.RED}\t Saldo insuficiente{Colors.RESET}")
        return

    # Definir colores para ruleta europea (0 es verde)
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
    
    if TipoApuesta == "1":  # Directo
        Numero = Validador(input(f"{Colors.MAGENTA}\t Ingrese numero (0-36) -> {Colors.RESET}"), "numero", f"{Colors.RED}\t Numero invalido{Colors.RESET}", lambda x: 0 <= x <= 36)
        if Numero == Resultado:
            Ganancia = Monto * 35
            print(f"{Colors.GREEN}\t ¡Ganaste! {Resultado} es el numero ganador. Ganancia: {Ganancia:.2f}{Colors.RESET}")
        else:
            Ganancia = -Monto
            print(f"{Colors.RED}\t Perdiste. Resultado: {Resultado}{Colors.RESET}")
        Descripcion = f"Ruleta Europea - Directo ({Numero})"
        
    elif TipoApuesta == "2":  # Rojo o Negro
        Color = input(f"{Colors.MAGENTA}\t Elija '{Colors.RED}rojo{Colors.RESET}{Colors.MAGENTA}' o '{Colors.PLOMO}negro{Colors.RESET}{Colors.MAGENTA}' -> {Colors.RESET}").lower()
        if Color not in ["rojo", "negro"]:
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
        
    elif TipoApuesta == "3":  # Par o Impar
        Paridad = input(f"{Colors.MAGENTA}\t Elija 'par' o 'impar' -> {Colors.RESET}").lower()
        if Paridad not in ["par", "impar"]:
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
        
    elif TipoApuesta == "4":  # Alto o Bajo
        AltoBajo = input(f"{Colors.MAGENTA}\t Elija 'alto' (19-36) o 'bajo' (1-18) -> {Colors.RESET}").lower()
        if AltoBajo not in ["alto", "bajo"]:
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
        
    elif TipoApuesta == "5":  # Docena
        Docena = input(f"{Colors.MAGENTA}\t Elija docena (1-12, 13-24 o 25-36) -> {Colors.RESET}")
        if Docena == "1-12":
            RangoDocena = range(1, 13)
        elif Docena == "13-24":
            RangoDocena = range(13, 25)
        elif Docena == "25-36":
            RangoDocena = range(25, 37)
        else:
            print(f"{Colors.RED}\t Docena inválida{Colors.RESET}")
            return
        
        if Resultado in RangoDocena:
            Ganancia = Monto * 2
            print(f"{Colors.GREEN}\t ¡Ganaste! {Resultado} está en la docena. Ganancia: {Ganancia:.2f}{Colors.RESET}")
        else:
            Ganancia = -Monto
            print(f"{Colors.RED}\t Perdiste. Resultado: {Resultado}{Colors.RESET}")
        Descripcion = f"Ruleta Europea - Docena {Docena}"
        
    elif TipoApuesta == "6":  # Columna
        Columna = input(f"{Colors.MAGENTA}\t Elija columna (1, 2 o 3) -> {Colors.RESET}")
        if Columna == "1":
            RangoColumna = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]
        elif Columna == "2":
            RangoColumna = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35]
        elif Columna == "3":
            RangoColumna = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]
        else:
            print(f"{Colors.RED}\t Columna inválida{Colors.RESET}")
            return
        
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


def Blackjack(Jugador):
    print(f"{Colors.MAGENTA}\t BIENVENIDO A BLACKJACK{Colors.RESET}")
    Monto = Validador(input(f"{Colors.YELLOW}\t Ingrese el monto de la apuesta -> {Colors.RESET}"), "decimal", f"{Colors.RED}\t Monto invalido, debe ser un numero positivo{Colors.RESET}", ValidarMontoPositivo)
    
    if not Jugador.TieneSaldoSuficiente(Monto):
        print(f"{Colors.RED}\t Saldo insuficiente{Colors.RESET}")
        return
    
    # Mazo simple (valores de cartas)
    Mazo = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4  # As es 11 al inicio
    
    def CalcularValor(Cartas):
        """Calcula el valor de una mano, ajustando ases si es necesario"""
        Total = sum(Cartas)
        Ases = Cartas.count(11)
        while Total > 21 and Ases > 0:
            Total -= 10
            Ases -= 1
        return Total
    
    def MostrarMano(Nombre, Cartas, MostrarOculta=True):
        """Muestra la mano del jugador o crupier"""
        if MostrarOculta and Nombre == "Crupier" and len(Cartas) > 1:
            print(f"{Colors.CYAN}\t {Nombre}: [{Cartas[0]}] [?] = {Cartas[0]}{Colors.RESET}")
        else:
            Valor = CalcularValor(Cartas)
            print(f"{Colors.CYAN}\t {Nombre}: {Cartas} = {Valor}{Colors.RESET}")
    
    # Repartir cartas iniciales
    ManoJugador = [choice(Mazo), choice(Mazo)]
    ManoCrupier = [choice(Mazo), choice(Mazo)]
    
    print(f"{Colors.YELLOW}\t --- INICIO DEL JUEGO ---{Colors.RESET}")
    MostrarMano("Tu mano", ManoJugador, False)
    MostrarMano("Crupier", ManoCrupier, True)
    
    ValorJugador = CalcularValor(ManoJugador)
    
    # Verificar blackjack inicial
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
    
    # Turno del jugador
    while True:
        Accion = input(f"{Colors.MAGENTA}\t ¿Pedir (h) o Plantarse (s)? -> {Colors.RESET}").lower()
        if Accion == "h":
            ManoJugador.append(choice(Mazo))
            ValorJugador = CalcularValor(ManoJugador)
            MostrarMano("Tu mano", ManoJugador, False)
            if ValorJugador > 21:
                print(f"{Colors.RED}\t ¡Te pasaste de 21! Pierdes.{Colors.RESET}")
                Ganancia = -Monto
                break
        elif Accion == "s":
            break
        else:
            print(f"{Colors.RED}\t Acción no válida{Colors.RESET}")
    
    # Si no se pasó, turno del crupier
    if ValorJugador <= 21:
        print(f"{Colors.YELLOW}\t --- TURNO DEL CRUPIER ---{Colors.RESET}")
        print(f"{Colors.CYAN}\t Crupier: {ManoCrupier}{Colors.RESET}")
        
        ValorCrupier = CalcularValor(ManoCrupier)
        while ValorCrupier < 17:
            ManoCrupier.append(choice(Mazo))
            ValorCrupier = CalcularValor(ManoCrupier)
            print(f"{Colors.CYAN}\t Crupier: {ManoCrupier} = {ValorCrupier}{Colors.RESET}")
        
        # Comparar manos
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
