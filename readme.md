# Proyecto de Sistema de Recomendación
## Implementado con Álgebra Lineal, Similitud del Coseno y SVD

Este proyecto demuestra cómo aplicar conceptos de álgebra lineal para construir tres tipos de sistemas de recomendación:

1. Sistema Colaborativo (similitud entre usuarios)
2. Sistema Basado en Contenido (similitud entre películas)
3. Sistema SVD / Espacio Latente (factorización matricial)

Incluye explicaciones matemáticas paso a paso impresas directamente en consola.

---

## Requerimientos

Asegúrate de tener instalado:

- Python 3.8 o superior  
- pip (gestor de paquetes de Python)

---

## Estructura del Proyecto

El proyecto debe tener la siguiente estructura:

proyecto_recomendacion/
│
├── main.py
├── colaborativo.py
├── contenido.py
├── svd_system.py
└── README.md



---

## Instalación de Dependencias

El proyecto solo requiere NumPy:

pip install numpy



---

## Cómo Ejecutarlo

Dentro de la carpeta del proyecto, ejecuta:

python main.py

markdown
Copiar código

El programa imprimirá:

### 1. Sistema Colaborativo
- Cálculo de similitud del coseno entre usuarios  
- Producto punto  
- Normas  
- Denominadores  
- Predicciones ponderadas  

### 2. Sistema Basado en Contenido
- Comparación entre vectores de características de películas  
- Cálculo de similitud de contenido  

### 3. Sistema SVD
- Matriz original  
- Matrices U, S y Vt completas  
- Truncamiento k  
- Reconstrucción aproximada  
- Predicciones en espacio latente  

---

## Explicación Matemática (Resumen)

### Representación en Vectores

Un usuario se representa como un vector en Rⁿ:

u = [r1, r2, ..., rn]



Una película se representa como un vector de características en Rᵏ.

---

### Similitud del Coseno

Usada para medir afinidad entre usuarios o ítems:

sim(a, b) = (a · b) / (||a|| * ||b||)



Donde:

- a · b : producto punto  
- ||a|| : norma euclidiana  
- Resultado en rango [-1, 1]

---

### Descomposición SVD

La matriz de calificaciones A se factoriza como:

A = U * S * V^T



Luego se aplica un truncamiento:

A_k = U_k * S_k * V_k^T



Esto genera un espacio latente donde usuarios y películas se representan por vectores comprimidos.

La predicción se calcula como:

predicción = user_latent · movie_latent



---

## Objetivo del Proyecto

Este proyecto sirve como ejemplo práctico para:

- Usar álgebra lineal en programación  
- Implementar similitud del coseno  
- Usar factorización matricial SVD  
- Comprender espacios latentes  
- Mostrar cálculos paso a paso para aprendizaje  

---

## Autor

Proyecto desarrollado y documentado con apoyo de ChatGPT.

---

## Extensiones posibles

Puedes solicitar:

- Versión con API REST  
- Interfaz gráfica  
- Notebook Jupyter  
- Informe técnico en PDF  