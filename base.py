#Base
#Datos de entrada del modelo entrenado
class DatosInspeccion:
   
    def __init__(self, tipo_defecto, tamaño_relativo, confianza, multiples_defectos):
        self.tipo_defecto = tipo_defecto
        self.tamaño_relativo = tamaño_relativo
        self.confianza = confianza
        self.multiples_defectos = multiples_defectos

    def __str__(self):
        return (f"Defecto: {self.tipo_defecto}, Tamaño: {self.tamaño_relativo}, "
                f"Confianza: {self.confianza}, Múltiples defectos: {self.multiples_defectos}")

#Datos de proceso ingresados por el usuario/registro de soldadura
class DatosProceso:
    def __init__(self, tipo_gas, flujo_gas_l_min, material_base, tipo_junta, metodo_soldadura):
        self.tipo_gas = tipo_gas
        self.flujo_gas_l_min = flujo_gas_l_min
        self.material_base = material_base
        self.tipo_junta = tipo_junta
        self.metodo_soldadura = metodo_soldadura

    def __str__(self):
        return (f"Gas: {self.tipo_gas}, Flujo: {self.flujo_gas_l_min} L/min, "
                f"Material: {self.material_base}, Junta: {self.tipo_junta}, "
                f"Método: {self.metodo_soldadura}")


class Soldadura:
    def __init__(self, id_soldadura, inspeccion=None, proceso=None):
        self.id_soldadura = id_soldadura
        self.inspeccion = inspeccion
        self.proceso = proceso

    def __str__(self):
        return (f"Soldadura ID: {self.id_soldadura}\n"
                f"  {self.inspeccion}\n"
                f"  {self.proceso}")   
    
#----------------------------------------------------------------------------------
# sistema_calculos.py

def calcular_tamaño_relativo(x_min, y_min, x_max, y_max, area_soldadura):
    """
    Calcula el tamaño relativo del defecto (R) respecto al área total de la soldadura.
    
    Parámetros:
        x_min, y_min, x_max, y_max (float): coordenadas del bounding box del defecto.
        area_soldadura (float): área total de la región de soldadura (en píxeles o mm², según corresponda).
    
    Retorna:
        float: valor de R = área_defecto / área_soldadura.
    """
    if area_soldadura <= 0:
        raise ValueError("El área de la soldadura debe ser mayor que cero.")

    ancho_defecto = x_max - x_min
    alto_defecto = y_max - y_min

    if ancho_defecto <= 0 or alto_defecto <= 0:
        raise ValueError("Las coordenadas del bounding box no son válidas.")

    area_defecto = ancho_defecto * alto_defecto
    R = area_defecto / area_soldadura

    return R





