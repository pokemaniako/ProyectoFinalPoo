from clases import GestionJugadores

GestionJugadores = GestionJugadores()
Apuestas = []

def AddJugador(Jugador):
    GestionJugadores.AgregarJugador(Jugador)

def FindPlayerByCredentials(Usuario, Contraseña):
    return GestionJugadores.BuscarPorCredenciales(Usuario, Contraseña)

def AddApuesta(Apuesta):
    # Determinar si la apuesta fue ganada
    if "Bono" in Apuesta:
        # Para el juego de dados
        Apuesta["ApuestaGanada"] = Apuesta["Bono"] > 0
    elif "Eleccion" in Apuesta and "Resultado" in Apuesta:
        # Para ruleta y rojo/negro
        Apuesta["ApuestaGanada"] = Apuesta["Eleccion"] == Apuesta["Resultado"]
    
    Apuestas.append(Apuesta)
    # Buscar el jugador por su nombre de usuario en la lista de jugadores
    for Jugador in GestionJugadores.ObtenerTodos():
        if Jugador.Usuario == Apuesta["Jugador"]:
            Jugador.AgregarApuesta(Apuesta)
            break
    # Guardar la apuesta en el archivo XLSX/CSV usando el módulo en src/Csv
    from Csv.graficos import GuardarApuestaCsv
    GuardarApuestaCsv(Apuesta)
