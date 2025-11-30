from clases import GestionJugadores

GestionJugadores = GestionJugadores()
Apuestas = []

def AddJugador(Jugador):
    GestionJugadores.AgregarJugador(Jugador)

def FindPlayerByCredentials(Usuario, Contraseña):
    return GestionJugadores.BuscarPorCredenciales(Usuario, Contraseña)

def AddApuesta(Apuesta):
    # agregar flag de apuesta ganada para el historial y graficos
    if "Bono" in Apuesta:
        Apuesta["ApuestaGanada"] = Apuesta["Bono"] > 0
    elif "Ganancia" in Apuesta:
        # para apuestas nuevas que usan ganancia en lugar de bono
        Apuesta["ApuestaGanada"] = Apuesta["Ganancia"] > 0
    elif "Eleccion" in Apuesta and "Resultado" in Apuesta:
        # comparar como cadenas para evitar problemas de tipo
        Apuesta["ApuestaGanada"] = str(Apuesta["Eleccion"]).strip().lower() == str(Apuesta["Resultado"]).strip().lower()
    else:
        # por defecto, apuesta ganada es falso
        Apuesta["ApuestaGanada"] = False
    
    Apuestas.append(Apuesta)
    for Jugador in GestionJugadores.ObtenerTodos():
        if Jugador.Usuario == Apuesta["Jugador"]:
            Jugador.AgregarApuesta(Apuesta)
            break
    # Importar el módulo de graficos de forma dinámica sin depender de sys.path
    try:
        from Csv.graficos import GuardarApuestaCsv
        GuardarApuestaCsv(Apuesta)
    except ModuleNotFoundError:
        import os
        import importlib.util
        graficos_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Csv', 'graficos.py'))
        if os.path.exists(graficos_path):
            spec = importlib.util.spec_from_file_location('Csv.graficos', graficos_path)
            graficos = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(graficos)
            graficos.GuardarApuestaCsv(Apuesta)
        else:
            # si no existe el archivo, simplemente ignorar (no guardar)
            return
