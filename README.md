# 🎮 Bot de Telegram para Overwatch 2 con Inteligencia Artificial (RAG Local)

¡Bienvenido! Este proyecto consiste en un asistente inteligente para **Telegram** diseñado para responder preguntas avanzadas
sobre los mejores *perks* y *superperks* de los héroes de Overwatch 2. 

El sistema implementa una arquitectura **RAG (Generación Aumentada por Recuperación)** corriendo de forma **100% local**.
Esto significa que la IA no inventa las respuestas (no alucina),
sino que primero busca la información real dentro de una guía en formato PDF y luego redacta una respuesta precisa
basada estrictamente en ese documento.

---

## 🛠️ Tecnologías y Arquitectura Utilizadas

El bot se sostiene sobre una infraestructura moderna dividida en contenedores y servicios locales:

* **Python 3.14 (Entorno Virtual):** El lenguaje y núcleo del proyecto, encargado de orquestar
  la comunicación entre la API de Telegram, la base de datos y los modelos de IA.
* **Docker Desktop:** Utilizado para levantar y gestionar los servicios externos de manera limpia y aislada a través de contenedores.
* **Qdrant (Vector Database):** Base de datos vectorial indexada en el puerto `6333`.
  Almacena los fragmentos del PDF convertidos en vectores matemáticos de **1024 dimensiones**.
* **Ollama (Local LLM Server):** Motor que ejecuta los modelos de Inteligencia Artificial localmente en el puerto `11434`,
   eliminando la necesidad de usar APIs de pago como OpenAI.
* **Telegram Bot API (`python-telegram-bot`):** Conexión segura con la app de Telegram mediante la técnica de *Polling*
   (sondeo constante desde la PC local), evitando abrir puertos en el router del hogar.

---

## 📄 Estructura de Archivos Entregados

El repositorio contiene los archivos esenciales de código fuente y documentación:

1.  **`mi_bot.py`:** El script principal del sistema.
    Contiene los manejadores de Telegram (`/start` y mensajes de texto), la función de búsqueda
    semántica en Qdrant empleando `query_points` y la estructura del *prompt* enviado a la IA.
4.  **`crear_guia.py`:** Script auxiliar utilizado para generar automáticamente el documento PDF
5.  que sirve como base de conocimientos del bot.
6.  **`overwatch_perks_completo.pdf`**: La guía oficial generada que contiene los datos técnicos de los perks
    de héroes como Pharah, Genji, D.Va, Ana, entre otros.
8.  **`.gitignore`**: Archivo de exclusión que evita subir carpetas pesadas de configuración local (`mi_entorno/`, `ollama_data/`)
9.  al repositorio público de GitHub.

---

## 🧠 Modelos de IA Optimizados

Para garantizar que el bot responda al instante y no sature la memoria RAM del equipo (evitando el error crítico del sistema `signal: killed` producido por modelos pesados como Llama 3 de 8B), el proyecto fue optimizado con los siguientes modelos ligeros:

1.  **`mxbai-embed-large` (Embedding):** Toma el texto estructurado del PDF y las preguntas
2.  del usuario para traducirlos a vectores de **1024 magnitudes**. Es el encargado de la comprensión semántica.
4.  **`qwen2.5:1.5b` (Generación de Texto):** Modelo de lenguaje (LLM) de 1.5 mil millones de parámetros.
5. < Su tamaño compacto requiere menos de 2 GB de RAM, ofreciendo respuestas fluidas, rápidas y con un excelente contexto de jerga gamer.

---

## 🚀 Guía Detallada de Instalación y Despliegue

Sigue estos pasos en orden para clonar, configurar y ejecutar el proyecto desde cero en cualquier entorno compatible (Ubuntu/WSL/Linux):

### Paso 1: Preparar la Infraestructura en Docker
Antes de iniciar el código de Python, los motores del proyecto deben estar activos en Docker Desktop.

1. Abre **Docker Desktop**.
2. Asegúrate de tener descargadas y corriendo las imágenes de **Qdrant** y **Ollama**.
3. Los contenedores deben exponer correctamente los puertos por defecto:
   * Qdrant: `6333:6333`
   * Ollama: `11434:11434`

### Paso 2: Descargar los Modelos de IA dentro del Contenedor
Abre una terminal en tu sistema y ejecuta los siguientes comandos para descargar
los modelos optimizados directamente dentro de tu contenedor de Ollama:

### Paso 3: Configurar el Entorno de Python
# 1. Entrar a la carpeta del proyecto
cd ~/progra_3/proyecto/"Nueva carpeta"

# 2. Activar el entorno virtual de Python
source mi_entorno/bin/activate

# 3. Asegurar las librerías necesarias (en caso de reinstalación)
pip install python-telegram-bot qdrant-client ollama pymupdf

Paso 4: Configurar las Credenciales (Token de Telegram)
TOKEN = "TU_TELEGRAM_BOT_TOKEN_AQUÍ"

Paso 5: Ejecución del Asistente
python mi_bot.py<
```bash
# Descargar el modelo para generar vectores (Embeddings)
docker exec -it ollama ollama pull mxbai-embed-large

# Descargar el cerebro de IA ligero para redactar respuestas
docker exec -it ollama ollama pull qwen2.5:1.5b
