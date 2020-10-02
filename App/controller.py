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

import config as cf
from App import model
import datetime
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________


def init():
    """
    Llama la funcion de inicializacion del modelo.
    """
    catalog=model.inicializar_catalogo()
    return catalog


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def loadData(analyzer, accidentsfile):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    Archivo = cf.data_dir + accidentsfile
    input_file = csv.DictReader(open(Archivo, encoding="utf-8"),
                                delimiter=",")
    for Accidente in input_file:
        model.añadirAccidente(analyzer, Accidente)
    return analyzer

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________
def sizeArbol(analyzer):
    size=model.size_Arbol(analyzer)
    return size

def Dar_cantidad_por_fecha(catalog,Fecha):
    initialDate = datetime.datetime.strptime(Fecha, '%Y-%m-%d')
    size,lista= model.Accidente_Fecha_severidad(catalog,initialDate.date())
    return size,lista
def sizeAccidentes(catalog):
    size=model.tamaño_Accidentes(catalog)
    return size
def Altura(catalog):
    size=model.alturA_arbol(catalog)
    return size