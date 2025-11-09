import pandas as pd
import matplotlib.pyplot as plt
import os
input("validado")
CsvPath = os.path.join(os.path.dirname(__file__), 'Apuestas.csv')

def GuardarApuestaCsv(Apuesta):
    Safe = {}
    for k, v in Apuesta.items():
        if isinstance(v, (list, tuple, dict)):
            Safe[k] = str(v)
        else:
            Safe[k] = v

    DfRow = pd.DataFrame([Safe])

    if not os.path.isfile(CsvPath):
        DfRow.to_csv(CsvPath, index=False, quoting=1, encoding='utf-8')
    else:
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
        if os.path.isfile(CsvPath):
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
