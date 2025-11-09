from clases import GestionJugadores

GestionJugadores = GestionJugadores()
Apuestas = []

def AddJugador(Jugador):
    GestionJugadores.AgregarJugador(Jugador)

def FindPlayerByCredentials(Usuario, Contraseña):
    return GestionJugadores.BuscarPorCredenciales(Usuario, Contraseña)

def AddApuesta(Apuesta):
 
    if "Bono" in Apuesta:
        Apuesta["ApuestaGanada"] = Apuesta["Bono"] > 0
    elif "Eleccion" in Apuesta and "Resultado" in Apuesta:
        Apuesta["ApuestaGanada"] = Apuesta["Eleccion"] == Apuesta["Resultado"]
    
    Apuestas.append(Apuesta)
    for Jugador in GestionJugadores.ObtenerTodos():
        if Jugador.Usuario == Apuesta["Jugador"]:
            Jugador.AgregarApuesta(Apuesta)
            break
    from Csv.graficos import GuardarApuestaCsv
    GuardarApuestaCsv(Apuesta)
