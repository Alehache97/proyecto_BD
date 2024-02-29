import funcionesproyectobd

db = funcionesproyectobd.connectMDB("localhost", "alejandroproyecto", "TNGVAQ", "proyecto")

programa_encendido = True

while programa_encendido:
    opcion_elegida = funcionesproyectobd.DBmenu()

    if opcion_elegida == 1:
        funcionesproyectobd.listadolibrosedit(db)

    elif opcion_elegida == 2:
        funcionesproyectobd.buscarlibrosxpvp(db)

    elif opcion_elegida == 3:
        funcionesproyectobd.libros_por_autor(db)

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

      
        funcionesproyectobd.insertuser(db, dict)

    elif opcion_elegida == 5:
        funcionesproyectobd.eliminar_documentos_por_autor(db)

    elif opcion_elegida == 6:
        funcionesproyectobd.aumentar_precio_por_editorial(db)

    elif opcion_elegida == 7:
        funcionesproyectobd.desconexion(db)
        programa_encendido = False
    
