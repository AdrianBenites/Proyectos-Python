import pandas as pd

# Cargar datos
df = pd.read_csv('ventas.csv', parse_dates=['Fecha'])
df['Total'] = df['Cantidad'] * df['PrecioUnitario']

# Agrupar por producto
resumen = df.groupby('Producto')['Total'].sum().reset_index()

# Agrupar por mes
df['Mes'] = df['Fecha'].dt.strftime('%Y-%m')
ventas_mes = df.groupby('Mes')['Total'].sum().reset_index()

# Guardar en Excel con estilo
with pd.ExcelWriter('reporte_ventas.xlsx', engine='openpyxl') as writer:
    resumen.to_excel(writer, index=False, sheet_name='Resumen por Producto')
    ventas_mes.to_excel(writer, index=False, sheet_name='Ventas por Mes')
    df.to_excel(writer, index=False, sheet_name='Detalle')

print("✅ Reporte generado: reporte_ventas.xlsx")


