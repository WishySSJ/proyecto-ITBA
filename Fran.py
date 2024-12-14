import sqlite3
import requests
import matplotlib.pyplot as plt
from datetime import datetime

# Configuración de la API
API_KEY = ""  # API key de nuestro usuario en polygon.io
BASE_URL = "https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{start_date}/{end_date}"
TICKER_LIST_URL = "https://api.polygon.io/v3/reference/tickers"

# Inicializa la base de datos y actualizar estructura (si es necesario)
def initialize_database():
    conn = sqlite3.connect("financial_data.db")
    cursor = conn.cursor()

    # Crea la tabla si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_data (
            ticker TEXT,
            date TEXT,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume INTEGER
        )
    """)

    # Verifica si la columna updated_at existe o no
    cursor.execute("PRAGMA table_info(stock_data)")
    columns = [col[1] for col in cursor.fetchall()]
    if "updated_at" not in columns:
        cursor.execute("ALTER TABLE stock_data ADD COLUMN updated_at TEXT")

    conn.commit()
    conn.close()

# Obtener datos de la API
def fetch_data(ticker, start_date, end_date):
    url = BASE_URL.format(ticker=ticker, start_date=start_date, end_date=end_date)
    params = {"apiKey": API_KEY}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 401:
            print("Error de autenticación: Verifique su clave de API.")
        elif response.status_code == 403:
            print("Error de acceso: El plan actual no permite acceder a esta información. Revise las fechas y su plan de suscripción.")
        else:
            print(f"Error HTTP: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Error en la solicitud: {req_err}")
    return None

# Listar tickers disponibles en polygon para consulta (en este caso consulto los de stocks)
def list_tickers():
    params = {"market": "stocks", "active": "true", "limit": 1000, "apiKey": API_KEY}
    try:
        response = requests.get(TICKER_LIST_URL, params=params)
        response.raise_for_status()
        data = response.json()
        tickers = data.get("results", [])

        if not tickers:
            print("No se encontraron tickers disponibles.")
            return

        print("\n--- Lista de Tickers Disponibles ---")
        for i, ticker in enumerate(tickers):
            print(f"{i + 1}. {ticker['ticker']} - {ticker.get('name', 'Sin descripción')}")
            if (i + 1) % 10 == 0:  # Mostrar en bloques de 10
                input("Presione Enter para continuar...")

    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Error en la solicitud: {req_err}")

# Guardar datos en SQLite
def save_to_database(ticker, start_date, end_date, data):
    conn = sqlite3.connect("financial_data.db")
    cursor = conn.cursor()
    updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    for result in data.get("results", []):
        cursor.execute(
            "INSERT INTO stock_data (ticker, date, open, high, low, close, volume, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (ticker, result["t"], result["o"], result["h"], result["l"], result["c"], result["v"], updated_at)
        )

    conn.commit()
    conn.close()
    print("Datos guardados correctamente.")

# Leemos los datos de SQLite
def read_summary_from_database():
    conn = sqlite3.connect("financial_data.db")
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT ticker, MIN(date), MAX(date) FROM stock_data GROUP BY ticker")
    data = cursor.fetchall()

    conn.close()
    return data

def read_data_for_plot(ticker):
    conn = sqlite3.connect("financial_data.db")
    cursor = conn.cursor()

    cursor.execute("SELECT date, close FROM stock_data WHERE ticker = ? ORDER BY date", (ticker,))
    data = cursor.fetchall()

    conn.close()

    # Convertir las fechas de str a int (timestamp)
    processed_data = [(int(row[0]), row[1]) for row in data]
    return processed_data

# Obtener log de última actualización
def get_last_update_log():
    conn = sqlite3.connect("financial_data.db")
    cursor = conn.cursor()

    cursor.execute("SELECT ticker, MIN(date), MAX(date), updated_at FROM stock_data ORDER BY updated_at DESC LIMIT 1")
    last_record = cursor.fetchone()

    conn.close()

    if last_record:
        ticker, start_date, end_date, updated_at = last_record
        readable_start_date = datetime.fromtimestamp(int(start_date) / 1000).strftime('%Y-%m-%d')
        readable_end_date = datetime.fromtimestamp(int(end_date) / 1000).strftime('%Y-%m-%d')
        print("\n--- Última Actualización ---")
        print(f"Ticker: {ticker}")
        print(f"Fecha de inicio: {readable_start_date}")
        print(f"Fecha de fin: {readable_end_date}")
        print(f"Actualizado el: {updated_at}")
    else:
        print("No se encontraron registros en la base de datos.")

# Depurar datos en la base de datos
def clear_database():
    conn = sqlite3.connect("financial_data.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM stock_data")
    conn.commit()
    conn.close()

    print("Todos los datos han sido eliminados de la base de datos.")

# Visualizar datos
def plot_data(data):
    if len(data) == 1:
        print("Nota: Solo se encontró un dato para el ticker seleccionado. El gráfico mostrará un único punto.")

    try:
        dates = [datetime.fromtimestamp(x[0] / 1000).strftime('%Y-%m-%d') for x in data]  # Convertir timestamp a fecha legible
        prices = [x[1] for x in data]

        plt.figure(figsize=(10, 5))
        plt.plot(dates, prices, marker="o")
        plt.title("Precio de cierre de las acciones")
        plt.xlabel("Fecha")
        plt.ylabel("Precio de cierre")
        plt.grid()
        plt.xticks(rotation=45)  # Para rotar las fechas (mejor legibilidad).
        plt.tight_layout()  # Ajustar el diseño para evitar solapamientos
        plt.show()
    except Exception as e:
        print(f"Ocurrió un error al intentar graficar los datos: {e}")

# Menú interactivo
def main_menu():
    initialize_database()

    while True:
        print("\n--- Menú Principal ---")
        print("1. Actualización de datos")
        print("2. Visualización de datos")
        print("3. Ver log de última actualización")
        print("4. Listar tickers disponibles")
        print("5. Depurar datos")
        print("6. Salir")

        choice = input("Seleccione una opción: ")

        if choice == "1":
            print("Ejemplo: Ticker: AAPL, Fecha de inicio: 2023-01-09, Fecha de fin: 2023-01-10")
            ticker = input("Ingrese ticker a pedir: ")
            start_date = input("Ingrese fecha de inicio (YYYY-MM-DD): ")
            end_date = input("Ingrese fecha de fin (YYYY-MM-DD): ")
            print("Pidiendo datos...")
            data = fetch_data(ticker, start_date, end_date)
            if data:
                save_to_database(ticker, start_date, end_date, data)
        elif choice == "2":
            print("\n--- Visualización de datos ---")
            print("1. Resumen")
            print("2. Gráfico")
            sub_choice = input("Seleccione una opción: ")

            if sub_choice == "1":
                summary = read_summary_from_database()
                print("\nLos tickers guardados en la base de datos son:")
                for row in summary:
                    print(f"{row[0]} - {row[1]} <-> {row[2]}")
            elif sub_choice == "2":
                print("Ejemplo: Para graficar, puede usar el ticker guardado: AAPL")
                ticker = input("Ingrese el ticker a graficar: ")
                data = read_data_for_plot(ticker)
                if data:
                    plot_data(data)
                else:
                    print("No se encontraron datos para el ticker ingresado.")
        elif choice == "3":
            get_last_update_log()
        elif choice == "4":
            list_tickers()
        elif choice == "5":
            clear_database()
        elif choice == "6":
            print("Saliendo del programa.")
            break
        else:
            print("Opción inválida. Intente nuevamente.")

if __name__ == "__main__":
    main_menu()
