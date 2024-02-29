import sys
import MySQLdb, psycopg2


def connectMDB(host,usuario,contraseña,nombrebd):
    try:
        db = MySQLdb.connect(host,usuario,contraseña,nombrebd)

    except:
        print("Conexión fallida en MariaDB")
        sys.exit(1)
    print("Conexión correcta en MariaDB")

    return db

def connectpostgres(host,nombrebd,usuario,contraseña):
    try:
        db = psycopg2.connect(host=host,database=nombrebd,user=usuario,password=contraseña)
    except:
        print("Conexión fallida en Postgres")
        sys.exit(1)
    print("Conexión correcta en Postgres")
    
    return db

def desconexion(db):
    print("Conexión finalizada")
    db.close()


def DBmenu():
    print("\nMENÚ DB EDITORIAL")
    print("-------------------------------------------------------------------------\n")
    print("1. Listar el titulo de todos los libros editados.")
    print("2. Mostrar libros editados cuyo precio este entre un valor inicial y otro final.")
    print("3. Pide por teclado un autor y muestra los libros que ha escrito")
    print("4. Añade un usuario nuevo a la tabla usuarios.")
    print("5. Pide por teclado un autor y elimina los documentos escritos por ese autor.")
    print("6. Pide por teclado una editorial y modifica los precios de los libros de esa editorial aumentando el precio de venta en un 10%.")
    print("7. Salir")

    while True:
        try:
            numero= int(input("Elige que consulta quieres realizar: "))
            while numero <= 0 or numero > 7:
                print("Elige una opción que este disponible")
                numero= int(input("Elige que consulta quieres realizar: "))
            break
        except ValueError:
            print ("Introduce un numero entero que corresponda con una de las opciones del menu")
    return numero


#Listar el titulo de todos los libros editados.


def listadolibrosedit(db):
    sql = "SELECT Titulo FROM documentos WHERE Codigo IN (SELECT CodDocumento FROM libros WHERE CodDocumento IN (SELECT CodDocumento FROM libroseditados));"
    cursor = db.cursor()

    try:
        cursor.execute(sql)
        registros = cursor.fetchall()
        
        if cursor.rowcount > 0:
            print("\nSe encuentran registrados los siguientes títulos de libros editados:")
            print("-------------------------------------------------------------------------\n")

            for registro in registros:
                print("-", registro[0])
            print("\nTotal de libros editados registrados:", cursor.rowcount)
        
        else:
            print("No hay libros editados registrados")
    
    except:
        print("Se ha producido un error en la consulta")


# Mostrar libros editados cuyo precio este entre un valor inicial y otro final”

def buscarlibrosxpvp(db):

    print("\n-------------------------------------------------------------------------\n")
    try:
        precio_min = float(input("Indica el precio mínimo: "))
        precio_max = float(input("Indica el precio máximo: "))
    except ValueError:
        print("Por favor, introduce un valor numérico para el precio.")
        return

    cursor = db.cursor()
    sql = "SELECT d.Titulo, le.PrecioVenta FROM documentos d, libroseditados le WHERE d.Codigo IN (SELECT l.CodDocumento FROM libros l WHERE l.CodDocumento = le.CodDocumento) AND le.PrecioVenta BETWEEN %s AND %s;"

    try:
        cursor.execute(sql, (precio_min, precio_max))
        libros = cursor.fetchall()
        if cursor.rowcount == 0:
            print("No hay libros editados en el rango de precios especificado.")
        else:
            print("+","-"*40,"+")
            print("| {:<30} {:<10} |".format("Título", "Precio"))
            print("+","-"*40,"+")
            for libro in libros:
                print("| {:<30} {:<10} |".format(libro[0], libro[1]))
            print("+","-"*40,"+")
    
    except:
        print("Error en la consulta:")

# Pide por teclado un autor y muestra los libros que ha escrito

def libros_por_autor(db):

    print("\n-------------------------------------------------------------------------\n")

    nombre_autor = input("Introduce el nombre del autor: ")
    apellido1_autor = input("Introduce el primer apellido del autor: ")
    apellido2_autor = input("Introduce el segundo apellido del autor: ")
    
    cursor = db.cursor()
    
    sql = """
    SELECT d.Titulo
    FROM documentos d
    WHERE d.Codigo IN (
        SELECT da.CodDocumento
        FROM documentos_autores da
        WHERE da.CodAutor IN (
            SELECT a.Codigo
            FROM autores a
            WHERE a.Nombre = %s
            AND a.Apellido1 = %s
            AND a.Apellido2 = %s
        )
    );
    """
    
    try:
        cursor.execute(sql, (nombre_autor, apellido1_autor, apellido2_autor))
        libros = cursor.fetchall()
        if cursor.rowcount == 0:
            print("\nEl autor no ha escrito ningún libro.")
        else:
            print("\nLibros escritos por {} {} {}: ".format(nombre_autor, apellido1_autor, apellido2_autor))
            print("-------------------------------------------------------------------------\n")
            for libro in libros:
                print(libro[0])
    
    except:
        print("Error en la consulta")

# Añade un usuario nuevo a la tabla usuarios.

def insertuser(db, usuario):
    cursor = db.cursor()
    sql="insert into usuarios values ('%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s' )" % (usuario["DNI"],usuario["Nombre"],usuario["Apellido1"],usuario["Apellido2"],usuario["DireccionEnvio"],usuario["DireccionFacturacion"],usuario["NTarjetaCredito"],usuario["Login"],usuario["Password"])
    try:
        cursor.execute(sql)
        db.commit()
        print('''El usuario %s %s %s ha sido añadido con exito.'''%(usuario["Nombre"],usuario["Apellido1"],usuario["Apellido2"]))
    except:
        print("Error en la insercion de datos.")
        db.rollback()

# Elimina los documentos escritos por un autor.
        
def eliminar_documentos_por_autor(db):

    nombre_autor = input("Introduce el nombre del autor: ")
    apellido1_autor = input("Introduce el primer apellido del autor: ")
    apellido2_autor = input("Introduce el segundo apellido del autor: ")


    sql = """
    DELETE FROM documentos
    WHERE Codigo IN (
        SELECT da.CodDocumento
        FROM documentos_autores da
        WHERE da.CodAutor IN (
            SELECT Codigo
            FROM autores
            WHERE Nombre = '{}' AND Apellido1 = '{}' AND Apellido2 = '{}'
        )
    );
    """.format(nombre_autor, apellido1_autor, apellido2_autor)

    try:
        resp = input("¿Realmente quieres eliminar los documentos escritos por {} {} {}? (pulsa 's' para sí, cualquier otra tecla para cancelar la eliminacion)".format(nombre_autor, apellido1_autor, apellido2_autor))
        if resp.lower() == "s":
            cursor = db.cursor()
            cursor.execute(sql)
            db.commit()
            if cursor.rowcount == 0:
                print("No se encontraron documentos escritos por {} {} {}.".format(nombre_autor, apellido1_autor, apellido2_autor))
            else:
                print("Documentos escritos por {} {} {} eliminados con éxito.".format(nombre_autor, apellido1_autor, apellido2_autor))
        else:
            print("Operación cancelada.")

    except:
        print("Error al borrar.")
        db.rollback()


# Pide por teclado una editorial y modifica los precios de los libros de esa editorial aumentando el precio de venta en un 10%.

def aumentar_precio_por_editorial(db):

    try:
        editorial = input("Introduce el nombre de la editorial: ")
        
        sql_update_price = """
        UPDATE libroseditados
        SET PrecioVenta = PrecioVenta * 1.10
        WHERE CodDocumento IN (
            SELECT CodDocumento
            FROM libros
            WHERE Editorial = %s
        )
        """

        cursor = db.cursor()

        cursor.execute(sql_update_price, (editorial,))
        db.commit()

        if cursor.rowcount > 0:
            print("El precio de venta de los libros de la editorial '{}' se ha aumentado en un 10%.".format(editorial))
        else:
            print("No se encontraron libros para la editorial '{}'.".format(editorial))
    
    except Exception as e:
        print("Error al intentar aumentar el precio de venta:", e)
        db.rollback()













