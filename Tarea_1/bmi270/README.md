# Tarea 1

**Grupo**:
- Benjamín Contreras S.
- Emile Pirali
- José Miguel Zapata

## Observaciones

- Es necesario hacer flash a la ESP32 con el programa dentro de la carpeta "bmi270", una vez hecho, para controlarla desde python, es necesario correr el programa "receiver_plot.py" en una ambiente virtual con las librerías de "requirements.txt". Para correr el programa, es necesario correr una vez el programa de python, cancelarlo con CTR+X, y correr inmediatamente de nuevo el programa, si se logra ver strings en formato de bytes impresos en la consola, el programa está funcionando correctamente. 

- Para controlar el programa, hay que elegir un número de los que se indican y presionar enter, cualquier otro input bota el programa y es necesario iniciar el programa nuevamente (iniciando, cancelando e iniciando de nuevo). En la consola se irá presentando lo que se va leyendo, y al final del proceso se mostrarán gráficos con las medidas tomadas y procesadas.