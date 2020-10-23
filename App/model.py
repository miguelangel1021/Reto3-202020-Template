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
import math
import config
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as m
import datetime
assert config

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria


"""

# -----------------------------------------------------
# API del TAD Catalogo de accidentes
# -----------------------------------------------------
def inicializar_catalogo():
    catalog={"Indice_fechas":None,"Accidentes":None}
    catalog['Accidentes'] = lt.newList('SINGLE_LINKED', compareAccidentes)
    catalog['Indice_fechas'] = om.newMap(omaptype='RBT',
                                      comparefunction=compararFechas)
    return catalog

def añadirAccidente(catalog,Accidente):
    lt.addLast(catalog["Accidentes"],Accidente)
    AñadirAccidenteFecha(catalog,Accidente)
    return catalog

def AñadirAccidenteFecha(catalog,Accidente):
    Fecha = Accidente['Start_Time']
    Fecha_accidente = datetime.datetime.strptime(Fecha, '%Y-%m-%d %H:%M:%S')
    entry = om.get(catalog["Indice_fechas"], Fecha_accidente.date())
    if entry is None:
        datentry = newDataEntry()
        om.put(catalog["Indice_fechas"], Fecha_accidente.date(), datentry)
    else:
        datentry = me.getValue(entry)
    Añadir_Accidente_Tipo(datentry, Accidente)
    
    
def newDataEntry():
    
    entry = {'Severidades': None, 'Accidentes': None}
    entry['Severidades'] = m.newMap(numelements=11,
                                     maptype='PROBING',
                                     comparefunction=compararSeveridad)
   
    entry['Accidentes'] = lt.newList('SINGLE_LINKED', compareAccidentes)
    return entry

def Añadir_Accidente_Tipo(datentry,Accidente):

    Severidad_Accidentes=datentry["Severidades"]
    Lista_Acci=datentry["Accidentes"]
    lt.addLast(Lista_Acci,Accidente)
    Seventry= m.get(Severidad_Accidentes,Accidente["Severity"])
    if Seventry == None:
        Entry= NuevaSeveridad(Accidente["Severity"])
        lt.addLast(Entry["Lista_Accidentes"],Accidente)
        m.put(Severidad_Accidentes,Accidente["Severity"],Entry)
    else:
        Entry= me.getValue(Seventry)
        lt.addLast(Entry["Lista_Accidentes"],Accidente)
    return datentry

def NuevaSeveridad(Severidad):
    
    Seventry = {'Severidad': None, 'Lista_Accidentes': None}
    Seventry['Severidad'] = Severidad
    Seventry['Lista_Accidentes'] = lt.newList('SINGLELINKED', compareAccidentes)
    return Seventry


# Funciones para agregar informacion al catalogo


# ==============================
# Funciones de consulta
# ==============================
def Accidente_Fecha_severidad(catalog,fecha):
    lista= lt.newList("ARRAY_LIST")
    Key_value= om.get(catalog["Indice_fechas"],fecha)
    if Key_value != None:
        entry= me.getValue(Key_value)
        cantidad_Accidentes=lt.size(entry["Accidentes"])
        llaves= m.keySet(entry["Severidades"])
        iterador= it.newIterator(llaves)
        while it.hasNext(iterador):
            elemento= it.next(iterador)
            En=m.get(entry["Severidades"],elemento)
            valor=me.getValue(En)
            lt.addLast(lista,valor)    
   
    return cantidad_Accidentes,lista

def Accidentes_en_Rango(catalog,Fecha_inicial,Fecha_final):
    Accidentes_fechas= om.values(catalog['Indice_fechas'],Fecha_inicial,Fecha_final)
    iterador=it.newIterator(Accidentes_fechas)
    total=0
    sev1=0
    sev2=0
    sev3=0
    sev4=0
    while it.hasNext(iterador):
        elemento=it.next(iterador)
        total+=lt.size(elemento["Accidentes"])
        llaves= m.keySet(elemento["Severidades"])
        iterador2= it.newIterator(llaves)
        while it.hasNext(iterador2):
                severidad= it.next(iterador2)
                En=m.get(elemento["Severidades"],severidad)
                valor=me.getValue(En)
                if severidad == "1":
                    sev1+= lt.size(valor["Lista_Accidentes"])
                if severidad == "2":
                    sev2+= lt.size(valor["Lista_Accidentes"])
                if severidad == "3":
                    sev3+= lt.size(valor["Lista_Accidentes"])
                if severidad == "4":
                    sev4+= lt.size(valor["Lista_Accidentes"])
    mayor=sev1
    severidad_es="1"
    if sev2>mayor:
        mayor=sev2
        severidad_es="2"
    if sev3>mayor:
        mayor=sev3
        severidad_es="3"
     if sev4>mayor:
        mayor=sev4
        severidad_es="4"
    
    return total,mayor,severidad_es

def Accidentes_por_hora(catalog,horainicial,horafinal):
    Hora=horainicial.split(":")
    if int(Hora[1])<=15:
        minuto=0
        hora_=int(Hora[0])
    elif 15<int(Hora[1])<=30:
        minuto=30
        hora_=int(Hora[0])
    elif 30<int(Hora[1])<=45:
        minuto=30
        hora_=int(Hora[0])
    else:
        minuto=00
        hora_=int(Hora[0])+1
        
    
    tiempo=(hora_*60)+minuto
    
    Hora2=horafinal.split(":")
    if int(Hora2[1])<=15:
        minuto2=0
        hora_2=int(Hora2[0])
    elif 15<int(Hora2[1])<=30:
        minuto2=30
        hora_2=int(Hora2[0])
    elif 30<int(Hora2[1])<=45:
        minuto2=30
        hora_2=int(Hora2[0])
    else:
        minuto2=00
        hora_2=int(Hora2[0])+1
    tiempo2=(hora_2*60)+minuto2
    total=0
    sev1=0
    sev2=0
    sev3=0
    sev4=0
    maximo=om.maxKey(catalog['Indice_fechas'])
    minimo=om.minKey(catalog['Indice_fechas'])
    Valores= om.values(catalog['Indice_fechas'],minimo,maximo)
   
    cant_tot= lt.size(catalog['Accidentes'])
    iterador= it.newIterator(Valores)
    while it.hasNext(iterador):
        valor= it.next(iterador)
        lista=valor["Accidentes"]
        iterador2= it.newIterator(lista)
        while it.hasNext(iterador2):
            accidente=it.next(iterador2)
            Hora = accidente['Start_Time']
            Hora_accidente = datetime.datetime.strptime(Hora, '%Y-%m-%d %H:%M:%S')
            hora_del=str(Hora_accidente.time())
            lista=hora_del.split(":")
            Tiempo= (int(lista[0])*60)+int(lista[1])
            if tiempo <= Tiempo <= tiempo2 :
                total+=1
                severidad=accidente['Severity']
                if severidad == "1":
                    sev1+= 1
                if severidad == "2":
                    sev2+= 1
                if severidad == "3":
                    sev3+= 1
                if severidad == "4":
                    sev4+= 1
    Diccionario={}
    Diccionario["1"]=sev1
    Diccionario["2"]=sev2
    Diccionario["3"]=sev3
    Diccionario["4"]=sev4
    porcentaje=(total/cant_tot)*100
    return total,Diccionario,porcentaje

def Accidentes_en_radio(catalog,latitud,longitud,radio,medida_r):
    if medida_r == "M":
        radio=float(radio)*1.609
    else:
        radio=float(radio)
    Latitud=float(latitud)/ 57.29577951
    Longitud=float(longitud)/ 57.29577951
    total=0
    maximo=om.maxKey(catalog['Indice_fechas'])
    minimo=om.minKey(catalog['Indice_fechas'])
    Valores= om.values(catalog['Indice_fechas'],minimo,maximo)
    iterador= it.newIterator(Valores)
    Diccionario={}
    while it.hasNext(iterador):
        valor= it.next(iterador)
        lista=valor["Accidentes"]
        iterador2= it.newIterator(lista)
        while it.hasNext(iterador2):
            accidente=it.next(iterador2)
            latitud2=float(accidente["Start_Lat"])/57.29577951
            longitud2=float(accidente["Start_Lng"])/ 57.29577951
            distancia= 3963.0 * math.acos(math.sin(Latitud)*math.sin(latitud2)+math.cos(Latitud)*math.cos(latitud2)*math.cos(longitud2 - Longitud))
            distancia*=1.609344
            if distancia<=radio:
                total+=1
                Fecha = accidente['Start_Time']
                Fecha_accidente = datetime.datetime.strptime(Fecha, '%Y-%m-%d %H:%M:%S')
                if Fecha_accidente.date() not in Diccionario:
                    Diccionario[Fecha_accidente.date()]=0
                    Diccionario[Fecha_accidente.date()]+=1
                else:
                    Diccionario[Fecha_accidente.date()]+=1
    return Diccionario,total


def size_Arbol(catalog):

    size = om.size(catalog["Indice_fechas"])
    return size
    

def tamaño_Accidentes(catalog):
    size= lt.size(catalog["Accidentes"])
    return size

def alturA_arbol(catalog):
    altura= om.height(catalog["Indice_fechas"])
    return altura

# ==============================
# Funciones de Comparacion
# ==============================
def compararFechas(Fecha1, Fecha2):

    if (Fecha1 == Fecha2):
        return 0
    elif (Fecha1 > Fecha2):
        return 1
    else:
        return -1

def compareAccidentes (Accidenteid, Accidentes):
    if (Accidenteid == Accidentes['ID'] ):
        return 0
    else:
        return 1

def compararSeveridad(Severidad1, Severidad2):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    Severidad = me.getKey(Severidad2)
    if (Severidad1 == Severidad):
        return 0
    elif (Severidad1 > Severidad):
        return 1
    else:
        return -1