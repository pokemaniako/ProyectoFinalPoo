
def validador(dato, tipo, mensaje_error, restriccion=None):
    """Valida los datos ingresados según el tipo y restricciones especificadas."""
    while True:
        try:
            if tipo == "texto":
                # Validar solo letras (a-z, A-Z) y espacios
                if not all(c.isspace() or (c.lower() in 'abcdefghijklmnopqrstuvwxyz') for c in dato):
                    print(mensaje_error)
                    dato = input("\t Ingrese nuevamente -> ")
                    continue
            elif tipo == "numero":
                dato = int(dato)
                if restriccion and not restriccion(dato):
                    print(mensaje_error)
                    dato = input("\t Ingrese nuevamente -> ")
                    continue
            elif tipo == "decimal":
                dato = float(dato)
                if restriccion and not restriccion(dato):
                    print(mensaje_error)
                    dato = input("\t Ingrese nuevamente -> ")
                    continue
            elif tipo == "genero":
                dato = dato.upper()
                if dato not in ['M', 'F']:
                    print(mensaje_error)
                    dato = input("\t Ingrese nuevamente -> ")
                    continue
            return dato
        except ValueError:
            print(mensaje_error)
            dato = input("\t Ingrese nuevamente -> ")