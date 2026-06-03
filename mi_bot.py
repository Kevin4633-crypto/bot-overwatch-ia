import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import ollama
import fitz  # PyMuPDF
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. Configuración de Clientes
qdrant_client = QdrantClient(host="localhost", port=6333)
COLLECTION_NAME = "documentos_pdf"

# FORZAR RECREACIÓN: Borramos la colección vieja si existe para cambiar el tamaño a 1024
try:
    if qdrant_client.collection_exists(collection_name=COLLECTION_NAME):
        qdrant_client.delete_collection(collection_name=COLLECTION_NAME)
        print(f"Colección antigua '{COLLECTION_NAME}' eliminada para actualizar tamaño.")
    
    # Crear la colección con el tamaño correcto de 1024 para mxbai-embed-large
    qdrant_client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
    )
    print(f"Colección '{COLLECTION_NAME}' creada con éxito con dimensión 1024.")
except Exception as e:
    print(f"Error al configurar la colección: {e}")

# 2. Funciones de Procesamiento RAG (Ingestión y Recuperación)
def get_embedding(text: str):
    """Genera embeddings usando Ollama (modelo mxbai-embed-large)."""
    response = ollama.embeddings(model="mxbai-embed-large", prompt=text)
    return response["embedding"]

def ingest_pdf(pdf_path: str):
    """Extrae el texto del PDF, lo divide en fragmentos y lo sube a Qdrant."""
    print(f"[INGEST] Procesando {pdf_path}...")
    doc = fitz.open(pdf_path)
    text_completo = ""
    for page in doc:
        text_completo += page.get_text()

    # Dividir el texto en fragmentos pequeños para que la IA los entienda mejor
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_text(text_completo)

    points = []
    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)
        points.append(
            PointStruct(
                id=i,
                vector=embedding,
                payload={"text": chunk, "source": pdf_path}
            )
        )

    # Subir vectores a Qdrant
    qdrant_client.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"[INGEST] ✓ {len(points)} puntos indexados con éxito en Qdrant.")

def buscar_contexto(query: str, limit: int = 3):
    """Busca los fragmentos de texto más relevantes en Qdrant usando query_points."""
    query_vector = get_embedding(query)
    search_result = qdrant_client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=limit
    )
    # Extraemos el texto de los puntos encontrados
    contexto = "\n---\n".join([point.payload["text"] for point in search_result.points])
    return contexto

def generar_respuesta_ia(contexto: str, pregunta: str):
    """Consulta a Ollama usando el contexto recuperado del PDF."""
    prompt = f"""
    Eres un asistente experto y un entrenador especializado en Overwatch 2. Tu objetivo es ayudar al usuario a elegir las mejores ventajas (perks) y superperks según sus personajes o su estilo de juego basándote estrictamente en la información provista.

    Información de referencia (Contexto del PDF):
    {contexto}

    Pregunta del usuario:
    {pregunta}

    Respuesta (sé claro, directo, con buen tono gamer y organiza la información usando viñetas si es necesario):
    """
    response = ollama.generate(model="qwen2.5:1.5b", prompt=prompt)
    return response["response"]

# 3. Controladores de Telegram
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start de Telegram."""
    await update.message.reply_text(
        "¡Hola Kevin! Soy tu asistente de Inteligencia Artificial para Overwatch 2. "
        "Pregúntame sobre las mejores perks para cualquier personaje o dime cuál es tu estilo "
        "de juego para recomendarte la mejor superperk. ¿A quién elegimos hoy?"
    )

async def atender_consulta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja los mensajes de texto ordinarios enviados al bot."""
    pregunta_usuario = update.message.text
    print(f"[BOT] Pregunta recibida: {pregunta_usuario}")
    
    # Enviar un mensaje temporal de "escribiendo..."
    mensaje_espera = await update.message.reply_text("Buscando en la guía táctica... 🎮")

    try:
        # 1. Buscar en el PDF guardado en Qdrant
        contexto_extraido = buscar_contexto(pregunta_usuario)
        
        # 2. Pasar el contexto a Llama3 para armar la respuesta
        respuesta_final = generar_respuesta_ia(contexto_extraido, pregunta_usuario)
        
        # 3. Responder al usuario en Telegram reemplazando el mensaje de espera
        await mensaje_espera.edit_text(respuesta_final)
    except Exception as e:
        print(f"[ERROR] Ocurrió un fallo al procesar: {e}")
        await mensaje_espera.edit_text("Lo siento, tuve un problema al leer la guía de perks. ¿Podrías intentar de nuevo?")

# 4. Función Principal de Arranque
def main():
    # Tu token de Telegram vinculado a tu bot
    TOKEN = "8729049179:AAFcLGtXSmbFKxJZSfQUT9XYbrWQR3nMRDE"
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, atender_consulta))
    
    # Carga automática de la guía completa de Overwatch 2
    try:
        pdf_a_cargar = "./overwatch_perks_completo.pdf"
        if os.path.exists(pdf_a_cargar):
            ingest_pdf(pdf_a_cargar)
        else:
            print(f"[ADVERTENCIA] No se encontró el archivo '{pdf_a_cargar}'. Asegúrate de correr primero 'python crear_guia.py'.")
    except Exception as e:
        print(f"[ADVERTENCIA] No se pudo indexar el PDF automáticamente: {e}")

    print("Bot con Inteligencia Artificial Iniciado...")
    application.run_polling()

if __name__ == '__main__':
    main()