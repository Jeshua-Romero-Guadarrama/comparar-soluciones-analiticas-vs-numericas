"""
Comparacion de Soluciones Analiticas vs Numericas para Ecuaciones Diferenciales Separables.

Este modulo resuelve la ecuacion diferencial separable:

    dy/dt = -2ty,    y(0) = 1

De forma analitica mediante separacion de variables y de forma numerica mediante el metodo de Euler.
Posteriormente genera una grafica comparativa entre ambas soluciones.

Autor: Jehsua Romero Guadarrama
"""

import math
import matplotlib.pyplot as plt

# Constantes de configuracion del problema

TIEMPO_INICIAL      = 0.0
TIEMPO_FINAL        = 1.0
PASO_H              = 0.2
CONDICION_INICIAL_Y = 1.0

# Funciones del problema

def ecuacion_diferencial(t: float, y: float) -> float:
    """
    Evalua el lado derecho de la EDO dy/dt = f(t, y).

    La ecuacion diferencial seleccionada es:
        dy/dt = -2 * t * y

    Una ecuacion separable clasica cuya solucion analitica 
    se puede obtener por el metodo de separacion de variables.

    Args:
        t: Variable independiente (tiempo).
        y: Variable dependiente.

    Returns:
        Valor de f(t, y) = -2ty.
    """
    return -2 * t * y


def solucion_analitica(t: float) -> float:
    """
    
    Calcula la solucion exacta de la EDO en el punto t.

    Proceso de separacion de variables:
        dy/dt            = -2ty
        (1/y) dy         = -2t dt          # Separamos variables
        integral(1/y) dy = integral(-2t) dt
        ln|y|            = -t^2 + C
        y                = A * e^(-t^2)

    Aplicando la condicion inicial y(0) = 1:
        1 = A * e^(0)  =>  A = 1

    Solucion exacta:
        y(t) = e^(-t^2)

    Args:
        t: Punto en el que se evalua la solucion.

    Returns:
        Valor exacto de y(t) = e^(-t^2).
    """
    return math.exp(-(t ** 2))


def metodo_de_euler(
    funcion: callable,
    t_inicial: float,
    y_inicial: float,
    t_final: float,
    paso: float,
) -> tuple[list[float], list[float]]:
    """
    Aproxima la solucion de una EDO mediante el metodo de Euler.

    El metodo de Euler es un esquema numerico de primer orden que
    avanza la solucion paso a paso usando la formula:

        y_{n+1} = y_n + h * f(t_n, y_n)

    Args:
        funcion:   Funcion f(t, y) que define la EDO dy/dt = f(t, y).
        t_inicial: Valor inicial de la variable independiente.
        y_inicial: Condicion inicial y(t_inicial).
        t_final:   Limite superior del intervalo de integracion.
        paso:      Tamano del paso h.

    Returns:
        Tupla con dos listas: (valores_t, valores_y) correspondientes a los puntos calculados por el metodo.
    """
    valores_t = [t_inicial]
    valores_y = [y_inicial]

    t_actual = t_inicial
    y_actual = y_inicial

    # Avanzamos paso a paso hasta alcanzar el tiempo final
    while t_actual < t_final - 1e-12:
        y_siguiente = y_actual + paso * funcion(t_actual, y_actual)
        t_actual    = round(t_actual + paso, 10)

        valores_t.append(t_actual)
        valores_y.append(y_siguiente)

        y_actual = y_siguiente

    return valores_t, valores_y

def calcular_errores(
    valores_t: list[float],
    valores_y_numericos: list[float],
) -> list[dict]:
    """
    Calcula el error absoluto entre la solucion numerica y la analitica.

    Para cada punto t_i se computa:
        error_absoluto = |y_analitica(t_i) - y_euler(t_i)|

    Args:
        valores_t:           Lista de puntos temporales.
        valores_y_numericos: Lista de valores aproximados por Euler.

    Returns:
        Lista de diccionarios con la informacion de cada paso:
        t, y_analitica, y_euler, error_absoluto.
    """
    resultados = []

    for t, y_euler in zip(valores_t, valores_y_numericos):
        y_exacta = solucion_analitica(t)
        error = abs(y_exacta - y_euler)
        resultados.append({
            "t": t,
            "y_analitica": y_exacta,
            "y_euler": y_euler,
            "error_absoluto": error,
        })

    return resultados


def imprimir_tabla_resultados(resultados: list[dict]) -> None:
    """Muestra en consola una tabla comparativa de ambas soluciones.

    Args:
        resultados: Lista de diccionarios generada por calcular_errores.
    """
    separador = "-" * 65
    encabezado = f"{'t':>6} | {'y analitica':>14} | {'y Euler':>14} | {'Error abs.':>14}"

    print("\n" + separador)
    print("  Comparacion: Solucion Analitica vs Metodo de Euler")
    print(f"  EDO: dy/dt = -2ty,  y(0) = 1,  h = {PASO_H}")
    print(separador)
    print(encabezado)
    print(separador)

    for fila in resultados:
        print(
            f"{fila['t']:>6.1f} | "
            f"{fila['y_analitica']:>14.10f} | "
            f"{fila['y_euler']:>14.10f} | "
            f"{fila['error_absoluto']:>14.10f}"
        )

    print(separador)


def generar_grafica(
    valores_t_euler: list[float],
    valores_y_euler: list[float],
) -> None:
    """
    Genera y guarda una grafica comparativa entre ambas soluciones.

    Se traza la curva continua de la solucion analitica junto con los
    puntos discretos obtenidos por el metodo de Euler.

    Args:
        valores_t_euler: Puntos temporales del metodo de Euler.
        valores_y_euler: Valores aproximados por Euler.
    """
    # Puntos finos para la curva analitica
    num_puntos_curva = 200
    t_fino = [
        TIEMPO_INICIAL + i * (TIEMPO_FINAL - TIEMPO_INICIAL) / num_puntos_curva
        for i in range(num_puntos_curva + 1)
    ]
    y_analitica_fino = [solucion_analitica(t) for t in t_fino]

    # Configuracion de la figura
    figura, ejes = plt.subplots(figsize=(10, 6))

    ejes.plot(
        t_fino,
        y_analitica_fino,
        label="Solucion analitica: $y = e^{-t^2}$",
        color="blue",
        linewidth=2,
    )
    ejes.plot(
        valores_t_euler,
        valores_y_euler,
        "o--",
        label=f"Metodo de Euler (h = {PASO_H})",
        color="red",
        markersize=8,
        linewidth=1.5,
    )

    ejes.set_xlabel("Tiempo (t)", fontsize=12)
    ejes.set_ylabel("y(t)", fontsize=12)
    ejes.set_title(
        "Comparacion: Solucion Analitica vs Metodo de Euler\n"
        "$dy/dt = -2ty$,  $y(0) = 1$",
        fontsize=14,
    )
    ejes.legend(fontsize=11)
    ejes.grid(True, linestyle="--", alpha=0.7)

    plt.tight_layout()

    nombre_archivo = "grafica_comparativa.png"
    figura.savefig(nombre_archivo, dpi=150)
    print(f"\nGrafica guardada como '{nombre_archivo}'.")

    plt.show()

# Punto de entrada principal

def main() -> None:
    """
    Ejecuta el flujo completo del programa.
    1. Aplica el metodo de Euler para obtener la solucion numerica.
    2. Calcula los errores comparando con la solucion analitica.
    3. Imprime la tabla de resultados en consola.
    4. Genera la grafica comparativa.
    """
    # Paso 1: Resolver numericamente con el metodo de Euler
    valores_t, valores_y = metodo_de_euler(
        funcion   = ecuacion_diferencial,
        t_inicial = TIEMPO_INICIAL,
        y_inicial = CONDICION_INICIAL_Y,
        t_final   = TIEMPO_FINAL,
        paso      = PASO_H,
    )

    # Paso 2: Calcular errores
    resultados = calcular_errores(valores_t, valores_y)

    # Paso 3: Mostrar tabla en consola
    imprimir_tabla_resultados(resultados)

    # Paso 4: Generar grafica
    generar_grafica(valores_t, valores_y)


if __name__ == "__main__":
    main()
