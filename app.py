from flask import Flask, jsonify, request
import json
import pandas as pd
from sqlalchemy import create_engine
import math

# engine = create_engine("sqlite:///db.db")
# url = "postgresql://postgres:password@34.16.85.147:5432/database3"
# engine = create_engine(url)

# Flask, needed



def calcular_cuotas_por_tipo(gastos_previstos, cantidad_vecinos, vecinos_con_bajo, vecinos_con_atico,  cuota_inicial):
    cuotas_con_bajo = []
    cuotas_sin_bajo = []
    cuota_con_atico = []

    coef_con_bajo = 0.2
    coef_atico = 0.2
    coef_resto = 0.6

    
    for año_del_pago, gasto_previsto in gastos_previstos:
        contribucion_acumulada = gasto_previsto / año_del_pago
        
        cuota_bajo = coef_con_bajo * contribucion_acumulada
        cuota_atico = coef_atico * contribucion_acumulada
        cuota_resto = coef_resto * contribucion_acumulada

        cuota_por_vecino = (cuota_resto / cantidad_vecinos) + cuota_inicial
        cuota_vecino_con_bajo = cuota_por_vecino + (cuota_bajo / vecinos_con_bajo) + cuota_inicial
        cuota_vecino_con_atico = cuota_por_vecino + (cuota_atico / vecinos_con_atico) + cuota_inicial

        cuotas_con_bajo.append(cuota_vecino_con_bajo)
        cuotas_sin_bajo.append(cuota_por_vecino)
        cuota_con_atico.append(cuota_vecino_con_atico)

    return cuotas_con_bajo, cuotas_sin_bajo, cuota_con_atico

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "Cálculo cuota por vecino"



@app.route('/calculo/', methods=['POST'])
def calculo_cuota():

    data = request.json
    gastos_previstos = [(item['años'], item['monto']) for item in data.get('tuplas', [])]

    cantidad_vecinos = 12 
    # vecinos_con_bajo = 2 
    # vecinos_con_atico = 1 

    cuota_inicial = 40 

    # cuotas_vecino_con_bajo, cuotas_vecino, cuotas_vecino_con_atico = calcular_cuotas_por_tipo(gastos_previstos, cantidad_vecinos=cantidad_vecinos, cuota_inicial=cuota_inicial)

    # cuotas_vecino_con_bajo = [round(valor, 2) for valor in cuotas_vecino_con_bajo]
    # cuotas_vecino = [round(valor, 2) for valor in cuotas_vecino]
    # cuotas_vecino_con_atico = [round(valor, 2) for valor in cuotas_vecino_con_atico]

    

    output = calcular_cuotas_por_tipo(gastos_previstos, n_propie=cantidad_vecinos, cuota=cuota_inicial)

    return jsonify({'Nueva/s cuota/s': output})


# (5, 3000), (7, 1500)
    

if __name__ == "__main__":
	app.run(debug=True, port=8000)