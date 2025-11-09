jugadores = []
apuestas = []

def AddJugador(jugador):
    jugadores.append(jugador)

def FindPlayerByCredentials(usuario, contraseña):
    for j in jugadores:
        if j["usuario"] == usuario and j["contraseña"] == contraseña:
            return j
    return 0

def AddApuesta(apuesta):
    apuestas.append(apuesta)