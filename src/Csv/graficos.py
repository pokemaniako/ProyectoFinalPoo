import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Ruta al archivo CSV de apuestas (Path object para operaciones más seguras)
CsvPath = Path(__file__).parent / 'Apuestas.csv'

def CargarDatos(NombreUsuario):
    """Carga y normaliza datos del CSV para un usuario.

    Devuelve un DataFrame filtrado por `Jugador` o None si no hay datos.
    """
    try:
        if not CsvPath.exists():
            # No hay archivo aún
            print(f"No se encontró {CsvPath}. Aún no hay apuestas guardadas.")
            return None
        Df = pd.read_csv(CsvPath, engine='python', on_bad_lines='skip', encoding='utf-8')
    except Exception as e:
        print(f"Error al leer CSV: {e}")
        return None

    if 'Jugador' not in Df.columns:
        print("El archivo no contiene la columna 'Jugador'.")
        return None

    DfUsuario = Df[Df['Jugador'] == NombreUsuario].copy()
    if DfUsuario.empty:
        print(f"No hay apuestas para el usuario: {NombreUsuario}")
        return None

    # Reset index for plotting convenience
    DfUsuario.reset_index(drop=True, inplace=True)
    return DfUsuario

def NormalizarApuestaGanada(Df):
    """Normaliza la columna ApuestaGanada"""
    if 'ApuestaGanada' not in Df.columns:
        if 'Ganancia' in Df.columns:
            Df['ApuestaGanada'] = pd.to_numeric(Df['Ganancia'], errors='coerce') > 0
        else:
            Df['ApuestaGanada'] = False
    return Df

def GuardarApuestaCsv(Apuesta):
    """Guarda una apuesta en el CSV"""
    Safe = {k: str(v) if isinstance(v, (list, tuple, dict)) else v for k, v in Apuesta.items()}
    DfRow = pd.DataFrame([Safe])
    
    try:
        if not Path(CsvPath).exists():
            DfRow.to_csv(CsvPath, index=False, quoting=1, encoding='utf-8')
        else:
            Cols = pd.read_csv(CsvPath, engine='python', on_bad_lines='skip', encoding='utf-8', nrows=0).columns.tolist()
            DfRow = DfRow.reindex(columns=Cols, fill_value='')
            DfRow.to_csv(CsvPath, mode='a', header=False, index=False, quoting=1, encoding='utf-8')
    except Exception as e:
        print(f"Error al guardar apuesta: {e}")


def Dashboard(NombreUsuario):
    """Dashboard con 3 gráficos: pizza (ganadas/perdidas), línea (evolución saldo) y barras (por tipo de juego)"""
    plt.close('all')
    
    DfUsuario = CargarDatos(NombreUsuario)
    if DfUsuario is None:
        return
    
    DfUsuario = NormalizarApuestaGanada(DfUsuario.copy())
    
    # Crear figura con 3 subplots
    Fig, Axes = plt.subplots(1, 3, figsize=(15, 5))
    Fig.suptitle(f'Dashboard de Apuestas - {NombreUsuario}', fontsize=14, fontweight='bold')
    
    # --- Gráfico 1: Pizza (Ganadas vs Perdidas) ---
    Ganadas = (DfUsuario['ApuestaGanada'] == True).sum()
    Perdidas = (DfUsuario['ApuestaGanada'] == False).sum()
    
    Axes[0].pie([Ganadas, Perdidas], labels=[f'Ganadas ({Ganadas})', f'Perdidas ({Perdidas})'], 
                colors=['green', 'red'], autopct='%1.1f%%', startangle=90)
    Axes[0].set_title('Distribución Ganadas/Perdidas')
    
    # --- Gráfico 2: Línea (Evolución del Saldo) ---
    if 'SaldoRestante' in DfUsuario.columns:
        SaldoNumeros = pd.to_numeric(DfUsuario['SaldoRestante'], errors='coerce').fillna(0).values
        Indices = range(1, len(SaldoNumeros) + 1)
        Axes[1].plot(Indices, SaldoNumeros, marker='o', linestyle='-', color='blue', linewidth=2, markersize=4)
        Axes[1].set_title('Evolución del Saldo')
        Axes[1].set_xlabel('Número de Apuesta')
        Axes[1].set_ylabel('Saldo Restante')
        Axes[1].grid(True, alpha=0.3)
    else:
        Axes[1].text(0.5, 0.5, 'Sin datos de Saldo', ha='center', va='center', transform=Axes[1].transAxes)
        Axes[1].set_title('Evolución del Saldo')
    
    # --- Gráfico 3: Barras (Apuestas por Tipo) ---
    if 'Tipo' in DfUsuario.columns and DfUsuario['Tipo'].notna().any():
        # Normalizar a string (evita listas/tuplas serializadas)
        Tipos = DfUsuario['Tipo'].astype(str).str.strip()
        # Contar apariciones
        TiposCuenta = Tipos.value_counts()

        if TiposCuenta.empty:
            Axes[2].text(0.5, 0.5, 'Sin datos de Tipo', ha='center', va='center', transform=Axes[2].transAxes)
            Axes[2].set_title('Apuestas por Tipo')
        else:
            # Si hay demasiadas categorías, mostrar top N + 'Otros'
            TopN = 10
            if len(TiposCuenta) > TopN:
                top = TiposCuenta.iloc[:TopN].copy()
                others = TiposCuenta.iloc[TopN:].sum()
                top['Otros'] = others
                PlotCounts = top
            else:
                PlotCounts = TiposCuenta

            x = list(range(len(PlotCounts)))
            bars = Axes[2].bar(x, PlotCounts.values, color='skyblue', edgecolor='navy')
            Axes[2].set_xticks(x)
            Axes[2].set_xticklabels(PlotCounts.index, rotation=45, ha='right', fontsize=8)
            Axes[2].set_title('Apuestas por Tipo')
            Axes[2].set_ylabel('Cantidad')

            # Añadir etiquetas de valor sobre cada barra
            max_val = PlotCounts.max() if len(PlotCounts) > 0 else 0
            for i, v in enumerate(PlotCounts.values):
                Axes[2].text(i, v + max_val * 0.02 + 0.01, str(int(v)), ha='center', va='bottom', fontsize=8)
    else:
        Axes[2].text(0.5, 0.5, 'Sin datos de Tipo', ha='center', va='center', transform=Axes[2].transAxes)
        Axes[2].set_title('Apuestas por Tipo')
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()
    plt.close()
    
    # Imprimir resumen
    print(f"\n{'='*50}")
    print(f"RESUMEN DE APUESTAS - {NombreUsuario}")
    print(f"{'='*50}")
    total = len(DfUsuario)
    print(f"Total de apuestas: {total}")
    if total > 0:
        print(f"Ganadas: {Ganadas} ({Ganadas/total*100:.1f}%)")
        print(f"Perdidas: {Perdidas} ({Perdidas/total*100:.1f}%)")
    else:
        print("Ganadas: 0 (0.0%)")
        print("Perdidas: 0 (0.0%)")
    if 'SaldoRestante' in DfUsuario.columns:
        SaldoFinal = pd.to_numeric(DfUsuario['SaldoRestante'].iloc[-1], errors='coerce')
        print(f"Saldo Final: {SaldoFinal:.2f}")
    print(f"{'='*50}\n")


def GraficarDistribucionGananciasPerdidas(NombreUsuario):
    """Alias para Dashboard (compatibilidad)"""
    Dashboard(NombreUsuario)


def GraficarSaldoEnTiempo(NombreUsuario):
    """Alias para Dashboard (compatibilidad)"""
    Dashboard(NombreUsuario)
