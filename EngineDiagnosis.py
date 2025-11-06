from experta import *

class InspeccionFact(Fact):
    tipo_defecto = Field(str, mandatory=True)
    R = Field(float, mandatory=True)
    confianza = Field(float, mandatory=True)
    multiples_defectos = Field(bool, mandatory=True)

class Diagnostico(Fact):
    descripcion = Field(str, mandatory=True)

class MotorDiagnostico(KnowledgeEngine):

    @Rule(InspeccionFact(tipo_defecto="porosidad", R=P(lambda r: r >= 0.6)))
    def porosidad_critica(self):
        mensaje = "Porosidad crítica detectada: riesgo de poros internos / atrapamiento de gas"
        self.declare(Diagnostico(descripcion=mensaje))
        print(mensaje)

    @Rule(InspeccionFact(tipo_defecto="discontinuidades", R=P(lambda r: 0.1 < r < 0.6)))
    def discontinuidad_moderada(self):
        mensaje = "Discontinuidad moderada: falta de fusión"
        self.declare(Diagnostico(descripcion=mensaje))
        print(mensaje)

    @Rule(InspeccionFact(tipo_defecto="manchas", confianza=P(lambda c: c >= 0.6)))
    def manchas_superficiales(self):
        mensaje = "Contaminación superficial detectada"
        self.declare(Diagnostico(descripcion=mensaje))
        print(mensaje)

    @Rule(InspeccionFact(multiples_defectos=True))
    def multiples_defectos(self):
        mensaje = "Múltiples defectos detectados: revisar proceso completo de soldadura"
        self.declare(Diagnostico(descripcion=mensaje))
        print(mensaje)
