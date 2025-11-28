# colaborativo.py
# ===============================================================
# SISTEMA COLABORATIVO BASADO EN VECTORES DE PREFERENCIAS (SIMILITUD COSENO)
# ===============================================================
# Este módulo contiene implementación y detalles pedagógicos paso a paso.
# Cada bloque de código viene acompañado de comentarios inter-bloques que
# explican la operación lineal, su finalidad y su interpretación.
# ===============================================================

import math

# -------------------------
# Producto punto (a · b)
# -------------------------
# Concepto: escalar resultado de multiplicar componente a componente y sumar.
# Uso: mide coincidencia direccional no-normalizada entre dos vectores.
def producto_punto(a, b):
    """
    PRODUCTO PUNTO (a · b)
    - Fórmula: Σ_i (a_i * b_i)
    - Significado geométrico: ||a|| ||b|| cos(θ)
    - En el recomendador: si ambos usuarios dieron alta calificación a las
      mismas películas, el producto punto será grande.
    """
    # Implementación directa: sumamos productos por coordenada.
    return sum(x * y for x, y in zip(a, b))


# -------------------------
# Norma euclidiana ||v||
# -------------------------
# Concepto: longitud del vector en R^n.
# Uso: normalizar (convertir a dirección) para comparar solo orientación.
def magnitud_vector(v):
    """
    NORMA EUCLIDIANA ||v||
    - Fórmula: sqrt(Σ_i v_i^2)
    - Uso en práctica: se combina con el producto punto para obtener cos(θ).
    """
    return math.sqrt(sum(x * x for x in v))


# -------------------------
# Similitud coseno
# -------------------------
# Concepto: coseno del ángulo entre vectores.
# Uso: compara direcciones (patrones de gustos) ignorando escala.
def similitud_coseno(a, b):
    """
    SIMILITUD COSENO
    - Fórmula: (a · b) / (||a|| * ||b||)
    - Interpretación: 1 = mismo patrón; 0 = ortogonales; -1 = opuestos.
    - Por qué útil: si un usuario puntúa alto por sistemática diferente
      (escala distinta), la similitud coseno los puede considerar iguales
      si sus preferencias relativas coinciden.
    """
    dot = producto_punto(a, b)
    mag_a = magnitud_vector(a)
    mag_b = magnitud_vector(b)

    # Protección contra división por cero (vector nulo)
    if mag_a == 0 or mag_b == 0:
        return 0.0

    return dot / (mag_a * mag_b)


# -------------------------
# detalle_similitudes_usuario
# -------------------------
# Este procedimiento:
#  1) Encuentra índices comunes (películas vistas por ambos usuarios).
#  2) Construye vectores restringidos a esos índices (sub-vectores).
#  3) Calcula producto punto, normas y coseno explicando cada término.
#
# Razonamiento algebraico:
# - Restringir a índices comunes es equivalente a proyectar los vectores
#   originales sobre la subbase formada por las coordenadas compartidas.
def detalle_similitudes_usuario(calificaciones, usuarios, usuario_index):
    usuario_actual = calificaciones[usuario_index]
    nombre_actual = usuarios[usuario_index]

    print(f"Calculando similitudes completas para: {nombre_actual}\n")
    resultados = []

    # Recorremos todos los usuarios (filas de la matriz de calificaciones)
    for i, otro in enumerate(calificaciones):
        if i == usuario_index:
            continue

        nombre_otro = usuarios[i]

        # 1) Índices comunes: solo consideramos coordenadas donde ambos tienen datos.
        #    Matemáticamente: intersección de soportes (support) de los vectores.
        indices_comunes = [j for j in range(len(usuario_actual)) if usuario_actual[j] != 0 and otro[j] != 0]

        print(f"--- {nombre_actual} vs {nombre_otro} ---")
        if not indices_comunes:
            # Si no hay intersección, el coseno no es aplicable: similitud 0.
            print("  No hay películas en común.\n")
            resultados.append((i, 0.0, None, None))
            continue

        # 2) Crear sub-vectores con solo los componentes comunes.
        #    Esto equivale a extraer coordenadas de la base canónica relevantes.
        vec_a = [usuario_actual[j] for j in indices_comunes]
        vec_b = [otro[j] for j in indices_comunes]

        print(f"  Índices comunes: {indices_comunes}")
        print(f"  Vector {nombre_actual}: {vec_a}")
        print(f"  Vector {nombre_otro}: {vec_b}")

        # 3) Producto punto entre los sub-vectores.
        #    Matématicamente: Σ vec_a[k]*vec_b[k]. Aquí mostramos sumandos para transparencia.
        dot = producto_punto(vec_a, vec_b)
        sumandos = " + ".join(f"{x}*{y}" for x, y in zip(vec_a, vec_b))
        print(f"  Producto punto = {sumandos} = {dot}")

        # 4) Magnitudes (normas) de los sub-vectores.
        #    Interpretación: factor de escala para convertir producto punto en cos(θ).
        mag_a = magnitud_vector(vec_a)
        mag_b = magnitud_vector(vec_b)
        print(f"  Magnitud {nombre_actual} = sqrt(" + " + ".join(f"{x}^2" for x in vec_a) + f") = {mag_a:.12f}")
        print(f"  Magnitud {nombre_otro} = sqrt(" + " + ".join(f"{x}^2" for x in vec_b) + f") = {mag_b:.12f}")

        denom = mag_a * mag_b
        print(f"  Denominador (||a|| * ||b||) = {mag_a:.12f} * {mag_b:.12f} = {denom:.12f}")

        # 5) Similitud coseno y guardado del resultado.
        sim = dot / denom if denom != 0 else 0.0
        print(f"  Similitud coseno = {dot} / {denom:.12f} = {sim:.12f}\n")

        # Guardamos: índice del usuario, similitud y los sub-vectores (útil para depuración)
        resultados.append((i, sim, vec_a, vec_b))

    return resultados


# -------------------------
# predecir_colaborativo_detalle
# -------------------------
# Propósito: generar predicciones para ítems no vistos por usuario objetivo.
# Fórmula usada: promedio ponderado por similitud.
#
# Interpretación lineal: la predicción es un estimador lineal que combina
# las calificaciones observadas por vecinos ponderadas por su "proyección"
# (similitud) sobre el usuario objetivo.
def predecir_colaborativo_detalle(calificaciones, usuarios, peliculas, usuario_index, usuarios_similares):
    usuario_actual = calificaciones[usuario_index]
    print(f"Predicciones detalladas para {usuarios[usuario_index]}:\n")

    predicciones = [None] * len(peliculas)

    # Recorremos todas las películas (coordenadas)
    for pelicula_idx in range(len(peliculas)):
        # Si el usuario ya la vio, no predecimos: conservamos la observación.
        if usuario_actual[pelicula_idx] != 0:
            print(f" - {peliculas[pelicula_idx]}: ya vista (calif={usuario_actual[pelicula_idx]})")
            continue

        print(f"\nCalculando predicción para: {peliculas[pelicula_idx]}")

        suma_ponderada = 0.0  # Σ sim(u,v) * rating_v(item)
        suma_sim = 0.0        # Σ sim(u,v)

        # Iteramos sobre vecinos proporcionados (índice, similitud)
        for otro_idx, sim in usuarios_similares:
            cal_otro = calificaciones[otro_idx][pelicula_idx]

            # Mostramos la contribución de cada vecino
            print(f"  Revisando usuario {usuarios[otro_idx]}: similitud={sim:.6f}, calificación en '{peliculas[pelicula_idx]}' = {cal_otro}")

            if cal_otro != 0:
                contrib = sim * cal_otro
                suma_ponderada += contrib
                suma_sim += sim
                print(f"    Aporta: {sim:.6f} * {cal_otro} = {contrib:.12f}")
            else:
                print("    No aportó (no la vio).")

        # Si hay información acumulada, calculamos promedio ponderado
        if suma_sim > 0:
            pred = suma_ponderada / suma_sim
            predicciones[pelicula_idx] = pred
            print(f"  Suma ponderada = {suma_ponderada:.12f}")
            print(f"  Suma de similitudes = {suma_sim:.12f}")
            print(f"  Predicción = {suma_ponderada:.12f} / {suma_sim:.12f} = {pred:.12f}")
        else:
            # No hay vecinos que hayan visto el item => no podemos estimar.
            print("  Ningún usuario similar vio esta película => no se puede predecir (quedará None).")
            predicciones[pelicula_idx] = None

    return predicciones
