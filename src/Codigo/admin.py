from colores import Colors
from console import Console
from clases import GestionJugadores, GestionAdministradores, Administrador

def MenuAdmin(Admin, GestionJugadores_Inst, GestionAdministradores_Inst):
    """Mini interfaz de administrador para gestionar apuestas y datos"""
    while True:
        print(f"""{Colors.RED}
        ╔════════════════════════════════════════════╗
        ║         PANEL DE ADMINISTRADOR             ║
        ║         Bienvenido: {Admin.Usuario:<24}║
        ╚════════════════════════════════════════════╝{Colors.RESET}
        """)
        print(f"{Colors.YELLOW}\t 1. Ver todos los jugadores{Colors.RESET}")
        print(f"{Colors.YELLOW}\t 2. Ver detalles de un jugador{Colors.RESET}")
        print(f"{Colors.YELLOW}\t 3. Ver todas las apuestas{Colors.RESET}")
        print(f"{Colors.YELLOW}\t 4. Modificar saldo de jugador{Colors.RESET}")
        print(f"{Colors.YELLOW}\t 5. Generar reporte{Colors.RESET}")
        print(f"{Colors.RED}\t 6. Cerrar sesión{Colors.RESET}")
        print(f"{Colors.MAGENTA}\t" + "=" * 52)
        
        Opcion = input(f"\t{Colors.MAGENTA}Seleccione una opción: {Colors.RESET}")
        
        if Opcion == "1":
            VerTodosJugadores(GestionJugadores_Inst)
        elif Opcion == "2":
            VerDetallesJugador(GestionJugadores_Inst)
        elif Opcion == "3":
            VerTodasApuestas(GestionJugadores_Inst)
        elif Opcion == "4":
            ModificarSaldoJugador(GestionJugadores_Inst)
        elif Opcion == "5":
            GenerarReporte(Admin, GestionJugadores_Inst)
        elif Opcion == "6":
            print(f"{Colors.GREEN}\t Sesión de admin cerrada. Hasta pronto.{Colors.RESET}")
            input(f"\t{Colors.BLUE}Presiona Enter para continuar...{Colors.RESET}")
            Console.clear()
            break
        else:
                print(f"{Colors.RED}\t Opción inválida{Colors.RESET}")
                input(f"\t{Colors.BLUE}Presiona Enter para continuar...{Colors.RESET}")
                Console.clear()


def VerTodosJugadores(GestionJugadores_Inst):
    """Muestra lista de todos los jugadores"""
    Jugadores = GestionJugadores_Inst.ObtenerTodos()
    if not Jugadores:
        print(f"{Colors.RED}\t No hay jugadores registrados{Colors.RESET}")
    else:
        print(f"{Colors.CYAN}\t --- LISTA DE JUGADORES ---{Colors.RESET}")
        for Jugador in Jugadores:
            print(f"{Colors.YELLOW}\t Usuario: {Jugador.Usuario} | Nombre: {Jugador.Nombre} {Jugador.ApellidoPaterno} | Saldo: {Jugador.ConsultarSaldo():.2f}{Colors.RESET}")
    input(f"\t{Colors.BLUE}Presiona Enter para continuar...{Colors.RESET}")
    Console.clear()


def VerDetallesJugador(GestionJugadores_Inst):
    """Muestra detalles de un jugador específico"""
    Usuario = input(f"{Colors.MAGENTA}\t Ingrese usuario del jugador -> {Colors.RESET}")
    Jugador = None
    for J in GestionJugadores_Inst.ObtenerTodos():
        if J.Usuario == Usuario:
            Jugador = J
            break
    
    if not Jugador:
        print(f"{Colors.RED}\t Jugador no encontrado{Colors.RESET}")
    else:
        print(f"{Colors.CYAN}\t --- DETALLES DEL JUGADOR ---{Colors.RESET}")
        print(f"{Colors.YELLOW}\t Usuario: {Jugador.Usuario}{Colors.RESET}")
        print(f"{Colors.YELLOW}\t Nombre: {Jugador.Nombre} {Jugador.ApellidoPaterno} {Jugador.ApellidoMaterno}{Colors.RESET}")
        print(f"{Colors.YELLOW}\t Edad: {Jugador.Edad}{Colors.RESET}")
        print(f"{Colors.YELLOW}\t Género: {Jugador.Genero}{Colors.RESET}")
        print(f"{Colors.YELLOW}\t Saldo: {Jugador.ConsultarSaldo():.2f}{Colors.RESET}")
        print(f"{Colors.YELLOW}\t Total apuestas: {len(Jugador.ObtenerHistorial())}{Colors.RESET}")
    input(f"\t{Colors.BLUE}Presiona Enter para continuar...{Colors.RESET}")
    Console.clear()


def VerTodasApuestas(GestionJugadores_Inst):
    """Muestra todas las apuestas de todos los jugadores"""
    print(f"{Colors.CYAN}\t --- TODAS LAS APUESTAS ---{Colors.RESET}")
    TotalApuestas = 0
    for Jugador in GestionJugadores_Inst.ObtenerTodos():
        Historial = Jugador.ObtenerHistorial()
        if Historial:
            print(f"{Colors.YELLOW}\t Jugador: {Jugador.Usuario}{Colors.RESET}")
            for Apuesta in Historial:
                print(f"{Colors.PLOMO}\t  - {Apuesta}{Colors.RESET}")
                TotalApuestas += 1
    print(f"{Colors.GREEN}\t Total de apuestas: {TotalApuestas}{Colors.RESET}")
    input(f"\t{Colors.BLUE}Presiona Enter para continuar...{Colors.RESET}")
    Console.clear()


def ModificarSaldoJugador(GestionJugadores_Inst):
    """Modifica el saldo de un jugador"""
    Usuario = input(f"{Colors.MAGENTA}\t Ingrese usuario del jugador -> {Colors.RESET}")
    Jugador = None
    for J in GestionJugadores_Inst.ObtenerTodos():
        if J.Usuario == Usuario:
            Jugador = J
            break
    
    if not Jugador:
        print(f"{Colors.RED}\t Jugador no encontrado{Colors.RESET}")
    else:
        print(f"{Colors.YELLOW}\t Saldo actual: {Jugador.ConsultarSaldo():.2f}{Colors.RESET}")
        try:
            Monto = float(input(f"{Colors.MAGENTA}\t Ingrese monto a sumar (negativo para restar) -> {Colors.RESET}"))
            Jugador.ActualizarSaldo(Monto)
            print(f"{Colors.GREEN}\t Nuevo saldo: {Jugador.ConsultarSaldo():.2f}{Colors.RESET}")
        except ValueError:
            print(f"{Colors.RED}\t Monto inválido{Colors.RESET}")
    input(f"\t{Colors.BLUE}Presiona Enter para continuar...{Colors.RESET}")
    Console.clear()


def GenerarReporte(Admin, GestionJugadores_Inst):
    """Genera un reporte de estadísticas generales"""
    Jugadores = GestionJugadores_Inst.ObtenerTodos()
    TotalJugadores = len(Jugadores)
    TotalApuestas = sum(len(J.ObtenerHistorial()) for J in Jugadores)
    SaldoTotal = sum(J.ConsultarSaldo() for J in Jugadores)
    
    print(f"{Colors.CYAN}\t --- REPORTE GENERAL ---{Colors.RESET}")
    print(f"{Colors.YELLOW}\t Generado por: {Admin.Usuario}{Colors.RESET}")
    print(f"{Colors.YELLOW}\t Total de jugadores: {TotalJugadores}{Colors.RESET}")
    print(f"{Colors.YELLOW}\t Total de apuestas: {TotalApuestas}{Colors.RESET}")
    print(f"{Colors.YELLOW}\t Saldo total (en circulación): {SaldoTotal:.2f}{Colors.RESET}")
    
    if TotalJugadores > 0:
        SaldoPromedio = SaldoTotal / TotalJugadores
        print(f"{Colors.YELLOW}\t Saldo promedio por jugador: {SaldoPromedio:.2f}{Colors.RESET}")
    
    input(f"\t{Colors.BLUE}Presiona Enter para continuar...{Colors.RESET}")
    Console.clear()
