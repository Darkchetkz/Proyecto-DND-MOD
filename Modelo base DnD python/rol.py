import random

# Definición de la clase Personaje
class Personaje:
    def __init__(self, nombre, clase, fuerza, destreza, constitucion, inteligencia, sabiduria, carisma):
        self.nombre = nombre
        self.clase = clase
        self.fuerza = fuerza
        self.destreza = destreza
        self.constitucion = constitucion
        self.inteligencia = inteligencia
        self.sabiduria = sabiduria
        self.carisma = carisma
        self.vida_maxima = 10 + self.modificador(constitucion)
        self.vida_actual = self.vida_maxima
        self.bolsa = []  # Bolsa de objetos del jugador
        self.ataque_extra = 0  # Bonus de ataque por objetos
        self.invisible = False  # Estado de invisibilidad
        self.equipado = None  # Objeto equipado

    def modificador(self, atributo):
        return (atributo - 10) // 2

    def iniciativa(self):
        return self.tirar_dado(20) + self.modificador(self.destreza)

    def atacar(self):
        return self.tirar_dado(20) + self.modificador(self.fuerza) + self.ataque_extra

    def defenderse(self):
        return self.tirar_dado(20) + self.modificador(self.destreza)

    def recibir_dano(self, dano):
        self.vida_actual -= dano
        if self.vida_actual < 0:
            self.vida_actual = 0

    def esta_vivo(self):
        return self.vida_actual > 0

    def ver_bolsa(self):
        if self.bolsa:
            print(f"Bolsa de {self.nombre}: {', '.join(self.bolsa)}")
        else:
            print(f"{self.nombre} no tiene objetos en su bolsa.")

    def agregar_objeto(self, objeto):
        self.bolsa.append(objeto)
        print(f"{self.nombre} ha recibido un {objeto}.")

    def usar_objeto(self, objeto):
        if objeto == "Espada":
            self.equipado = "Espada"
            self.ataque_extra += 2
            print(f"{self.nombre} se ha equipado una Espada. ¡Ataque aumentado en 2!")
        elif objeto == "Poción de Vida":
            self.vida_actual = min(self.vida_maxima, self.vida_actual + 10)
            print(f"{self.nombre} usa una Poción de Vida. ¡Vida recuperada en 10 puntos!")
        elif objeto == "Poción de Invisibilidad":
            self.invisible = True
            print(f"{self.nombre} usa una Poción de Invisibilidad. ¡Ahora está invisible!")
        self.bolsa.remove(objeto)

    def tirar_dado(self, caras):
        resultado = random.randint(1, caras)
        print(f"{self.nombre} tira un dado de {caras} caras y saca un {resultado}.")
        return resultado

    def __str__(self):
        return f"{self.nombre} ({self.clase}) - Vida: {self.vida_actual}/{self.vida_maxima}"

# Definición de la clase Enemigo
class Enemigo:
    def __init__(self, nombre, fuerza, destreza, constitucion):
        self.nombre = nombre
        self.fuerza = fuerza
        self.destreza = destreza
        self.constitucion = constitucion
        self.vida_maxima = 10 + self.modificador(constitucion)
        self.vida_actual = self.vida_maxima

    def modificador(self, atributo):
        return (atributo - 10) // 2

    def iniciativa(self):
        return self.tirar_dado(20) + self.modificador(self.destreza)

    def atacar(self):
        return self.tirar_dado(20) + self.modificador(self.fuerza)

    def defenderse(self):
        return self.tirar_dado(20) + self.modificador(self.destreza)

    def recibir_dano(self, dano):
        self.vida_actual -= dano
        if self.vida_actual < 0:
            self.vida_actual = 0

    def esta_vivo(self):
        return self.vida_actual > 0

    def tirar_dado(self, caras):
        resultado = random.randint(1, caras)
        print(f"{self.nombre} tira un dado de {caras} caras y saca un {resultado}.")
        return resultado

    def __str__(self):
        return f"{self.nombre} - Vida: {self.vida_actual}/{self.vida_maxima}"

# Definición de la clase DungeonMaster
class DungeonMaster:
    def __init__(self):
        self.jugadores = []
        self.enemigos = []
        self.objetos_disponibles = {"E": "Espada", "V": "Poción de Vida", "I": "Poción de Invisibilidad"}

    def agregar_jugador(self, jugador):
        self.jugadores.append(jugador)

    def agregar_enemigo(self, enemigo):
        self.enemigos.append(enemigo)

    def determinar_orden_turnos(self):
        participantes = self.jugadores + self.enemigos
        participantes.sort(key=lambda x: x.iniciativa(), reverse=True)
        print("\nOrden de los turnos basado en la iniciativa:")
        for i, participante in enumerate(participantes):
            print(f"{i + 1}: {participante.nombre} (Iniciativa: {participante.iniciativa()})")
        return participantes

    def combate(self):
        print("¡Comienza el combate!")
        orden_turnos = self.determinar_orden_turnos()
        while any(jugador.esta_vivo() for jugador in self.jugadores) and any(enemigo.esta_vivo() for enemigo in self.enemigos):
            for participante in orden_turnos:
                if participante.esta_vivo():
                    print(f"\nTurno de {participante.nombre}:")
                    if participante in self.jugadores:
                        self.menu_jugador(participante)
                    else:
                        jugadores_vivos = [j for j in self.jugadores if j.esta_vivo()]
                        if not jugadores_vivos:
                            print("¡Todos los jugadores han sido derrotados!")
                            return
                        objetivo = random.choice(jugadores_vivos)
                        if objetivo.invisible:
                            print(f"{objetivo.nombre} está invisible y no puede ser atacado.")
                        else:
                            print(f"{participante.nombre} ataca a {objetivo.nombre}!")
                            ataque = participante.atacar()
                            defensa = objetivo.defenderse()
                            print(f"{objetivo.nombre} se defiende con un {defensa}.")
                            if ataque > defensa:
                                print(f"¡El ataque de {participante.nombre} supera la defensa de {objetivo.nombre}!")
                                self.dm_decide_intervencion(objetivo, participante)
                            else:
                                print(f"¡El ataque de {participante.nombre} no supera la defensa de {objetivo.nombre}!")
                    print(participante)
                    if participante in self.jugadores:
                        for enemigo in self.enemigos:
                            print(enemigo)
                    input("Presiona Enter para continuar...")

        if any(jugador.esta_vivo() for jugador in self.jugadores):
            print("¡Los jugadores han ganado el combate!")
        else:
            print("¡Los enemigos han ganado el combate!")

    def dm_decide_intervencion(self, objetivo, atacante):
        # El DM decide si un aliado interviene para defender
        print(f"El ataque de {atacante.nombre} ha superado la defensa de {objetivo.nombre}.")
        decision = input("DM, ¿quieres que un aliado intervenga para defender? (s/n): ").lower()
        if decision == "s":
            if atacante in self.jugadores:
                aliados = [e for e in self.enemigos if e.esta_vivo() and e != objetivo]
            else:
                aliados = [j for j in self.jugadores if j.esta_vivo() and j != objetivo]
            if not aliados:
                print("No hay aliados disponibles para intervenir.")
                self.aplicar_dano(objetivo)
                return
            print("Aliados disponibles para intervenir:")
            for i, aliado in enumerate(aliados):
                print(f"{i + 1}: {aliado.nombre}")
            opcion = input("DM, elige el número del aliado que interviene: ")
            try:
                indice = int(opcion) - 1
                if 0 <= indice < len(aliados):
                    aliado = aliados[indice]
                    print(f"{aliado.nombre} intenta intervenir para evitar el daño.")
                    resultado_intervencion = aliado.tirar_dado(20)
                    if resultado_intervencion >= 10:
                        print(f"¡{aliado.nombre} ha evitado el daño!")
                    else:
                        print(f"¡{aliado.nombre} no ha podido evitar el daño!")
                        self.aplicar_dano(objetivo)
                else:
                    print("Número de aliado no válido.")
                    self.aplicar_dano(objetivo)
            except ValueError:
                print("Entrada no válida. Ingresa un número.")
                self.aplicar_dano(objetivo)
        else:
            print("El DM decide no intervenir.")
            self.aplicar_dano(objetivo)

    def aplicar_dano(self, objetivo):
        opcion_dano = input("¿Quieres ingresar el daño manualmente o calcularlo automáticamente? (m/a): ").lower()
        if opcion_dano == "m":
            dano = int(input("Ingresa la cantidad de daño: "))
            objetivo.recibir_dano(dano)
            print(f"{objetivo.nombre} recibe {dano} de daño.")
        else:
            dano = random.randint(1, 6) + self.modificador_fuerza(objetivo)
            objetivo.recibir_dano(dano)
            print(f"{objetivo.nombre} recibe {dano} de daño.")

    def modificador_fuerza(self, objetivo):
        return (objetivo.fuerza - 10) // 2

    def menu_jugador(self, jugador):
        while True:
            accion = input(f"{jugador.nombre}, ¿qué deseas hacer? (a: atacar, b: ver bolsa, u: usar objeto): ").lower()
            if accion == "a":
                if jugador.invisible:
                    jugador.invisible = False
                    print(f"{jugador.nombre} ya no está invisible.")
                enemigos_vivos = [e for e in self.enemigos if e.esta_vivo()]
                if not enemigos_vivos:
                    print("¡Todos los enemigos han sido derrotados!")
                    return
                objetivo = random.choice(enemigos_vivos)
                print(f"{jugador.nombre} ataca a {objetivo.nombre}!")
                ataque = jugador.atacar()
                defensa = objetivo.defenderse()
                print(f"{objetivo.nombre} se defiende con un {defensa}.")
                if ataque > defensa:
                    print(f"¡El ataque de {jugador.nombre} supera la defensa de {objetivo.nombre}!")
                    self.dm_decide_intervencion(objetivo, jugador)
                else:
                    print(f"¡El ataque de {jugador.nombre} no supera la defensa de {objetivo.nombre}!")
                break
            elif accion == "b":
                jugador.ver_bolsa()
            elif accion == "u":
                if jugador.bolsa:
                    print("Objetos en la bolsa:")
                    for i, objeto in enumerate(jugador.bolsa):
                        print(f"{i + 1}: {objeto}")
                    opcion = input("Elige el número del objeto que quieres usar: ")
                    try:
                        indice = int(opcion) - 1
                        if 0 <= indice < len(jugador.bolsa):
                            jugador.usar_objeto(jugador.bolsa[indice])
                        else:
                            print("Número de objeto no válido.")
                    except ValueError:
                        print("Entrada no válida. Ingresa un número.")
                else:
                    print("No tienes objetos en tu bolsa.")
                break
            else:
                print("Acción no válida. Usa 'a', 'b' o 'u'.")

    def dar_objeto(self, jugador):
        while True:
            print("Objetos disponibles:")
            for key, value in self.objetos_disponibles.items():
                print(f"{key}: {value}")
            opcion = input("Elige el objeto que quieres dar (E, V, I) o 's' para salir: ").upper()
            if opcion == "S":
                break
            elif opcion in self.objetos_disponibles:
                jugador.agregar_objeto(self.objetos_disponibles[opcion])
            else:
                print("Opción no válida.")

    def revivir_jugador(self, jugador):
        while True:
            try:
                vida = int(input(f"Ingresa la cantidad de vida con la que quieres revivir a {jugador.nombre}: "))
                if vida < 0:
                    print("La vida no puede ser negativa.")
                else:
                    jugador.vida_actual = min(vida, jugador.vida_maxima)
                    print(f"{jugador.nombre} ha sido revivido con {jugador.vida_actual} puntos de vida.")
                    break
            except ValueError:
                print("Entrada no válida. Ingresa un número.")

# Función principal
def main():
    print("¡Bienvenido al juego de rol!")
    dm = DungeonMaster()

    num_jugadores = int(input("¿Cuántos jugadores hay? "))
    for i in range(num_jugadores):
        print(f"\nCreando personaje {i + 1}:")
        nombre = input("Nombre: ")
        clase = input("Clase (Guerrero, Mago, Ladrón): ")
        print("Distribuye tus atributos (Fuerza, Destreza, Constitución, Inteligencia, Sabiduría, Carisma).")
        fuerza = int(input("Fuerza: "))
        destreza = int(input("Destreza: "))
        constitucion = int(input("Constitución: "))
        inteligencia = int(input("Inteligencia: "))
        sabiduria = int(input("Sabiduría: "))
        carisma = int(input("Carisma: "))
        jugador = Personaje(nombre, clase, fuerza, destreza, constitucion, inteligencia, sabiduria, carisma)
        dm.agregar_jugador(jugador)

    num_enemigos = int(input("¿Cuántos enemigos hay? "))
    for i in range(num_enemigos):
        nombre = f"Enemigo {i + 1}"
        fuerza = random.randint(8, 12)
        destreza = random.randint(8, 12)
        constitucion = random.randint(8, 12)
        enemigo = Enemigo(nombre, fuerza, destreza, constitucion)
        dm.agregar_enemigo(enemigo)

    print("\n¡Comienza la aventura!")
    while True:
        accion_dm = input("\nDM, ¿qué deseas hacer? (d: dar objeto, c: comenzar combate, r: revivir jugador, s: salir): ").lower()
        if accion_dm == "d":
            jugador_index = int(input("¿A qué jugador quieres darle un objeto? (ingresa el número): ")) - 1
            dm.dar_objeto(dm.jugadores[jugador_index])
        elif accion_dm == "c":
            dm.combate()
        elif accion_dm == "r":
            jugador_index = int(input("¿A qué jugador quieres revivir? (ingresa el número): ")) - 1
            dm.revivir_jugador(dm.jugadores[jugador_index])
        elif accion_dm == "s":
            print("¡Gracias por jugar!")
            break
        else:
            print("Acción no válida. Usa 'd', 'c', 'r' o 's'.")

if __name__ == "__main__":
    main()