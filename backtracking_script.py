M = [ 
    
    [ [2,0,3,0,2] , [0,2,0,4,4] ], #Ramo 4 y sus secciones
    [ [1,0,1,0,1] , [2,0,2,0,2] ], #Ramo 2 y sus secciones
    [ [0,3,4,0,3] , [0,4,3,0,4] ], #Ramo 3 y sus secciones
    [ [2,0,2,0,3] , [3,0,3,0,2] ], #Ramo 1 y sus secciones

    ]

S = []

def backtracking (options, i_course, i_section):

    if i_course >= len(M): #Revisión si quedan más ramos por revisar
        print("caso 1")
        return
    elif i_section >= len(options[i_course]): #Revisión si quedan más secciones por revisar
        print("caso 2")
        i_section = 0
        return backtracking(options, i_course + 1, i_section)
    else:
        if len(S) == 0:
            S.append(options[i_course][i_section])
            print(S)
            i_section = 0
            return backtracking(options,i_course + 1, i_section)
        check = True
        for section in range(len(S)):
            for block in range(len(S[section])):
                print(block)
                if S[section][block] == options[i_course][i_section][block] and S[section][block] != 0:
                    check = False
                    break
            if check == False:
                return backtracking(options, i_course, i_section + 1)
        if check == True:
            S.append(options[i_course][i_section])
            print(S)
            print("Ramo" + str(i_course))
            i_section = 0
            return backtracking(options, i_course + 1, i_section)

backtracking(M,0,0)
print(S)