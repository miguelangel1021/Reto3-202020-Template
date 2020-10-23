"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

import sys
import config
from App import controller
assert config
from DISClib.DataStructures import listiterator as it
from DISClib.ADT import list as lt
"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________



Archiaccidentes ="test3.csv"


# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de accidentes")
    print("3- Accidente por fecha")
    print("4- Accidentes en rango de fechas")
    print("5- Accidentes en rango de horas")
    print("6- Accidentes en radio")
    print("0- Salir")
    print("*******************************************")


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        Analyzer = controller.init()
        print("Se ha inicializado el catalogo...")

    elif int(inputs[0]) == 2:
        print("\nCargando información de accidentes ....\n")
        controller.loadData(Analyzer,Archiaccidentes)
        print('Accidentes cargados: ' + str(controller.sizeAccidentes(Analyzer)))
        print('Fechas cargadas: ' + str(controller.sizeArbol(Analyzer)),"\n")
        print('La altura del arbol es: ' + str(controller.Altura(Analyzer)),"\n")

    elif int(inputs[0]) == 3:
        Fecha=input('Ingrese una fecha en este formato (YYYY-MM-DD)\n>')
        tamaño,lista=controller.Dar_cantidad_por_fecha(Analyzer,Fecha)
        print("\nSe encontraron",tamaño,"accidentes registrados en la fecha",Fecha)
        iterador=it.newIterator(lista)
        while it.hasNext(iterador):
            element=it.next(iterador)
            Severidad=element["Severidad"]
            size=lt.size(element["Lista_Accidentes"])
            print("La severidad",Severidad,"tiene",size,"Accidentes")
    
    elif int(inputs[0]) == 4:
        Fecha_inical=input("ingrese el rango inicial (YYYY-MM-DD):")
        Fecha_final=input(("ingrese el rango final (YYYY-MM-DD):"))
        cantidad,mayor,severidad=controller.Accidentes_rango(Analyzer,Fecha_inical,Fecha_final)
        print("\nSe encontraron",cantidad,"accidentes registrados en el rango de fechas")
        print("La severidad con mayor cantidad de accidentes en esta fecha fue la severidad",severidad,"con un numero de",mayor,"Accidentes\n")
    
    elif int(inputs[0]) == 5:
        Hora_inicla=input("Ingrese la hora inical (HH:MM):")
        Hora_final=input("Ingrese la hora final (HH:MM):")
        total,Diccionario,porcentaje=controller.Accidentes_Hora(Analyzer,Hora_inicla,Hora_final)
        print("Hay un numero de",total,"accidentes en este rango de horas")
        print(Diccionario["1"],"de severidad 1")
        print(Diccionario["2"],"de severidad 2")
        print(Diccionario["3"],"de severidad 3")
        print(Diccionario["4"],"de severidad 4")
        print("Este numero de accidentes equivalen a el",str(porcentaje)+"%","de los accidentes." )
    
    elif int(inputs[0]) == 6:
        lat=input("Ingrese la latitud:")
        longi=input("Ingrese la longitud:")
        medida_rad=input("Indique la unidad de medida del radio (M (millas), Kl (kilometros)):")
        radio=input("Ingrese la medida del radio:")
        Diccionario,total=controller.Accidentes_en_radio(Analyzer,lat,longi,radio,medida_rad)
        print("El total de los acidentes a la redonda de el punto es",total)
        for key,value in Diccionario.items():
            print("En la fecha",key,"se encontraron",value,"accidentes")
    else:
        sys.exit(0)
sys.exit(0)
