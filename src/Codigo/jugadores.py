import validadores as vt
from data import GestionJugadores, AddJugador, FindPlayerByCredentials
from clases import Jugador

def ValidarEdadMayor18(Edad):
    return Edad >= 18

def ValidarSaldoNoNegativo(Saldo):
    return Saldo >= 0

def RegistrarJugador():
    print("\t Has seleccionado REGISTRO")
    Nombre = vt.Validador(input("\t Ingrese su nombre -> "), "texto", "\t Nombre invalido, solo letras y espacios")
    ApellidoPaterno = vt.Validador(input("\t Ingrese su apellido paterno -> "), "texto", "\t Apellido invalido, solo letras y espacios")
    ApellidoMaterno = vt.Validador(input("\t Ingrese su apellido materno -> "), "texto", "\t Apellido invalido, solo letras y espacios")
    Sexo = vt.Validador(input("\t Ingrese su genero (M/F) -> "), "genero", "\t Genero invalido, solo M o F")
    Edad = vt.Validador(input("\t Ingrese su edad -> "), "numero", "\t Edad invalida, debe ser mayor o igual a 18", ValidarEdadMayor18)
    Usuario = vt.Validador(input("\t Cree un nombre de usuario -> "), "espacio", "\t El nombre de usuario no puede estar vacio")
    

    if GestionJugadores.ExisteUsuario(Usuario):
        print("\t Usuario ya existe, elija otro")
        return None
    
    Contraseña = vt.Validador(input("\t Cree una contraseña -> "), "espacio", "\t La contraseña no puede estar vacia")
    Saldo = vt.Validador(input("\t Ingrese su saldo en soles -> "), "decimal", "\t Saldo invalido, debe ser un numero no negativo", ValidarSaldoNoNegativo)

  
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
    print(f"\t Usuario {Usuario} registrado. Saldo inicial: {Saldo:.2f}")
    return JugadorNuevo

def IniciarSesion():
    print("\t Has seleccionado iniciar sesion")
    Usuario = vt.Validador(input("\t Usuario -> "), "espacio", "\t El nombre de usuario no puede estar vacio")
    Contraseña = vt.Validador(input("\t Contrasena -> "), "espacio", "\t La contrasena no puede estar vacia")
    
    JugadorEncontrado = FindPlayerByCredentials(Usuario, Contraseña)
    if JugadorEncontrado:
        print(f"\t Bienvenido, {JugadorEncontrado.Nombre}")
        return JugadorEncontrado
    
    print("\t Usuario o contrasena incorrectos")
    return None