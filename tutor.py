import streamlit as st
import google.generativeai as genai
import re  # Para buscar la solución en la respuesta de Gemini

# --- Reemplaza con tu clave de API de Gemini ---
GOOGLE_API_KEY = "AIzaSyCOuE1e0BVXaXHnissaXUQxi4Wu5T79bqk"
# --- Fin de la clave de API ---

# Configura la API de Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# Inicializar la variable de sesión si no existe
if 'explicacion_recibida' not in st.session_state:
    st.session_state.explicacion_recibida = False
if 'mostrar_solucion' not in st.session_state:
    st.session_state.mostrar_solucion = False
if 'respuesta_con_solucion' not in st.session_state:
    st.session_state.respuesta_con_solucion = None

# Título de la aplicación
st.title("EduAI Tutor - Tu Tutor Virtual Personalizado")

# --- Sección para que el usuario elija un tema ---
tema_aprendizaje = st.selectbox("¿Qué tema te gustaría aprender hoy?",
                                  ["Álgebra", "Geometría", "Cálculo", "Programación", "Historia", "Ciencias"])

# --- Sección para que el usuario indique su nivel (opcional para adaptar la explicación inicial) ---
nivel_usuario = st.selectbox("¿Cuál es tu nivel de experiencia en este tema?",
                              ["Principiante", "Intermedio", "Avanzado"],
                              index=0)

st.subheader(f"Aprendiendo sobre: {tema_aprendizaje}")

# --- Botón para solicitar una explicación inicial ---
if st.button("Obtener Explicación"):
    prompt_explicacion = f"Explica el concepto básico de {tema_aprendizaje} para un estudiante de nivel {nivel_usuario}."
    try:
        response = model.generate_content(prompt_explicacion)
        st.info(response.text)
        st.session_state.explicacion_recibida = True
        st.session_state.respuesta_con_solucion = None # Resetear la respuesta con solución
        st.session_state.mostrar_solucion = False
    except Exception as e:
        st.error(f"Error al obtener la explicación: {e}")

# --- Sección para interactuar y pedir más detalles o ejercicios después de la explicación ---
if st.session_state.explicacion_recibida:
    pregunta_usuario = st.text_input("¿Tienes alguna pregunta o te gustaría practicar con un ejercicio?", "")
    if st.button("Enviar Pregunta/Solicitud"):
        if pregunta_usuario:
            prompt_interaccion = f"El estudiante preguntó: '{pregunta_usuario}'. Basándote en la explicación anterior sobre {tema_aprendizaje}, proporciona una respuesta clara o genera un ejercicio práctico relacionado. Si es un ejercicio, incluye la solución al final, marcada claramente como 'Solución:'."
            try:
                response = model.generate_content(prompt_interaccion)
                st.session_state.respuesta_con_solucion = response.text
                st.session_state.mostrar_solucion = False # Ocultar la solución inicialmente
            except Exception as e:
                st.error(f"Error al procesar tu pregunta/solicitud: {e}")
        else:
            st.warning("Por favor, ingresa tu pregunta o solicitud.")

    # Mostrar la respuesta (ejercicio) y el botón de solución si hay una respuesta con solución
    if st.session_state.respuesta_con_solucion:
        solucion_match = re.search(r"(Solución:\s*.*)", st.session_state.respuesta_con_solucion, re.IGNORECASE | re.DOTALL)
        if solucion_match:
            ejercicio = st.session_state.respuesta_con_solucion.split(solucion_match.group(0))[0].strip()
            st.info(ejercicio)
            if st.button("Mostrar Solución"):
                st.session_state.mostrar_solucion = True
            if st.session_state.mostrar_solucion:
                st.success(solucion_match.group(0).strip())
        else:
            st.info(st.session_state.respuesta_con_solucion) # Si no se encuentra el patrón de solución

# --- Posible futura funcionalidad para retroalimentación ---
st.subheader("Retroalimentación (Próximamente)")
st.markdown("Aquí podrás recibir retroalimentación sobre tus respuestas a los ejercicios.")

# --- Posible futura funcionalidad para seguimiento del progreso ---
st.subheader("Seguimiento de Progreso (Próximamente)")
st.markdown("Aquí podrás ver tu progreso y áreas de mejora sugeridas.")