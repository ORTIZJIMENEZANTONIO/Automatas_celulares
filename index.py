from flask import Flask, render_template, request, jsonify
import json
import numpy as np
import random
import math

app = Flask(__name__) 

def bin_8( regla ):
 binario = bin ( int(regla) )
 binario = binario.replace( "0b", "" )
 bin_tam = len ( binario )
 if bin_tam<8:
  while bin_tam < 8:
   binario = "0" + binario
   bin_tam+=1
 return binario[::-1] 

def obtener_regla( regla ):
  universo = np.array(['000', '001', '010', '011', '100', '101', '110', '111'])
  binario  = bin_8(regla)
  array_asociativo = {}
  counter = 0
  while counter < len(binario):
   letra = binario[counter]
   #print(str(universo[counter]) + "->" + str(letra))
   array_asociativo[universo[counter]] = letra
   counter += 1
  return array_asociativo

@app.route('/')
def init(): 
 return render_template('index.html')

@app.route('/algo/<int:num>')
def index(num):
 if num == 1:
  pass
  return render_template('automata.html', num=str(num))

@app.route('/proces', methods=['POST'])
def draw_automata():
  content  = request.get_json()
  response = ' '
  filas 	 = int(content['generaciones'])
  columnas = int(content['celulas'])
  regla 	 = content['regla']
  tipo		 = content['tipo']
  porcentaje = int(content['porcentaje'])/100
  graph_generaciones = "'G-0', "
  array_asociativo   = obtener_regla( regla )
  principal  = list()
  secundario = list()
  graph_generaciones = ""
  graph_celulas = ""
  graph_0 = ""
  graph_1 = ""
  graph_0_media = ''
  graph_1_media = ''
  graph_0_varianza = ''
  graph_1_varianza = ''
  count_0 = 0
  count_1 = 0
  varianza_0_array = list()
  varianza_1_array = list()
  state_left  = ""
  state_right = ""
  state_center= ""
  try:
   if tipo == "1":
    j = 0
    while j < columnas:
     a = np.arange(10)
     p = np.zeros_like(a, dtype=float)
     p[0] = 1.0 - porcentaje
     p[1] = porcentaje
     state = np.random.choice(a, 1, p=p)
     state = str(state[0])
     principal.append(state)
     j += 1
    #print(principal)
   elif tipo == "0":
    j = 0
    while j < columnas:
     if j == math.ceil(columnas/2):
      principal.append('1')
     else:
      principal.append('0')
     j += 1

   tam = len(principal)
   i = 0
   while i<filas:
     pass
     graph_generaciones += "'G-"+str(i)+"',";
     response +="<tr>";
     k = 0
     while k<tam:
       pass
       state_center = principal[k]
       if k == 0:
        state_left = principal[tam-1];
        state_right = principal[k+1];
       elif k == tam-1: 
         state_left = principal[k-1];
         state_right = principal[0];
       else:
         state_right = principal[k+1];
         state_left = principal[k-1];

       comparar = state_left + state_center + state_right
       secundario.append(array_asociativo[comparar])

       if principal[k] == "1" :
         if (columnas>200) :
          response +=  "<td class='bg-dark' style='border: 1mm solid #464855'></td>";
          varianza_1_array.append(1)
          varianza_0_array.append(0)
         else:
          response += "<td class='p-1 bg-dark' style='border: 1px solid #464855'></td>";
         count_1+=1
         varianza_1_array.append(1)
         varianza_0_array.append(0)

       elif principal[k] == "0" :
        if columnas>200 :
         response += "<td class=' bg-white' style='border: 1mm solid #E5E5E5'></td>";
         varianza_0_array.append(1)
         varianza_1_array.append(0)
        else:
         response += "<td class='p-1 bg-white' style='border: 1px solid #464855'></td>";
        count_0+=1
        varianza_0_array.append(1)
        varianza_1_array.append(0)

       k+=1

     response += '</tr>'

     graph_0 += str(count_0)+", "
     graph_1 += str(count_1)+", "
     graph_0_media += str(np.mean(varianza_0_array))+", "
     graph_1_media += str(np.mean(varianza_1_array))+", "
     graph_0_varianza += str(np.var(varianza_0_array))+", "
     graph_1_varianza += str(np.var(varianza_1_array))+", "
     count_0 = 0
     count_1 = 0
     principal.clear()
     principal = list(secundario)  
     secundario.clear()
     i += 1

   response += "<script type='text/javascript'>"
      
   response += "if (window.lineChart) {"
   response += "window.lineChart.clear();"
   response += "window.lineChart.destroy();"
   response += "}"

   response += "if (window.lineChart_2) {"
   response += "window.lineChart_2.clear();"
   response += "window.lineChart_2.destroy();"
   response += "}"

   response += "if (window.lineChart_3) {"
   response += "window.lineChart_3.clear();"
   response += "window.lineChart_3.destroy();"
   response += "}"

   response += "$('#column-chart').empty();"
   response += "$('#column-chart-2').empty();"
   response += "$('#column-chart-3').empty();"
   """
   response += "$('#varianza-0').empty();"
   response += "$('#varianza-1').empty();"
   response += "$('#varianza-0').append("+ str(np.var(varianza_0_array)) +");"
   response += "$('#varianza-1').append("+ str(np.var(varianza_1_array)) +");"
   response += "$('#media-0').empty();"
   response += "$('#media-1').empty();"
   response += "$('#media-0').append("+ str(np.mean(varianza_0_array)) +");"
   response += "$('#media-1').append("+ str(np.mean(varianza_1_array)) +");"
   """
   response += "var ctx = $('#column-chart');"
   response += "var ctx2 = $('#column-chart-2');"
   response += "var ctx3 = $('#column-chart-3');"

   response += "var chartOptions = {"
   response += "elements: {"
   response += "rectangle: {"
   response += "borderWidth: 2,"
   response += "borderColor: 'rgb(0, 255, 0)',"
   response += "borderSkipped: 'bottom'"
   response += "}"
   response += "},"
   response += "responsive: true,"
   response += "maintainAspectRatio: false,"
   response += "responsiveAnimationDuration:500,"
   response += "legend: {"
   response += "position: 'top',"
   response += "},"
   response += "scales: {"
   response += "xAxes: [{"
   response += "display: true,"
   response += "gridLines: {"
   response += "color: '#f3f3f3',"
   response += "drawTicks: false,"
   response += "},"
   response += "scaleLabel: {"
   response += "display: true,"
   response += "}"
   response += "}],"
   response += "yAxes: [{"
   response += "display: true,"
   response += "gridLines: {"
   response += "color: '#f3f3f3',"
   response += "drawTicks: false,"
   response += "},"
   response += "scaleLabel: {"
   response += "display: true,"
   response += "}"
   response += "}]"
   response += "}"
    
   response += "};"
   #Dsitribución de 0s y 1s
   response += "var chartData = {"
   response += "labels: [" + graph_generaciones +"],"
   response += "datasets: [{"
   response += "label: '0',"
   response += "data: ["+ graph_0 + "],"
   response += "backgroundColor: 'transparent',"
   response += "borderColor: '#183886'"
   response += "}, {"
   response += "label: '1',"
   response += "data: ["+ graph_1 +"],"
   response += "borderColor: '#862C18',"
   response += "backgroundColor: 'transparent',"
   response += "}]"
   response += "};"

   #Dsitribución de la MEDIA de 0s y 1s
   response += "var chartData2 = {"
   response += "labels: [" + graph_generaciones +"],"
   response += "datasets: [{"
   response += "label: '0',"
   response += "data: ["+ graph_0_media + "],"
   response += "backgroundColor: 'transparent',"
   response += "borderColor: '#183886'"
   response += "}, {"
   response += "label: '1',"
   response += "data: ["+ graph_1_media +"],"
   response += "borderColor: '#862C18',"
   response += "backgroundColor: 'transparent',"
   response += "}]"
   response += "};"

   #Dsitribución de la VARIANZA de 0s y 1s
   response += "var chartData3 = {"
   response += "labels: [" + graph_generaciones +"],"
   response += "datasets: [{"
   response += "label: '0',"
   response += "data: ["+ graph_0_varianza + "],"
   response += "backgroundColor: 'transparent',"
   response += "borderColor: '#183886'"
   response += "}, {"
   response += "label: '1',"
   response += "data: ["+ graph_1_varianza +"],"
   response += "borderColor: '#862C18',"
   response += "backgroundColor: 'transparent',"
   response += "}]"
   response += "};"


   #distribución
   response += "var config = {"
   response += "type: 'line',"

   response += "options : chartOptions,"

   response += "data : chartData"
   response += "};"
   #media
   response += "var config2 = {"
   response += "type: 'line',"

   response += "options : chartOptions,"

   response += "data : chartData2"
   response += "};"

   #varianza
   response += "var config3 = {"
   response += "type: 'line',"

   response += "options : chartOptions,"

   response += "data : chartData3"
   response += "};"

   response += "window.lineChart = new Chart(ctx, config);"
   response += "window.lineChart_2 = new Chart(ctx2, config2);"
   response += "window.lineChart_3 = new Chart(ctx3, config3);"

   response += "</script>"
  
  except:
   print("An exception occurred")
   response = "ocurrio un error"
  finally:
   return response
   
if __name__ == '__main__': 
 app.run(debug=True)
 #app.run()