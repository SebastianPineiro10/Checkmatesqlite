# Instrucciones para configurar el entorno de desarrollo

Sigue los pasos a continuación para configurar el entorno virtual y las dependencias de este proyecto en **macOS** y **Windows**.

## Descripción

Este proyecto requiere configurar un entorno virtual y las dependencias necesarias para su ejecución en tu máquina local. A continuación se detallan los pasos tanto para **macOS** como para **Windows**.

---

## Para usuarios de **macOS**:

### Crear el entorno virtual

Para crear un entorno virtual, ejecuta el siguiente comando en el directorio de tu proyecto:

`python3 -m venv venv`

### Activar el entorno virtual

Activa el entorno virtual con el siguiente comando:

`source venv/bin/activate`

El prompt de la terminal mostrará el nombre del entorno (`venv`), indicando que está activado.

### Instalar las dependencias desde `requirements.txt`

Con el entorno virtual activo, instala las dependencias necesarias con:

`pip install -r requirements.txt`

### Verificar las dependencias instaladas

Para verificar que las dependencias se instalaron correctamente, ejecuta:

`pip list`

Este comando te mostrará una lista de los paquetes instalados en tu entorno virtual.

### Desactivar el entorno virtual

Cuando hayas terminado de trabajar, puedes desactivar el entorno virtual con:

`deactivate`

---



## Para usuarios de **Windows**:

### Crear el entorno virtual

Para crear un entorno virtual, ejecuta el siguiente comando en el directorio de tu proyecto:

`python -m venv venv`

### Activar el entorno virtual

Para activar el entorno virtual en **Windows**, usa el siguiente comando:

`.\\venv\\Scripts\\activate`

El prompt de la terminal mostrará el nombre del entorno (`venv`), indicando que está activado.

### Instalar las dependencias desde `requirements.txt`

Con el entorno virtual activo, instala las dependencias necesarias con:

`pip install -r requirements.txt`

### Verificar las dependencias instaladas

Para verificar que las dependencias se instalaron correctamente, ejecuta:

`pip list`

Este comando te mostrará una lista de los paquetes instalados en tu entorno virtual.

### Desactivar el entorno virtual

Cuando hayas terminado de trabajar, puedes desactivar el entorno virtual con:

`deactivate`

---

## ¿Qué hacer si no tienes **pip** instalado?

Si no tienes **pip** instalado, puedes instalarlo siguiendo estos pasos:

### Para **macOS** y **Linux**:
`sudo easy_install pip`

### Para **Windows**:
Si usas Python 3.4 o superior, **pip** ya debería estar instalado por defecto. Si no es así, puedes seguir [estas instrucciones](https://pip.pypa.io/en/stable/installation/) para instalarlo manualmente.

---

## ¡Listo para ejecutar!

¡Con estos pasos deberías tener todo listo para ejecutar tu aplicación en **macOS** o **Windows**! Si tienes alguna pregunta adicional o encuentras algún problema, no dudes en preguntar.
