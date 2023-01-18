import pandas as pd

archivo = 'excel_ejemplo.xlsx'
#cabecera = ['1', '2', '3', '4', '5','6','7','8','9'] # cambia el nombre de las columnas
df = pd.read_excel(archivo, sheet_name= 'subtotales') # lee archivo y el nombre de la hoja
#df.columns = cabecera # especifica el nombre las cabeceras por el array del objeto cabecera
print(df.describe())
#df.to_json('exportado.json') [exportando en modo json]