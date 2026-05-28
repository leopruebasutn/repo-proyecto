# =============================================================================
# analisis_torneo.py
# Escenario D – Estadísticas de Resultados Deportivos
# Cátedra: Organización Empresarial – UTN TUP
# =============================================================================
# Este script procesa los resultados de un torneo de fútbol y genera:
#   - Tabla de posiciones
#   - Cantidad de partidos ganados por equipo
#   - Promedio de goles por partido
#   - Gráfico comparativo de rendimiento entre equipos
# =============================================================================

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

# -----------------------------------------------------------------------------
# 1. CONFIGURACIÓN DE RUTAS
# Se usan rutas relativas para garantizar reproducibilidad en cualquier entorno
# (Google Colab, entorno local, etc.)
# -----------------------------------------------------------------------------
RUTA_DATOS     = os.path.join('datos', 'resultados_torneo.csv')
RUTA_RESULTADOS = 'resultados'

# Crear carpeta de resultados si no existe
os.makedirs(RUTA_RESULTADOS, exist_ok=True)

# -----------------------------------------------------------------------------
# 2. CARGA DE DATOS
# Se importa el dataset con los resultados de cada partido del torneo
# -----------------------------------------------------------------------------
df = pd.read_csv(RUTA_DATOS, parse_dates=['fecha'])

print("=== DATOS CARGADOS CORRECTAMENTE ===")
print(f"Total de partidos: {len(df)}")
print(df.head(), "\n")

# -----------------------------------------------------------------------------
# 3. OBTENER LA LISTA DE EQUIPOS PARTICIPANTES
# Se extraen todos los equipos únicos del torneo (locales y visitantes)
# -----------------------------------------------------------------------------
equipos = sorted(set(df['equipo_local'].unique()) | set(df['equipo_visitante'].unique()))

# -----------------------------------------------------------------------------
# 4. CALCULAR ESTADÍSTICAS POR EQUIPO
# Para cada equipo se calculan: partidos jugados, ganados, empatados, perdidos,
# goles a favor, goles en contra, diferencia de goles y puntos totales.
# Regla de puntos: victoria = 3 pts | empate = 1 pt | derrota = 0 pts
# -----------------------------------------------------------------------------
stats = []

for equipo in equipos:
    # Partidos jugados como local
    local = df[df['equipo_local'] == equipo].copy()
    # Partidos jugados como visitante
    visitante = df[df['equipo_visitante'] == equipo].copy()

    # --- Victorias ---
    victorias = (
        len(local[local['goles_local'] > local['goles_visitante']]) +
        len(visitante[visitante['goles_visitante'] > visitante['goles_local']])
    )

    # --- Empates ---
    empates = (
        len(local[local['goles_local'] == local['goles_visitante']]) +
        len(visitante[visitante['goles_local'] == visitante['goles_visitante']])
    )

    # --- Derrotas ---
    derrotas = (
        len(local[local['goles_local'] < local['goles_visitante']]) +
        len(visitante[visitante['goles_visitante'] < visitante['goles_local']])
    )

    # --- Goles a favor y en contra ---
    gf = local['goles_local'].sum() + visitante['goles_visitante'].sum()
    gc = local['goles_visitante'].sum() + visitante['goles_local'].sum()

    pj = victorias + empates + derrotas
    puntos = victorias * 3 + empates * 1

    stats.append({
        'Equipo':    equipo,
        'PJ':        pj,
        'PG':        victorias,
        'PE':        empates,
        'PP':        derrotas,
        'GF':        gf,
        'GC':        gc,
        'DG':        gf - gc,
        'Puntos':    puntos
    })

# Convertir a DataFrame y ordenar por puntos (criterio: DG como desempate)
tabla = pd.DataFrame(stats).sort_values(
    by=['Puntos', 'DG', 'GF'],
    ascending=False
).reset_index(drop=True)

# La posición empieza en 1
tabla.index = tabla.index + 1
tabla.index.name = 'Pos'

# -----------------------------------------------------------------------------
# 5. MOSTRAR RESULTADOS EN CONSOLA
# -----------------------------------------------------------------------------
print("=== TABLA DE POSICIONES ===")
print(tabla.to_string())
print()

# Equipo con más victorias
mejor_equipo = tabla.loc[tabla['PG'].idxmax(), 'Equipo']
print(f"Equipo con más victorias: {mejor_equipo} ({tabla['PG'].max()} victorias)")

# Promedio de goles por partido (suma total de goles / total de partidos)
total_goles   = df['goles_local'].sum() + df['goles_visitante'].sum()
total_partidos = len(df)
promedio_goles = total_goles / total_partidos
print(f"Promedio de goles por partido: {promedio_goles:.2f}")
print()

# -----------------------------------------------------------------------------
# 6. EXPORTAR TABLA DE POSICIONES A CSV
# Se guarda el resultado procesado en /resultados para facilitar su revisión
# -----------------------------------------------------------------------------
ruta_csv = os.path.join(RUTA_RESULTADOS, 'tabla_posiciones.csv')
tabla.to_csv(ruta_csv)
print(f"Tabla exportada a: {ruta_csv}")

# -----------------------------------------------------------------------------
# 7. GENERAR GRÁFICO COMPARATIVO DE RENDIMIENTO
# Gráfico de barras apiladas: victorias, empates y derrotas por equipo
# -----------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Estadísticas del Torneo 2024', fontsize=14, fontweight='bold')

colores = {'PG': '#2ecc71', 'PE': '#f39c12', 'PP': '#e74c3c'}

# -- Subplot 1: Barras apiladas (PG / PE / PP) --
bottom_vals = [0] * len(tabla)
labels_map  = {'PG': 'Victorias', 'PE': 'Empates', 'PP': 'Derrotas'}

for col in ['PG', 'PE', 'PP']:
    axes[0].bar(
        tabla['Equipo'],
        tabla[col],
        bottom=bottom_vals,
        color=colores[col],
        label=labels_map[col]
    )
    bottom_vals = [b + v for b, v in zip(bottom_vals, tabla[col])]

axes[0].set_title('Rendimiento por Equipo')
axes[0].set_xlabel('Equipo')
axes[0].set_ylabel('Partidos')
axes[0].legend()
axes[0].tick_params(axis='x', rotation=15)

# -- Subplot 2: Puntos totales --
bars = axes[1].bar(tabla['Equipo'], tabla['Puntos'], color='#3498db', edgecolor='navy')
axes[1].set_title('Puntos Totales')
axes[1].set_xlabel('Equipo')
axes[1].set_ylabel('Puntos')
axes[1].tick_params(axis='x', rotation=15)

# Agregar etiqueta de valor sobre cada barra
for bar in bars:
    h = bar.get_height()
    axes[1].text(
        bar.get_x() + bar.get_width() / 2,
        h + 0.2,
        str(int(h)),
        ha='center', va='bottom', fontsize=11, fontweight='bold'
    )

plt.tight_layout()

ruta_grafico = os.path.join(RUTA_RESULTADOS, 'grafico_rendimiento.png')
plt.savefig(ruta_grafico, dpi=150, bbox_inches='tight')
plt.show()
print(f"Gráfico guardado en: {ruta_grafico}")

print("\n=== ANÁLISIS COMPLETADO ===")
