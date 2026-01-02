# Sistema de Gestión de Facturas con Python y SQLite

Este es mi proyecto final para la asignatura **Programación 1**. Es una aplicación de consola desarrollada en Python que permite la gestión completa del ciclo de facturación, desde el registro de usuarios hasta la generación de comprobantes en formato PDF.

## Características

- **Sistema de Seguridad:** Registro e inicio de sesión de usuarios con recuperación de contraseña mediante código de seguridad.
- **Gestión de Facturas (CRUD):** - Creación de facturas con múltiples productos.
    - Consulta por ID o por nombre de cliente.
    - Modificación de datos y eliminación de registros.
- **Persistencia de Datos:** Uso de bases de datos relacionales con **SQLite**.
- **Generación de Reportes:** Exportación de facturas a archivos **PDF**.
- **Sistema de Logs:** Registro detallado de operaciones en un archivo *registros.log* para auditoría y depuración.

## Tecnologías Utilizadas

- **Lenguaje:** Python 3
- **Base de Datos:** SQLite3
- **Librerías Externas:** *fpdf*: Para la creación de los documentos PDF.
- **Otras librerías (Estándar):** *json*, *logging*, *datetime*, *os*.

## Estructura del Proyecto

- *main.py*: Código principal del programa.
- *Factura.sql* / *Login.sql*: Scripts para la inicialización de las tablas de la base de datos.
- *registros.log*: Archivo generado automáticamente para seguimiento de errores y eventos.
- *requirements.txt*: Lista de dependencias necesarias.

## Instalación y Ejecución

Para ejecutar este proyecto localmente, sigue estos pasos:

1. Clonar el repositorio.
2. Instalar dependencias: *pip install -r requirements.txt*.
3. Ejecutar *main.py*.

## Para ejecutar el archivo .exe (Windows)

Si no tienes Python instalado, puedes utilizar la versión ejecutable siguiendo estos pasos:

1. Ve a la sección de **Releases** en este repositorio.
2. Descarga el archivo *GestorFacturas.exe*.
3. Ejecuta el archivo. 
   - Al abrirse por primera vez, el programa generará automáticamente los archivos *GestorFacturas.db* y *GestorLogin.db* en la misma carpeta.
   - También se creará un archivo *registros.log* donde se guardará el historial de operaciones.

> [!NOTE]
> Al no tener una firma digital, es posible que Windows muestre una advertencia de "Protegió su PC". Haz clic en **"Más información"** y luego en **"Ejecutar de todas formas"**. El código fuente está disponible aquí para tu revisión y seguridad.

**Autor:** Frandy Sena Taveras
