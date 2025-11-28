# main.py
# ===============================================================
# ORQUESTADOR: ejecuta los 3 sistemas (colaborativo, contenido, SVD)
# Comentarios entre bloques explican el propósito de cada paso.
# ===============================================================

from colaborativo import detalle_similitudes_usuario, predecir_colaborativo_detalle
from contenido import detalle_similitud_peliculas
from svd_system import svd_y_reconstruccion_detalle, predicciones_svd_detalle

# -------------------------
# Datos de ejemplo
# -------------------------
# usuarios: lista de nombres -> filas de la matriz de calificaciones
# peliculas: lista de títulos -> columnas de la matriz
usuarios = ['Ana', 'Carlos', 'Elena', 'David', 'Maria']
peliculas = ['Matrix', 'Avatar', 'Titanic', 'Star Wars', 'Inception']

# Matriz calificaciones: filas=usuarios, columnas=películas
# Valor 0 indica "no vista" / dato faltante
calificaciones = [
    [5, 4, 2, 3, 0],  # Ana
    [4, 5, 0, 2, 4],  # Carlos
    [0, 5, 4, 4, 3],  # Elena
    [3, 0, 5, 0, 5],  # David
    [5, 3, 0, 4, 0]   # Maria
]

# Vectores de características (ejemplo simple: presencia/ausencia de rasgos)
caracteristicas_peliculas = [
    [1, 0, 0, 1],  # Matrix
    [1, 0, 0, 1],  # Avatar
    [0, 1, 1, 0],  # Titanic
    [1, 0, 0, 1],  # Star Wars
    [1, 0, 0, 1]   # Inception
]

# -------------------------
# 1) COLABORATIVO
# -------------------------
# Objetivo: medir similitud entre usuarios y predecir ratings para Ana (índice 0)
# Paso A: obtener similitudes completas (con sub-vectores y detalle)
similitudes = detalle_similitudes_usuario(calificaciones, usuarios, 0)

# Paso B: escogemos los top2 vecinos por similitud (índice, similitud)
# Nota algebraica: ordenar por coseno es ordenar por la proyección relativa.
top2 = [(i, sim) for (i, sim, _, _) in sorted(similitudes, key=lambda x: x[1], reverse=True)[:2]]

# Paso C: predicción ponderada usando los vecinos seleccionados
preds_colab = predecir_colaborativo_detalle(calificaciones, usuarios, peliculas, 0, top2)
print("\nPredicciones colaborativas (Ana):", preds_colab)


# -------------------------
# 2) CONTENIDO
# -------------------------
# Objetivo: recomendar por similitud de atributos respecto a 'Matrix' (índice 0)
# Llamada corregida: (caracteristicas, indice_objetivo, lista_peliculas)
# Comentario: esto compara vectores en espacio de características (no usuarios).
recs_contenido = detalle_similitud_peliculas(caracteristicas_peliculas, 0, peliculas)
print("\nPelículas más parecidas a Matrix (contenido):", recs_contenido)


# -------------------------
# 3) SVD
# -------------------------
# Objetivo: factorizar la matriz y predecir en espacio latente (k=2)
# Paso A: descomponer y truncar (obtener U_k, S_k, Vt_k)
U_k, S_k, Vt_k, A_approx = svd_y_reconstruccion_detalle(calificaciones, k=2)

# Paso B: predecir usando vectores latentes para Ana (índice 0)
preds_svd = predicciones_svd_detalle(U_k, S_k, Vt_k, calificaciones, 0, usuarios, peliculas)
print("\nPredicciones SVD (Ana):", preds_svd)
