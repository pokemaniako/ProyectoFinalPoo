class Persona:
    def __init__(self, Nombre, ApellidoPaterno, ApellidoMaterno, Genero, Edad, Usuario, Contraseña):
        self.Nombre = Nombre
        self.ApellidoPaterno = ApellidoPaterno
        self.ApellidoMaterno = ApellidoMaterno
        self.Genero = Genero
        self.Edad = Edad
        self.Usuario = Usuario
        self.Contraseña = Contraseña

class Jugador(Persona):
    def __init__(self, Nombre, ApellidoPaterno, ApellidoMaterno, Genero, Edad, Usuario, Contraseña, Saldo):
        super().__init__(Nombre, ApellidoPaterno, ApellidoMaterno, Genero, Edad, Usuario, Contraseña)
        self.Saldo = Saldo
        self.Apuestas = []
    
    def ConsultarSaldo(self):
        return self.Saldo
    
    def ActualizarSaldo(self, Monto):
        self.Saldo += Monto
        return self.Saldo
    
    def TieneSaldoSuficiente(self, Monto):
        return self.Saldo >= Monto
    
    def AgregarApuesta(self, Apuesta):
        self.Apuestas.append(Apuesta)
    
    def ObtenerHistorial(self):
        return self.Apuestas
#Nota: todavia falta implementar en el menu de inicio opcion de admin y usuario, la estructura de clases con herencia y polimorfismo ya esta
class Administrador(Persona):
    def __init__(self, Nombre, ApellidoPaterno, ApellidoMaterno, Genero, Edad, Usuario, Contraseña, NivelAcceso):
        super().__init__(Nombre, ApellidoPaterno, ApellidoMaterno, Genero, Edad, Usuario, Contraseña)
        self.NivelAcceso = NivelAcceso
    
    def GenerarReporte(self):
        return "Reporte generado"
    
    def GestionarJugadores(self):
        return "Gestión de jugadores"

class GestionJugadores:
    def __init__(self):
        self.Jugadores = []
    
    def AgregarJugador(self, Jugador):
        self.Jugadores.append(Jugador)
    
    def BuscarPorCredenciales(self, Usuario, Contraseña):
        for Jugador in self.Jugadores:
            if Jugador.Usuario == Usuario and Jugador.Contraseña == Contraseña:
                return Jugador
        return None
    
    def ExisteUsuario(self, Usuario):
        return any(Jugador.Usuario == Usuario for Jugador in self.Jugadores)
    
    def ObtenerTodos(self):
        return self.Jugadores

class GestionAdministradores:
    def __init__(self):
        self.Administradores = []
    
    def AgregarAdministrador(self, Administrador):
        self.Administradores.append(Administrador)
    
    def BuscarAdministrador(self, Usuario, Contraseña):
        for Administrador in self.Administradores:
            if Administrador.Usuario == Usuario and Administrador.Contraseña == Contraseña:
                return Administrador
        return None
