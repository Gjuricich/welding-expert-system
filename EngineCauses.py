from experta import *


class DiagnosticoFact(Fact):
    """Hecho con el diagnóstico generado en el nivel anterior."""
    descripcion = Field(str, mandatory=True)

class ProcesoFact(Fact):
    """Hecho con los datos del proceso de soldadura."""
    flujo_gas = Field(float, mandatory=True)
    material_base = Field(str, mandatory=True)
    tipo_junta = Field(str, mandatory=True)


class CausaProbable(Fact):
    """Hecho de salida: causa probable inferida."""
    descripcion = Field(str, mandatory=True)


class MotorCausas(KnowledgeEngine):


    @Rule(
        DiagnosticoFact(descripcion=MATCH.desc),
        ProcesoFact(flujo_gas=MATCH.flujo_gas),
        TEST(lambda desc, flujo_gas: desc.lower().startswith("porosidad") and flujo_gas < 5)
    )
    def proteccion_gas_insuficiente(self):
        mensaje = "Protección de gas insuficiente o gas contaminado"
        self.declare(CausaProbable(descripcion=mensaje))
        print(f"Causa probable: {mensaje}")


    @Rule(
        DiagnosticoFact(descripcion=MATCH.desc),
        ProcesoFact(material_base=MATCH.material),
        TEST(lambda desc, material: desc.lower().startswith("discontinuidad") and material.lower() == "acero inoxidable")
    )
    def contaminacion_superficie(self):
        mensaje = "Contaminación de superficie o humedades residuales"
        self.declare(CausaProbable(descripcion=mensaje))
        print(f"Causa probable: {mensaje}")


    @Rule(
        DiagnosticoFact(descripcion=MATCH.desc),
        ProcesoFact(tipo_junta=MATCH.junta),
        TEST(lambda desc, junta: "múltiples defectos detectados" in desc.lower() and junta.lower() == "v-groove")
    )
    def preparacion_junta_inadecuada(self):
        mensaje = "Configuración de junta o preparación de ranura inadecuada"
        self.declare(CausaProbable(descripcion=mensaje))
        print(f"Causa probable: {mensaje}")
