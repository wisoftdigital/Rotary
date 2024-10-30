import pdfkit

# Ruta al archivo HTML que deseas convertir
input_file = 'Resivo/RC.html'
# Nombre del archivo PDF de salida
output_file = 'output.pdf'
# Ruta del ejecutable de wkhtmltopdf (si es necesario)
# config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')

# Opciones adicionales para manejar CSS y cargar archivos locales
options = {
    'enable-local-file-access': None,
    'page-size': 'A4',
    'encoding': 'UTF-8'
}

# Convierte el archivo HTML a PDF
try:
    pdfkit.from_file(input_file, output_file, options=options)
    print(f'PDF creado exitosamente: {output_file}')
except Exception as e:
    print(f'Ocurrió un error: {e}')
