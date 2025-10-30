from experta import *


class CausaProbableFact(Fact):
    """Hecho con la causa probable detectada en el nivel anterior."""
    descripcion = Field(str, mandatory=True)


class Recomendacion(Fact):
    """Hecho de salida: recomendación de acción."""
    descripcion = Field(str, mandatory=True)


class MotorRecomendaciones(KnowledgeEngine):


    @Rule(CausaProbableFact(descripcion=MATCH.causa),
          TEST(lambda causa: "protección de gas insuficiente" in causa.lower()))
    def ajuste_gas(self):
        mensaje = ("Verificar conexiones de gas, ajustar flujo, "
                   "cambiar mangueras dañadas, verificar que el gas no esté contaminado")
        self.declare(Recomendacion(descripcion=mensaje))
        print(f"Recomendación: {mensaje}")


    @Rule(CausaProbableFact(descripcion=MATCH.causa),
          TEST(lambda causa: "contaminación de superficie" in causa.lower()))
    def limpieza_secado(self):
        mensaje = "Limpiar superficie con cepillo de acero, secar material antes de soldar"
        self.declare(Recomendacion(descripcion=mensaje))
        print(f"Recomendación: {mensaje}")


    @Rule(CausaProbableFact(descripcion=MATCH.causa),
          TEST(lambda causa: "configuración de junta" in causa.lower()))
    def revision_junta(self):
        mensaje = "Revisar plano de junta, alineación y planificar soldadura conforme norma"
        self.declare(Recomendacion(descripcion=mensaje))
        print(f"Recomendación: {mensaje}")
