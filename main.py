from eq_general import economia, agente


#----------------------------------------------------------------------------------
#   UTILITY FUNCTIONS
#
#   Introduce in each function the utility function of each agent in the eocnomy
#   If both have the same utility function, just intialize the agent with the same.

def u0(q1, q2):
    return(q1*q2)

def u1(q1,q2):
    return(q1*q1*q1*q2)

#----------------------------------------------------------------------------------


if __name__ == "__main__":
    #Establecemos el ratio de precios y la dotacion de cada agente 
    r=0.5
    dotacion0=[1,0]
    dotacion1=[0,1]

    #Inicializamos la economia
    eco1=economia(2,2, r)

    
    #Creamos y añadimos al agente0 a la economia
    agente0=agente("agente0",r, utility=u0)
    agente0.dotar(dotacion0)
    agente0.show_w()
    eco1.plusagente(agente0)


    #Creamos y añadimos al agente1 a la economía
    agente1=agente("agente1", r, utility=u1)
    agente1.dotar(dotacion1)
    agente1.show_w()
    eco1.plusagente(agente1)


    #Comprobamos si hay equilibrio walrasiano
    eco1.hay_wal()

    #Si no hay equilibrio walrasiano de partida, lo calculamos mediante un proceso de "tatonement".
    eco1.calcular_wal()

