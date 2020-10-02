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