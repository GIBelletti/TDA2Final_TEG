import random

PROPIETARIOS_COLORES = ["Negro", "Rojo", "Amarillo", "Verde", "Azul", "Magenta"]
PAISES_A_REPARTIR = 50

def obtener_orden_de_turnos_de_jugadores(cantidad_de_jugadores=6):
    posibles = PROPIETARIOS_COLORES[:cantidad_de_jugadores]
    random.shuffle(posibles)
    return posibles

def obtener_orden_de_propietarios(cantidad_de_jugadores=6):
    """Retorna una lista de 50 valores uniformememente distribuidos segun la cantidad de jugadores.
    En el caso de que no sea posible dar una distribucion uniforme se usara las reglas del TEG
    para seleccionar los restantes."""
    resultado = []
    cantidad_otorgada = {}
    limite = PAISES_A_REPARTIR // cantidad_de_jugadores
    sobrante = PAISES_A_REPARTIR % cantidad_de_jugadores
    restantes = PAISES_A_REPARTIR - sobrante
    for jugador in PROPIETARIOS_COLORES:
        cantidad_otorgada[jugador] = 0
    while restantes > 0:
        jugador = PROPIETARIOS_COLORES[random.randint(0, 5)]
        if cantidad_otorgada[jugador] == limite:
            continue
        resultado.append(jugador)
        cantidad_otorgada[jugador] += 1
        restantes -= 1
    # while sobrante > 0:
    #     posibles_jugadores = obtener_jugadores_con_menos_paises(cantidad_otorgada,
    #                                                             PROPIETARIOS_COLORES[:cantidad_de_jugadores - 1])
    #     nuevo_propietario = obtener_desenpate_por_mayor_dado(posibles_jugadores)
    #     resultado.append(nuevo_propietario)
    #     cantidad_otorgada[nuevo_propietario] += 1
    #     sobrante -= 1

    posibles_jugadores = obtener_jugadores_con_menos_paises(cantidad_otorgada,
                                                            PROPIETARIOS_COLORES[:cantidad_de_jugadores - 1])
    resultado += obtener_desenpate_por_mayor_dado(posibles_jugadores)
    return resultado


def obtener_jugadores_con_menos_paises(cantidad_otorgada, jugadores):
    resultado = []
    minimo = 50
    for jugador in jugadores:
        cantidad = cantidad_otorgada[jugador]
        if cantidad < minimo:
            resultado = []
            minimo = cantidad_otorgada[jugador]
            resultado.append(jugador)
        elif cantidad == minimo:
            resultado.append(jugador)
    return resultado


def obtener_desenpate_por_mayor_dado(jugadores):
    """Siguiendo las reglas del TEG genera un desenpate por los 2 paises restantes"""
    valores = {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
    maximo = 0
    for jugador in jugadores:
        valor_dado = random.randint(1, 6)
        valores[valor_dado].append(jugador)
        if maximo < valor_dado:
            maximo = valor_dado
    mejores = valores[maximo]
    while len(mejores) < 2:
        maximo -= 1
        mejores += valores[maximo]
    if len(mejores) == 2:
        return mejores
    return obtener_desenpate_por_mayor_dado(mejores)

class Propietario_TEG:
    def __init__(self, propietario):
        self.propietario = propietario
        self.ejercitos = 1

    def propietario(self):
        return self.propietario

    def defender(self, atacante):
        """Retorna True si se logro defender, False si cambio de propietario"""
        cantidad_ejercito = atacante.ejercitos_de_ofensiva()
        bajas = self._combate(cantidad_ejercito)
        atacante.desplazar(bajas)
        if self.ejercitos == 0:
            self.propietario = atacante.propietario()
            self.ejercitos = cantidad_ejercito - bajas
            atacante.desplazar(self.ejercitos)
            return False
        return True

    def reforzar(self, cantidad):
        self.ejercitos += cantidad

    def desplazar(self, cantidad):
        self.ejercitos -= cantidad

    def _combate(self, cant_atacantes):
        bajas_atacantes = 0
        dados_defensor = []
        for i in range(self.ejercitos):
            dados_defensor.append(random.randint(1, 6))
        dados_atacante = []
        for i in range(cant_atacantes):
            dados_atacante.append(random.randint(1, 6))
        dados_defensor.sort(reverse=True)
        dados_atacante.sort(reverse=True)
        combatientes = min(len(dados_atacante), len(dados_defensor))
        for combate in combatientes:
            if dados_defensor[combate] < dados_atacante:
                self.ejercitos -= 1
            else:
                bajas_atacantes += 1
        return bajas_atacantes

    def puede_atacar(self):
        return self.ejercitos > 1

    def ejercitos_de_ofensiva(self):
        atacantes = self.ejercitos - 1
        if atacantes > 3:
            atacantes = 3
        return atacantes

    def es_limitrofe(self, otro):
        return otro.propietario() != self.propietario
