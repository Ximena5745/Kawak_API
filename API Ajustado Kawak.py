import os
import requests
import json
import pandas as pd
import time
import csv
from pathlib import Path
from dotenv import load_dotenv

# ─── Carga automática del archivo .env ───────────────────────────────────────
# El archivo .env debe estar en la misma carpeta que este script.
# Nunca subas .env a git (está en .gitignore).
_env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=_env_path)

_EMAIL     = os.environ.get("KAWAK_EMAIL",     "")
_PASSWORD  = os.environ.get("KAWAK_PASSWORD",  "")
_INSTANCIA = os.environ.get("KAWAK_INSTANCIA", "")

if not all([_EMAIL, _PASSWORD, _INSTANCIA]):
    raise EnvironmentError(
        "Faltan credenciales. Crea el archivo .env en la misma carpeta con:\n"
        "  KAWAK_EMAIL=tu_email\n"
        "  KAWAK_PASSWORD=tu_contraseña\n"
        "  KAWAK_INSTANCIA=nombre_instancia\n"
        "Consulta .env.example como guía."
    )

# Authentications
url = "https://api.kawak.com.co/login"
payload = {
    "email":     _EMAIL,
    "password":  _PASSWORD,
    "instancia": _INSTANCIA,
}
response = requests.post(url, json=payload)
response.raise_for_status()

try:
    token = response.json()["message"]["Authorization"]
except KeyError:
    print("Error: 'Authorization' token not found in the response.")
    print("Response content:", response.text)
    raise
headers2= {
    'Authorization': token,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

def fetch_data(ff, f, npage, headers):
    url = "https://api.kawak.com.co/api/v1/indicadores/result"
    payload = json.dumps({
        "cutoffDate": ff,
        "frequency": f,
        "page": npage
    })
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 500:
        print(f"Internal Server Error for date {ff}, frequency {f}, page {npage}")
        return None
    response.raise_for_status()  # Check for other request errors
    return response.json()

def Api_Kawak(head,url):   
    try:
        response = requests.get(url,headers=head)  
        if response.status_code == 200:
            print("Solicitud exitosa:")
            print(response.json())  # Imprimir la respuesta en formato JSON
        else:
            print(f"Error: {response.status_code}")
            print(response.text)  # Imprimir el cuerpo de la respuesta en caso de error
    except Exception as e:
        print(f"Excepción: {e}")
    return response.json()

def mostrar_menu():
    print("\nMenú de opciones:")
    print("1. Indicadores")
    print("2. Salidas No Conformes")
    print("3. Acciones Mejora")
    print("4. Documentos")
    print("5. Riesgos")
    print("6. Salir")

def opcion_1():
    print("Ejecutando opción 1: indicadores.")
    df_ind = None
    dates = ["2022-01-31", "2022-02-28", "2022-03-31", "2022-04-30","2022-05-31","2022-06-30","2022-07-31","2022-08-31","2022-09-30","2022-10-31","2022-11-30", "2022-12-31", "2023-01-31", "2023-02-28", "2023-03-31", "2023-04-30", "2023-05-31","2023-06-30","2023-07-31","2023-08-31","2023-09-30","2023-10-31","2023-11-30","2023-12-31", "2024-01-31", "2024-02-29", "2024-03-31", "2024-04-30", "2024-05-31","2024-06-30","2024-07-31","2024-08-31","2024-09-30","2024-10-31","2024-11-30","2024-12-31", "2025-01-31", "2025-02-28", "2025-03-31", "2025-04-30", "2025-05-31","2025-06-30","2025-07-31","2025-08-31","2025-09-30","2025-10-31","2025-11-30","2025-12-31"]
    frequencies = [2, 3, 5, 6, 7]
    for ff in dates:
        for f in frequencies:
            npage = 1
            while True:
                response_data = fetch_data(ff, f, npage, {'Content-type': 'application/json', 'Authorization': token})
                if response_data is None:
                    break
                
                if 'message' not in response_data or 'data' not in response_data['message']:
                    print(f"No data found for date {ff} and frequency {f}")
                    break
                
                df_nested_list = pd.json_normalize(response_data["message"], record_path=['data'])
                df_nested_list['frecuencia'] = f
                if df_nested_list.empty:
                    print(f"No data returned for date {ff}, frequency {f}, and page {npage}")
                    break
                if df_ind is None:
                    df_ind = df_nested_list
                else:
                    df_ind = pd.concat([df_ind, df_nested_list])
                npage += 1
    # Save to Excel
    if df_ind is not None:
        df_ind.to_excel('Consulta_Cierre Agosto 16-09-25.xlsx', index=False)
    else:
        print("No data was retrieved.")

def opcion_2():
    print("Ejecutando opción 2: salidasNoConformes.")        
    try:
        SalidasNoConformes =  Api_Kawak(headers2,url = 'https://api.kawak.com.co/api/v1/salidasNoConformes/pool')
        if SalidasNoConformes and 'message' in SalidasNoConformes and 'data' in SalidasNoConformes['message']:
            data = SalidasNoConformes['message']['data']
            # Convertir los datos en un DataFrame de pandas
            df = pd.json_normalize(data)
            # Guardar el DataFrame en un archivo Excel
            output_file = "datos_api.xlsx"
            df.to_excel(output_file, index=False, engine='openpyxl')
            print(f"Datos guardados en {output_file}")
        else:
            print("No se encontraron datos válidos en la respuesta.")
    except Exception as e:
        print(f"Error al procesar opción 2: {e}")

def opcion_3():
    print("Ejecutando opción 3: Acciones de Mejora.")
    try:
        accionesMejora =  Api_Kawak(headers2,url='https://api.kawak.com.co/api/v1/accionesMejora')
        if accionesMejora and 'message' in accionesMejora and 'data' in accionesMejora['message']:
            dataMejora = accionesMejora['message']['data']
            # Convertir los datos en un DataFrame de pandas
            df = pd.json_normalize(dataMejora)
            # Guardar el DataFrame en un archivo Excel
            output_file = "datos_Mejora.xlsx"
            df.to_excel(output_file, index=False, engine='openpyxl')
            print(f"Datos guardados en {output_file}")
        else:
            print("No se encontraron datos válidos en la respuesta.")
    except Exception as e:
        print(f"Error al procesar opción 3: {e}")

def opcion_4():    
    print("Ejecutando opción 4: Guardar datos.")
    Documental =  Api_Kawak(headers2,url='https://api.kawak.com.co/api/v1/docs')
    if  Documental.get("status") == "error":
        print("Por favor, verifique la consulta SQL y asegúrese de que sea válida.")
    else:    
        dataDoc = Documental['message']['data']
        # Convertir los datos en un DataFrame de pandas
        df = pd.json_normalize(dataDoc)
        # Guardar el DataFrame en un archivo Excel
        output_file = "datos_Documental.xlsx"
        df.to_excel(output_file, index=False, engine='openpyxl')

###def opcion_5():
   # print("Ejecutando opción 5: ")
    #ControlRiesgos =  Api_Kawak(headers2,url='https://api.kawak.com.co/api/v1/controlesRiesgo?id_del_sistema_de_gestion_de_riesgos=10')
    #data = ControlRiesgos['message']['data']
    # Convertir los datos en un DataFrame de pandas
    #df = pd.json_normalize(data)
    # Guardar el DataFrame en un archivo Excel
    #output_file = "datos_Riesgos.xlsx"
    #df.to_excel(output_file, index=False, engine='openpyxl')


def opcion_5():
    print("Ejecutando opción 5: Riesgos")
    codigos = [6, 8, 9, 10, 11, 12, 13]
    output_file = "datos_Riesgos.xlsx"

    # Crear una lista para almacenar todos los DataFrames
    dataframes = []

    for codigo in codigos:
        try:
            print(f"Consultando código {codigo}...")
            ControlRiesgos = Api_Kawak(
                headers2,
                url=f'https://api.kawak.com.co/api/v1/controlesRiesgo?id_del_sistema_de_gestion_de_riesgos={codigo}'
            )
            if ControlRiesgos and 'message' in ControlRiesgos and 'data' in ControlRiesgos['message']:
                data = ControlRiesgos['message']['data']
                if data:  # Verificar que hay datos
                    # Convertir los datos en un DataFrame de pandas
                    df = pd.json_normalize(data)
                    # Añadir una columna para identificar el código
                    df['codigo'] = codigo
                    dataframes.append(df)
                else:
                    print(f"No hay datos para el código {codigo}")
            else:
                print(f"Respuesta inválida para el código {codigo}")
        except Exception as e:
            print(f"Error al procesar código {codigo}: {e}")

    if dataframes:
        # Combinar todos los DataFrames en uno solo
        df_combined = pd.concat(dataframes, ignore_index=True)
        # Guardar el DataFrame combinado en un archivo Excel
        df_combined.to_excel(output_file, index=False, engine='openpyxl')
        print(f"Datos guardados en el archivo {output_file}.")
    else:
        print("No se obtuvieron datos para procesar.")

def salir():
    print("Saliendo del programa. ¡Hasta luego!")

while True:
    mostrar_menu()  # Muestra el menú
    opcion = input("Seleccione una opción (1-6): ")

    if opcion == "1":
        opcion_1()
    elif opcion == "2":
        opcion_2()
    elif opcion == "3":
        opcion_3()
    elif opcion == "4":
        opcion_4()
    elif opcion == "5":
        opcion_5()        
    elif opcion == "6":
        salir()
        break           
    else:
        print("⚠️ Opción no válida. Intente de nuevo.")














