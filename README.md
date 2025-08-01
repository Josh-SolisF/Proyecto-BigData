## Big Data, Ciencia de los Datos
### Proyecto 1: Joshua Solís
El repositorio actual comprende los archivos generados para el proyecto 1, que son necesarios para su correcto funcionamiento.

## Manual de Ejecución
Debe ejecutarse en este orden:
1. `bash build_image.sh` ( crear imagen con Docker).
2. `bash run-postgres.sh` (levanta la imagen de la Base de Datos).
    * Credenciales: usuario= `postgres`, contraseña=`pword`, puerto=`5433`
2. `bash run_image.sh`. Se levanta un contenedor con la imagen del paso anterior (`bd-tarea3`), el contenedor se llamará `bd-tarea3-container`. Si no esta disponible bash en esta etapa, puede ejecutar el comando: `docker run -p 8888:8888 -it --rm --name bd-tarea3-container bd-tarea3 /bin/bash`
3. Procure asegurarse de estar dentro del shell de Bash .
4. `bash jupyter-server.sh`. Ejecutamos el servidor de Jupyter.
5. Copiar el enlace al final de la salida generada por el paso anterior. No trate de acceder  únicamente contectando al puerto 8888 en `localhost`, porque le pedirá este token o clave de autenticación.

### Ejecución del cuaderno de Jupyter: cosas qué considerar
El cuaderno ya tiene las salidas de la última ejecución, la cual fue probada varias veces previo a realizar la entrega del trabajo. Si de igual forma se desea ejecutar, tenga los siguientes datos en cuenta:
* Durante todo el cuaderno se arroja unos warnings que se deben a la configuración de spark, cada vez que se dispara un hilo que utiliza una cantidad "alta" de memoria. Esto mejor no cambiarlo para evitar causar un error fatal. 

* Tanto el entrenamiento de RF, como el uso de Cross-Validation, así como la generación de los cuartiles y otras cosas más son muy lentos si se ejecutan en arquitecturas distintas a la de la plataforma del contenedor (amd64).

