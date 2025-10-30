from experta import *

class ProcesoFact(Fact):
    flujo_gas = Field(float, mandatory=True)

class InspeccionFact(Fact):
    R = Field(float, mandatory=True)

class Clasificacion(KnowledgeEngine):

    @Rule(ProcesoFact(flujo_gas=P(lambda x: x < 5)))
    def flujo_bajo(self):
        print("Clasificación: flujo de gas BAJO (<5 L/min)")

    @Rule(ProcesoFact(flujo_gas=P(lambda x: x > 19)))
    def flujo_alto(self):
        print("Clasificación: flujo de gas ALTO (>19 L/min)")

    @Rule(ProcesoFact(flujo_gas=P(lambda x: 5 <= x <= 19)))
    def flujo_normal(self):
        print("Clasificación: flujo de gas NORMAL (5–19 L/min)")

    @Rule(InspeccionFact(R=P(lambda x: x <= 0.1)))
    def defecto_leve(self):
        print("Clasificación: defecto LEVE (R ≤ 0.1)")

    @Rule(InspeccionFact(R=P(lambda x: 0.1 < x < 0.6)))
    def defecto_moderado(self):
        print("Clasificación: defecto MODERADO (0.1 < R < 0.6)")

    @Rule(InspeccionFact(R=P(lambda x: x >= 0.6)))
    def defecto_critico(self):
        print("Clasificación: defecto CRÍTICO (R ≥ 0.6)")
