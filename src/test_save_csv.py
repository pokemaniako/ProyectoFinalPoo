from Csv.graficos import GuardarApuestaCsv
from pathlib import Path
p = Path(__file__).parent / 'Csv' / 'Apuestas.csv'
# three test rows
GuardarApuestaCsv({'Jugador':'test','MontoApostado':10,'SaldoRestante':20,'Eleccion':'rojo','Resultado':'rojo'})
GuardarApuestaCsv({'Jugador':'test','MontoApostado':5,'SaldoRestante':0,'Eleccion':'negro','Resultado':'rojo'})
GuardarApuestaCsv({'Jugador':'test','MontoApostado':3,'SaldoRestante':6,'Eleccion':[1,2,3],'Resultado':[1,2,3]})
print('--- CSV PREVIEW ---')
if p.exists():
    with p.open('r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= 10:
                break
            print(line.rstrip())
else:
    print('CSV no existe')
