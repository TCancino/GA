import copy

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

def backtracking (options, i_course, i_section, S, V):

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

#def max_rest(V):
#
#    if len(V) == 0:
#        return -1
#
#    max_aux = -1
#
#    for x in V:
#
#
#
#    return


M = [

    [ [1,0,1,0,1] , [2,0,2,0,2], [3,0,3,0,3] ], #Ramo 1 y sus secciones
    [ [4,0,4,0,4] , [5,0,5,0,5], [6,0,6,0,6] ], #Ramo 2 y sus secciones
    [ [7,0,7,0,7] , [8,0,8,0,8], [9,0,9,0,9] ]  #Ramo 3 y sus secciones

    ]


V = backtracking(M,0,0,[],[])
#max_rest(V)

for s in V:
    print(s)
#print(V)