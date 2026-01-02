import datetime 
import sqlite3
import json 
from fpdf import FPDF 
import logging 
import os 
import sys 

def resource_path(relative_path): 
  try:
    base_path = sys._MEIPASS 
  except Exception:
    base_path = os.path.abspath(".")
  return os.path.join(base_path, relative_path)

#=======================================================================================

def configurar_logging(): 
  logging.basicConfig(filename='registros.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
  
  logging.info('Inicio del programa')

configurar_logging() 

conn = sqlite3.connect("GestorFacturas.db")
cursor = conn.cursor()

connlogin = sqlite3.connect("GestorLogin.db")
cursorlogin = connlogin.cursor()

with open(resource_path('Factura.sql'), 'r', encoding='utf-8') as f:
  sql_script = f.read()
  cursor.executescript(sql_script)
conn.commit()

with open(resource_path('Login.sql'), 'r', encoding='utf-8') as f:
  sql_script = f.read()
  cursorlogin.executescript(sql_script)
connlogin.commit()

class Producto: 
  
  def __init__(self, nombre, precio, cantidad):
    self.__nombre = nombre
    self.__precio = precio
    self.__cantidad = cantidad
    self.__total = 0

  @property
  def nombre(self):
    return self.__nombre

  @property
  def precio(self):
    return self.__precio

  @property
  def cantidad(self):
    return self.__cantidad

  @property
  def total(self):
    return self.__total

  @nombre.setter
  def nombre(self, nombre):
    self.__nombre = nombre

  @precio.setter
  def precio(self, precio):
    self.__precio = precio

  @cantidad.setter
  def cantidad(self, cantidad):
    self.__cantidad = cantidad

  def calcular_total(self):
    self.__total = self.__precio * self.__cantidad
    return self.__total

#=======================================================================================

class Factura:
  __contador_id = 1

  def __init__(self, cliente, empresa, forma_pago):
      self.__id_factura = Factura.__contador_id
      Factura.__contador_id += 1
      self.__cliente = cliente
      self.__empresa = empresa
      self.__fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      self.__productos = []
      self.__total = 0
      self.__forma_pago = forma_pago

  @property
  def cliente(self):
    return self.__cliente

  @property
  def empresa(self):
    return self.__empresa

  @property
  def id_factura(self):
    return self.__id_factura

  @property
  def fecha(self):
    return self.__fecha

  @property
  def productos(self):
    return self.__productos

  @property
  def total(self):
    return self.__total

  @property
  def forma_pago(self):
    return self.__forma_pago

  @cliente.setter
  def cliente(self, cliente):
    self.__cliente = cliente

  @empresa.setter
  def empresa(self, empresa):
    self.__empresa = empresa    

  @productos.setter
  def productos(self, productos):
    self.__productos = productos

  @total.setter
  def total(self, total):
    self.__total = total

  @forma_pago.setter
  def forma_pago(self, forma_pago):
    self.__forma_pago = forma_pago

  def crear_agregar_producto(self, nombre, precio, cantidad):
    if precio <= 0:
      print("El precio no puede ser negativo o cero")
      return
      
    if cantidad <= 0:
      print("La cantidad no puede ser negativa o cero")
      return

    producto = Producto(nombre, precio, cantidad)
    self.productos.append(producto)
    self.__total = self.calcular_total()
    print("Producto agregado")

#=======================================================================================

  def calcular_total(self):
    self.__total = 0
    
    for producto in self.productos:
        self.__total += producto.calcular_total()
    return self.__total

#=======================================================================================

cursor.execute("SELECT MAX(id_factura) FROM Factura")
max_id = cursor.fetchone()[0]
if max_id is not None:
  Factura.__contador_id = max_id + 1

#=======================================================================================

def crear_factura_teclado(self):
  
  print("="*80)
  print("Ingrese los datos de la factura:")
  print("="*80)

  while True:
    self.cliente = input("Ingrese el nombre del cliente: ")
    print("-"*80)
    if self.cliente == "":
      print("El nombre del cliente no puede estar vacío. Intente nuevamente.")
      print("-"*80)
      continue
    else:
      break
  
  while True:
    self.empresa = input("Ingrese el nombre de la empresa: ")
    print("-"*80)
    if self.empresa == "":
      print("El nombre de la empresa no puede estar vacío. Intente nuevamente.")
      print("-"*80)
      continue
    else:
      break
  
  while True:
    print("Ingrese la forma de pago:")
    print("1- Efectivo")
    print("2- Tarjeta")
    print("3- Transferencia")
    print("4- Cheque")
    print("-"*80)
    opcion = input("Ingrese una opción: ")
    print("-"*80)
    
    if opcion == "1":
      self.forma_pago = "efectivo"
      break
    elif opcion == "2":
      self.forma_pago = "tarjeta"
      break
    elif opcion == "3":
      self.forma_pago = "transferencia"
      break
    elif opcion == "4":
      self.forma_pago = "cheque"
      break
    else:
      print("Opción inválida. Intente nuevamente.")
      print("-"*80)
      continue

  while True:
      nombre = input("Ingrese el nombre del producto: ")
      print("-"*80)
      if nombre.lower() == 'fin':
          break

      while True:
          try:
            precio = float(input("Ingrese el precio del producto: "))
            print("-"*80)
            if precio <= 0:
                print("El precio no puede ser negativo o igual a cero. Intente nuevamente.")
                print("-"*80)
                continue
            break
          except ValueError:
            print("Debe ingresar un número válido.")
            print("-"*80)

      while True:
        try:
            cantidad = int(input("Cantidad del producto: "))
            print("-"*80)
            if cantidad <= 0:
                print("La cantidad no puede ser negativo o igual a cero. Intente nuevamente.")
                print("-"*80)
                continue
            break
        except ValueError:
            print("Debe ingresar un número entero válido.")
            print("-"*80)

      self.crear_agregar_producto(nombre, precio, cantidad)
      print("Escriba 'fin' para terminar")

#=======================================================================================

def crear_factura():
  
  while True:
    factura = Factura("", "", "")
    print("="*80)
    print("----CREAR FACTURA----")
    crear_factura_teclado(factura)
  
    productos_json = json.dumps([{
      'nombre': p.nombre,
      'precio': p.precio,
      'cantidad': p.cantidad,
      'total': p.total
    } for p in factura.productos])

    cursor.execute("""
    INSERT INTO Factura (cliente, empresa, fecha, productos, total, forma_pago)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (factura.cliente, factura.empresa, 
          factura.fecha, productos_json, factura.total, factura.forma_pago))
    conn.commit()
    
    print("Factura agregada a la base de datos")
    logging.info(f"Factura {factura.id_factura}, Cliente: {factura.cliente}, Empresa: {factura.empresa}, Fecha: {factura.fecha}, Total: {factura.total}, Forma de pago: {factura.forma_pago}") 
    respuesta = input("Desea agregar otra factura? (s/n): ")
    if respuesta.lower() == 's':
      continue
    else:
      break

#=======================================================================================

def mostrar_facturas():

  try:
      cursor.execute("SELECT * FROM Factura") 
      facturas = cursor.fetchall() 

      if not facturas:
          print("="*80)
          print("No hay facturas registradas")
          logging.info("Intento de mostrar facturas: No se encontraron facturas registradas.")
          print("="*80)
          return

      logging.info(f"Consulta de todas las facturas exitosa. Se encontraron {len(facturas)} facturas.")

      print("="*80)
      for factura in facturas:
          print(f"ID: {factura[0]}")
          print("="*80)
          print(f"Cliente: {factura[1]}\nEmpresa: {factura[2]}\nFecha: {factura[3]}")

          try:
              productos = json.loads(factura[4])
          except json.JSONDecodeError as e:
              productos = []
              print(f"Advertencia: Error al leer productos de la factura ID {factura[0]}. Los datos podrían estar corruptos.")
              logging.error(f"Error al decodificar JSON de productos en Factura ID {factura[0]}: {e}")

          print("="*80)
          print("Productos:")
          print("="*80)

          for producto in productos:
              print(f" Nombre: {producto['nombre']}\n Precio: {producto['precio']}\n Cantidad: {producto['cantidad']}\n Total: {producto['total']}")
              print("-"*80)

          print(f"Total a Pagar: {factura[5]}\nForma de pago: {factura[6]}")
          print("="*80)

  except sqlite3.Error as e:
      print("Ocurrió un error en la base de datos al intentar mostrar las facturas.")
      logging.critical(f"Error crítico de SQLite al intentar mostrar todas las facturas: {e}")
      print("="*80)
    
#=======================================================================================

def mostrar_factura_id():
  print("="*80)
  print("----MOSTRAR FACTURA----")
  print("="*80)

  id_factura = None
  try:
      id_factura = int(input("Ingrese el ID de la factura a mostrar: ")) 

  except ValueError:
      print("Error: Debe ingresar un número entero válido para el ID.")
      logging.warning("Intento de mostrar factura fallido. El ID ingresado no es un número entero.")
      return 

  try:
      cursor.execute("SELECT * FROM Factura WHERE id_factura = ?", (id_factura,))
      factura = cursor.fetchone()

      if factura:
          logging.info(f"Factura ID {id_factura} consultada exitosamente.")

          print(f"ID: {factura[0]}")
          print("="*80)
          print(f"Cliente: {factura[1]}\nEmpresa: {factura[2]}\nFecha: {factura[3]}")

          productos = json.loads(factura[4])

          print("="*80)
          print("Productos:")
          print("="*80)

          for producto in productos:
              print(f"  Nombre: {producto['nombre']}\n Precio: {producto['precio']}\n Cantidad: {producto['cantidad']}\n Total: {producto['total']}")
              print("-"*80)

          print(f"Total a Pagar: {factura[5]}\nForma de pago: {factura[6]}")
          print("="*80)

      else:
          print("Factura no encontrada")
          logging.info(f"Intento de consulta factura ID no encontrada: {id_factura}")
          print("="*80)

  except sqlite3.Error as e:
      print("Ocurrió un error en la base de datos al intentar buscar la factura")
      logging.error(f"Error crítico de SQLite al buscar Factura ID {id_factura}: {e}")
      print("="*80)

#=======================================================================================

def mostrar_factura_cliente():
  print("="*80)
  print("----MOSTRAR FACTURA----")
  print("="*80)

  cliente = input("Ingrese el nombre del cliente: ")

  if not cliente:
      print("El nombre del cliente no puede estar vacío.")
      logging.warning("Intento de consulta de factura con nombre de cliente vacío.")
      return

  try:
      cursor.execute("SELECT * FROM Factura WHERE cliente = ?", (cliente,)) 
      facturas = cursor.fetchall() 
    
      if facturas:
          logging.info(f"Facturas consultadas exitosamente para el cliente: {cliente}. Se encontraron {len(facturas)} resultados.")

          for factura in facturas:
              print(f"ID: {factura[0]}")
              print("="*80)
              print(f"Cliente: {factura[1]}\nEmpresa: {factura[2]}\nFecha: {factura[3]}")

              try:
                  productos = json.loads(factura[4])
              except json.JSONDecodeError as e:
                  productos = []
                  print(f"Advertencia: Error al leer la lista de productos para la factura ID {factura[0]}. Los datos podrían estar corruptos.")
                  logging.error(f"Error al decodificar JSON de productos en Factura ID {factura[0]}: {e}")

              print("="*80)
              print("Productos:")
              print("="*80)

              for producto in productos:
                  print(f"  Nombre: {producto['nombre']}\n Precio: {producto['precio']}\n Cantidad: {producto['cantidad']}\n Total: {producto['total']}")
                  print("-"*80)

              print(f"Total a Pagar: {factura[5]}\nForma de pago: {factura[6]}")
              print("="*80)
      else:
          print("Factura no encontrada")
          logging.info(f"Intento de consulta. No se encontraron facturas para el cliente: {cliente}")
          print("="*80)

  except sqlite3.Error as e:
      print("Ocurrió un error en la base de datos al intentar buscar la factura por cliente.")
      logging.error(f"Error crítico de SQLite al buscar Factura por cliente {cliente}: {e}")
      print("="*80)

#=======================================================================================

def eliminar_factura_id():
  print("="*80)
  print("----Eliminar FACTURA----")
  print("="*80)

  id_factura = None

  try:
    id_factura = int(input("Ingrese el ID de la factura a eliminar: ")) 
  except ValueError:
    print("Debe ingresar un número válido.")
    print("-"*80)
    logging.warning(f"Intento de eliminar factura con ID inválido {id_factura}") 
    return

  respuesta = input("¿Está seguro de que desea eliminar esta factura? (s/n): ")
  
  if respuesta.lower() == 's':
    try:
      cursor.execute("DELETE FROM Factura WHERE id_factura = ?", (id_factura,)) 
      if cursor.rowcount == 0:
        print(f"Factura no encontrada con ID {id_factura}")
        logging.info(f"Intento de eliminar factura con ID no encontrado {id_factura}") 

      else:
        conn.commit() 
        logging.info(f"Factura {id_factura} eliminada") 
        print("Factura eliminada")
        print("="*80)
        
    except sqlite3.Error as e:
      print(f"Error al eliminar la factura: {e}")
      logging.error(f"Error al eliminar factura {id_factura}: {e}")
      print("="*80)
      
    
  else:
    print("Eliminación cancelada")
    print("="*80)

#=======================================================================================
def eliminar_factura_cliente():
  print("="*80)
  print("----Eliminar FACTURA----")

  print("="*80)
  cliente = input("Ingrese el nombre del cliente: ") 
  respuesta = input("¿Está seguro de que desea eliminar esta factura? (s/n): ")
  
  if respuesta.lower() == 's':
    try:
      cursor.execute("DELETE FROM Factura WHERE cliente = ?", (cliente,)) 

      if cursor.rowcount == 0:
        print(f"Factura no encontrada con cliente {cliente}")
        logging.info(f"Intento de eliminar factura con cliente no encontrado {cliente}")
        print("="*80)

      else:
        conn.commit()
        logging.info(f"Factura del cliente {cliente} eliminada") 
        print("Factura eliminada")
        print("="*80)

    except sqlite3.Error as e:
       print(f"Error al eliminar la factura: {e}")
       logging.error(f"Error al eliminar factura del cliente {cliente}: {e}")
    
  else:
    print("Eliminación cancelada")
    print("="*80)

#=======================================================================================
def modificar_factura():
  print("="*80)
  print("----Modificar FACTURA----")
  print("="*80)

  id_factura = None
  try:
      id_factura = int(input("Ingrese el ID de la factura a modificar: "))

      if id_factura <= 0:
          print("El ID de la factura debe ser un número positivo.")
          logging.warning(f"Intento de modificación con ID inválido (no positivo): {id_factura}")
          return

  except ValueError:
      print("Error: Debe ingresar un número entero válido para el ID.")
      logging.warning("Intento de modificación fallido. El ID ingresado no es un número entero.")
      return

  respuesta = input(f"¿Está seguro de que desea modificar la factura ID {id_factura}? (s/n): ")

  if respuesta.lower() == 's':
      try:
          cursor.execute("SELECT * FROM Factura WHERE id_factura = ?", (id_factura,)) 
          factura = cursor.fetchone()

          if factura: 
              factura_modificada = Factura(factura[1], factura[2], factura[6]) 
              factura_modificada.productos = [] 
              factura_modificada.total = factura[5]

              print("="*80)
              print("Ingrese los nuevos datos de la factura:") 
              print("="*80)

              crear_factura_teclado(factura_modificada)

              productos_json = json.dumps([{
                  'nombre': p.nombre,
                  'precio': p.precio,
                  'cantidad': p.cantidad,
                  'total': p.total
              } for p in factura_modificada.productos])

              cursor.execute("""
              UPDATE Factura
              SET cliente = ?, empresa = ?, fecha = ?, productos = ?, total = ?, forma_pago = ?
              WHERE id_factura = ?
              """, (factura_modificada.cliente, factura_modificada.empresa, factura_modificada.fecha, productos_json, factura_modificada.total, factura_modificada.forma_pago, id_factura))

              conn.commit()

              logging.info(f"Factura MODIFICADA exitosamente. ID: {id_factura}") 
              print("Factura modificada")
              print("="*80)

          else:
              print("Factura no encontrada")
              logging.info(f"Intento de modificar factura NO ENCONTRADA. ID: {id_factura}") 
              print("="*80)

      except sqlite3.Error as e:
          print("Ocurrió un error en la base de datos al intentar modificar la factura")
          logging.error(f"Error CRÍTICO de SQLite al MODIFICAR Factura ID {id_factura}: {e}")
          print("="*80)

  else:
      print("Modificación cancelada")
      logging.info(f"Modificación de factura ID {id_factura} cancelada") 
      print("="*80)

#=======================================================================================

def menu_mostrar():
  while True:
    print("="*80)
    print("----MENU MOSTRAR----")
    print("="*80)
    print("1. Mostrar todas las facturas")
    print("2. Mostrar factura por ID")
    print("3. Mostrar factura por cliente")
    print("4. Volver al menú principal")
    print("="*80)
    opcion = input("Ingrese una opción: ")

    if opcion == "1":
      mostrar_facturas()
      continue
    elif opcion == "2":
      mostrar_factura_id()
      continue
    elif opcion == "3":
      mostrar_factura_cliente()
      continue
    elif opcion == "4":
      break
    else:
      print("Opción inválida. Intente nuevamente.")
      print("="*80)
      continue

#=======================================================================================

def menu_eliminar():
  while True:
    print("="*80)
    print("----MENU ELIMINAR----")
    print("="*80)
    print("1. Eliminar factura por ID")
    print("2. Eliminar factura por cliente")
    print("3. Volver al menú principal")
    print("="*80)
    opcion = input("Ingrese una opción: ")

    if opcion == "1":
      eliminar_factura_id()
      continue
    elif opcion == "2":
      eliminar_factura_cliente()
      continue
    elif opcion == "3":
      break
    else:
      print("Opción inválida. Intente nuevamente.")
      print("="*80)
      continue
      
#=======================================================================================

def menu_principal():
  while True:
    print("="*80)
    print("----MENU PRINCIPAL----")
    print("="*80)
    print("1. Crear factura")
    print("2. Mostrar facturas")
    print("3. Eliminar factura")
    print("4. Modificar factura")
    print("5. Generar PDF")
    print("6. Salir")
    print("="*80)
    opcion = input("Ingrese una opción: ")

    if opcion == "1":
      crear_factura()
      continue
    elif opcion == "2":
      menu_mostrar()
      continue
    elif opcion == "3":
      menu_eliminar()
      continue
    elif opcion == "4":
      modificar_factura()
      continue
    elif opcion == "5":
      generar_pdf()
      continue
    elif opcion == "6":
      print("¡Hasta luego!")
      break
    else:
      print("Opción inválida. Intente nuevamente.")
      print("="*80)
      continue

#=======================================================================================

def registrar_usuario():
  print("="*80)
  print("----REGISTRAR USUARIO----")
  print("="*80)
  while True: 
    usuario = input("Ingrese un nombre de usuario: ")
    if usuario == "":
      print("El nombre de usuario no puede estar vacío. Intente nuevamente.")
      print("="*80)
      continue
    else:
      break

  while True:
    contraseña = input("Ingrese una contraseña: ")
    if contraseña == "":
      print("La contraseña no puede estar vacía. Intente nuevamente.")
      print("="*80)
      continue
    else:
      break

  while True:
    confirmar_contraseña = input("Confirme la contraseña: ")
    if confirmar_contraseña == "":
      print("La confirmación de contraseña no puede estar vacía. Intente nuevamente.")
      print("="*80)
      continue
    elif confirmar_contraseña != contraseña:
      print("Las contraseñas no coinciden. Intente nuevamente.")
      print("="*80)
      continue
    else:
      break

  while True:
    codigoRecuperacion = input("Ingrese un código de recuperación: ")
    if codigoRecuperacion == "":
      print("El código de recuperación no puede estar vacío. Intente nuevamente.")
      print("="*80)
      continue
    else:
      break

  cursorlogin.execute("INSERT INTO Usuario (nombre_usuario, contraseña, codigo_recuperacion) VALUES (?, ?, ?)", (usuario, contraseña, codigoRecuperacion))
  connlogin.commit()
  print("Usuario registrado correctamente")
  print("="*80)

#=======================================================================================

def iniciar_sesion():
  while True:
    print("="*80)
    print("----INICIAR SESIÓN----")
    print("="*80)

    while True:
      usuario = input("Ingrese su nombre de usuario: ")
      if usuario == "":
        print("El nombre de usuario no puede estar vacío. Intente nuevamente.")
        print("="*80)
        continue
      else:
        break

    while True:
      contraseña = input("Ingrese su contraseña: ")
      if contraseña == "":
        print("La contraseña no puede estar vacía. Intente nuevamente.")
        print("="*80)
        continue
      else:
        break

    cursorlogin.execute("SELECT * FROM Usuario WHERE nombre_usuario = ? AND contraseña = ?", (usuario, contraseña))
    usuario_encontrado = cursorlogin.fetchone()

    if usuario_encontrado:
      print("Inicio de sesión exitoso")
      print("="*80)
      menu_principal()
      return  
    else:
      print("Nombre de usuario o contraseña incorrectos")
      print("="*80)
      print("1. Volver a intentar")
      print("2. Recuperar contraseña")
      print("3. Salir")
      print("="*80)
      opcion = input("Ingrese una opción: ")

      if opcion == "1":
        continue 
      elif opcion == "2":
        recuperar_contraseña()
        return 
      elif opcion == "3":
        return
      else:
        print("Opción inválida. Intente nuevamente.")
        print("="*80)
        continue

#=======================================================================================

def recuperar_contraseña():
  while True: 
    print("="*80)
    print("----RECUPERAR CONTRASEÑA----")
    print("="*80)

    while True:
      usuario = input("Ingrese su nombre de usuario: ")
      if usuario == "":
        print("El nombre de usuario no puede estar vacío. Intente nuevamente.")
        print("="*80)
        continue
      else:
        break

    while True:
      codigoRecuperacion = input("Ingrese su código de recuperación: ")
      if codigoRecuperacion == "":
        print("El código de recuperación no puede estar vacío. Intente nuevamente.")
        print("="*80)
        continue
      else:
        break

    cursorlogin.execute("SELECT * FROM Usuario WHERE nombre_usuario = ? AND codigo_recuperacion = ?", (usuario, codigoRecuperacion))
    usuario_encontrado = cursorlogin.fetchone()

    if usuario_encontrado:
      print("Código de recuperación correcto")
      print("="*80)
      cambiar_contraseña(usuario_encontrado)
      return
    else:
      print("Nombre de usuario o código de recuperación incorrectos")
      print("="*80)
      print("1. Volver a intentar")
      print("2. Salir")
      print("="*80)
      opcion = input("Ingrese una opción: ")

      if opcion == "1":
        continue 
      elif opcion == "2":
        return
      else:
        print("Opción inválida. Intente nuevamente.")
        print("="*80)

#=======================================================================================

def cambiar_contraseña(usuario):
  print("="*80)
  print("----CAMBIAR CONTRASEÑA----")
  print("="*80)

  while True:
    contraseña = input("Ingrese su nueva contraseña: ")
    if contraseña == "":
      print("La contraseña no puede estar vacía. Intente nuevamente.")
      print("="*80)
      continue
    else:
      break

  while True:
    confirmar_contraseña = input("Confirme su nueva contraseña: ")
    if confirmar_contraseña == "":
      print("La confirmación de contraseña no puede estar vacía. Intente nuevamente.")
      print("="*80)
      continue
    elif confirmar_contraseña != contraseña:
      print("Las contraseñas no coinciden. Intente nuevamente.")
      print("="*80)
      continue
    else:
      break

  cursorlogin.execute("UPDATE Usuario SET contraseña = ? WHERE nombre_usuario = ?", (contraseña, usuario[1]))
  connlogin.commit()
  print("Contraseña cambiada correctamente")
  print("="*80)

#=======================================================================================

def menu_login():
  while True:
    print("="*80)
    print("----MENU LOGIN----")
    print("="*80)
    print("1. Iniciar sesión")
    print("2. Registrarse")
    print("3. Salir")
    print("="*80)

    opcion = input("Ingrese una opción: ")
    if opcion == "1":
      iniciar_sesion()
    elif opcion == "2":
      registrar_usuario()
    elif opcion == "3":
      print("¡Hasta luego!")
      logging.info('Fin del programa')
      break
    else:
      print("Opción inválida. Intente nuevamente.")
      print("="*80)

#=======================================================================================

def generar_pdf():
  print("="*80)
  print("----GENERAR PDF----")
  print("="*80)

  while True:
    try:
      id_factura = int(input("Ingrese el ID de la factura a generar: "))
      if id_factura <= 0:
        print("El ID de la factura no puede ser negativo o cero. Intente nuevamente.")
        print("="*80)
        continue
      else:
        break
        
    except ValueError:
      print("Debe ingresar un número válido.")
      print("-"*80)
  
  cursor.execute("SELECT * FROM Factura WHERE id_factura = ?", (id_factura,))
  factura = cursor.fetchone()
  
  if factura:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 12)
    pdf.cell(0, 10, f"FACTURA #{factura[0]}", ln=True, align='C')
    pdf.ln(10)

    pdf.cell(0, 10, f"Cliente: {factura[1]}", ln=True)
    pdf.cell(0, 10, f"Empresa: {factura[2]}", ln=True)
    pdf.cell(0, 10, f"Fecha: {factura[3]}", ln=True)
    pdf.ln(10)

    productos = json.loads(factura[4])
    for producto in productos:
      pdf.cell(0, 10, f"Nombre: {producto['nombre']}", ln=True)
      pdf.cell(0, 10, f"Precio: {producto['precio']}", ln=True)
      pdf.cell(0, 10, f"Cantidad: {producto['cantidad']}", ln=True)
      pdf.cell(0, 10, f"Total: ${producto['total']}", ln=True)
      pdf.ln(10)

    pdf.cell(0, 10, f"Total a Pagar: ${factura[5]}", ln=True)
    pdf.cell(0, 10, f"Forma de pago: {factura[6]}", ln=True)

    pdf.output(f"Factura_{factura[0]}.pdf")
    print("PDF generado correctamente")
    logging.info(f"PDF generado correctamente para la factura {factura[0]}")
    print("="*80)

  else:
    print("Factura no encontrada")
    logging.info(f"Intento de generar PDF para factura no encontrada {id_factura}")
    print("="*80)
    return

#=======================================================================================

menu_login()