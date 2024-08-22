## Web App en Producción
https://chatbot-khaki-zeta.vercel.app/

# Setup para ejecución local

### Environment Variables

Para /backend se debe crear un ```.env``` que siga el formato de ```.env.template``` encontrado en el repositorio

### Documentos
Dentro de ```/backend/data``` se deben introducir los archivos .pdf entregados para el desafío siguiendo el mismo nombre de archivo original. En caso de tener distintos nombres de archivos a los originales, cambiar parámetros en ```/backend/params.py```



# Instalación y Ejecución
## Frontend

Dentro de /frontend ejecutar ```pnpm install```. Luego correr con ```pnpm run dev```

## Backend

Dos maneras para instalar dependencias:
* Usando Poetry: ```poetry install```
* Usando pip: ```pip install -r requirements.txt```
En caso de tener problemas con la instalación, se recomienda descargar todas las librerías especificadas en el Colab entregado, además de ```flask``` y ```python-dotenv```.

Luego ejecutar app de Flask: ```python app.py```



