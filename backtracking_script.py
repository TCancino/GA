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
    
    if i_course == len(M): #Revisión si quedan más ramos por revisar
        print(S)
        return S

    elif i_section == len(options[i_course]): #Revisión si quedan más secciones por revisar
        return S

    else:
        if len(S) == 0:
            backtracking(options, i_course, i_section + 1, [])

        else:
            backtracking(options, i_course, i_section + 1, S)

        if checking(S, options, i_course, i_section): #Se revisa compatibilidad
            S.append(options[i_course][i_section])
            #print(S)
            backtracking(options, i_course + 1, 0, S)

            S.pop()

#M = [ 
#    
#    [ [2,0,2,0,3] , [3,0,3,0,2] ], #Ramo 1 y sus secciones
#    [ [1,0,1,0,1] , [7,0,7,0,7] ], #Ramo 2 y sus secciones
#    [ [0,3,4,0,3] , [0,4,3,0,4] ], #Ramo 3 y sus secciones
#    [ [2,0,3,0,2] , [0,6,0,6,6] ], #Ramo 4 y sus secciones
#
#    ]

M = [ 
    
    [ [1,0,1,0,1] , [2,0,2,0,2], [3,0,3,0,3] ], #Ramo 1 y sus secciones
    [ [4,0,4,0,4] , [5,0,5,0,5], [6,0,6,0,6] ], #Ramo 2 y sus secciones
    [ [7,0,7,0,7] , [8,0,8,0,8], [9,0,9,0,9] ]

    ]

backtracking(M,0,0,[])
#for s in V:
#    print(s)
#print(V)