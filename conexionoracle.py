import funcionesproyectobdoracle

db = funcionesproyectobdoracle.connectoracle("alejandroproyecto", "TNGVAQ", "localhost")

programa_encendido = True

while programa_encendido:
    opcion_elegida = funcionesproyectobdoracle.DBmenu()

    if opcion_elegida == 1:
        funcionesproyectobdoracle.listadolibrosedit(db)

    elif opcion_elegida == 2:
        funcionesproyectobdoracle.buscarlibrosxpvp(db)

    elif opcion_elegida == 3:
        funcionesproyectobdoracle.libros_por_autor(db)

    elif opcion_elegida == 4:

        print("\n-------------------------------------------------------------------------")
        print("Indica los datos para introducir un nuevo usuario en la tabla usuarios:")
        dict={}
        dict["DNI"]=input("DNI: ")
        dict["Nombre"]=input("Nombre: ")
        dict["Apellido1"]=input("Primer apellido: ")
        dict["Apellido2"]=input("Segundo apellido: ")
        dict["DireccionEnvio"]=input("Direccion de envio: ")
        dict["DireccionFacturacion"]=input("Direccion de facturacion: ")
        dict["NTarjetaCredito"]=input("Numero tarjera de credito: ")
        dict["Login"]=input("Nombre de usuario: ")
        dict["Password"]=input("Contraseña: ")

      
        funcionesproyectobdoracle.insertuser(db, dict)

    elif opcion_elegida == 5:
        funcionesproyectobdoracle.eliminar_documentos_por_autor(db)

    elif opcion_elegida == 6:
        funcionesproyectobdoracle.aumentar_precio_por_editorial(db)

    elif opcion_elegida == 7:
        funcionesproyectobdoracle.desconexion(db)
        programa_encendido = False