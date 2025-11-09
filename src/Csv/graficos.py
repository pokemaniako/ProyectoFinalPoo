import pandas as pd
import matplotlib.pyplot as plt
import os

# Rutas para los archivos
XlsxPath = os.path.join(os.path.dirname(__file__), 'Apuestas.xlsx')
CsvPath = os.path.join(os.path.dirname(__file__), 'Apuestas.csv')

def GuardarApuestaCsv(Apuesta):
    """Guarda la apuesta en CSV y luego intenta convertir a XLSX."""
    df_new = pd.DataFrame([Apuesta])
    
    # Primero, siempre guardamos en CSV (nuestro respaldo seguro)
    if not os.path.isfile(CsvPath):
        df_new.to_csv(CsvPath, index=False)
    else:
        df_new.to_csv(CsvPath, mode='a', header=False, index=False)
    
    try:
        # Intentar crear/actualizar el XLSX desde el CSV completo
        df_complete = pd.read_csv(CsvPath)
        df_complete.to_excel(XlsxPath, index=False, engine=None)  # engine=None intentará usar el mejor disponible
    except Exception as e:
        # Si falla la conversión a XLSX, no hay problema, ya tenemos el CSV
        print(f"Nota: Los datos están seguros en CSV. XLSX no disponible: {e}")


def GraficarApuestasPorUsuario(NombreUsuario):
    """Genera un gráfico de barras de apuestas ganadas y perdidas para el usuario."""
    # Cerrar todas las figuras existentes
    plt.close('all')
    
    # Primero intentamos leer el XLSX, si falla usamos el CSV
    try:
        if os.path.isfile(XlsxPath):
            df = pd.read_excel(XlsxPath, engine=None)  # engine=None intentará usar el mejor disponible
        else:
            df = pd.read_csv(CsvPath)  # Si no hay XLSX, usar CSV
    except Exception:
        # Si falla la lectura del XLSX, intentar con CSV
        if os.path.isfile(CsvPath):
            try:
                df = pd.read_csv(CsvPath)
            except Exception as e:
                print(f"Error al leer el archivo de datos: {e}")
                return
        else:
            print("No hay apuestas registradas todavía.")
            return

    if 'Jugador' not in df.columns or 'ApuestaGanada' not in df.columns:
        # Si no existe la columna ApuestaGanada, intentamos determinar por SaldoRestante y MontoApostado
        if 'SaldoRestante' not in df.columns or 'MontoApostado' not in df.columns:
            print("El archivo de datos no contiene las columnas necesarias.")
            return
        # Calculamos si ganó comparando el saldo restante con el monto apostado
        df['ApuestaGanada'] = df.apply(lambda row: row['SaldoRestante'] > row['MontoApostado'], axis=1)

    dfUsuario = df[df['Jugador'] == NombreUsuario]
    if dfUsuario.empty:
        print("No hay apuestas para este usuario.")
        return

    # Contar apuestas ganadas y perdidas
    Ganadas = dfUsuario[dfUsuario['ApuestaGanada'] == True].shape[0]
    Perdidas = dfUsuario[dfUsuario['ApuestaGanada'] == False].shape[0]
    Total = Ganadas + Perdidas
    
    if Total == 0:
        print("No hay apuestas registradas para este usuario.")
        return

    PorcentajeGanadas = (Ganadas / Total) * 100
    PorcentajePerdidas = (Perdidas / Total) * 100

    # Crear una única figura
    fig, ax = plt.subplots(figsize=(8, 6))
    bars = ax.bar(['Ganadas', 'Perdidas'], [Ganadas, Perdidas], color=['green', 'red'])
    
    # Añadir etiquetas con valores exactos sobre las barras
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom')

    ax.set_title(f'Historial de Apuestas de {NombreUsuario}')
    ax.set_xlabel('Resultado')
    ax.set_ylabel('Cantidad de Apuestas')
    
    # Ajustar el diseño y mostrar
    plt.tight_layout()
    plt.show()
    
    # Cerrar la figura actual
    plt.close()
    
    print(f"\nResumen de apuestas de {NombreUsuario}:")
    print(f"Total de apuestas: {Total}")
    print(f"Ganadas: {Ganadas} ({PorcentajeGanadas:.1f}%)")
    print(f"Perdidas: {Perdidas} ({PorcentajePerdidas:.1f}%)")
