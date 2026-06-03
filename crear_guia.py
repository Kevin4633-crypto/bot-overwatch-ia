import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generar_pdf_overwatch():
    pdf_filename = "overwatch_perks_completo.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=22, spaceAfter=15, textColor="#F99E1A")
    role_style = ParagraphStyle('RoleStyle', parent=styles['Heading2'], fontSize=16, spaceBefore=15, spaceAfter=10, textColor="#405275")
    hero_style = ParagraphStyle('HeroStyle', parent=styles['Heading3'], fontSize=12, spaceBefore=8, spaceAfter=4, textColor="#00a8ff")
    body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=10, leading=14, spaceAfter=6)

    datos_overwatch = [
        ("ROL: TANQUES", [
            ("Reinhardt", "• Mejor Perk: 'Escudo Dinámico Reutilizable' (Aumenta la velocidad de regeneración del escudo un 20% tras romperlo).\n• Superperk por Estilo de Juego: Pasivo/Defensivo -> 'Baluarte Táctico'. Ofrece resistencia masiva al aguantar la carga con tu equipo."),
            ("D.Va", "• Mejor Perk: 'Propulsores de Micro-Misiles' (Reduce el enfriamiento de los propulsores si impactas todos los micro-misiles).\n• Superperk por Estilo de Juego: Agresivo/Flanker -> 'Adrenalina del Verdugo' para divear la línea trasera y escapar instantáneamente."),
            ("Winston", "• Mejor Perk: 'Salto Electrificado' (Genera un área de daño eléctrico al aterrizar con el salto).\n• Superperk por Estilo de Juego: Iniciador/Agresivo -> 'Impacto Conmocionante Potenciado' para desestabilizar la defense enemiga."),
            ("Doomfist", "• Mejor Perk: 'Bloqueo Generador' (Bloquear daño exitosamente reduce el tiempo de recarga del Puño Cohete).\n• Superperk por Estilo de Juego: Ultra Agresivo -> 'Adrenalina del Verdugo' para encadenar bajas en combo."),
            ("Orisa", "• Mejor Perk: 'Fortificación Reforzada' (Refleja un 10% del daño recibido mientras estés fortificado).\n• Superperk por Estilo de Juego: Defensivo/Anchor -> 'Baluarte Táctico' para volverte una muralla inamovible."),
            ("Sigma", "• Mejor Perk: 'Barrera Absorbente' (Convierte un 15% más de daño absorbido en escudos personales).\n• Superperk por Estilo de Juego: Técnico/Control -> 'Sinergia Definitiva' para lanzar el Flujo Gravitacional más rápido."),
        ]),
        ("ROL: DAÑO (DPS)", [
            ("Pharah (Fara)", "• Mejor Perk: 'Restauración de Combustible Crítica' (Impactos directos recuperan 15% de propulsores).\n• Superperk por Estilo de Juego: Agresivo Aéreo -> 'Propulsor de Emergencia' para huir automáticamente al tener baja vida."),
            ("Genji", "• Mejor Perk: 'Reflejo Letal' (Desviar ataques exitosamente aumenta tu velocidad de ataque un 10% durante 3s).\n• Superperk por Estilo de Juego: Flanker/Agresivo -> 'Adrenalina del Verdugo'. Crucial para reiniciar habilidades con la Hoja Dragón."),
            ("Tracer", "• Mejor Perk: 'Regresión Curativa Potenciada' (Regresar en el tiempo te cura un 20% adicional de la salud perdida).\n• Superperk por Estilo de Juego: Hostigador/Hit & Run -> 'Adrenalina del Verdugo' para mantener la presión constante."),
            ("Reaper", "• Mejor Perk: 'Cosecha de Almas Ampliada' (Aumenta el robo de vida pasivo al 40% a corta distancia).\n• Superperk por Estilo de Juego: Asesino Cercano -> 'Baluarte Táctico' para sobrevivir en medio del equipo enemigo."),
            ("Soldado: 76", "• Mejor Perk: 'Visor Táctico Optimizado' (Los disparos a la cabeza reducen el enfriamiento del Campo Biótico).\n• Superperk por Estilo de Juego: Tradicional/Sustento -> 'Sinergia Definitiva' para apoyar al equipo curando y atacando."),
            ("Cassidy", "• Mejor Perk: 'Evasión Recargada' (Rodar otorga inmunidad al daño durante 0.2 segundos).\n• Superperk por Estilo de Juego: Duelista/Táctico -> 'Impacto Conmocionante Potenciado' para mejorar tu granada magnética."),
            ("Hanzo", "• Mejor Perk: 'Flecha de Reconocimiento Persistente' (Los enemigos revelados reciben un 10% más de daño).\n• Superperk por Estilo de Juego: Francotirador Pasivo -> 'Baluarte Táctico' para asegurar posiciones elevadas."),
        ]),
        ("ROL: APOYO (SUPPORTS)", [
            ("Ana", "• Mejor Perk: 'Dardo Sedante de Respuesta' (Fallar el dardo reduce su enfriamiento a la mitad).\n• Superperk por Estilo de Juego: Utilidad/Control -> 'Impacto Conmocionante Potenciado' para que la granada biótica cure y dañe más."),
            ("Kiriko", "• Mejor Perk: 'Paso Rápido Purificador' (Teletransportarse limpia automáticamente efectos de estado negativos personales).\n• Superperk por Estilo de Juego: Ofensivo/Flanker -> 'Adrenalina del Verdugo' para conseguir bajas críticas con kunais."),
            ("Mercy", "• Mejor Perk: 'Resurrección Protegida' (Obtienes un escudo del 50% de tu vida máxima mientras resucitas a un aliado).\n• Superperk por Estilo de Juego: Pasivo puro/Bolsillo -> 'Baluarte Táctico' para resistir el foco enemigo mientras curas."),
            ("Baptiste", "• Mejor Perk: 'Matriz Amplificadora Eficiente' (Curar aliados dentro de tu Matriz carga tu Definitiva el doble de rápido).\n• Superperk por Estilo de Juego: Técnico/Tejedor -> 'Sinergia Definitiva' para cambiar el rumbo de las peleas de equipo."),
            ("Lucio", "• Mejor Perk: 'Ritmo de Pared Acelerado' (Desplazarse por paredes aumenta el radio de tus canciones un 30%).\n• Superperk por Estilo de Juego: Agresivo/Utilidad -> 'Impacto Conmocionante Potenciado' para empujar enemigos masivamente."),
            ("Moira", "• Mejor Perk: 'Evanescencia Prolongada' (Aumenta la distancia recorrida con Evanescencia un 25%).\n• Superperk por Estilo de Juego: Sanación Masiva / Agresivo -> 'Adrenalina del Verdugo' para recargar energía biótica rápido."),
        ])
    ]

    story.append(Paragraph("GUÍA MAESTRA DE PERKS Y ESTILOS DE JUEGO - OVERWATCH 2", title_style))
    story.append(Spacer(1, 15))

    for rol, heroes in datos_overwatch:
        story.append(Paragraph(rol, role_style))
        for heroe, info in heroes:
            story.append(Paragraph(heroe, hero_style))
            for linea in info.split('\n'):
                story.append(Paragraph(linea, body_style))
            story.append(Spacer(1, 5))
        story.append(Spacer(1, 10))

    doc.build(story)
    print(f"✓ ¡Archivo '{pdf_filename}' creado con todos los personajes con éxito!")

if __name__ == '__main__':
    generar_pdf_overwatch()