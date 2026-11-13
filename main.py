"""
Generador de Árboles de Derivación
Temática 24: Configuración de Infraestructura Virtual
Estudiante: Juan Pablo López Buitrago
"""

import sys
class Nodo:
    def __init__(self, simbolo):
        self.simbolo = simbolo
        self.hijos = []

    def imprimir_arbol(self, nivel=0):
        # Estilo de líneas jerárquicas limpias tipo árbol sintáctico
        conector = "└── " if nivel > 0 else ""
        indent = "    " * (nivel - 1) + conector if nivel > 0 else ""
        print(f"{indent}{self.simbolo}")
        for hijo in self.hijos:
            hijo.imprimir_arbol(nivel + 1)

def cargar_gramatica(ruta_archivo):
    producciones = {}
    simbolo_inicial = None
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        for linea in f:
            linea = linea.strip()
            if not linea or linea.startswith('#'):
                continue
            if '->' not in linea:
                continue
            izq, der = linea.split('->')
            izq = izq.strip()
            if simbolo_inicial is None:
                simbolo_inicial = izq
            alternativas = der.split('|')
            if izq not in producciones:
                producciones[izq] = []
            for alt in alternativas:
                simbolos_alt = alt.strip().split()
                producciones[izq].append(simbolos_alt)
    return simbolo_inicial, producciones

def cargar_derivacion(ruta_archivo):
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        lineas = [l.strip() for l in f if l.strip() and not l.startswith('#')]
    modo = lineas[0].lower()
    pasos = lineas[1:]
    return modo, pasos

def simular_derivacion(simbolo_inicial, producciones, modo, pasos):
    no_terminales = set(producciones.keys())
    raiz = Nodo(simbolo_inicial)
    frontera = [raiz]

    for i, regla_str in enumerate(pasos):
        if '->' in regla_str:
            izq, der = regla_str.split('->')
            der_simbolos = der.strip().split()
        else:
            der_simbolos = regla_str.split()

        nodo_a_expandir = None
        indice_a_expandir = -1

        if modo == 'izquierda':
            for idx, nodo in enumerate(frontera):
                if nodo.simbolo in no_terminales:
                    nodo_a_expandir = nodo
                    indice_a_expandir = idx
                    break
        elif modo == 'derecha':
            for idx in range(len(frontera) - 1, -1, -1):
                if frontera[idx].simbolo in no_terminales:
                    nodo_a_expandir = frontera[idx]
                    indice_a_expandir = idx
                    break

        if not nodo_a_expandir:
            return None

        nuevos_hijos = [Nodo(s) for s in der_simbolos]
        nodo_a_expandir.hijos = nuevos_hijos
        frontera[indice_a_expandir:indice_a_expandir+1] = nuevos_hijos

    return raiz

def extraer_cadena(nodo):
    if not nodo.hijos:
        return [nodo.simbolo]
    cadena = []
    for hijo in nodo.hijos:
        cadena.extend(extraer_cadena(hijo))
    return cadena

def main():
    archivo_gramatica = sys.argv[1] if len(sys.argv) >= 3 else "gramatica.txt"
    archivo_derivacion = sys.argv[2] if len(sys.argv) >= 3 else "derivacion_w1.txt"

    simbolo_inicial, producciones = cargar_gramatica(archivo_gramatica)
    modo, pasos = cargar_derivacion(archivo_derivacion)

    raiz = simular_derivacion(simbolo_inicial, producciones, modo, pasos)

    if raiz:
        print("=== ÁRBOL DE DERIVACIÓN (ESTILO SINTÁCTICO) ===")
        raiz.imprimir_arbol()

        cadena_tokens = extraer_cadena(raiz)
        print("\n=== CADENA OBTENIDA ===")
        print(" ".join(cadena_tokens))

if __name__ == "__main__":
    main()