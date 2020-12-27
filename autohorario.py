import copy
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
        self.ramo = ramo #nombre del ramo al que pertenece la sección, aqui va una clase Ramo

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
        return self.ramo

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
    comb_secciones = [] #arreglo con todas las combinaciones de secciones, posibles o no
    ventana_mas_chica = 7
    peso_minimo = 40
    if cant_ramos == 1:
        print ("NO NECESITAS ESTA 'APP', VE LA SECCION KE MAS TE GUSTE ¬¬")
        comb_secciones = secciones_disp_de_ramos_elegidos[0]
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
                        comb_secciones.append([big_ventana_de_combi,[i1,i2]])
                        if big_ventana_de_combi < ventana_mas_chica:
                            ventana_mas_chica = big_ventana_de_combi
                    elif opcion_elegida == 3:
                        peso_de_combi = op_3([i1,i2])
                        comb_secciones.append([peso_de_combi,[i1,i2]])
                        if peso_de_combi < peso_minimo:
                            peso_minimo = peso_de_combi
                    elif opcion_elegida == 4:
                        if op_4([i1,i2]) == True:
                            comb_secciones.append([i1,i2])
                    elif opcion_elegida == 5:
                        if op_5([i1,i2]) == True:
                            comb_secciones.append([i1,i2])
                    else:
                        comb_secciones.append([i1,i2])
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
                            comb_secciones.append([big_ventana_de_combi,[i1,i2,i3]])
                            if big_ventana_de_combi < ventana_mas_chica:
                                ventana_mas_chica = big_ventana_de_combi
                        elif opcion_elegida == 3:
                            peso_de_combi = op_3([i1,i2,i3])
                            comb_secciones.append([peso_de_combi,[i1,i2,i3]])
                            if peso_de_combi < peso_minimo:
                                peso_minimo = peso_de_combi
                        elif opcion_elegida == 4:
                            if op_4([i1,i2,i3]) == True:
                                comb_secciones.append([i1,i2,i3])
                        elif opcion_elegida == 5:
                            if op_5([i1,i2,i3]) == True:
                                comb_secciones.append([i1,i2,i3])
                        else:
                            comb_secciones.append([i1,i2,i3])
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
                                comb_secciones.append([big_ventana_de_combi,[i1,i2,i3,i4]])
                                if big_ventana_de_combi < ventana_mas_chica:
                                    ventana_mas_chica = big_ventana_de_combi
                            elif opcion_elegida == 3:
                                peso_de_combi = op_3([i1,i2,i3,i4])
                                comb_secciones.append([peso_de_combi,[i1,i2,i3,i4]])
                                if peso_de_combi < peso_minimo:
                                    peso_minimo = peso_de_combi
                            elif opcion_elegida == 4:
                                if op_4([i1,i2,i3,i4]) == True:
                                    comb_secciones.append([i1,i2,i3,i4])
                            elif opcion_elegida == 5:
                                if op_5([i1,i2,i3,i4]) == True:
                                    comb_secciones.append([i1,i2,i3,i4])
                            else:
                                comb_secciones.append([i1,i2,i3,i4])
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
                                    comb_secciones.append([big_ventana_de_combi,[i1,i2,i3,i4,i5]])
                                    if big_ventana_de_combi < ventana_mas_chica:
                                        ventana_mas_chica = big_ventana_de_combi
                                elif opcion_elegida == 3:
                                    peso_de_combi = op_3([i1,i2,i3,i4,i5])
                                    comb_secciones.append([peso_de_combi,[i1,i2,i3,i4,i5]])
                                    if peso_de_combi < peso_minimo:
                                        peso_minimo = peso_de_combi
                                elif opcion_elegida == 4:
                                    if op_4([i1,i2,i3,i4,i5]) == True:
                                        comb_secciones.append([i1,i2,i3,i4,i5])
                                elif opcion_elegida == 5:
                                    if op_5([i1,i2,i3,i4,i5]) == True:
                                        comb_secciones.append([i1,i2,i3,i4,i5])
                                else:
                                    comb_secciones.append([i1,i2,i3,i4,i5])
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
                                        comb_secciones.append([big_ventana_de_combi,[i1,i2,i3,i4,i5,i6]])
                                        if big_ventana_de_combi < ventana_mas_chica:
                                            ventana_mas_chica = big_ventana_de_combi
                                    elif opcion_elegida == 3:
                                        peso_de_combi = op_3([i1,i2,i3,i4,i5,i6])
                                        comb_secciones.append([peso_de_combi,[i1,i2,i3,i4,i5,i6]])
                                        if peso_de_combi < peso_minimo:
                                            peso_minimo = peso_de_combi
                                    elif opcion_elegida == 4:
                                        if op_4([i1,i2,i3,i4,i5,i6]) == True:
                                            comb_secciones.append([i1,i2,i3,i4,i5,i6])
                                    elif opcion_elegida == 5:
                                        if op_5([i1,i2,i3,i4,i5,i6]) == True:
                                            comb_secciones.append([i1,i2,i3,i4,i5,i6])
                                    else:
                                        comb_secciones.append([i1,i2,i3,i4,i5,i6])
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
                                            comb_secciones.append([big_ventana_de_combi,[i1,i2,i3,i4,i5,i6,i7]])
                                            if big_ventana_de_combi < ventana_mas_chica:
                                                ventana_mas_chica = big_ventana_de_combi
                                        elif opcion_elegida == 3:
                                            peso_de_combi = op_3([i1,i2,i3,i4,i5,i6,i7])
                                            comb_secciones.append([peso_de_combi,[i1,i2,i3,i4,i5,i6,i7]])
                                            if peso_de_combi < peso_minimo:
                                                peso_minimo = peso_de_combi
                                        elif opcion_elegida == 4:
                                            if op_4([i1,i2,i3,i4,i5,i6,i7]) == True:
                                                comb_secciones.append([i1,i2,i3,i4,i5,i6,i7])
                                        elif opcion_elegida == 5:
                                            if op_5([i1,i2,i3,i4,i5,i6,i7]) == True:
                                                comb_secciones.append([i1,i2,i3,i4,i5,i6,i7])
                                        else:
                                            comb_secciones.append([i1,i2,i3,i4,i5,i6,i7])
    if opcion_elegida == 2:
        arr = []
        for co_s in comb_secciones:
            if ventana_mas_chica == co_s[0]:
                arr.append(co_s[1])
        return arr
    elif opcion_elegida == 3:
        arr = []
        for co_s in comb_secciones:
            if peso_minimo == co_s[0]:
                arr.append(co_s[1])
        return arr
    else:
        return comb_secciones

def hacer_horario(combi_secciones):
    H = [["Bloque",      "LUNES","MARTES","MIÉRCOLES","JUEVES","VIERNES"],
        ["A 8:30-9:50",  ""     ,""      ,""         ,""      ,""       ],
        ["B 10:00-11:20",""     ,""      ,""         ,""      ,""       ],
        ["C 11:30-12:50",""     ,""      ,""         ,""      ,""       ],
        ["D 13:00-14:20",""     ,""      ,""         ,""      ,""       ],
        ["E 14:30-15:50",""     ,""      ,""         ,""      ,""       ],
        ["F 16:00-17:20",""     ,""      ,""         ,""      ,""       ],
        ["G 17:25-18:45",""     ,""      ,""         ,""      ,""       ],
        ["H 18:50-20:10",""     ,""      ,""         ,""      ,""       ]]
    for section in combi_secciones:
        clases_seccion = section.get_clas()
        for d in range(5): #d -> día
            b = clases_seccion[d] #b -> bloque
            if b != 0:
                H[b][d+1] = section.get_ramo_nom() + ' - Sección ' + str(section.get_num())
    return H

def checking(S, options, i_course, i_section):
    check = True
    for section in range(len(S)):
        for block in range(5):
            if S[section].get_class(block) == options[i_course][i_section].get_class(block) and S[section].get_class(block) != 0:
                check = False
                break
        if check == False:
            return check
    return check

def backtracking(options, i_course, i_section, S, V):
    if i_course == len(options): #Revisión si quedan más ramos por revisar
        V.append(copy.deepcopy(S))
        return V
    elif i_section == len(options[i_course]): #Revisión si quedan más secciones por revisar
        return V
    else:
        backtracking(options, i_course, i_section + 1, S, V)
        if checking(S, options, i_course, i_section): #Se revisa compatibilidad
            S.append(options[i_course][i_section])
            backtracking(options, i_course + 1, 0, S, V)
            S.pop()
        return V