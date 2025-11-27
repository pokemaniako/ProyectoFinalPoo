class ConsoleManager:
    """interfaz ligera para operaciones de consola

    no se usa abc para evitar imports adicionales
    """
    def clear(self):
        raise NotImplementedError()


class DefaultConsole(ConsoleManager):
    """implementacion por defecto que limpia pantalla con secuencia ansi"""
    def clear(self):
        # usar secuencia ansi en lugar de os.system
        print('\033[2J\033[H', end='')


# instancia reutilizable
Console = DefaultConsole()
