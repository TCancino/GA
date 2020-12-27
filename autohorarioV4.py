import random
import xlrd #para leer planillas Excel

class Ramo:
    def __init__(self, name, codigo):
        self.nombre = name
        self.codigo = codigo #irrelevante de momento
        self.abreviacion = 'XD' # ejemplo: Calculo 1 -> C1

    def set_abrev(self):
        x = input("Ingrese abreviacion del ramo ", self.nombre, ": ")
        self.abreviacion = x
    
    def get_nom(self):
        return self.nombre
    
    def get_cod(self):
        return self.codigo
    
    def get_abrev(self):
        return self.abreviacion

class Seccion:
    def __init__(self, n, cupo_disp, ramo):
        self.numero = n #número de la sección
        self.cupo_diponible = cupo_disp #cuantos cupos quedan disponibles en la sección.
        self.profe = ''
        self.clases = [0,0,0,0,0] #arreglo de clases: [0,3,2,0,3] ->Lu sin clases, Ma C, Mi B, Ju sin clases, Vi C
        self.ramo = ramo #ramo al que pertenece la sección, aqui va una clase Ramo

    def set_profe(self, profe):
        self.profe = profe

    def set_clase(self, dia, bloque):
        aux_d = 5 #Sábado (Sa)
        aux_b = 9 #20:15 - 21:35 -> Vespertino
        hay_horario = True
        if dia == 'LU':
            aux_d = 0
        elif dia == 'MA':
            aux_d = 1
        elif dia == 'MI':
            aux_d = 2
        elif dia == 'JU':
            aux_d = 3
        elif dia == 'VI':
            aux_d = 4
        else:
            hay_horario = False
        if bloque.split(":")[0] == '08' or bloque.split(":")[0] == '8': #8:30 - 9:50 -> Bloque A
            aux_b = 1
        elif bloque.split(":")[0] == '10': #10:00 - 11:20 -> Bloque B
            aux_b = 2
        elif bloque.split(":")[0] == '11': #11:30 - 12:50 -> Bloque C
            aux_b = 3
        elif bloque.split(":")[0] == '13': #13:00 - 14:20 -> Bloque D
            aux_b = 4
        elif bloque.split(":")[0] == '14': #14:30 - 15:50 -> Bloque E
            aux_b = 5
        elif bloque.split(":")[0] == '16': #16:00 - 17:20 -> Bloque F
            aux_b = 6
        elif bloque.split(":")[0] == '17': #17:25 - 18:45 -> Bloque G
            aux_b = 7
        elif bloque.split(":")[0] == '18': #18:50 - 20:10 -> Bloque H
            aux_b = 8
        else:
            hay_horario = False

        if hay_horario == True:
            self.clases[aux_d] = aux_b

    def get_clas(self):
        return self.clases

    def get_class(self, x):
        return self.clases[x]

    def get_prof(self):
        return self.profe

    def get_cupo(self):
        return self.cupo_diponible

    def get_num(self):
        return self.numero

    def get_ramo_nom(self):
        return self.ramo.get_nom()

    def get_ramo_abv(self):
        return self.ramo.get_abrev()

    def get_ramo_data(self):
        return [self.ramo.get_nom(), self.ramo.get_cod(), self.ramo.get_abrev()]

def op_2(secciones):
    biggest_ventana = 0
    for i in secciones:
        for j in secciones:
            if i == j:
                pass
            else:
                for k in range(5):
                    if i.get_class(k) == 0 or j.get_class(k) == 0:
                        pass
                    else:
                        ventana_size = abs(i.get_class(k)-j.get_class(k))
                        if ventana_size > biggest_ventana:
                            biggest_ventana = ventana_size
    return biggest_ventana

def op_3(secciones):
    ventanas_de_cada_dia = []
    for i in secciones:
        for j in secciones:
            if i == j:
                pass
            else:
                for k in range(5):
                    if i.get_class(k) == 0 or j.get_class(k) == 0:
                        ventanas_de_cada_dia.append(0)
                    else:
                        ventanas_de_cada_dia.append(abs(i.get_class(k)-j.get_class(k)))
    VML = max(ventanas_de_cada_dia) #Ventana Mas Larga
    Peso = 0
    for p in ventanas_de_cada_dia:
        Peso = Peso + p
    Peso = Peso * VML  #Suma ventana de c/dia y la multiplica por la ventana más larga
    return Peso

def op_4(secciones): #Salir Temprano
    for i in secciones:
        for j in range(5):
            if i.get_class(j) > 4:
                return False
    return True

def op_5(secciones): #Entrar Tarde
    for i in secciones:
        for j in range(5):
            if i.get_class(j) < 3:
                return False
    return True

#Quizá aqui es el Backtracking
def combinacion_de_secciones_1(cant_ramos, secciones_disp_de_ramos_elegidos, opcion_elegida): #Restricción "minima" (no tope de horario)
    combi_secciones = [] #arreglo con todas las combinaciones de secciones, posibles o no
    ventana_mas_chica = 7
    peso_minimo = 40
    if cant_ramos == 1:
        print ("NO NECESITAS ESTA 'APP', VE LA SECCION KE MAS TE GUSTE ¬¬")
        combi_secciones = secciones_disp_de_ramos_elegidos[0]
    elif cant_ramos == 2:
        for i1 in secciones_disp_de_ramos_elegidos[0]:
            for i2 in secciones_disp_de_ramos_elegidos[1]:
                combi_sirve = True
                for k in range(5):
                    if i1.get_class(k) == 0 and i2.get_class(k) == 0:
                        pass
                    else:
                        if i1.get_class(k) == i2.get_class(k):
                            combi_sirve = False
                            break
                if combi_sirve == True:
                    if opcion_elegida == 2:
                        big_ventana_de_combi = op_2([i1,i2])
                        combi_secciones.append([big_ventana_de_combi,[i1,i2]])
                        if big_ventana_de_combi < ventana_mas_chica:
                            ventana_mas_chica = big_ventana_de_combi
                    elif opcion_elegida == 3:
                        peso_de_combi = op_3([i1,i2])
                        combi_secciones.append([peso_de_combi,[i1,i2]])
                        if peso_de_combi < peso_minimo:
                            peso_minimo = peso_de_combi
                    elif opcion_elegida == 4:
                        if op_4([i1,i2]) == True:
                            combi_secciones.append([i1,i2])
                    elif opcion_elegida == 5:
                        if op_5([i1,i2]) == True:
                            combi_secciones.append([i1,i2])
                    else:
                        combi_secciones.append([i1,i2])
    elif cant_ramos == 3:
        for i1 in secciones_disp_de_ramos_elegidos[0]:
            for i2 in secciones_disp_de_ramos_elegidos[1]:
                for i3 in secciones_disp_de_ramos_elegidos[2]:
                    combi_sirve = True
                    for k in range(5):
                        if i1.get_class(k) == 0 and i2.get_class(k) == 0 and i3.get_class(k) == 0:
                            pass
                        else:
                            if i1.get_class(k) == i2.get_class(k) or i1.get_class(k) == i3.get_class(k):
                                combi_sirve = False
                                break
                            elif i2.get_class(k) == i3.get_class(k):
                                combi_sirve = False
                                break
                    if combi_sirve == True:
                        if opcion_elegida == 2:
                            big_ventana_de_combi = op_2([i1,i2,i3])
                            combi_secciones.append([big_ventana_de_combi,[i1,i2,i3]])
                            if big_ventana_de_combi < ventana_mas_chica:
                                ventana_mas_chica = big_ventana_de_combi
                        elif opcion_elegida == 3:
                            peso_de_combi = op_3([i1,i2,i3])
                            combi_secciones.append([peso_de_combi,[i1,i2,i3]])
                            if peso_de_combi < peso_minimo:
                                peso_minimo = peso_de_combi
                        elif opcion_elegida == 4:
                            if op_4([i1,i2,i3]) == True:
                                combi_secciones.append([i1,i2,i3])
                        elif opcion_elegida == 5:
                            if op_5([i1,i2,i3]) == True:
                                combi_secciones.append([i1,i2,i3])
                        else:
                            combi_secciones.append([i1,i2,i3])
    elif cant_ramos == 4:
        for i1 in secciones_disp_de_ramos_elegidos[0]:
            for i2 in secciones_disp_de_ramos_elegidos[1]:
                for i3 in secciones_disp_de_ramos_elegidos[2]:
                    for i4 in secciones_disp_de_ramos_elegidos[3]:
                        combi_sirve = True
                        for k in range(5):
                            if i1.get_class(k) == 0 and i2.get_class(k) == 0 and i3.get_class(k) == 0 and i4.get_class(k) == 0:
                                pass
                            else:
                                if i1.get_class(k) == i2.get_class(k) or i1.get_class(k) == i3.get_class(k) or i1.get_class(k) == i4.get_class(k):
                                    combi_sirve = False
                                    break
                                elif i2.get_class(k) == i3.get_class(k) or i2.get_class(k) == i4.get_class(k):
                                    combi_sirve = False
                                    break
                                elif i3.get_class(k) == i4.get_class(k):
                                    combi_sirve = False
                                    break
                        if combi_sirve == True:
                            if opcion_elegida == 2:
                                big_ventana_de_combi = op_2([i1,i2,i3,i4])
                                combi_secciones.append([big_ventana_de_combi,[i1,i2,i3,i4]])
                                if big_ventana_de_combi < ventana_mas_chica:
                                    ventana_mas_chica = big_ventana_de_combi
                            elif opcion_elegida == 3:
                                peso_de_combi = op_3([i1,i2,i3,i4])
                                combi_secciones.append([peso_de_combi,[i1,i2,i3,i4]])
                                if peso_de_combi < peso_minimo:
                                    peso_minimo = peso_de_combi
                            elif opcion_elegida == 4:
                                if op_4([i1,i2,i3,i4]) == True:
                                    combi_secciones.append([i1,i2,i3,i4])
                            elif opcion_elegida == 5:
                                if op_5([i1,i2,i3,i4]) == True:
                                    combi_secciones.append([i1,i2,i3,i4])
                            else:
                                combi_secciones.append([i1,i2,i3,i4])
    elif cant_ramos == 5:
        for i1 in secciones_disp_de_ramos_elegidos[0]:
            for i2 in secciones_disp_de_ramos_elegidos[1]:
                for i3 in secciones_disp_de_ramos_elegidos[2]:
                    for i4 in secciones_disp_de_ramos_elegidos[3]:
                        for i5 in secciones_disp_de_ramos_elegidos[4]:
                            combi_sirve = True
                            for k in range(5):
                                if i1.get_class(k) == 0 and i2.get_class(k) == 0 and i3.get_class(k) == 0 and i4.get_class(k) == 0 and i5.get_class(k) == 0:
                                    pass
                                else:
                                    if i1.get_class(k) == i2.get_class(k) or i1.get_class(k) == i3.get_class(k) or i1.get_class(k) == i4.get_class(k) or i1.get_class(k) == i5.get_class(k):
                                        combi_sirve = False
                                        break
                                    elif i2.get_class(k) == i3.get_class(k) or i2.get_class(k) == i4.get_class(k) or i2.get_class(k) == i5.get_class(k):
                                        combi_sirve = False
                                        break
                                    elif i3.get_class(k) == i4.get_class(k) or i3.get_class(k) == i5.get_class(k):
                                        combi_sirve = False
                                        break
                                    elif i4.get_class(k) == i5.get_class(k):
                                        combi_sirve = False
                                        break
                            if combi_sirve == True:
                                if opcion_elegida == 2:
                                    big_ventana_de_combi = op_2([i1,i2,i3,i4,i5])
                                    combi_secciones.append([big_ventana_de_combi,[i1,i2,i3,i4,i5]])
                                    if big_ventana_de_combi < ventana_mas_chica:
                                        ventana_mas_chica = big_ventana_de_combi
                                elif opcion_elegida == 3:
                                    peso_de_combi = op_3([i1,i2,i3,i4,i5])
                                    combi_secciones.append([peso_de_combi,[i1,i2,i3,i4,i5]])
                                    if peso_de_combi < peso_minimo:
                                        peso_minimo = peso_de_combi
                                elif opcion_elegida == 4:
                                    if op_4([i1,i2,i3,i4,i5]) == True:
                                        combi_secciones.append([i1,i2,i3,i4,i5])
                                elif opcion_elegida == 5:
                                    if op_5([i1,i2,i3,i4,i5]) == True:
                                        combi_secciones.append([i1,i2,i3,i4,i5])
                                else:
                                    combi_secciones.append([i1,i2,i3,i4,i5])
    elif cant_ramos == 6:
        for i1 in secciones_disp_de_ramos_elegidos[0]:
            for i2 in secciones_disp_de_ramos_elegidos[1]:
                for i3 in secciones_disp_de_ramos_elegidos[2]:
                    for i4 in secciones_disp_de_ramos_elegidos[3]:
                        for i5 in secciones_disp_de_ramos_elegidos[4]:
                            for i6 in secciones_disp_de_ramos_elegidos[5]:
                                combi_sirve = True
                                for k in range(5):
                                    if i1.get_class(k) == 0 and i2.get_class(k) == 0 and i3.get_class(k) == 0 and i4.get_class(k) == 0 and i5.get_class(k) == 0 and i6.get_class(k) == 0:
                                        pass
                                    else:
                                        if i1.get_class(k) == i2.get_class(k) or i1.get_class(k) == i3.get_class(k) or i1.get_class(k) == i4.get_class(k) or i1.get_class(k) == i5.get_class(k) or i1.get_class(k) == i6.get_class(k):
                                            combi_sirve = False
                                            break
                                        elif i2.get_class(k) == i3.get_class(k) or i2.get_class(k) == i4.get_class(k) or i2.get_class(k) == i5.get_class(k) or i2.get_class(k) == i6.get_class(k):
                                            combi_sirve = False
                                            break
                                        elif i3.get_class(k) == i4.get_class(k) or i3.get_class(k) == i5.get_class(k) or i3.get_class(k) == i6.get_class(k):
                                            combi_sirve = False
                                            break
                                        elif i4.get_class(k) == i5.get_class(k) or i4.get_class(k) == i6.get_class(k):
                                            combi_sirve = False
                                            break
                                        elif i5.get_class(k) == i6.get_class(k):
                                            combi_sirve = False
                                            break
                                if combi_sirve == True:
                                    if opcion_elegida == 2:
                                        big_ventana_de_combi = op_2([i1,i2,i3,i4,i5,i6])
                                        combi_secciones.append([big_ventana_de_combi,[i1,i2,i3,i4,i5,i6]])
                                        if big_ventana_de_combi < ventana_mas_chica:
                                            ventana_mas_chica = big_ventana_de_combi
                                    elif opcion_elegida == 3:
                                        peso_de_combi = op_3([i1,i2,i3,i4,i5,i6])
                                        combi_secciones.append([peso_de_combi,[i1,i2,i3,i4,i5,i6]])
                                        if peso_de_combi < peso_minimo:
                                            peso_minimo = peso_de_combi
                                    elif opcion_elegida == 4:
                                        if op_4([i1,i2,i3,i4,i5,i6]) == True:
                                            combi_secciones.append([i1,i2,i3,i4,i5,i6])
                                    elif opcion_elegida == 5:
                                        if op_5([i1,i2,i3,i4,i5,i6]) == True:
                                            combi_secciones.append([i1,i2,i3,i4,i5,i6])
                                    else:
                                        combi_secciones.append([i1,i2,i3,i4,i5,i6])
    elif cant_ramos == 7:
        for i1 in secciones_disp_de_ramos_elegidos[0]:
            for i2 in secciones_disp_de_ramos_elegidos[1]:
                for i3 in secciones_disp_de_ramos_elegidos[2]:
                    for i4 in secciones_disp_de_ramos_elegidos[3]:
                        for i5 in secciones_disp_de_ramos_elegidos[4]:
                            for i6 in secciones_disp_de_ramos_elegidos[5]:
                                for i7 in secciones_disp_de_ramos_elegidos[6]:
                                    combi_sirve = True
                                    for k in range(5):
                                        if i1.get_class(k) == 0 and i2.get_class(k) == 0 and i3.get_class(k) == 0 and i4.get_class(k) == 0 and i5.get_class(k) == 0 and i6.get_class(k) == 0 and i7.get_class(k) == 0:
                                            pass
                                        else:
                                            if i1.get_class(k) == i2.get_class(k) or i1.get_class(k) == i3.get_class(k) or i1.get_class(k) == i4.get_class(k) or i1.get_class(k) == i5.get_class(k) or i1.get_class(k) == i6.get_class(k) or i1.get_class(k) == i7.get_class(k):
                                                combi_sirve = False
                                                break
                                            elif i2.get_class(k) == i3.get_class(k) or i2.get_class(k) == i4.get_class(k) or i2.get_class(k) == i5.get_class(k) or i2.get_class(k) == i6.get_class(k) or i2.get_class(k) == i7.get_class(k):
                                                combi_sirve = False
                                                break
                                            elif i3.get_class(k) == i4.get_class(k) or i3.get_class(k) == i5.get_class(k) or i3.get_class(k) == i6.get_class(k) or i3.get_class(k) == i7.get_class(k):
                                                combi_sirve = False
                                                break
                                            elif i4.get_class(k) == i5.get_class(k) or i4.get_class(k) == i6.get_class(k) or i4.get_class(k) == i7.get_class(k):
                                                combi_sirve = False
                                                break
                                            elif i5.get_class(k) == i6.get_class(k) or i5.get_class(k) == i7.get_class(k):
                                                combi_sirve = False
                                                break
                                            elif i6.get_class(k) == i7.get_class(k):
                                                combi_sirve = False
                                                break
                                    if combi_sirve == True:
                                        if opcion_elegida == 2:
                                            big_ventana_de_combi = op_2([i1,i2,i3,i4,i5,i6,i7])
                                            combi_secciones.append([big_ventana_de_combi,[i1,i2,i3,i4,i5,i6,i7]])
                                            if big_ventana_de_combi < ventana_mas_chica:
                                                ventana_mas_chica = big_ventana_de_combi
                                        elif opcion_elegida == 3:
                                            peso_de_combi = op_3([i1,i2,i3,i4,i5,i6,i7])
                                            combi_secciones.append([peso_de_combi,[i1,i2,i3,i4,i5,i6,i7]])
                                            if peso_de_combi < peso_minimo:
                                                peso_minimo = peso_de_combi
                                        elif opcion_elegida == 4:
                                            if op_4([i1,i2,i3,i4,i5,i6,i7]) == True:
                                                combi_secciones.append([i1,i2,i3,i4,i5,i6,i7])
                                        elif opcion_elegida == 5:
                                            if op_5([i1,i2,i3,i4,i5,i6,i7]) == True:
                                                combi_secciones.append([i1,i2,i3,i4,i5,i6,i7])
                                        else:
                                            combi_secciones.append([i1,i2,i3,i4,i5,i6,i7])
    if opcion_elegida == 2:
        arr = []
        for c_s in combi_secciones:
            if ventana_mas_chica == c_s[0]:
                arr.append(c_s[1])
        return arr
    elif opcion_elegida == 3:
        arr = []
        for c_s in combi_secciones:
            if peso_minimo == c_s[0]:
                arr.append(c_s[1])
        return arr
    else:
        return combi_secciones

def imprimir_horario(h):
    for i in h:
        print('\t',i)

def hacer_horario(combi_secciones, ramos_arr):
    H = [["|______|","__LU__|","__MA__|","__MI__|","__JU__|","__VI__|"],
        ["|___A__|","______|","______|","______|","______|","______|"],
        ["|___B__|","______|","______|","______|","______|","______|"],
        ["|___C__|","______|","______|","______|","______|","______|"],
        ["|___D__|","______|","______|","______|","______|","______|"],
        ["|___E__|","______|","______|","______|","______|","______|"],
        ["|___F__|","______|","______|","______|","______|","______|"],
        ["|___G__|","______|","______|","______|","______|","______|"],
        ["|___H__|","______|","______|","______|","______|","______|"]]
    for section in combi_secciones:
        for i in range(len(ramos_arr)): #Nombre del Ramo, va a ser el número que le corresponde en la lista por falta de espacio
            if ramos_arr[i].get_nom() == section.get_ramo_nom():
                if (i - 9) < 0:
                    nom_ramo = 'R0' + str(i+1)
                else:
                    nom_ramo = 'R' + str(i+1)
        if int(section.get_num()) < 10:
            nom_sec = 'S0' + section.get_num()
        else:
            nom_sec = 'S' + section.get_num()
        nom_ramo_sec = nom_ramo + nom_sec
        clases_seccion = section.get_clas()
        for d in range(5): #d -> día
            b = clases_seccion[d] #b -> bloque
            if b != 0:
                H[b][d+1] = nom_ramo_sec + '|'
    imprimir_horario(H)

#MAIN

#Solo para las pruebas
print("Indique el numero que corresponda al año y semestre que quiera revisar: ")
print("\n1) 2017-1\n2) 2017-2\n3) 2018-1\n4) 2018-2\n5) 2019-1\n6) 2019-2\n7) 2020-1\n8) 2020-2\n")
hoja_excel = int(input("-> "))

print("\t\t\t\tLEYENDO ARCHIVO...")
documento = xlrd.open_workbook("./static/files/"+"cursos_2017-2020.xlsx") #'abre' el Excel
#Reminder: sección != seccion; se puede distinguir entre ambos.
doc = documento.sheet_by_index(hoja_excel-1)
#si celda está vacia se muestra como '' (string vacio)

ramos = []#Guardar RAMOS ingresados
ramos_codes = []#Guardar codigos de RAMOS ya ingresados
secciones = []#Guardar SECCIONES ingresadas

for i in range(1, doc.nrows): #RECORRER el EXCEL para llenar llenar los arreglos con las clases que corresponden
    if doc.cell_value(i,7) == '': #cambio de sección
        if seccion in secciones:
            pass
        else:
            if seccion.get_cupo() > 0:
                secciones.append(seccion)
        continue
    else:
        # GUARDAR RAMOS:
        if doc.cell_value(i,1) in ramos_codes: #verificar que el ramo no se haya registrado.
            pass
        else:
            ramos.append(Ramo(doc.cell_value(i,2),doc.cell_value(i,1)))
            ramos_codes.append(doc.cell_value(i,1))
        # GUARDAR SECCIONES:
        if doc.cell_value(i-1,3) != doc.cell_value(i,3) or doc.cell_value(i-1,1) != doc.cell_value(i,1): #se cumple al cambiar de seccion o ramo
            for j in range(len(ramos_codes)):
                if ramos_codes[j] == doc.cell_value(i,1):
                    ramo_seccion = ramos[j]
                    break
            seccion = Seccion(doc.cell_value(i,3).split(" ")[1], int(doc.cell_value(i,12)), ramo_seccion)
        aux = doc.cell_value(i,7).split(" ")
        if doc.cell_value(i,5).split(" ")[0] == 'CÁTEDRA' or len(doc.cell_value(i,7)) > 16:
            cat1 = aux[0]
            cat2 = aux[1]
            profe = doc.cell_value(i,9)
            seccion.set_profe(profe)
            if (doc.cell_value(i,2).split(" ")[0] == 'CÁLCULO' and doc.cell_value(i,2).split(" ")[1] != 'III') or doc.cell_value(i,2).split(" ")[0] == 'ÁLGEBRA': #TIENEN 3 CÁTEDRAS
                cat3 = aux[2]
                horario_clases = aux[3]
                seccion.set_clase(cat3, horario_clases)
            else:
                horario_clases = aux[2]
            seccion.set_clase(cat1, horario_clases)
            seccion.set_clase(cat2, horario_clases)
        else:
            dia_clases = aux[0]
            horario_clases = aux[1]
            seccion.set_clase(dia_clases, horario_clases)
#YA HAY SECCIONES Y RAMOS

#BORRAR
'''
for i in secciones:
    print("RAMO: ",i.get_ramo_nom())
    print("Numero Seccion: ", i.get_num())
    print("Profe: ", i.get_prof())
    print("Horario (arreglo): ", i.get_clas())
    print("\t\t--------------------o------------------\n")
'''
#BORRAR HASTA ACA

cant_ramos_a_tomar = int(input("Ingrese cuantos ramos desea tomar este semestre: "))
if (cant_ramos_a_tomar > 7) or cant_ramos_a_tomar < 1: #Que no tome + de 7 ramos ni - de 1
    while (cant_ramos_a_tomar > 7 or cant_ramos_a_tomar < 1):
        print("Puede tomar un máximo de 7 ramos y minimo de 1")
        cant_ramos_a_tomar = int(input("Ingrese cuantos ramos desea tomar este semestre: "))

print("Ramos Disponibles: ")
for i in range(len(ramos)):
    print('\t',i+1,') ', ramos[i].get_nom())
nombres_ramos_elegidos = []
secciones_disp_de_ramos_elegidos = []
for i in range(cant_ramos_a_tomar): #Elegir ramos a tomar
    cont_aux = 0
    if i != 0:
        for j in nombres_ramos_elegidos:
            if cont_aux == 0:
                print ("LLeva los siguientes ramos: ")
            print("\t -> ",j)
            cont_aux = cont_aux + 1
    ramo_elegido = int(input("Ingrese el numero que corresponda al ramo que desea tomar: "))
    if ramo_elegido > len(ramos) or ramo_elegido < 1: #Que elija un ramo que exista en el registro
        while (ramo_elegido > len(ramos) or ramo_elegido < 1):
            print("El numero que ingreso no tiene un ramo asignado, intente con otro numero. \nEntre 1 y ",len(ramos))
            ramo_elegido = int(input("Ingrese el numero que corresponda al ramo que desea tomar: "))
    nombres_ramos_elegidos.append(ramos[ramo_elegido-1].get_nom())
    secciones_disp_de_ramos_elegidos.append([]) #Asi se tiene un arreglo, para cada ramo elegido, donde se podrán guardar las secciones de ese ramo.

cont_aux = 0
for i in nombres_ramos_elegidos: #imprime los ramos que se "tomarán"
    if cont_aux == 0:
        print ("Se tomaron en cuenta los siguientes ramos: ")
    print("\t -> ",i)
    cont_aux = cont_aux + 1

cont_aux = 0
for i in nombres_ramos_elegidos: #Se guardan las secciones disponibles de cada ramo en un arreglo respectivo.
    for j in secciones:
        if i == j.get_ramo_nom(): #si el nombre del ramo de la seccion es igual al nombre del ramo que se desea tomar se cumple la condicion
            secciones_disp_de_ramos_elegidos[cont_aux].append(j) #guarda en el arreglo un arreglo con las secciones que hay del ramo 'i'
    cont_aux = cont_aux + 1

inwhile = True
while(inwhile):
    print("\nSi desea algún tipo de 'optimizacion' para su horario indique el numero que corresponda.")
    print("\n\t 1)  Ver TODAS las Opciones.\n\t 2)  Ventanas entre clases chikitas(v1).\n\t 3)  Ventanas entre clases chikitas(v2).\n\t 4)  Salir Temprano (antes del bloque E).\n\t 5)  Entrar Tarde (desde el bloque C).")
    print("\t Para Salir Ingrese Cualquier Otro Numero.")
    x = int(input("Ingrese el numero que desee: "))

    if x == 1: # Ver todas las opciones
        V_solucion = combinacion_de_secciones_1(cant_ramos_a_tomar, secciones_disp_de_ramos_elegidos, x)
        cont_opciones = 1
        if len(V_solucion) == 0:
            print ("\t\t\t\t\tERROR!!!")
            print("\t\tNo hay una Combinación de Secciones para los Ramos Escogidos.")
        for combi in V_solucion:
            print("\nOpcion ", cont_opciones,': ')
            hacer_horario(combi, ramos)
            cont_opciones = cont_opciones + 1
    elif x == 2: #Ventana mas chica V1
        V_solucion = combinacion_de_secciones_1(cant_ramos_a_tomar, secciones_disp_de_ramos_elegidos, x)
        cont_opciones = 1
        if len(V_solucion) == 0:
            print ("\t\t\t\t\tERROR!!!")
            print("\t\tNo hay una Combinación de Secciones para los Ramos Escogidos.")
        for combi in V_solucion:
            print("\nOpcion ", cont_opciones,': ')
            hacer_horario(combi, ramos)
            cont_opciones = cont_opciones + 1
    elif x == 3: #Ventana mas chica V2
        V_solucion = combinacion_de_secciones_1(cant_ramos_a_tomar, secciones_disp_de_ramos_elegidos, x)
        cont_opciones = 1
        if len(V_solucion) == 0:
            print ("\t\t\t\t\tERROR!!!")
            print("\t\tNo hay una Combinación de Secciones para los Ramos Escogidos.")
        for combi in V_solucion:
            print("\nOpcion ", cont_opciones,': ')
            hacer_horario(combi, ramos)
            cont_opciones = cont_opciones + 1
    elif x == 4: #Salir Temprano (antes del bloque E)
        V_solucion = combinacion_de_secciones_1(cant_ramos_a_tomar, secciones_disp_de_ramos_elegidos, x)
        cont_opciones = 1
        if len(V_solucion) == 0:
            print ("\t\t\t\t\tERROR!!!")
            print("\t\tNo hay una Combinación de Secciones para los Ramos Escogidos, donde se salga antes del bloque E.")
        for combi in V_solucion:
            print("\nOpcion ", cont_opciones,': ')
            hacer_horario(combi, ramos)
            cont_opciones = cont_opciones + 1
    elif x == 5: #Entrar Tarde (después del bloque B)
        V_solucion = combinacion_de_secciones_1(cant_ramos_a_tomar, secciones_disp_de_ramos_elegidos, x)
        cont_opciones = 1
        if len(V_solucion) == 0:
            print ("\t\t\t\t\tERROR!!!")
            print("\t\tNo hay una Combinación de Secciones para los Ramos Escogidos, donde se entre después del bloque B.")
        for combi in V_solucion:
            print("\nOpcion ", cont_opciones,': ')
            hacer_horario(combi, ramos)
            cont_opciones = cont_opciones + 1
    else:
        inwhile = False

#_#