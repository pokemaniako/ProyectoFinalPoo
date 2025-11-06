import validadores as vt
import data

def RegistrarJugador():
    print("\t Has seleccionado REGISTRAR")
    Nombre = vt.validador(input("\t Ingrese su nombre -> "), "texto", "\t Nombre inválido, solo letras y espacios permitidos.")
    ApellidoPaterno = vt.validador(input("\t Ingrese su apellido paterno -> "), "texto", "\t Apellido paterno inválido, solo letras y espacios permitidos.")
    ApellidoMaterno = vt.validador(input("\t Ingrese su apellido materno -> "), "texto", "\t Apellido materno inválido, solo letras y espacios permitidos.")
    Sexo = vt.validador(input("\t Ingrese su genero (M: masculino, F: Femenino) -> "), "genero", "\t Género inválido, solo M o F.")
    Edad = vt.validador(input("\t Ingrese su edad -> "), "numero", "\t Edad inválida, debe ser un número mayor a 18.", lambda x: x >= 18)
    Usuario = input("\t Cree un nombre de usuario -> ")
    Contraseña = input("\t Cree una contraseña -> ")
    Saldo = vt.validador(input("\t Ingrese su saldo en soles -> "), "decimal", "\t Saldo inválido, debe ser un número no negativo.", lambda x: x >= 0)

    Jugador = {
        "nombre": Nombre,
        "apellido_paterno": ApellidoPaterno,
        "apellido_materno": ApellidoMaterno,
        "genero": Sexo,
        "edad": Edad,
        "usuario": Usuario,
        "contraseña": Contraseña,
        "saldo": Saldo
    }
    data.AddJugador(Jugador)
    print(f"\t Usuario {Usuario} registrado con exito. Saldo inicial: {Saldo:.2f} solsitos")
    return Jugador

def IniciarSesion():
    print("\t Has seleccionado INICIAR SESIÓN")
    Usuario = input("\t Usuario -> ")
    Contraseña = input("\t Contraseña -> ")
    Jugador = data.FindPlayerByCredentials(Usuario, Contraseña)
    if Jugador:
        print(f"\t\t\n Bienvenido de nuevo, {Jugador['nombre']}!")
        if Jugador != 0:
            return Jugador
    print("\t Usuario o contraseña incorrecto")
    return 0