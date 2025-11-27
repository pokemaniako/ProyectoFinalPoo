import pandas as pd
import matplotlib.pyplot as plt

# ruta al archivo csv de apuestas como cadena
file_path = __file__
normalized = file_path.replace('\\', '/')
csv_dir = normalized.rsplit('/', 1)[0]
CsvPath = csv_dir + '/Apuestas.csv'

def file_exists(path):
    try:
        with open(path, 'r', encoding='utf-8'):
            return True
    except Exception:
        return False

def GuardarApuestaCsv(Apuesta):
    Safe = {}
    for k, v in Apuesta.items():
        if isinstance(v, (list, tuple, dict)):
            Safe[k] = str(v)
        else:
            Safe[k] = v

    DfRow = pd.DataFrame([Safe])

    if not file_exists(CsvPath):
        DfRow.to_csv(CsvPath, index=False, quoting=1, encoding='utf-8')
    else:
        # Detect if the existing CSV lost its header (first row contains data instead)
        # leer la primera linea para detectar cabecera dañada
        try:
            with open(CsvPath, 'r', encoding='utf-8') as fh:
                first_line = fh.readline().strip()
        except Exception:
            first_line = ''

        # If the first line does not contain expected column names, try to repair
        if first_line and 'Jugador' not in first_line and (',' in first_line or '"' in first_line):
            try:
                existing = pd.read_csv(CsvPath, engine='python', header=None, on_bad_lines='skip', encoding='utf-8')
                # assign sensible column names based on current Apuesta keys
                expected_cols = list(DfRow.columns)
                # If the file has same number of columns as expected, set them; otherwise keep numeric names
                if existing.shape[1] == len(expected_cols):
                    existing.columns = expected_cols
                # overwrite file with header
                existing.to_csv(CsvPath, index=False, quoting=1, encoding='utf-8')
            except Exception:
                # if repair fails, continue and append — avoid crashing the program
                pass

        try:
            Cols = pd.read_csv(CsvPath, engine='python', on_bad_lines='skip', encoding='utf-8', nrows=0).columns.tolist()
            DfRow = DfRow.reindex(columns=Cols, fill_value='')
        except Exception:
            pass
        DfRow.to_csv(CsvPath, mode='a', header=False, index=False, quoting=1, encoding='utf-8')

    return


def GraficarApuestasPorUsuario(NombreUsuario):
    plt.close('all')
    try:
        Df = pd.read_csv(CsvPath, engine='python', on_bad_lines='skip', encoding='utf-8')
    except Exception:
        if file_exists(CsvPath):
            try:
                Df = pd.read_csv(CsvPath, engine='python', on_bad_lines='skip', encoding='utf-8')
            except Exception as e:
                print(f"Error al leer el archivo de datos: {e}")
                return
        else:
            print("No hay apuestas registradas todavía.")
            return

    if 'Jugador' not in Df.columns:
        print("El archivo de datos no contiene las columnas necesarias.")
        return

    def NormalizeBoolSeries(S):
        if S.dtype == bool:
            return S
        def ToBool(V):
            if pd.isna(V):
                return False
            if isinstance(V, (bool,)):
                return V
            if isinstance(V, (int, float)):
                return V != 0
            Vs = str(V).strip().lower()
            return Vs in ('true', '1', 'yes', 'si')
        return S.apply(ToBool)

    if 'ApuestaGanada' in Df.columns:
        Df['ApuestaGanada'] = NormalizeBoolSeries(Df['ApuestaGanada'])
    else:
        if 'Bono' in Df.columns:
            BonoNum = pd.to_numeric(Df['Bono'], errors='coerce').fillna(0)
            Df['ApuestaGanada'] = BonoNum > 0
        elif 'Eleccion' in Df.columns and 'Resultado' in Df.columns:
            Df['ApuestaGanada'] = Df['Eleccion'].astype(str).str.strip().str.lower() == Df['Resultado'].astype(str).str.strip().str.lower()
        else:
            MontoCol = 'Monto' if 'Monto' in Df.columns else ('MontoApostado' if 'MontoApostado' in Df.columns else None)
            if 'SaldoRestante' not in Df.columns or MontoCol is None:
                print("El archivo de datos no contiene las columnas necesarias.")
                return
            SaldoNum = pd.to_numeric(Df['SaldoRestante'], errors='coerce')
            MontoNum = pd.to_numeric(Df[MontoCol], errors='coerce')
            Df['ApuestaGanada'] = SaldoNum > MontoNum

    DfUsuario = Df[Df['Jugador'] == NombreUsuario]
    if DfUsuario.empty:
        print("No hay apuestas para este usuario.")
        return

    Ganadas = DfUsuario[DfUsuario['ApuestaGanada'] == True].shape[0]
    Perdidas = DfUsuario[DfUsuario['ApuestaGanada'] == False].shape[0]
    Total = Ganadas + Perdidas

    if Total == 0:
        print("No hay apuestas registradas para este usuario.")
        return

    PorcentajeGanadas = (Ganadas / Total) * 100
    PorcentajePerdidas = (Perdidas / Total) * 100

    Fig, Ax = plt.subplots(figsize=(8, 6))
    Bars = Ax.bar(['Ganadas', 'Perdidas'], [Ganadas, Perdidas], color=['green', 'red'])
    
    for Bar in Bars:
        Height = Bar.get_height()
        Ax.text(Bar.get_x() + Bar.get_width()/2., Height,
                f'{int(Height)}',
                ha='center', va='bottom')

    Ax.set_title(f'Historial de Apuestas de {NombreUsuario}')
    Ax.set_xlabel('Resultado')
    Ax.set_ylabel('Cantidad de Apuestas')
    
    plt.tight_layout()
    plt.show()
    
    plt.close()
    
    print(f"\nResumen de apuestas de {NombreUsuario}:")
    print(f"Total de apuestas: {Total}")
    print(f"Ganadas: {Ganadas} ({PorcentajeGanadas:.1f}%)")
    print(f"Perdidas: {Perdidas} ({PorcentajePerdidas:.1f}%)")


def GraficarSaldoEnTiempo(NombreUsuario):
    plt.close('all')
    try:
        Df = pd.read_csv(CsvPath, engine='python', on_bad_lines='skip', encoding='utf-8')
    except Exception:
        if file_exists(CsvPath):
            try:
                Df = pd.read_csv(CsvPath, engine='python', on_bad_lines='skip', encoding='utf-8')
            except Exception as e:
                print(f"Error al leer el archivo de datos: {e}")
                return
        else:
            print("No hay apuestas registradas todavía.")
            return

    if 'Jugador' not in Df.columns or 'SaldoRestante' not in Df.columns:
        print("El archivo de datos no contiene las columnas necesarias.")
        return

    DfUsuario = Df[Df['Jugador'] == NombreUsuario].reset_index(drop=True)
    if DfUsuario.empty:
        print("No hay apuestas para este usuario.")
        return

    SaldoNumeros = pd.to_numeric(DfUsuario['SaldoRestante'], errors='coerce').fillna(0)
    Indices = range(1, len(SaldoNumeros) + 1)

    Fig, Ax = plt.subplots(figsize=(10, 6))
    Ax.plot(Indices, SaldoNumeros, marker='o', linestyle='-', color='blue', linewidth=2, markersize=6)
    Ax.set_title(f'Evolución del Saldo de {NombreUsuario}')
    Ax.set_xlabel('Número de Apuesta')
    Ax.set_ylabel('Saldo Restante')
    Ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    plt.close()


def GraficarDistribucionGananciasPerdidas(NombreUsuario):
    plt.close('all')
    try:
        Df = pd.read_csv(CsvPath, engine='python', on_bad_lines='skip', encoding='utf-8')
    except Exception:
        if file_exists(CsvPath):
            try:
                Df = pd.read_csv(CsvPath, engine='python', on_bad_lines='skip', encoding='utf-8')
            except Exception as e:
                print(f"Error al leer el archivo de datos: {e}")
                return
        else:
            print("No hay apuestas registradas todavía.")
            return

    if 'Jugador' not in Df.columns:
        print("El archivo de datos no contiene las columnas necesarias.")
        return

    def NormalizeBoolSeries(S):
        if S.dtype == bool:
            return S
        def ToBool(V):
            if pd.isna(V):
                return False
            if isinstance(V, (bool,)):
                return V
            if isinstance(V, (int, float)):
                return V != 0
            Vs = str(V).strip().lower()
            return Vs in ('true', '1', 'yes', 'si')
        return S.apply(ToBool)

    if 'ApuestaGanada' in Df.columns:
        Df['ApuestaGanada'] = NormalizeBoolSeries(Df['ApuestaGanada'])
    else:
        if 'Bono' in Df.columns:
            BonoNum = pd.to_numeric(Df['Bono'], errors='coerce').fillna(0)
            Df['ApuestaGanada'] = BonoNum > 0
        elif 'Eleccion' in Df.columns and 'Resultado' in Df.columns:
            Df['ApuestaGanada'] = Df['Eleccion'].astype(str).str.strip().str.lower() == Df['Resultado'].astype(str).str.strip().str.lower()
        else:
            MontoCol = 'Monto' if 'Monto' in Df.columns else ('MontoApostado' if 'MontoApostado' in Df.columns else None)
            if 'SaldoRestante' not in Df.columns or MontoCol is None:
                print("El archivo de datos no contiene las columnas necesarias.")
                return
            SaldoNum = pd.to_numeric(Df['SaldoRestante'], errors='coerce')
            MontoNum = pd.to_numeric(Df[MontoCol], errors='coerce')
            Df['ApuestaGanada'] = SaldoNum > MontoNum

    DfUsuario = Df[Df['Jugador'] == NombreUsuario]
    if DfUsuario.empty:
        print("No hay apuestas para este usuario.")
        return

    Ganadas = DfUsuario[DfUsuario['ApuestaGanada'] == True].shape[0]
    Perdidas = DfUsuario[DfUsuario['ApuestaGanada'] == False].shape[0]
    Total = Ganadas + Perdidas

    if Total == 0:
        print("No hay apuestas registradas para este usuario.")
        return

    Fig, Ax = plt.subplots(figsize=(8, 6))
    Colores = ['green', 'red']
    Etiquetas = [f'Ganadas ({Ganadas})', f'Perdidas ({Perdidas})']
    Datos = [Ganadas, Perdidas]
    
    Wedges, Textos, Autotexts = Ax.pie(Datos, labels=Etiquetas, colors=Colores, autopct='%1.1f%%', startangle=90)
    
    for Autotext in Autotexts:
        Autotext.set_color('white')
        Autotext.set_fontweight('bold')
    
    Ax.set_title(f'Distribución Ganadas/Perdidas de {NombreUsuario}')
    
    plt.tight_layout()
    plt.show()
    plt.close()
