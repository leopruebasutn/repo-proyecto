# Análisis de Resultados Deportivos – Torneo 2024

## Integrantes del Equipo

| Rol | Nombre | Responsabilidad |
|-----|--------|-----------------|
| P1 – Líder y Organizador (Hugo) | Leonardo Emanuel Diaz | Creación del repositorio, estructura de carpetas y README |
| P2 – Desarrollador Técnico (Paco) | Leonardo Emanuel Diaz | Script Python de análisis estadístico |
| P3 – Revisor y QA (Luis) | Leonardo Emanuel Diaz | Peer Review, documentación y cierre de Pull Request |

## Escenario Elegido

**Escenario D – Estadísticas de Resultados Deportivos**

## Descripción del Proyecto

Este proyecto analiza los resultados de un torneo de fútbol amateur con cuatro equipos participantes. A partir de un dataset 
de partidos jugados, el script calcula la tabla de posiciones completa, estadísticas individuales por equipo y genera 
visualizaciones comparativas del rendimiento.

## Dataset Utilizado

- **Archivo:** `datos/resultados_torneo.csv`
- **Contenido:** 16 partidos del torneo (jornadas de marzo y abril 2024)
- **Columnas:** fecha, equipo_local, equipo_visitante, goles_local, goles_visitante
- **Origen:** Dataset simulado de elaboración propia para uso educativo

## Estructura del Repositorio
repo-proyecto/
├── datos/
│   └── resultados_torneo.csv
├── scripts/
│   └── analisis_torneo.py
├── resultados/
│   ├── tabla_posiciones.csv
│   └── grafico_rendimiento.png
├── README.md
└── .gitignore

## Instrucciones para Ejecutar

1. Clonar el repositorio: `git clone https://github.com/leopruebasutn/repo-proyecto.git`
2. Ejecutar en Google Colab: `python scripts/analisis_torneo.py`

## Dependencias

- Python 3.8+
- pandas
- matplotlib

---
