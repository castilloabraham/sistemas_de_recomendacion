# contenido.py
# ===============================================================
# SISTEMA BASADO EN CONTENIDO: COMPARACIÓN ENTRE VECTORES DE CARACTERÍSTICAS
# ===============================================================
# Comentarios paso a paso explican operaciones vectoriales, interpretación
# de producto punto, magnitud y similitud coseno en el contexto de ítems.
# ===============================================================

import math

# -------------------------
# Producto punto entre vectores de características
# -------------------------
# Se usa para capturar coincidencia por atributo entre dos ítems.
def producto_punto(a, b):
    """
    Producto punto simple: Σ a_i * b_i
    - En vectores de características binarios: cuenta coincidencias ponderadas.
    - En vectores reales: pondera similitud por intensidad de cada característica.
    """
    return sum(x * y for x, y in zip(a, b))


# -------------------------
# Magnitud del vector de características
# -------------------------
# Interpreta cuántas/qué tan intensas son las características de un ítem.
def magnitud_vector(v):
    """
    ||v|| = sqrt(Σ v_i^2)
    - Para vectores binarios indica sqrt(#características presentes)
    """
    return math.sqrt(sum(x * x for x in v))


# -------------------------
# detalle_similitud_peliculas
# -------------------------
# Para una película objetivo, comparamos con todas las demás.
# Paso 1: extraer vector target.
# Paso 2: para cada otro vector:
#    - calcular producto punto (coincidencia atributo a atributo)
#    - calcular magnitudes
#    - calcular coseno (direccionalidad entre vectores)
def detalle_similitud_peliculas(caracteristicas, pelicula_index, peliculas):
    target = caracteristicas[pelicula_index]
    nombre_target = peliculas[pelicula_index]

    # Explicación: estamos proyectando la información de la película objetivo
    # sobre el conjunto de características y comparándola con otras proyecciones.
    print(f"Comparando todas las películas con: {nombre_target}\n")

    resultados = []

    for i, vec in enumerate(caracteristicas):
        if i == pelicula_index:
            continue

        print(f"--- {nombre_target} vs {peliculas[i]} ---")
        print(f"  Vector {nombre_target}: {target}")
        print(f"  Vector {peliculas[i]}: {vec}")

        # Producto punto = Σ target_j * vec_j
        # Interpretación: cuánto comparten en términos de características.
        dot = producto_punto(target, vec)
        sumandos = " + ".join(f"{a}*{b}" for a, b in zip(target, vec))
        print(f"  Producto punto = {sumandos} = {dot}")

        # Magnitudes: escalas de cada vector (para normalizar)
        mag_t = magnitud_vector(target)
        mag_o = magnitud_vector(vec)
        print(f"  Magnitud {nombre_target} = sqrt(" + " + ".join(f"{x}^2" for x in target) + f") = {mag_t:.12f}")
        print(f"  Magnitud {peliculas[i]} = sqrt(" + " + ".join(f"{x}^2" for x in vec) + f") = {mag_o:.12f}")

        # Denominador = ||target|| * ||vec||
        denom = mag_t * mag_o

        # Similitud coseno = (producto punto) / (denominador)
        # Significado práctica: similaridad en términos de orientación de características.
        sim = dot / denom if denom != 0 else 0.0
        print(f"  Similitud coseno = {dot} / {denom:.12f} = {sim:.12f}\n")

        resultados.append((i, sim))

    # Ordenamos por similitud descendente para obtener recomendaciones por contenido
    resultados.sort(key=lambda x: x[1], reverse=True)
    return resultados
