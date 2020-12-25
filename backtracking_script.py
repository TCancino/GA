#M = [ 
#    
#    [ [2,0,2,0,3] , [3,0,3,0,2] ], #Ramo 1 y sus secciones
#    [ [1,0,1,0,1] , [2,0,2,0,2] ], #Ramo 2 y sus secciones
#    [ [0,3,4,0,3] , [0,4,3,0,4] ], #Ramo 3 y sus secciones
#    [ [2,0,3,0,2] , [0,2,0,4,4] ], #Ramo 4 y sus secciones
#
#    ]

M = [ 
    
    [ [2,0,2,0,3] , [3,0,3,0,2] ], #Ramo 1 y sus secciones
    [ [1,0,1,0,1] , [2,0,2,0,2] ], #Ramo 2 y sus secciones

    ]

V = []

def checking (S, options, i_course, i_section):
    check = True
    for section in range(len(S)):
        for block in range(len(S[section])):
            if S[section][block] == options[i_course][i_section][block] and S[section][block] != 0:
                check = False
                break
        if check == False:
            return check
    return check

def backtracking (options, i_course, i_section, S):
    
    if i_course >= len(M): #Revisión si quedan más ramos por revisar
        #if len(S) < 3 and S not in V:
        #    V.append(S)
        print(S)
        return
    elif i_section >= len(options[i_course]): #Revisión si quedan más secciones por revisar
        if len(S) == 0:
            return
        i_section = 0
        return backtracking(options, i_course + 1, i_section, S)
    else:
        backtracking(options,i_course, i_section + 1, S)
        check = checking(S, options, i_course, i_section) #Se revisa compatibilidad
        if check == False:
            return backtracking(options, i_course, i_section + 1, [])
        if check == True:
            S.append(options[i_course][i_section])
            i_section = 0
            if S not in V:
                V.append(S)
            return backtracking(options, i_course + 1, i_section, S)

S = []
backtracking(M,0,0,S)
for s in V:
    print(s)