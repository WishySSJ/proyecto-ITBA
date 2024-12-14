# Proyecto de Cierre del Curso de Python - ITBA

Este repositorio contiene el proyecto final desarrollado como parte del curso de Python dictado en el ITBA. El proyecto está enfocado en el manejo de datos financieros mediante la interacción con una API externa, almacenamiento en una base de datos SQLite y visualización de información a través de gráficos.

---

## Contenidos del Repositorio

1. **Código Principal:** Archivo `tp.py` que contiene el desarrollo completo del programa.
2. **Archivo de Dependencias:** `requirements.txt` con las librerías necesarias para ejecutar el proyecto.

---

## Funcionalidades

1. **Conexión a una API externa:** Obtiene datos financieros de una fuente confiable.
2. **Gestión de base de datos:** Almacena y organiza los datos obtenidos utilizando SQLite.
3. **Visualización de datos:** Crea gráficos para analizar la evolución de los precios.
4. **Interfaz interactiva:** Menú principal que permite al usuario realizar diversas acciones, como listar tickers, graficar datos y más.

---

## Requisitos Previos

1. Python 3.9 o superior instalado.
2. Librerías necesarias instaladas. Ver sección de [Instalación](#instalación).

---

## Instalación

1. Clonar este repositorio:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd <NOMBRE_DEL_REPOSITORIO>
   ```

2. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Ejecutar el programa:
   ```bash
   python tp.py
   ```

---

## Estructura del Proyecto

```
<repositorio>
│
├── tp.py              # Código principal del proyecto
├── requirements.txt   # Dependencias del proyecto
├── README.md          # Este archivo
├── financial_data.db  # Base de datos SQLite generada automáticamente luego de la primer actualziacion de datos
```

---

## Uso

1. **Actualizar datos:**
   - Desde el menú principal, selecciona la opción `1` e ingresa los parámetros solicitados (ticker, fecha inicial y fecha final).

2. **Visualización de datos:**
   - Resumen: Opción `2.1`.
   - Gráfico: Opción `2.2`.

3. **Ver log de última actualización:**
   - Selecciona la opción `3` en el menú.

4. **Eliminar datos existentes:**
   - Selecciona la opción `5` para limpiar la base de datos.


---

## Créditos

Desarrollado por **Francisco Xavier Areses** como proyecto final del curso de Python en el ITBA.

