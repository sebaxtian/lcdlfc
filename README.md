# lcdlfc: La Casa de los Famosos Colombia - 2024

Este proyecto consiste en la automatización del proceso de votaciones publicadas por el programa "La Casa de los Famosos
Colombia - 2024". Las votaciones pueden ser para eliminación o salvación de participantes por parte del público, u otro
tipo de votaciones en las que el público puede elegir.

## Requerimientos

* Linux: Ubuntu 22.04.3 LTS
* Python 3.10+
* Poetry 1.7+
    * [Install Poetry](https://python-poetry.org/docs/#installation)
* Chrome Browser for Testing
    * [Stable](https://googlechromelabs.github.io/chrome-for-testing/#stable)
* Chrome Driver for Testing
    * [Stable](https://googlechromelabs.github.io/chrome-for-testing/#stable)

## ¿Cómo usar?

Lea y ejecute cada paso a continuación:

### Paso 1

Instalar poetry usando el script:

```bash
./install-poetry.sh
```

Agregar poetry al PATH:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Tambien puede agregar poetry al final del archivo .bashrc:

```bash
nano ~/.bashrc
```

### Paso 2

Comando para decirle a poetry qué versión de Python usar para el proyecto actual:

```bash
poetry env use 3.12
```

### Paso 3

Activando el entorno virtual:

```bash
poetry shell
```

### Paso 4

Instalando dependencias:

```bash
poetry install --no-root
```

### Paso 5

Descargue la aplicación Chrome y el driver para pruebas y copie cada uno en la carpeta específica:

* Chrome App: **.webbrowser/app**
* Chrome Driver: **.webbrowser/driver**

### Opcional

Visualización de la información del entorno:

```bash
poetry env info
```

Agrega los paquetes necesarios a su pyproject.toml y los instala:

```bash
poetry add selenium
```

Desactivar el entorno virtual y salir:

```bash
exit
# Para desactivar el entorno virtual sin salir del shell utilice desactivar
deactivate
```

## Ejecutar Proceso de Votaciones

Desde el la raiz del proyecto ejecutar el archivo main de python:

```bash
python main.py
```

---

***Eso es todo por ahora ...***

---

#### Licencia

[MIT License](./LICENSE)

[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/?ref=chooser-v1)

#### Acerca de mí

[https://about.me/sebaxtian](https://about.me/sebaxtian)
