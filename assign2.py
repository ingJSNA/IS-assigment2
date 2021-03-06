from networkx.classes.function import neighbors

# coding: utf-8

# # Intelligent Systems Assignment 2
# 
# ## Bayes' net inference
# 
# **Names:**
# 
# **IDs:**
# 

# In[9]:

class Directions:
    NORTH = 'North'
    SOUTH = 'South'
    EAST = 'East'
    WEST = 'West'
    STOP = 'Stop'


# ### a. Bayes' net for instant perception and position.
# 
# Build a Bayes' net that represent the relationships between the random variables. Based on it, write an expression for the joint probability distribution of all the variables.
# 
# ![title](img/BayesNet1.png)
# $P(X, E_{N}, E_{S}, E_{W},E_{E}) = P(X)P(E_{N}|X)P(E_{S}|X)P(E_{W}|X)P(E_{E}|X)$
# 
# ### b. Probability functions calculated from the instant model.
# 
# Assuming an uniform distribution for the Pacman position probability, write functions to calculate the following probabilities:
# 
# i. $P(X=x|E_{N}=e_{N},E_{S}=e_{S})$

# In[ ]:

import copy

def getMapa():
    mapa = [[0] * 6 for i in range(1, 6)]
    mapa[1][1] = 1
    mapa[1][3] = 1
    mapa[1][4] = 1
    
    mapa[3][1] = 1
    mapa[3][3] = 1
    mapa[3][4] = 1
    return mapa

def getMap():
    mapa = getMapa()

    matriz = [[None] * 6 for i in range(1, 6)]
    
    px = 1 / float(24)
    
    for x in range(0, 5):
        for y in range(0, 6):
            if(mapa [x][y] == 1):
                p = 0.0
            else:
                p = px
            
            if(x == 0):
                n = True
            elif(mapa[x - 1][y] == 1):
                n = True
            else:
                n = False
            
            if(x == 4):
                s = True
            elif(mapa[x + 1][y] == 1):
                s = True
            else:
                s = False
            
            if(y == 0):
                l = True
            elif(mapa[x][y - 1] == 1):
                l = True
            else:
                l = False
            
            if(y == 5):
                r = True
            elif(mapa[x][y + 1] == 1):
                r = True
            else:
                r = False
            
            matriz[x][y] = [n, l, p, r, s]
            
    return matriz

def getNeighbors(matrix, x, y):
    neighbors = []
    
    if x > 0:
        neighbors.append([x-1, y])
    if x+1 < len(matrix):
        neighbors.append([x+1, y])
    if y > 0:
        neighbors.append([x, y-1])
    if y+1 < len(matrix[x]):
        neighbors.append([x, y+1])
    
    return neighbors

# In[10]:

def P_1(eps, E_N, E_S):
    '''
    Calculates: P(X=x|E_{N}=e_{N},E_{S}=e_{S})
    Arguments: E_N, E_S \in {True,False}
               0 <= eps <= 1 (epsilon)
    '''
    truePerception = 1 - eps;
    falsePerception = eps;
    
    
    matrix = getMap()
    den = 0
    for i in range(len(matrix)):
        row = matrix[i]
        for j in range(len(row)):
            n, l, p, r, s = row[j]
            
            pn = falsePerception
            ps = falsePerception
            if n == E_N:
                pn = truePerception
            if s == E_S:
                ps = truePerception
            den += (p * pn * ps)
    
    
    pd = {(x, y):0 for x in range(1, 7) for y in range(1, 6)}
    
    for i in range(len(matrix)):
        row = matrix[i]
        for j in range(len(row)):
            n, l, p, r, s = row[j]
            pn = falsePerception
            ps = falsePerception
            if n == E_N:
                pn = truePerception
            if s == E_S:
                ps = truePerception
            p = (p * pn * ps) / den
            
            row[j] = [n, l, p, r, s]
            # Cambiar a coordenadas cartesianas
            pd[(j + 1, 5 - i)] = p
                
    
    return pd

P_1(0.0, True, False)


# ii. $P(E_{E}=e_{E}|E_{N}=e_{N},E_{S}=E_{S})$

# In[11]:

def P_2(eps, E_N, E_S):
    '''
    Calculates: P(E_{E}=e_{E}|E_{N}=e_{N},E_{S}=E_{S})
    Arguments: E_N, E_S \in {True,False}
               0 <= eps <= 1
    '''
    
    truePerception = 1 - eps;
    falsePerception = eps;
    
    mapa = getMapa()
    matrix = getMap()
    den = 0
    for i in range(len(matrix)):
        row = matrix[i]
        for j in range(len(row)):
            n, w, p, e, s = row[j]
            
            pn = falsePerception
            ps = falsePerception

            if n == E_N:
                pn = truePerception
            if s == E_S:
                ps = truePerception
                
            if mapa[i][j]==0:
                wall=1
            else:
                wall=0
                
            den += (p * pn * ps * wall)
            #print den    

    peTrue=0
    
    for i in range(len(matrix)):
        row = matrix[i]
        for j in range(len(row)):
            n, w, p, e, s = row[j]
            
            pn = falsePerception
            ps = falsePerception
            pe = falsePerception
            
            if n == E_N:
                pn = truePerception
            if s == E_S:
                ps = truePerception
            if e == True: # fix perception
                pe = truePerception
           # print r
            if mapa[i][j]==0:
                wall=1
            else:
                wall=0
            
            peTrue += (p * pn * ps * pe  * wall)
            #/den
        #print i,' ',j,' ',pr,' ',pr/den
# print count    
    peTrue = peTrue/den
#    print pr
            
    pd = {True:peTrue, False:(1-peTrue)}   
    
    return pd

P_2(0.2, True, False)


# iii. $P(S)$, where $S\subseteq\{e_{N},e_{S},e_{E},e_{W}\}$

# In[12]:

def P_3(eps, S):
    '''
    Calculates: P(S), where S\subseteq\{e_{N},e_{S},e_{E},e_{W}\}
    Arguments: S a dictionary with keywords in Directions and values in
    {True,False}
               0 <= eps <= 1
    '''
#   for i in range(len(S)):
#        print S[i]

    mapa = getMapa()
    matrix = getMap()
    truePerception = 1 - eps;
    falsePerception = eps;
    
    pb=0
    
    if(len(S)==1):
        
        for i in range(len(matrix)):
                row = matrix[i]
                for j in range(len(row)):
                    n, l, p, r, s = row[j]
                   
                    pr = falsePerception
                    pn = falsePerception
                    pl = falsePerception
                    ps = falsePerception
                    
                    if mapa[i][j]==0:
                        wall=1
                    else:
                        wall=0

                    if S.get(Directions.EAST) != None:
                        if r == S.get(Directions.EAST):
                            pr = truePerception
                        pb += (pr*wall*p)
                    elif S.get(Directions.WEST) != None:
                        if l == S.get(Directions.WEST):
                            pl = truePerception
                        pb += (pl*wall*p)
                    elif S.get(Directions.SOUTH) != None:
                        if s == S.get(Directions.SOUTH):
                            ps = truePerception
                        pb += (ps*wall*p)
                    elif S.get(Directions.NORTH) != None:
                        if n == S.get(Directions.NORTH):
                            pn = truePerception
                        pb += (pn*wall*p)
    elif(len(S)==2):
        for i in range(len(matrix)):
                row = matrix[i]
                for j in range(len(row)):
                    n, l, p, r, s = row[j]
                  
                    pr = falsePerception
                    pn = falsePerception
                    pl = falsePerception
                    ps = falsePerception
                    
                    if mapa[i][j]==0:
                        wall=1
                    else:
                        wall=0

                    if S.get(Directions.EAST) != None and S.get(Directions.WEST) != None:
                        if r == S.get(Directions.EAST):
                            pr = truePerception
                        if l == S.get(Directions.WEST):
                            pl = truePerception
                        pb += (pr*pl*wall*p)
                    elif S.get(Directions.EAST) != None and S.get(Directions.SOUTH) != None:
                        if r == S.get(Directions.EAST):
                            pr = truePerception
                        if s == S.get(Directions.SOUTH):
                            ps = truePerception
                        pb += (pr*ps*wall*p)
                    elif S.get(Directions.EAST) != None and S.get(Directions.NORTH) != None:
                        if r == S.get(Directions.EAST):
                            pr = truePerception
                        if n == S.get(Directions.NORTH):
                            pn = truePerception
                        pb += (pr*pn*wall*p)
                    elif S.get(Directions.WEST) != None and S.get(Directions.SOUTH) != None:
                        if l == S.get(Directions.WEST):
                            pl = truePerception
                        if s == S.get(Directions.SOUTH):
                            ps = truePerception
                        pb += (pl*ps*wall*p)
                    
                    elif S.get(Directions.WEST) != None and S.get(Directions.NORTH) != None:
                        if l == S.get(Directions.WEST):
                            pl = truePerception
                        if n == S.get(Directions.NORTH):
                            pn = truePerception
                        pb += (pl*pn*wall*p)
                    elif S.get(Directions.NORTH) != None and S.get(Directions.SOUTH) != None:
                        if n == S.get(Directions.NORTH):
                            pn = truePerception
                        if s == S.get(Directions.SOUTH):
                            ps = truePerception
                        pb += (pn*ps*wall*p)
                    
    
    elif(len(S)==3):
        for i in range(len(matrix)):
                row = matrix[i]
                for j in range(len(row)):
                    n, l, p, r, s = row[j]
                  
                    pr = falsePerception
                    pn = falsePerception
                    pl = falsePerception
                    ps = falsePerception
                    
                    if mapa[i][j]==0:
                        wall=1
                    else:
                        wall=0

                    if S.get(Directions.EAST) != None and S.get(Directions.WEST) != None and S.get(Directions.SOUTH) != None:
                        if r == S.get(Directions.EAST):
                            pr = truePerception
                        if l == S.get(Directions.WEST):
                            pl = truePerception
                        if s == S.get(Directions.SOUTH):
                            ps = truePerception
                        pb += (pr*pl*ps*wall*p)
                    elif S.get(Directions.EAST) != None and S.get(Directions.WEST) and S.get(Directions.NORTH) != None:
                        if r == S.get(Directions.EAST):
                            pr = truePerception
                        if l == S.get(Directions.WEST):
                            pl = truePerception
                        if n == S.get(Directions.NORTH):
                            pn = truePerception
                        pb += (pr*pl*pn*wall*p)
                    elif S.get(Directions.EAST) != None and S.get(Directions.NORTH) != None and S.get(Directions.SOUTH) != None:
                        if r == S.get(Directions.EAST):
                            pr = truePerception
                        if n == S.get(Directions.NORTH):
                            pn = truePerception
                        if s == S.get(Directions.SOUTH):
                            ps = truePerception
                        pb += (pr*pn*ps*wall*p)    
                    elif S.get(Directions.WEST) != None and S.get(Directions.NORTH) != None and S.get(Directions.SOUTH) != None:
                        if l == S.get(Directions.WEST):
                            pl = truePerception
                        if n == S.get(Directions.NORTH):
                            pn = truePerception
                        if s == S.get(Directions.SOUTH):
                            ps = truePerception
                        pb += (pl*pn*ps*wall*p)  
                    
    elif(len(S)==4):
        for i in range(len(matrix)):
                row = matrix[i]
                for j in range(len(row)):
                    n, l, p, r, s = row[j]
                  
                    pr = falsePerception
                    pn = falsePerception
                    pl = falsePerception
                    ps = falsePerception
                    
                    if mapa[i][j]==0:
                        wall=1
                    else:
                        wall=0

                    if S.get(Directions.EAST) != None and S.get(Directions.WEST) != None and S.get(Directions.SOUTH) != None and S.get(Directions.NORTH) != None:
                        if r == S.get(Directions.EAST):
                            pr = truePerception
                        if l == S.get(Directions.WEST):
                            pl = truePerception
                        if s == S.get(Directions.SOUTH):
                            ps = truePerception
                        if n == S.get(Directions.NORTH):
                            pn = truePerception
                        pb += (pr*pl*ps*pn*wall*p)
                    
                    
#    print pb
    
    
    return pb

P_3(0.3, {Directions.EAST: True, Directions.SOUTH: False})


# ### c. Bayes' net for dynamic perception and position.
# 
# Now we will consider a scenario where the Pacman moves a finite number of steps $n$. In this case we have $n$
# different variables for the positions $X_{1},\dots,X_{n}$, as well as for each one of the perceptions, e.g.
# $E_{N_{1}},\dots,E_{N_{n}}$ for the north perception. For the initial Pacman position, assume an uniform 
# distribution among the valid positions. Also assume that at each time step the Pacman choses, to move, one of the valid neighbor positions with uniform probability. Draw the corresponding Bayes' net for $n=4$.
# 
# ### d. Probability functions calculated from the dynamic model.
# 
# Assuming an uniform distribution for the Pacman position probability, write functions to calculate the following probabilities:
# 
# i. $P(X_{4}=x_{4}|E_{1}=e_{1},E_{3}=e_{3})$

# In[13]:
    

def P_4(eps, E_1, E_3):
    '''
    Calculates: P(X_{4}=x_{4}|E_{1}=e_{1},E_{3}=e_{3})
    Arguments: E_1, E_3 dictionaries of type Directions --> {True,False}
               0 <= eps <= 1
    '''
    truePerception = 1 - eps;
    falsePerception = eps;
    

    matrix = getMap()       # P(X1)
    for i in range(len(matrix)):
        row = matrix[i]
        for j in range(len(row)):
            n, w, p, e, s = row[j]
            
            pn = falsePerception
            ps = falsePerception
            pe = falsePerception
            pw = falsePerception
            if n == E_1[Directions.NORTH]:
                pn = truePerception
            if s == E_1[Directions.SOUTH]:
                ps = truePerception
            if e == E_1[Directions.EAST]:
                pe = truePerception
            if w == E_1[Directions.WEST]:
                pw = truePerception
            p = (p * pn * ps * pe * pw)     # P(X1)P(E1 | X1)
            row[j][2] = p
            
            matrix2 = copy.deepcopy(matrix)
            for i2 in range(len(matrix2)):
                row2 = matrix2[i]
                for j2 in range(len(row2)):
                    n2, w2, p2, e2, s2 = row2[j]
                    neighbors = getNeighbors(matrix2, i,j)
                    px2 = 1/float(len(neighbors))
                    isNeighbor = False
                    for neighbor in neighbors:
                        a, b = neighbor
                        if i2==a and j2 == b:
                            p2 = p2 * px2   # P(X1)P(E1 | X1)P(X2 | X1)
                            isNeighbor = True
                    if isNeighbor == False:
                        p2 = 0
                    
                    row2[j][2] = p2
                    
                        
    
    
    
    pd = {(x, y):0 for x in range(1, 7) for y in range(1, 6)}
    
    for i in range(len(matrix)):
        row = matrix[i]
        for j in range(len(row)):
            n, w, p, e, s = row[j]
                        # Cambiar a coordenadas cartesianas
            pd[(j + 1, 5 - i)] = p
                
    
    return pd

E_1 = {Directions.NORTH: True, Directions.SOUTH: False, Directions.EAST: True, Directions.WEST: False}
E_3 = {Directions.NORTH: True, Directions.SOUTH: True, Directions.EAST: False, Directions.WEST: False}
P_4(0.1, E_1, E_3)


# ii. $P(X_{2}=x_{2}|E_{2}=e_{2},E_{3}=e_{3},E_{4}=e_{4})$

# In[14]:

def P_5(eps, E_2, E_3, E_4):
    '''
    Calculates: P(X_{2}=x_{2}|E_{2}=e_{2},E_{3}=e_{3},E_{4}=e_{4})
    Arguments: E_2, E_3, E_4 dictionaries of type Directions --> {True,False}
               0 <= eps <= 1
    '''
    pd = {(x, y):0 for x in range(1, 7) for y in range(1, 6)}
    return pd

E_2 = {Directions.NORTH: True, Directions.SOUTH: False, Directions.EAST: True, Directions.WEST: False}
E_3 = {Directions.NORTH: True, Directions.SOUTH: True, Directions.EAST: False, Directions.WEST: False}
E_4 = {Directions.NORTH: True, Directions.SOUTH: False, Directions.EAST: True, Directions.WEST: False}
P_5(0.1, E_2, E_3, E_4)


# iii. $P(E_{4}=e_{4}|E_{1}=e_{1},E_{2}=e_{2},E_{3}=e_{3})$

# In[15]:

def P_6(eps, E_1, E_2, E_3):
    '''
    Calculates: P(E_{4}=e_{4}|E_{1}=e_{1},E_{2}=e_{2},E_{3}=e_{3})
    Arguments: E_1, E_2, E_3 dictionaries of type Directions --> {True,False}
               0 <= eps <= 1
    '''
    pd = {(n, s, e, w): 0 for n in [False, True] for s in [False, True] 
                                 for e in [False, True] for w in [False, True]}
    return pd

E_1 = {Directions.NORTH: True, Directions.SOUTH: False, Directions.EAST: True, Directions.WEST: False}
E_2 = {Directions.NORTH: True, Directions.SOUTH: False, Directions.EAST: True, Directions.WEST: False}
E_3 = {Directions.NORTH: True, Directions.SOUTH: True, Directions.EAST: False, Directions.WEST: False}
P_6(0.1, E_1, E_2, E_3)


# iv. $P(E_{E_{2}}=e_{E_{2}}|E_{N_{2}}=e_{N_{2}},E_{S_{2}}=E_{S_{2}})$

# In[16]:

def P_7(eps, E_N, E_S):
    '''
    Calculates: P(E_{E_{2}}=e_{E_{2}}|E_{N_{2}}=e_{N_{2}},E_{S_{2}}=E_{S_{2}})
    Arguments: E_N_2, E_S_2 \in {True,False}
               0 <= eps <= 1
    '''
    pd = {True:0, False:0}
    return pd

P_7(0.1, True, False)


# ### Test functions
# 
# You can use the following functions to test your solutions.

# In[17]:

def approx_equal(val1, val2):
    return abs(val1 - val2) <= 0.00001

def test_P_1():
    pd = P_1(0.0, True, True)
    assert approx_equal(pd[(2, 1)], 0.1111111111111111)
    assert approx_equal(pd[(3, 1)], 0)
    pd = P_1(0.3, True, False)
    assert approx_equal(pd[(2, 1)], 0.03804347826086956)
    assert approx_equal(pd[(3, 1)], 0.016304347826086956)
    print "pass test 1"

def test_P_2():
    pd = P_2(0.0, True, True)
    assert approx_equal(pd[False], 1.0)
    pd = P_2(0.3, True, False)
    assert approx_equal(pd[False], 0.5514492753623188)
    print "pass test 2"

def test_P_3():
    pd = P_3(0.1, {Directions.EAST: True, Directions.WEST: True})
    assert approx_equal(pd, 0.2299999999999999)
    pd = P_3(0.1, {Directions.EAST: True})
    assert approx_equal(pd, 0.3999999999999999)
    pd = P_3(0.2, {Directions.EAST: False, Directions.WEST: True, Directions.SOUTH: True})
    assert approx_equal(pd, 0.0980000000000000)
    print "pass test 3"

def test_P_4():
    E_1 = {Directions.NORTH: False, Directions.SOUTH: False, Directions.EAST: True, Directions.WEST: True}
    E_3 = {Directions.NORTH: False, Directions.SOUTH: False, Directions.EAST: True, Directions.WEST: True}
    pd = P_4(0.0, E_1, E_3)
    assert approx_equal(pd[(6, 3)], 0.1842105263157895)
    assert approx_equal(pd[(4, 3)], 0.0)
    pd = P_4(0.2, E_1, E_3)
    assert approx_equal(pd[(6, 3)], 0.17777843398830864)
    assert approx_equal(pd[(4, 3)], 0.000578430282649176)
    E_1 = {Directions.NORTH: True, Directions.SOUTH: False, Directions.EAST: True, Directions.WEST: False}
    E_3 = {Directions.NORTH: False, Directions.SOUTH: False, Directions.EAST: True, Directions.WEST: False}
    pd = P_4(0.0, E_1, E_3)
    assert approx_equal(pd[(6, 2)], 0.3333333333333333)
    assert approx_equal(pd[(4, 3)], 0.0)

def test_P_5():
    E_2 = {Directions.NORTH: True, Directions.SOUTH: True, Directions.EAST: False, Directions.WEST: False}
    E_3 = {Directions.NORTH: True, Directions.SOUTH: False, Directions.EAST: False, Directions.WEST: False}
    E_4 = {Directions.NORTH: True, Directions.SOUTH: True, Directions.EAST: False, Directions.WEST: False}
    pd = P_5(0, E_2, E_3, E_4)
    assert approx_equal(pd[(2, 5)], 0.5)
    assert approx_equal(pd[(4, 3)], 0.0)
    pd = P_5(0.3, E_2, E_3, E_4)
    assert approx_equal(pd[(2, 5)], 0.1739661245168835)
    assert approx_equal(pd[(4, 3)], 0.0787991740545979)

def test_P_7():
    pd = P_7(0.0, True, False)
    assert approx_equal(pd[False], 0.7142857142857143)
    pd = P_7(0.3, False, False)
    assert approx_equal(pd[False], 0.5023529411764706)
    
test_P_3()


# In[ ]:



