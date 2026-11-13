import sys
import os

class Nodo:
    def __init__(self, simbolo):
        self.simbolo = simbolo
        self.hijos = []

    def imprimir_arbol(self, nivel=0):
        indent = "  " * nivel
        print(f"{indent}- {self.simbolo}")
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
    modo = lineas[0].lower()  # 'izquierda' o 'derecha'
    pasos = lineas[1:]
    return modo, pasos

def es_no_terminal(simbolo, no_terminales):
    return simbolo in no_terminales

def simular_derivacion(simbolo_inicial, producciones, modo, pasos):
    no_terminales = set(producciones.keys())
    raiz = Nodo(simbolo_inicial)
    frontera = [raiz]

    print(f"--- Iniciando simulación (Modo: {modo}) ---")

    for i, regla_str in enumerate(pasos):
        if '->' in regla_str:
            izq, der = regla_str.split('->')
            izq = izq.strip()
            der_simbolos = der.strip().split()
        else:
            der_simbolos = regla_str.split()
            izq = None

        nodo_a_expandir = None
        indice_a_expandir = -1

        if modo == 'izquierda':
            for idx, nodo in enumerate(frontera):
                if es_no_terminal(nodo.simbolo, no_terminales):
                    nodo_a_expandir = nodo
                    indice_a_expandir = idx
                    break
        elif modo == 'derecha':
            for idx in range(len(frontera) - 1, -1, -1):
                if es_no_terminal(frontera[idx].simbolo, no_terminales):
                    nodo_a_expandir = frontera[idx]
                    indice_a_expandir = idx
                    break

        if not nodo_a_expandir:
            print(f"Error en paso {i+1}: No se encontró ningún no terminal para expandir en la frontera.")
            return None

        simbolo_nt = nodo_a_expandir.simbolo
        simbolos_expansion = der_simbolos

        nuevos_hijos = [Nodo(s) for s in simbolos_expansion]
        nodo_a_expandir.hijos = nuevos_hijos
        frontera[indice_a_expandir:indice_a_expandir+1] = nuevos_hijos

        sentencial_actual = " ".join([n.simbolo for n in frontera])
        print(f"Paso {i+1} ({simbolo_nt} -> {' '.join(simbolos_expansion)}): {sentencial_actual}")

    restantes = [n.simbolo for n in frontera if es_no_terminal(n.simbolo, no_terminales)]
    if restantes:
        print(f"Advertencia: Aún quedan no terminales sin expandir: {restantes}")
    else:
        print("¡Derivación completada con éxito!")

    return raiz

def extraer_cadena(nodo):
    if not nodo.hijos:
        return [nodo.simbolo]
    cadena = []
    for hijo in nodo.hijos:
        cadena.extend(extraer_cadena(hijo))
    return cadena

def main():
    if len(sys.argv) >= 3:
        archivo_gramatica = sys.argv[1]
        archivo_derivacion = sys.argv[2]
    else:
        archivo_gramatica = "gramatica.txt"
        archivo_derivacion = "derivacion_w1.txt"
        print(f"Usando archivos por defecto: {archivo_gramatica} y {archivo_derivacion}\n")

    if not os.path.exists(archivo_gramatica) or not os.path.exists(archivo_derivacion):
        print(f"Error: No se encuentran los archivos '{archivo_gramatica}' o '{archivo_derivacion}'.")
        return

    simbolo_inicial, producciones = cargar_gramatica(archivo_gramatica)
    modo, pasos = cargar_derivacion(archivo_derivacion)

    raiz = simular_derivacion(simbolo_inicial, producciones, modo, pasos)

    if raiz:
        print("\n=== ÁRBOL DE DERIVACIÓN JERÁRQUICO ===")
        raiz.imprimir_arbol()

        cadena_tokens = extraer_cadena(raiz)
        print("\n=== CADENA OBTENIDA ===")
        print(" ".join(cadena_tokens))

if __name__ == "__main__":
    main()