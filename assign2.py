
# coding: utf-8

# # Intelligent Systems Assignment 2
# 
# ## Bayes' net inference
# 
# **Names:**
# 
# **IDs:**
# 

# In[1]:

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
# ### b. Probability functions calculated from the instant model.
# 
# Assuming an uniform distribution for the Pacman position probability, write functions to calculate the following probabilities:
# 
# i. $P(X=x|E_{N}=e_{N},E_{S}=e_{S})$

# In[24]:

def P_1(E_N, E_S):
    '''
    Calculates: P(X=x|E_{N}=e_{N},E_{S}=e_{S})
    Arguments: E_N, E_S \in {True,False}
    '''
    pd = {(x,y):0 for x in range(1,7) for y in range(1,6)}
    return pd

P_1(True, False)


# ii. $P(E_{E}=e_{E}|E_{N}=e_{N},E_{S}=E_{S})$

# In[25]:

def P_2(E_N, E_S):
    '''
    Calculates: P(E_{E}=e_{E}|E_{N}=e_{N},E_{S}=E_{S})
    Arguments: E_N, E_S \in {True,False}
    '''
    pd = {True:0, False:0}
    return pd

P_2(True, False)


# iii. $P(S)$, where $S\subseteq\{e_{N},e_{S},e_{E},e_{W}\}$

# In[26]:

def P_3(S):
    '''
    Calculates: P(S), where S\subseteq\{e_{N},e_{S},e_{E},e_{W}\}
    Arguments: S a dictionary with keywords in Directions and values in
    {True,False}
    '''
    return 0

P_3({Directions.EAST: True, Directions.SOUTH: False})


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

# In[27]:

def P_4(E_1, E_3):
    '''
    Calculates: P(X_{4}=x_{4}|E_{1}=e_{1},E_{3}=e_{3})
    Arguments: E_1, E_3 dictionaries of type Directions --> {True,False}
    '''
    pd = {(x,y):0 for x in range(1,7) for y in range(1,6)}
    return pd

E_1 = {Directions.NORTH: True, Directions.SOUTH: False, Directions.EAST: True, Directions.WEST: False}
E_3 = {Directions.NORTH: True, Directions.SOUTH: True, Directions.EAST: False, Directions.WEST: False}
P_4(E_1, E_3)


# ii. $P(X_{2}=x_{2}|E_{2}=e_{2},E_{3}=e_{3},E_{4}=e_{4})$

# In[28]:

def P_5(E_2, E_3, E_4):
    '''
    Calculates: P(X_{2}=x_{2}|E_{2}=e_{2},E_{3}=e_{3},E_{4}=e_{4})
    Arguments: E_2, E_3, E_4 dictionaries of type Directions --> {True,False}
    '''
    pd = {(x,y):0 for x in range(1,7) for y in range(1,6)}
    return pd

E_2 = {Directions.NORTH: True, Directions.SOUTH: False, Directions.EAST: True, Directions.WEST: False}
E_3 = {Directions.NORTH: True, Directions.SOUTH: True, Directions.EAST: False, Directions.WEST: False}
E_4 = {Directions.NORTH: True, Directions.SOUTH: False, Directions.EAST: True, Directions.WEST: False}
P_5(E_2, E_3, E_4)


# iii. $P(E_{4}=e_{4}|E_{1}=e_{1},E_{2}=e_{2},E_{3}=e_{3})$

# In[29]:

def P_6(E_1, E_2, E_3):
    '''
    Calculates: P(E_{4}=e_{4}|E_{1}=e_{1},E_{2}=e_{2},E_{3}=e_{3})
    Arguments: E_1, E_2, E_3 dictionaries of type Directions --> {True,False}
    '''
    pd = {(n, s, e, w): 0 for n in [False, True] for s in [False, True] 
                                 for e in [False, True] for w in [False, True]}
    return pd

E_1 = {Directions.NORTH: True, Directions.SOUTH: False, Directions.EAST: True, Directions.WEST: False}
E_2 = {Directions.NORTH: True, Directions.SOUTH: False, Directions.EAST: True, Directions.WEST: False}
E_3 = {Directions.NORTH: True, Directions.SOUTH: True, Directions.EAST: False, Directions.WEST: False}
P_6(E_1, E_2, E_3)


# iv. $P(E_{E_{2}}=e_{E_{2}}|E_{N_{2}}=e_{N_{2}},E_{S_{2}}=E_{S_{2}})$

# In[30]:

def P_7(E_N, E_S):
    '''
    Calculates: P(E_{E_{2}}=e_{E_{2}}|E_{N_{2}}=e_{N_{2}},E_{S_{2}}=E_{S_{2}})
    Arguments: E_N_2, E_S_2 \in {True,False}
    '''
    pd = {True:0, False:0}
    return pd

P_7(True, False)

