from EngineClasification import Clasificacion, ProcesoFact, InspeccionFact as InspeccionFactClasif
from EngineDiagnosis import MotorDiagnostico, InspeccionFact as InspeccionFactDiag, Diagnostico
from EngineCauses import MotorCausas, DiagnosticoFact, ProcesoFact as ProcesoFactCausa, CausaProbable
from EngineRecomendations import MotorRecomendaciones, CausaProbableFact
from base import DatosInspeccion, DatosProceso, Soldadura, calcular_tamaño_relativo


def main():
    print("=== Sistema Experto de Diagnóstico de Soldadura ===")

    # ----- Datos hardcodeados del proceso -----
    tipo_gas = "Argón"
    flujo_gas = 12.5
    material_base = "Acero inoxidable"
    tipo_junta = "V-groove"
    metodo_soldadura = "GTAW"

    datos_proceso = DatosProceso(
        tipo_gas=tipo_gas,
        flujo_gas_l_min=flujo_gas,
        material_base=material_base,
        tipo_junta=tipo_junta,
        metodo_soldadura=metodo_soldadura
    )

    # ----- Datos hardcodeados de inspección -----
    tipo_defecto = "porosidad"
    x_min, y_min = 10, 20
    x_max, y_max = 80, 120
    area_soldadura = 10000
    confianza = 0.92
    multiples_defectos = False
    
    # ----- Preprocesamiento de R con datos de Boxplotting -----
    R = calcular_tamaño_relativo(x_min, y_min, x_max, y_max, area_soldadura)

    datos_inspeccion = DatosInspeccion(
        tipo_defecto=tipo_defecto,
        tamaño_relativo=R,
        confianza=confianza,
        multiples_defectos=multiples_defectos
    )

    soldadura = Soldadura(id_soldadura="S001", inspeccion=datos_inspeccion, proceso=datos_proceso)

    print("\n=== Datos de entrada ===")
    print(soldadura)

    # --- Lista de mensajes y nivel alcanzado ---
    mensajes = []
    nivel_alcanzado = None

    # ----- Nivel 0: Clasificación -----
    motor_clasif = Clasificacion()
    motor_clasif.reset()
    motor_clasif.declare(ProcesoFact(flujo_gas=flujo_gas))
    motor_clasif.declare(InspeccionFactClasif(R=R))
    motor_clasif.run()

    for fact in motor_clasif.facts.values():
        if "clasificacion" in str(type(fact)).lower():
            mensajes.append(f"Clasificación: {fact}")
            nivel_alcanzado = "Clasificación"

    # ----- Nivel 1: Diagnóstico -----
    motor_diag = MotorDiagnostico()
    motor_diag.reset()
    motor_diag.declare(InspeccionFactDiag(
        tipo_defecto=tipo_defecto,
        R=R,
        confianza=confianza,
        multiples_defectos=multiples_defectos
    ))
    motor_diag.run()

    diag_fact = None
    for fact in motor_diag.facts.values():
        if isinstance(fact, Diagnostico):
            diag_fact = fact
            mensajes.append(f"Diagnóstico: {fact['descripcion']}")
            nivel_alcanzado = "Diagnóstico"
            break

    # ----- Nivel 2: Causa Probable -----
    causa_fact = None
    if diag_fact:
        motor_causa = MotorCausas()
        motor_causa.reset()
        motor_causa.declare(DiagnosticoFact(descripcion=diag_fact["descripcion"]))
        motor_causa.declare(ProcesoFactCausa(
            flujo_gas=flujo_gas,
            material_base=material_base,
            tipo_junta=tipo_junta
        ))
        motor_causa.run()

        for fact in motor_causa.facts.values():
            if isinstance(fact, CausaProbable):
                causa_fact = fact
                mensajes.append(f"Causa probable: {fact['descripcion']}")
                nivel_alcanzado = "Causa probable"
                break

    # ----- Nivel 3: Recomendación de acción -----
    if causa_fact:
        motor_reco = MotorRecomendaciones()
        motor_reco.reset()
        motor_reco.declare(CausaProbableFact(descripcion=causa_fact["descripcion"]))
        motor_reco.run()
        nivel_alcanzado = "Recomendación"

    # ----- Resultados finales -----
    print("\n=== RESULTADOS ===")
    if mensajes:
        for m in mensajes:
            print(f"- {m}")
        print(f"\nEl sistema llegó hasta el nivel: {nivel_alcanzado}")
    else:
        print("No se identificaron reglas aplicables con los datos ingresados.")


if __name__ == "__main__":
    main()
