import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

hora_dia = ctrl.Antecedent(np.arange(0, 24, 1), 'hora_dia')
ocupacao = ctrl.Antecedent(np.arange(0, 11, 1), 'ocupacao')
tarifa = ctrl.Antecedent(np.arange(0, 11, 1), 'tarifa')
consumo_energia = ctrl.Consequent(np.arange(0, 101, 1), 'consumo_energia')

hora_dia['morning'] = fuzz.trimf(hora_dia.universe, [5, 8, 11])
hora_dia['afternoon'] = fuzz.trimf(hora_dia.universe, [12, 15, 18])
hora_dia['evening'] = fuzz.trimf(hora_dia.universe, [19, 21, 23])
hora_dia['night'] = fuzz.trimf(hora_dia.universe, [0, 3, 5])

ocupacao['low'] = fuzz.trapmf(ocupacao.universe, [0, 0, 2, 4])
ocupacao['medium'] = fuzz.trapmf(ocupacao.universe, [3, 5, 6, 8])
ocupacao['high'] = fuzz.trapmf(ocupacao.universe, [7, 9, 10, 10])

tarifa['low'] = fuzz.trimf(tarifa.universe, [0, 2, 4])
tarifa['medium'] = fuzz.trimf(tarifa.universe, [3, 5, 7])
tarifa['high'] = fuzz.trimf(tarifa.universe, [6, 8, 10])

consumo_energia['low'] = fuzz.trapmf(consumo_energia.universe, [0, 0, 20, 40])
consumo_energia['medium'] = fuzz.trapmf(consumo_energia.universe, [30, 50, 50, 70])
consumo_energia['high'] = fuzz.trapmf(consumo_energia.universe, [60, 80, 100, 100])

regra1 = ctrl.Rule(hora_dia['morning'] & ocupacao['low'] & tarifa['low'], consumo_energia['low'])
regra2 = ctrl.Rule(hora_dia['evening'] & ocupacao['high'] & tarifa['high'], consumo_energia['high'])
regra3 = ctrl.Rule(hora_dia['afternoon'] & ocupacao['medium'] & tarifa['medium'], consumo_energia['medium'])


sistema_controle = ctrl.ControlSystem([regra1, regra2, regra3])
sistema_simulacao = ctrl.ControlSystemSimulation(sistema_controle)


hora = float(input("Digite a hora do dia (0 a 23): "))
ocup = float(input("Digite o nível de ocupação (0 a 10): "))
tar = float(input("Digite a tarifa de energia (0 a 10): "))


sistema_simulacao.input['hora_dia'] = hora
sistema_simulacao.input['ocupacao'] = ocup
sistema_simulacao.input['tarifa'] = tar
sistema_simulacao.compute()

consumo = sistema_simulacao.output['consumo_energia']

if consumo <= 40:
    resultado = "baixo"
elif consumo <= 70:
    resultado = "médio"
else:
    resultado = "alto"

print(f"Para a hora do dia {hora}, ocupação {ocup}, tarifa {tar}, o consumo de energia é {consumo:.2f}, considerado {resultado}.")