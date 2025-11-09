def ValidarEspacioBlanco(Dato):
    """Valida que el dato no este vacio o solo contenga espacios"""
    return Dato.strip() != ""

def Validador(Dato, Tipo, MensajeError, Restriccion=None):
    """Valida datos segun tipo y restricciones"""
    while True:
        try:

            if not ValidarEspacioBlanco(Dato):
                print(MensajeError)
                Dato = input("\t Ingrese otra vez \n\t-> ")
                continue
                
            if Tipo == "texto":
                
                if not all(Caracter.isspace() or (Caracter.lower() in 'abcdefghijklmnopqrstuvwxyz') for Caracter in Dato):
                    print(MensajeError)
                    Dato = input("\t Ingrese otra vez \n\t-> ")
                    continue
            elif Tipo == "numero":
                Dato = int(Dato)
                if Restriccion and not Restriccion(Dato):
                    print(MensajeError)
                    Dato = input("\t Ingrese otra vez \n\t-> ")
                    continue
            elif Tipo == "decimal":
                Dato = float(Dato)
                if Restriccion and not Restriccion(Dato):
                    print(MensajeError)
                    Dato = input("\t Ingrese otra vez \n\t-> ")
                    continue
            elif Tipo == "genero":
                Dato = Dato.upper()
                if Dato not in ['M', 'F']:
                    print(MensajeError)
                    Dato = input("\t Ingrese otra vez \n\t-> ")
                    continue
            elif Tipo == "espacio":
                
                Dato = Dato.strip()
                if not Dato:
                    print(MensajeError)
                    Dato = input("\t Ingrese otra vez \n\t-> ")
                    continue
            
            return Dato
        except ValueError:
            print(MensajeError)
            Dato = input("\t Ingrese otra vez \n\t-> ")

def ValidarMontoPositivo(Monto):
    return Monto > 0

def ValidarNumeroRuleta(Numero):
    return 1 <= Numero <= 36

def ValidarNumerosDado(Numeros):
    if len(Numeros) != 3:
        return False
    try:
        N1 = int(Numeros[0])
        N2 = int(Numeros[1])
        N3 = int(Numeros[2])
        if N1 == N2 or N1 == N3 or N2 == N3:
            return False
        if not (1 <= N1 <= 6 and 1 <= N2 <= 6 and 1 <= N3 <= 6):
            return False
        return True
    except ValueError:
        return False
