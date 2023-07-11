# Generador de niveles de servicio

Para ejecutar este programa es necesario tener un archivo en  `resources/request.xlsx`. Cada fila representa un viaje con un origen, destino, modo y hora de viaje. 
## Dependencias

Para instalar todas las librerias necesarias para correr el programa basta con tener instalado pip y ejecutar el siguiente código en la línea de comandos
```sh
pip install -r requirements.txt
```
En caso de que el usuario prefiera usar un entorno de desarrollo se recomienda usar [pipenv](https://pypi.org/project/pipenv/) seguir los comandos 
```sh
pipenv shell
pipenv install -r requirements.txt
```
## Routes API

Para correr el programa usando [Routes API](https://developers.google.com/maps/documentation/routes) basta con ejecutar el siguiente código en la línea de comandos 

```sh
python main.py routes
```

## Directions API

Para correr el programa usando [Directions API](https://developers.google.com/maps/documentation/directions)  basta con ejecutar el siguiente código en la línea de comandos 

```sh
python main.py directions
```