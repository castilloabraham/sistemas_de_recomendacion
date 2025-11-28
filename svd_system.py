# svd_system.py
# ===============================================================
# SISTEMA SVD (Descomposición en Valores Singulares) — EXPLICADO PASO A PASO
# ===============================================================
# Objetivo: factorizar la matriz A (usuarios x películas) en U * S * V^T,
# y usar truncamiento para hallar espacios latentes compactos.
# Cada bloque tiene comentarios que enlazan la operación matricial
# con su interpretación en el recomendador.
# ===============================================================

import numpy as np

# -------------------------
# svd_y_reconstruccion_detalle
# -------------------------
# 1) Convertir matriz de calificaciones a numpy.array
# 2) Aplicar np.linalg.svd para obtener U, s, Vt
# 3) Truncar a k componentes: U_k, S_k, Vt_k
# 4) Reconstruir A_k = U_k * S_k * Vt_k (aprox.)
def svd_y_reconstruccion_detalle(matriz, k=2):
    """
    Descompone y reconstruye con explicación:
    - U: base ortonormal en el espacio de usuarios (columnas = factores)
    - s: valores singulares (importancia de cada factor)
    - Vt: base ortonormal en el espacio de películas
    - Truncamiento: seleccionar las k dimensiones con mayor energía (s_i grandes)
    """

    # 1) Matriz A: filas=usuarios, columnas=películas
    A = np.array(matriz, dtype=float)
    print("Matriz original A (usuarios x películas):")
    print(A, "\n")

    # 2) SVD completa
    # U shape: (m, m') donde m' = min(m,n)
    # s shape: (min(m,n),) valores singulares
    # Vt shape: (min(m,n), n)
    U, s, Vt = np.linalg.svd(A, full_matrices=False)

    # Mostrar resultados completos (útil para análisis manual)
    print("Descomposición SVD completa (U, s, Vt):")
    print("U (filas=usuarios, columnas=componentes):\n", np.round(U, 6))
    print("s (vector de valores singulares):\n", np.round(s, 6))
    print("Vt (filas=componentes, columnas=películas):\n", np.round(Vt, 6), "\n")

    # 3) Truncamiento: quedarnos con las k componentes principales
    # Razonamiento: los primeros k valores singulares contienen la mayor parte
    # de la 'energía' de la matriz (varianza). Reducimos ruido y dimensionalidad.
    U_k = U[:, :k]             # (m, k)
    S_k = np.diag(s[:k])       # (k, k)
    Vt_k = Vt[:k, :]           # (k, n)

    print(f"Truncamiento a k = {k} componentes latentes:")
    print("U_k (m x k):\n", np.round(U_k, 6))
    print("S_k (k x k):\n", np.round(S_k, 6))
    print("Vt_k (k x n):\n", np.round(Vt_k, 6), "\n")

    # 4) Reconstrucción aproximada A_k = U_k * S_k * Vt_k
    # Interpretación: reconstrucción en un subespacio de dimensión k que
    # aproxima las relaciones usuario-item.
    A_approx = U_k @ S_k @ Vt_k
    print("Reconstrucción aproximada A_k = U_k * S_k * Vt_k:")
    print(np.round(A_approx, 6), "\n")

    return U_k, S_k, Vt_k, A_approx


# -------------------------
# predicciones_svd_detalle
# -------------------------
# Idea: representar usuario y películas en espacio latente k y calcular
# producto punto entre vectores latentes -> estimación de rating.
def predicciones_svd_detalle(U_k, S_k, Vt_k, calificaciones, usuario_index, usuarios=None, peliculas=None):
    """
    Predicciones paso a paso:
    - user_latent = (U_k[usuario] * S_k)  -> vector en R^k
    - movie_latent = Vt_k[:, pelicula]     -> vector en R^k
    - pred = user_latent · movie_latent
    Justificación: los factores latentes capturan características abstractas.
    """

    if usuarios is None:
        usuarios = [f"user{i}" for i in range(len(calificaciones))]
    if peliculas is None:
        peliculas = [f"item{j}" for j in range(len(calificaciones[0]))]

    print(f"Predicciones usando SVD truncada para el usuario {usuarios[usuario_index]} (índice {usuario_index}):\n")

    # 1) Vector latente del usuario en R^k
    #    U_k[usuario_index] es la coordenada del usuario en la base de factores.
    #    Multiplicarlo por S_k reescala las coordenadas según la energía de cada factor.
    u_row = U_k[usuario_index]            # (k,)
    user_latent = u_row @ S_k             # (k,)  (fila por matriz diagonal)
    print("Vector latente del usuario (U_k[row] * S_k):")
    for idx, val in enumerate(user_latent):
        print(f"  componente {idx}: U_k[{usuario_index},{idx}] * S_k[{idx},{idx}] = {u_row[idx]:.12f} * {S_k[idx, idx]:.12f} = {val:.12f}")
    print()

    usuario_original = calificaciones[usuario_index]
    preds = [None] * len(peliculas)

    # 2) Para cada película no vista, calcular su vector latente y el producto punto
    for m_idx in range(len(peliculas)):
        if usuario_original[m_idx] != 0:
            # Conservamos rating observado: no predecimos sobre datos ya conocidos.
            print(f" - {peliculas[m_idx]}: ya vista (calif={usuario_original[m_idx]})")
            continue

        # movie_latent es la columna correspondiente en V (o fila en Vt transpuesta).
        movie_latent = Vt_k[:, m_idx]  # (k,)

        print(f"\nCalculando predicción SVD para película '{peliculas[m_idx]}' (índice {m_idx}):")
        # Desglose por componente latente:
        for r in range(len(movie_latent)):
            comp_user = user_latent[r]
            comp_movie = movie_latent[r]
            print(f"  componente {r}: user_latent[{r}] * movie_latent[{r}] = {comp_user:.12f} * {comp_movie:.12f} = {comp_user * comp_movie:.12f}")

        # Predicción final: producto punto de vectores latentes.
        pred = float(np.dot(user_latent, movie_latent))
        preds[m_idx] = pred
        print(f"  Predicción final (suma de componentes) = {pred:.12f}")

    return preds
