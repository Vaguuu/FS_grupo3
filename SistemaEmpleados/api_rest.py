class Profesional:
    def __init__(self, mn, nombre, especialidad, correo, horarios):
        self.mn = mn
        self.nombre = nombre
        self.especialidad = especialidad
        self.correo = correo
        self.horarios = horarios
    
    def modificar(self, nueva_especialidad, nuevo_correo, nuevos_horarios):
        self.especialidad = nueva_especialidad
        self.correo = nuevo_correo
        self.horarios = nuevos_horarios

profesional = Profesional("222222", "Juan Carlos Perez", "Fertilidad", "jcperez@gmail.com", "Viernes de 10.00 a 20.00 horas.")


class Staff:
    def __init__(self):
        self.profesionales = []

    def agregar_profesional(self, mn, nombre, especialidad, correo, horarios):
        nuevo_profesional = Profesional (mn, nombre, especialidad, correo, horarios)
        self.profesionales.append(nuevo_profesional)
    
    def consultar_profesional(self, nombre):
        for profesional in self.profesionales:
            if profesional.nombre == nombre:
                return profesional
            elif profesional.mn == nombre:
                return profesional
            else:
                print(f'El profesional {nombre} no se encuentra en el staff.')
    
    def modificar_profesional(self, nombre, nueva_especialidad, nuevo_correo, nuevos_horarios):
        profesional = self.consultar_profesional(nombre)
        if profesional:
            profesional.modificar(nueva_especialidad, nuevo_correo, nuevos_horarios)
        else:
            print(f'El profesional {nombre} no se encuentra en el staff.')

    def eliminar_profesional(self, nombre):
        eliminar = False
        for profesional in self.profesionales:
            if profesional.nombre == nombre:
                eliminar = True
                profesional_eliminar = profesional
            if profesional.nm == nombre:
                eliminar = True
                profesional_eliminar = profesional
        if eliminar == True:
            self.profesionales.remove(profesional_eliminar)
            print(f'El profesional {nombre} ha sido removido del staff.')
        else:
            print(f'El profesional {nombre} no se encuentra en el staff.')

    def listar_profesionales(self):
        print("-"*30)
        print("Listado del Staff:")
        print("MN\tNOMBRE\t\t\tESPECIALIDAD\t\t\tHORARIOS")
        for profesional in self.profesionales:
            print(f'{profesional.mn}\t{profesional.nombre}\t\t{profesional.especialidad}\t\t\t{profesional.horarios}')
        print("-"*30)

mi_staff = Staff()

mi_staff.agregar_profesional("444444","Juan Carlos Perez","Obstetra","jcperez@gmail.com","Lunes 10.00 a 20.00 horas.")
mi_staff.agregar_profesional("222222","Ana Laura Gomez","Fertilidad","algomez@gmail.com","Martes 10.00 a 20.00 horas.")
mi_staff.agregar_profesional("333333","Nicolás Díaz","Enfermedades cuello de útero","ndiaz@gmail.com","Miércoles 10.00 a 20.00 horas.")


mi_staff.listar_profesionales()