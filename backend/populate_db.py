# backend/populate_db.py
import requests
import time
import os

# --- CONFIGURACIÓN INTERNA ---
# Al correr dentro del contenedor, nos conectamos directo a FastAPI (localhost:8000)
# en lugar de salir a Nginx.
API_URL = "http://localhost:8000/api/cases/"

# Obtenemos credenciales directo de las variables de entorno del contenedor
# Esto es más seguro que escribirlas en el código.
USERNAME = os.getenv("API_USERNAME", "admin")
PASSWORD = os.getenv("API_PASSWORD", "secretpassword")

CASES_TO_INSERT = [
    {
        "title": "Ruido en suspensión delantera",
        "vehicle_model": "Tiguan",
        "year": 2021,
        "construction_group": "Suspensión",
        "problem_description": "El cliente reporta un ruido tipo 'golpe seco' (clunk) al pasar por baches o reductores de velocidad, especialmente en el lado derecho.",
        "solution_description": "Se diagnosticó desgaste prematuro en los bujes de la horquilla inferior. Se reemplazaron ambos bujes y se realizó alineación. Ruido eliminado."
    },
    {
        "title": "Pérdida de potencia y Check Engine",
        "vehicle_model": "Jetta",
        "year": 2019,
        "construction_group": "Motor",
        "problem_description": "Motor vibra en ralentí y testigo de motor encendido. Escáner muestra código P0300 (Misfire aleatorio).",
        "solution_description": "Bobina de encendido del cilindro 3 defectuosa. Se reemplazó la bobina y las 4 bujías por mantenimiento preventivo."
    },
    {
        "title": "Falla en elevador de cristal",
        "vehicle_model": "Golf",
        "year": 2018,
        "construction_group": "Eléctrico",
        "problem_description": "La ventana del conductor baja pero no sube con el botón automático. Se escucha el motor funcionar pero el cristal no se mueve.",
        "solution_description": "Soportes plásticos del mecanismo elevador rotos. Se reemplazó el kit de reparación del elevador sin cambiar el motor."
    },
    {
        "title": "Vibración al frenar a alta velocidad",
        "vehicle_model": "Taos",
        "year": 2022,
        "construction_group": "Frenos",
        "problem_description": "Al frenar bajando de 100 km/h a 80 km/h se siente vibración fuerte en el volante.",
        "solution_description": "Discos delanteros alabeados (deformados) por choque térmico. Se rectificaron discos y se cambiaron balatas."
    },
    {
        "title": "Golpe al insertar reversa",
        "vehicle_model": "Amarok",
        "year": 2020,
        "construction_group": "Transmisión",
        "problem_description": "Transmisión automática golpea fuerte al pasar de P a R en frío.",
        "solution_description": "Nivel de aceite ATF bajo y software de TCU desactualizado. Se rellenó nivel y se realizó ajuste básico con escáner ODIS."
    },
    {
        "title": "Aire acondicionado no enfría",
        "vehicle_model": "Vento",
        "year": 2017,
        "construction_group": "Climatización",
        "problem_description": "Sale aire a temperatura ambiente. El compresor no entra.",
        "solution_description": "Fuga de gas refrigerante en el condensador (piedra en carretera). Se cambió condensador y se recargó gas R134a."
    },
    {
        "title": "Pantalla negra en infoentretenimiento",
        "vehicle_model": "ID.4",
        "year": 2023,
        "construction_group": "Infoentretenimiento",
        "problem_description": "La pantalla central se queda en negro al encender el auto, aunque el radio se escucha.",
        "solution_description": "Bloqueo de software en el módulo 5F. Se realizó reinicio forzado (Hard Reset) desconectando batería de 12V por 10 minutos y actualizando firmware."
    },
    {
        "title": "Olor a gasolina en cabina",
        "vehicle_model": "Saveiro",
        "year": 2016,
        "construction_group": "Motor",
        "problem_description": "Fuerte olor a combustible al encender el aire acondicionado.",
        "solution_description": "Oring de inyectores resecos permitiendo pequeña fuga. Se cambiaron sellos de inyectores y se lavó el motor."
    },
    {
        "title": "Testigo de ABS encendido",
        "vehicle_model": "Polo",
        "year": 2020,
        "construction_group": "Frenos",
        "problem_description": "Luces de ABS y Control de Tracción encendidas en el tablero de forma intermitente.",
        "solution_description": "Sensor de velocidad de rueda trasera izquierda sucio con lodo metálico. Se limpió el sensor y la pista magnética de la maza."
    },
    {
        "title": "Cajuela no abre eléctricamente",
        "vehicle_model": "Teramont",
        "year": 2021,
        "construction_group": "Carrocería",
        "problem_description": "El portón trasero eléctrico hace tres pitidos y no abre.",
        "solution_description": "Desalineación en las bisagras detectada por los sensores de aprisionamiento. Se ajustaron bisagras y se realizó ajuste básico."
    }
]

def populate():
    print(f"🚀 [MODO CONTENEDOR] Iniciando carga de {len(CASES_TO_INSERT)} casos...")
    print(f"📡 Target: {API_URL}")

    success_count = 0
    
    for case in CASES_TO_INSERT:
        try:
            print(f"   ➡️  Procesando: {case['title']}...", end=" ")
            
            response = requests.post(
                API_URL,
                json=case,
                auth=(USERNAME, PASSWORD),
                timeout=15 
            )

            if response.status_code in [200, 201]:
                print("✅ OK")
                success_count += 1
            else:
                print(f"❌ Error {response.status_code}: {response.text}")

        except Exception as e:
            print(f"❌ Excepción: {e}")
        
        time.sleep(0.5)

    print("\n" + "="*40)
    print(f"🏁 Carga completada: {success_count}/{len(CASES_TO_INSERT)} insertados.")

if __name__ == "__main__":
    populate()