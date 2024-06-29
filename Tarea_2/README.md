# Tarea 1

**Grupo**:
- Benjamín Contreras S.
- Emile Pirali
- José Miguel Zapata

## Observaciones

- Es necesario hacer flash a la ESP32 con el programa dentro de la carpeta "Tarea_2", una vez hecho, para controlarla desde python, es necesario correr el programa "main.py" en una ambiente virtual con las librerías de "requirements_windows.txt". Para correr el programa, se debe conectar primero la ESP32 junto al sensor deseado, y luego correr el programa "main.py"m si se logra ver strings en formato de bytes impresos en la consola, el programa está funcionando correctamente, si nada ocurre, cerrar el programa, desconectar y conectar la ESP32 e intentar de nuevo.

- Para controlar el programa, hay que elegir los valores que se utilizarán en los dropdown, (acelerómetro, giroscopio, modo de operación), y el tamaño de la ventana (spinbox), una vez se está satisfecho con los parámetros, *SE DEBE APRETAR EL BOTÓN* "Iniciar configuración" y *LUEGO* "Iniciar captación de datos". Una vez captados y procesados los datos, los gráficos se mostrarán en la parte inferior, donde se puede ir al gráfico siguiente o anterior con los botones correspondientes.

- Se debe reiniciar el programa para poder utilizar otro sensor.