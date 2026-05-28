# =============================================================================
# analisis_torneo.py
# Escenario D – Estadísticas de Resultados Deportivos
# Cátedra: Organización Empresarial – UTN TUP
# Revisión QA: P3 – Luis
# =============================================================================
# Este script procesa los resultados de un torneo de fútbol y genera:
#   - Tabla de posiciones completa
#   - Cantidad de partidos ganados por equipo
#   - Promedio de goles por partido
#   - Gráfico comparativo de rendimiento entre equipos
#
# REQUISITOS:
#   - Python 3.8+
#   - pandas
#   - matplotlib
#
# EJECUCIÓN:
#   Desde la raíz del proyecto: python scripts/analisis_torneo.py
# =============================================================================

import pandas as pd
import matplotlib.pyplot as plt
import os

# -----------------------------------------------------------------------------
# 1. CONFIGURACIÓN DE RUTAS
# Se usan rutas RELATIVAS para garantizar reproducibilidad en cualquier entorno
# (Google Colab, entorno local, CI/CD, etc.)
# NO usar rutas absolutas como /home/usuario/... ya que rompen la portabilidad
# -----------------------------------------------------------------------------
RUTA_DATOS      = os.path.join('datos', 'resultados_torneo.csv')
RUTA_RESULTADOS = 'resultados'

# Crear carpeta de resultados si no existe (evita error en primera ejecución)
os.makedirs(RUTA_RESULTADOS, exist_ok=True)

# -----------------------------------------------------------------------------
# 2. CARGA DE DATOS
# Se importa el dataset con parse_dates para convertir la columna fecha
# automáticamente a tipo datetime, facilitando análisis temporales futuros
# -----------------------------------------------------------------------------
df = pd.read_csv(RUTA_DATOS, parse_dates=['fecha'])
print("=== DATOS CARGADOS CORRECTAMENTE ===")
print(f"Total de partidos: {len(df)}")
print(df.head(), "\n")

# -----------------------------------------------------------------------------
# 3. OBTENER EQUIPOS PARTICIPANTES
# Se extraen equipos únicos del torneo usando unión de conjuntos (set)
# sorted() garantiza orden alfabético consistente en cada ejecución
# -----------------------------------------------------------------------------
equipos = sorted(set(df['equipo_local'].unique()) | set(df['equipo_visitante'].unique()))

# -----------------------------------------------------------------------------
# 4. CALCULAR ESTADÍSTICAS POR EQUIPO
# Para cada equipo se calculan todas las métricas del torneo.
# Regla de puntos estándar: victoria = 3 pts | empate = 1 pt | derrota = 0 pts
# Se consideran tanto los partidos jugados como local y como visitante
# -----------------------------------------------------------------------------
stats = []
for equipo in equipos:
    # Filtrar partidos donde el equipo participó como local o visitante
    local     = df[df['equipo_local'] == equipo].copy()
    visitante = df[df['equipo_visitante'] == equipo].copy()

    # Victorias: gana como local O gana como visitante
    victorias = (
        len(local[local['goles_local'] > local['goles_visitante']]) +
        len(visitante[visitante['goles_visitante'] > visitante['goles_local']])
    )
    # Empates: igualdad de goles en cualquiera de los dos roles
    empates = (
        len(local[local['goles_local'] == local['goles_visitante']]) +
        len(visitante[visitante['goles_local'] == visitante['goles_visitante']])
    )
    # Derrotas: pierde como local O pierde como visitante
    derrotas = (
        len(local[local['goles_local'] < local['goles_visitante']]) +
        len(visitante[visitante['goles_visitante'] < visitante['goles_local']])
    )

    # Goles a favor y en contra (sumando ambos roles)
    gf = local['goles_local'].sum() + visitante['goles_visitante'].sum()
    gc = local['goles_visitante'].sum() + visitante['goles_local'].sum()

    stats.append({
        'Equipo': equipo,
        'PJ': victorias + empates + derrotas,
        'PG': victorias,
        'PE': empates,
        'PP': derrotas,
        'GF': gf,
        'GC': gc,
        'DG': gf - gc,          # Diferencia de goles (criterio de desempate)
        'Puntos': victorias * 3 + empates
    })

# Ordenar por puntos, usando DG y GF como criterios de desempate
tabla = pd.DataFrame(stats).sort_values(
    by=['Puntos', 'DG', 'GF'], ascending=False
).reset_index(drop=True)
tabla.index = tabla.index + 1
tabla.index.name = 'Pos'

# -----------------------------------------------------------------------------
# 5. MOSTRAR RESULTADOS EN CONSOLA
# -----------------------------------------------------------------------------
print("=== TABLA DE POSICIONES ===")
print(tabla.to_string())
print()
print(f"Equipo con más victorias: {tabla.loc[tabla['PG'].idxmax(), 'Equipo']} ({tabla['PG'].max()} victorias)")
total_goles = df['goles_local'].sum() + df['goles_visitante'].sum()
print(f"Promedio de goles por partido: {total_goles / len(df):.2f}")

# -----------------------------------------------------------------------------
# 6. EXPORTAR TABLA A CSV
# Se guarda en /resultados para separar claramente datos de entrada y salida
# -----------------------------------------------------------------------------
ruta_csv = os.path.join(RUTA_RESULTADOS, 'tabla_posiciones.csv')
tabla.to_csv(ruta_csv)
print(f"\nTabla exportada a: {ruta_csv}")

# -----------------------------------------------------------------------------
# 7. GENERAR GRÁFICO COMPARATIVO
# Subplot izquierdo: barras apiladas (PG/PE/PP) para comparar rendimiento
# Subplot derecho: puntos totales para ver la clasificación final
# -----------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Estadísticas del Torneo 2024', fontsize=14, fontweight='bold')

colores = {'PG': '#2ecc71', 'PE': '#f39c12', 'PP': '#e74c3c'}
bottom_vals = [0] * len(tabla)
for col in ['PG', 'PE', 'PP']:
    axes[0].bar(tabla['Equipo'], tabla[col], bottom=bottom_vals,
                color=colores[col],
                label={'PG': 'Victorias', 'PE': 'Empates', 'PP': 'Derrotas'}[col])
    bottom_vals = [b + v for b, v in zip(bottom_vals, tabla[col])]
axes[0].set_title('Rendimiento por Equipo')
axes[0].set_xlabel('Equipo')
axes[0].set_ylabel('Partidos')
axes[0].legend()
axes[0].tick_params(axis='x', rotation=15)

bars = axes[1].bar(tabla['Equipo'], tabla['Puntos'], color='#3498db', edgecolor='navy')
axes[1].set_title('Puntos Totales')
axes[1].set_xlabel('Equipo')
axes[1].set_ylabel('Puntos')
axes[1].tick_params(axis='x', rotation=15)
for bar in bars:
    h = bar.get_height()
    axes[1].text(bar.get_x() + bar.get_width() / 2, h + 0.2, str(int(h)),
                 ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.tight_layout()
ruta_grafico = os.path.join(RUTA_RESULTADOS, 'grafico_rendimiento.png')
plt.savefig(ruta_grafico, dpi=150, bbox_inches='tight')
plt.show()
print(f"Gráfico guardado en: {ruta_grafico}")
print("\n=== ANÁLISIS COMPLETADO ===")
