import pandas as pd
import os

CsvPath = os.path.join(os.path.dirname(__file__), 'ExcelBackup.csv')

def GuardarApuestaCsv(Apuesta):
    Safe = {}
    for k, v in Apuesta.items():
        Safe[k] = str(v) if isinstance(v, (list, tuple, dict)) else v

    DfRow = pd.DataFrame([Safe])

    if not os.path.isfile(CsvPath):
        DfRow.to_csv(CsvPath, index=False)
    else:
        DfRow.to_csv(CsvPath, mode='a', header=False, index=False)
