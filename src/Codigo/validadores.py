def ValidarEspacioBlanco(Dato):
    """Valida que el dato no esté vacío o solo contenga espacios"""
    return Dato.strip() != ""

def Validador(Dato, Tipo, MensajeError, Restriccion=None):
    """Valida los datos ingresados según el tipo y restricciones especificadas."""
    while True:
        try:
            # Validar espacio en blanco primero
            if not ValidarEspacioBlanco(Dato):
                print(MensajeError)
                Dato = input("\t Ingrese nuevamente -> ")
                continue
                
            if Tipo == "texto":
                # Validar solo letras (a-z, A-Z) y espacios
                if not all(Caracter.isspace() or (Caracter.lower() in 'abcdefghijklmnopqrstuvwxyz') for Caracter in Dato):
                    print(MensajeError)
                    Dato = input("\t Ingrese nuevamente -> ")
                    continue
            elif Tipo == "numero":
                Dato = int(Dato)
                if Restriccion and not Restriccion(Dato):
                    print(MensajeError)
                    Dato = input("\t Ingrese nuevamente -> ")
                    continue
            elif Tipo == "decimal":
                Dato = float(Dato)
                if Restriccion and not Restriccion(Dato):
                    print(MensajeError)
                    Dato = input("\t Ingrese nuevamente -> ")
                    continue
            elif Tipo == "genero":
                Dato = Dato.upper()
                if Dato not in ['M', 'F']:
                    print(MensajeError)
                    Dato = input("\t Ingrese nuevamente -> ")
                    continue
            elif Tipo == "espacio":
                # Validación específica para espacios (si es necesario)
                Dato = Dato.strip()
                if not Dato:
                    print(MensajeError)
                    Dato = input("\t Ingrese nuevamente -> ")
                    continue
            
            return Dato
        except ValueError:
            print(MensajeError)
            Dato = input("\t Ingrese nuevamente -> ")
