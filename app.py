
import streamlit as st
import sqlite3

st.set_page_config(page_title="Portal Unilink", page_icon="📂", layout="wide")

def conectar_bd():
    return sqlite3.connect("unilink_docs.db")

def crear_tabla():
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            carpeta TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            link TEXT NOT NULL
        )
    ''')
    conexion.commit()
    conexion.close()

def guardar_documento(nombre, carpeta, descripcion, link):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT INTO documentos (nombre, carpeta, descripcion, link)
        VALUES (?, ?, ?, ?)
    ''', (nombre, carpeta, descripcion, link))
    conexion.commit()
    conexion.close()

def buscar_documentos(termino):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    patron = f"%{termino}%"
    cursor.execute('''
        SELECT nombre, carpeta, descripcion, link 
        FROM documentos 
        WHERE nombre LIKE ? OR carpeta LIKE ? OR descripcion LIKE ?
    ''', (patron, patron, patron))
    resultados = cursor.fetchall()
    conexion.close()
    return resultados

def obtener_todos():
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute('SELECT id, nombre, carpeta, descripcion, link FROM documentos')
    resultados = cursor.fetchall()
    conexion.close()
    return resultados

crear_tabla()

st.title("📂 Portal de Documentación - Unilink")

pestana_buscar, pestana_agregar, pestana_inventario = st.tabs([
    "🔍 Buscar Documento", "➕ Registrar", "📋 Inventario"
])

with pestana_buscar:
    busqueda = st.text_input("Escribe una palabra clave para buscar:")
    if busqueda:
        resultados = buscar_documentos(busqueda)
        if resultados:
            for doc in resultados:
                st.markdown(f"### 📄 {doc[0]}")
                st.write(f"**Carpeta:** `{doc[1]}` | **Descripción:** {doc[2]}")
                st.markdown(f"[➡️ Abrir en Google Drive]({doc[3]})")
                st.divider()
        else:
            st.warning("No se encontraron resultados.")

with pestana_agregar:
    with st.form("nuevo_doc", clear_on_submit=True):
        n = st.text_input("Nombre del archivo:")
        c = st.text_input("Carpeta en Drive:")
        d = st.text_area("Descripción:")
        l = st.text_input("Enlace de Drive:")
        if st.form_submit_button("Guardar"):
            if n and c and d and l:
                guardar_documento(n, c, d, l)
                st.success("Guardado correctamente!")
            else:
                st.error("Completa todos los campos.")

with pestana_inventario:
    docs = obtener_todos()
    if docs:
        datos = [{"ID": d[0], "Nombre": d[1], "Carpeta": d[2], "Descripción": d[3], "Link": d[4]} for d in docs]
        st.dataframe(datos, use_container_width=True)
    else:
        st.info("No hay documentos aún.")
