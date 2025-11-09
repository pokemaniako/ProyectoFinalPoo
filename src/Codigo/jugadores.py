import validadores as vt
from data import GestionJugadores, AddJugador, FindPlayerByCredentials
from clases import Jugador

def ValidarEdadMayor18(Edad):
    return Edad >= 18

def ValidarSaldoNoNegativo(Saldo):
    return Saldo >= 0

def RegistrarJugador():
    print("\t Has seleccionado REGISTRAR")
    Nombre = vt.Validador(input("\t Ingrese su nombre -> "), "texto", "\t Nombre inválido, solo letras y espacios permitidos.")
    ApellidoPaterno = vt.Validador(input("\t Ingrese su apellido paterno -> "), "texto", "\t Apellido paterno inválido, solo letras y espacios permitidos.")
    ApellidoMaterno = vt.Validador(input("\t Ingrese su apellido materno -> "), "texto", "\t Apellido materno inválido, solo letras y espacios permitidos.")
    Sexo = vt.Validador(input("\t Ingrese su genero (M: masculino, F: Femenino) -> "), "genero", "\t Género inválido, solo M o F.")
    Edad = vt.Validador(input("\t Ingrese su edad -> "), "numero", "\t Edad inválida, debe ser un número mayor a 18.", ValidarEdadMayor18)
    Usuario = vt.Validador(input("\t Cree un nombre de usuario -> "), "espacio", "\t El nombre de usuario no puede estar vacío.")
    
    # Verificar si el usuario ya existe
    if GestionJugadores.ExisteUsuario(Usuario):
        print("\t Este usuario ya existe. Por favor, elija otro.")
        return None
    
    Contraseña = vt.Validador(input("\t Cree una contraseña -> "), "espacio", "\t La contraseña no puede estar vacía.")
    Saldo = vt.Validador(input("\t Ingrese su saldo en soles -> "), "decimal", "\t Saldo inválido, debe ser un número no negativo.", ValidarSaldoNoNegativo)

    # Crear instancia de Jugador
    JugadorNuevo = Jugador(
        Nombre=Nombre,
        ApellidoPaterno=ApellidoPaterno,
        ApellidoMaterno=ApellidoMaterno,
        Genero=Sexo,
        Edad=Edad,
        Usuario=Usuario,
        Contraseña=Contraseña,
        Saldo=Saldo
    )
    
    AddJugador(JugadorNuevo)
    print(f"\t Usuario {Usuario} registrado con exito. Saldo inicial: {Saldo:.2f} solsitos")
    return JugadorNuevo

def IniciarSesion():
    print("\t Has seleccionado INICIAR SESIÓN")
    Usuario = vt.Validador(input("\t Usuario -> "), "espacio", "\t El nombre de usuario no puede estar vacío.")
    Contraseña = vt.Validador(input("\t Contraseña -> "), "espacio", "\t La contraseña no puede estar vacía.")
    
    JugadorEncontrado = FindPlayerByCredentials(Usuario, Contraseña)
    if JugadorEncontrado:
        print(f"\t\t\n Bienvenido de nuevo, {JugadorEncontrado.Nombre}!")
        return JugadorEncontrado
    
    print("\t Usuario o contraseña incorrecto")
    return None