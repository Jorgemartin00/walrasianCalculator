#!/usr/bin/python
class economia:
    'economia de intercambio 2x2'
    def __init__(self, nmercados, nagentes, precios):
        self.nmercados=nmercados
        self.nagentes=nagentes
        self.precios=precios
        self.agentes=[]
        self.W=[]
        self.equilibrio=True or False
        self.Z1=[]
        self.Z2=[]
        self.Z=[[],[]] #matriz con 1fila para cada bien y tantas columnas como equilibrios calculemos, nos servira para acumular los valores de Zi para cada ratio que evaluemos
    


    def dota(self, a):        
        #for e in range(0,2):   
        for o in range(0,2):
            
            if (len(self.W)<=o):
                #si no hay ningun individuo añadido tampoco habrá dotaciones en el vector
                self.W.append(a.w[o])
            else:
                #si ya hay algun individuo añadido solo hará falta sumarle la dotacion del nuevo
                self.W[o]=self.W[o]+a.w[o]
            #print(e)
        print("La dotacion de la economia es ahora ", self.W)
        
        
    def plusagente(self, ag):
        #añadimos un agente
        self.agentes.append(ag)

        #actualizamos la dotacion de la economia
        #self.dot_total() 
        print("se añade a ", ag.name, " a la economia")
        self.dota(ag)


    def show_agentes(self):
        print("\nAgentes de la economia")
        for i in self.agentes:
            print(i.name)

    def fed(self, n):
        q=0
        for i in self.agentes:
            q+=i.qeq[n]
        return(q-self.W[n])
    
    def hay_wal(self):
        for i in self.agentes:
            i.maxu()
        Z=[]
        Z1=float
        Z2=float
        cont=0
        for i in range(self.nmercados):
            Z.append(self.fed(i))   #con esto veremos los valores de las Z para cada r
            self.Z[i].append(self.fed(i))  #con esto metemos los valores de las Z en unos vectores temporales que nos serviran para guardar los valores de Z segun cambia el ratio

        print("Funciones de exceso de demanda: ", Z)
        for u in Z:
            if abs(u)>0.1:
                cont+=1
        if cont==0:
            print("Hay equilibrio Walrasiano\n")
            self.equilibrio=True
        else:
            print("No hay equilibrio walrasiano\n")
            self.equilibrio=False

    def calcular_wal(self):
        p=1
        while (self.equilibrio==False):
            
            self.precios+=p
            print("ratio de precios: ", self.precios)
            #actualizamos el ratio de precios al que evaluaremos si genera equilibrio
            for i in self.agentes:
                i.precios=self.precios
    
            #comprobamos si hay equilibrio walrasiano
            self.hay_wal()

            #si hay equilibrio se para el bucle
            if (self.equilibrio==True):
                break
            else:
                #si no hay equilibrio, cambiamos el vector de precios
                '''puede ocurrir que del vector de precios que partiamos, el nuevo ratio nos aleje del equilibrio walrasiano o nos acerque
                supondrmeos que las funciones de exceso de demanda son monotonas y que solo hay un vector de precios que produzca walrasiano
                Tambien podemos interpretarlo como que nos llevara al ratio de precios que genere walrasiano mas cercano al ratio con el que hemos empezado
                '''

                '''EL proceso de cambio de precios tiene 3 pasos:
                1) ver si el precio era mayor o menor que cero
                2) si al cambiar el precio en la direccion preestablecida, comprobar si nos alejamos o acercamos al eq walrasiano
                3) si al cambiar el precio, el exceso de demanda se convierte en exceso de oferta o al reves

                Si en el caso dos nos alejamos, tendremos que cambiar la direccion en que cambia el ratio
                Si en el caso tres pasamos de un exceso al otro, tendremos que retroceder al precio que teniamos antes y reducir la variacion
                '''            
                if(self.Z[0][0]>0):  

                    
                    if(self.Z[0][0]<self.Z[0][-1]): #si al aumentar los precios el valor de Z nos ha dado mayor, cambiamos a negativa la variacion en los precios
                        p=p*(-1)
                    
                    
                    if(self.Z[0][-1]<0): #si el nuevo valor de Z nos da por debajo de 0, volvemos al Z anterior y reducimos la variacion en los precios a la mitad4
                        self.precios=self.precios-p #retrocedemos al anterior
                        p=p/2           #reducimos la variacion a la mitad


                if(self.Z[0][0]<0): 

                    
                    if(self.Z[0][0]>self.Z[0][-1]): #si al aumentar los precios el valor de Z nos ha dado mayor, cambiamos a positiva la variacion en los precios
                        p=p*(-1)
                    
                    
                    if(self.Z[0][-1]>0): #si el nuevo valor de Z nos da por encima de 0, volvemos al Z anterior y reducimos la variacion en los precios a la mitad4
                        self.precios=self.precios-p #retrocedemos al anterior
                        p=p/2           #reducimos la variacion a la mitad
                    



    #   def calcular_eqwal():
    #funcion que calcule el vector de precios 



class agente:
    'agente que participa en una economia d eintercambio'
    def __init__(self, name, precios, utility):
        #definimos el vector de dotaciones, siendo la primera componente la dotacion del bien 1
        self.name=name
        self.precios=precios
        self.w=[]  
        self.qeq=[]
        self.utility=utility
    
    def dotar(self, d):
        for i in d:
            self.w.append(i)

    def show_w(self):
        print ("Dotacion de ", self.name, self.w)



    def maxu(self):
        # escribimos la expresion de la funcion de utilidad de los individuos
        def utilidad(q1, q2):
            return q1*q2

        #establecemos el paso que queremos para las x
        h=0.1

        #al ser una restriccion positiva solo evaluaremos la funcion en el primer cuadrante, por lo que al, ser decreciente, encontramos el corte con el eje de las x
        d=self.w[0]+(1/self.precios)*self.w[1]

        #el tamaño de los arrays que utilizaremos será de d/h
        tamaño_array=d/h

        #array donde almacenaremos las coordenadas x de la restriccion
        cx=[]

        #array donde almacenaremos las coordenadas y de la restriccion
        cy=[]

        #array donde almacenaremos la imagen de cada punto de la restriccion en la funcion de utilidad
        u=[]

        #realizamos un bucle en el que evaluaremos todos los puntos de la restriccion en la funcion de utilidad
        for e in range(0,int(tamaño_array)):
            cx.append(e*h)
            cy.append(self.precios*(self.w[0]-cx[-1])+self.w[1])
            #print("c", cx[-1], cy[-1])
            #print(cx[-1]*cy[-1])
            #u.append(cx[-1]*cy[-1])  
            u.append(self.utility(cx[-1], cy[-1]))  

        #nos quedamos con la máxima utilidad y su correspondiente vector de cantidades
        umax=max(u)
        print("Maxima uilidad alcanzable de ", self.name,":",  umax)
        i=u.index(max(u))        
        self.qeq=[cx[i], cy[i]]
        print(self.name," (q1, q2) ", self.qeq)




