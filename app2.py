import html
import os
import re
from datetime import datetime

import pandas as pd
import streamlit as st

# ==========================================
# CONFIGURACIÓN GENERAL
# ==========================================

st.set_page_config(
    page_title="ITP Empleo Local · Portal Universitario",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

CARRERAS_ITP = [
    "Ingeniería en Tecnologías de la Información y Comunicaciones",
    "Ingeniería Industrial",
    "Ingeniería en Gestión Empresarial",
    "Ingeniería Electromecánica",
    "Ingeniería Mecánica",
    "Ingeniería Eléctrica",
    "Ingeniería Química",
    "Ingeniería Ambiental",
    "Licenciatura en Administración",
]

AREAS_INTERES = [
    "Desarrollo y TI",
    "Datos e Inteligencia Artificial",
    "Procesos y Manufactura",
    "Administración y Finanzas",
    "Logística y Cadena de Suministro",
    "Mantenimiento y Energía",
    "Marketing y Vinculación",
]

ESTADOS_POSTULACION = [
    "Enviada",
    "En revisión",
    "Entrevista",
    "Aceptada",
    "Rechazada",
]

# ==========================================
# COLORES Y DISEÑO INSTITUCIONAL + EMPLEO
# ==========================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Montserrat:wght@500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: linear-gradient(180deg,#f5f8fc 0%,#eef3f9 100%); }
.block-container { max-width: 1420px; padding-top: 1.5rem; padding-bottom: 2.5rem; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #102542, #173b65);
    border-right: 1px solid rgba(255,255,255,.12);
}
[data-testid="stSidebar"] *:not([data-testid="stAlert"]):not([data-testid="stAlert"] *) {
    color: white !important;
}
[data-testid="stSidebar"] .stRadio label { font-weight:600; }

/* Alertas dentro del sidebar con contraste legible */
[data-testid="stSidebar"] [data-testid="stAlert"] {
    background-color: #e8f2ff !important;
    border: 1px solid #bfdbfe !important;
    border-radius: 10px;
}
[data-testid="stSidebar"] [data-testid="stAlert"] * {
    color: #102542 !important;
}

.gov-strip { background:#f1f1f1; color:#303030; padding:9px 16px; border-radius:7px; font-size:13px; margin-bottom:14px; display:flex; justify-content:space-between; flex-wrap:wrap; gap:8px; }
.institution-header { background:white; border:1px solid #e4eaf2; border-radius:12px; padding:17px 22px; margin-bottom:20px; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:14px; }
.brand-left { display:flex; align-items:center; gap:14px; }
.brand-icon { background:#102542; color:white; border-radius:10px; padding:12px 15px; font-size:24px; }
.brand-title { color:#102542; font-family:'Montserrat',sans-serif; font-weight:800; font-size:20px; line-height:1.2; }
.brand-sub { color:#64748b; font-size:11px; letter-spacing:1px; font-weight:600; margin-top:5px; }
.badge-uni { background:#e8f2ff; color:#102542; border:1px solid #bfd8fa; padding:6px 12px; border-radius:999px; font-size:12px; font-weight:700; }
.hero { background:linear-gradient(120deg,#102542,#1769aa); padding:42px 38px; border-radius:18px; color:white; margin-bottom:25px; }
.hero h1 { font-size:36px; font-weight:800; color:white; font-family:'Montserrat',sans-serif; margin-bottom:10px; }
.hero p { font-size:16px; color:#e1edfa; margin-bottom:0; }
.section-title { color:#102542; font-size:24px; font-weight:800; margin-top:14px; margin-bottom:10px; font-family:'Montserrat',sans-serif; }
.stat-card { background:white; padding:20px; border-radius:15px; border:1px solid #e4eaf2; box-shadow:0 5px 18px rgba(16,37,66,.045); }
.stat-number { color:#1769aa; font-size:28px; font-weight:800; }
.stat-label { color:#64748b; font-size:13px; }
.job-card { background:white; border:1px solid #e2e8f0; border-radius:15px; padding:22px; margin-bottom:15px; box-shadow:0 7px 22px rgba(16,37,66,.06); transition:transform .18s ease,box-shadow .18s ease; }
.job-card:hover { transform:translateY(-2px); box-shadow:0 12px 28px rgba(16,37,66,.10); }
.job-card h3 { color:#102542; margin-bottom:5px; }
.job-company { color:#1769aa; font-weight:700; }
.job-info { color:#64748b; font-size:14px; margin:4px 0; }
.tag { display:inline-block; background:#e8f2ff; color:#1769aa; padding:5px 11px; border-radius:20px; font-size:12px; font-weight:600; margin:5px 5px 5px 0; }
.tag-match { display:inline-block; background:#dcfce7; color:#166534; padding:5px 11px; border-radius:20px; font-size:12px; font-weight:700; margin:5px 5px 5px 0; }
.tag-ver { display:inline-block; background:#fef3c7; color:#92400e; padding:5px 11px; border-radius:20px; font-size:12px; font-weight:700; margin:5px 5px 5px 0; }
.info-box { background:white; padding:20px; border-radius:14px; border-left:5px solid #1769aa; margin-bottom:14px; border-top:1px solid #e2e8f0; border-right:1px solid #e2e8f0; border-bottom:1px solid #e2e8f0; box-shadow:0 5px 18px rgba(16,37,66,.045); }
.notif-box { background:#f8fafc; padding:12px 16px; border-radius:10px; border-left:4px solid #0f766e; margin-bottom:8px; font-size:14px; }
.footer { text-align:center; color:#8492a6; padding:30px; font-size:13px; }
.stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] { border-radius:10px; }
.stButton > button, .stFormSubmitButton > button { background:#1769aa; color:white; border-radius:9px; border:none; font-weight:600; padding:8px 18px; min-height:42px; transition:all .18s ease; box-shadow:0 3px 10px rgba(23,105,170,.12); }
.stButton > button:hover, .stFormSubmitButton > button:hover { background:#102542; color:white; transform:translateY(-1px); box-shadow:0 6px 16px rgba(16,37,66,.18); }
@media(max-width:700px) { .hero {padding:28px 20px;} .hero h1 {font-size:28px;} .institution-header {flex-wrap:wrap;} }
</style>
""", unsafe_allow_html=True)

# ==========================================
# INICIALIZACIÓN DE ESTADO Y DATOS
# ==========================================


def init_state():
    if "usuarios" not in st.session_state:
        st.session_state.usuarios = {
            "admin@pachuca.tecnm.mx": {
                "nombre": "Coordinación de Vinculación ITP",
                "correo": "admin@pachuca.tecnm.mx",
                "password": "AdminITP2026!",
                "rol": "Administrador",
                "activo": True,
                "carrera": "Ingeniería en Gestión Empresarial",
                "semestre": "N/A",
                "area_interes": "Administración y Finanzas",
                "habilidades": "Gestión institucional, vinculación académica y supervisión",
                "disponibilidad": "Matutino",
                "telefono": "771-710-5250",
            },
            "l22200123@pachuca.tecnm.mx": {
                "nombre": "Ana Sofía Hernández",
                "correo": "l22200123@pachuca.tecnm.mx",
                "password": "Alumno2026!",
                "rol": "Estudiante",
                "activo": True,
                "carrera": "Ingeniería en Tecnologías de la Información y Comunicaciones",
                "semestre": "7°",
                "area_interes": "Datos e Inteligencia Artificial",
                "habilidades": "Python, SQL, Pandas, Streamlit, Git",
                "disponibilidad": "Vespertino",
                "telefono": "771-123-4567",
            },
            "vinculacion@solucionestecnologicas.mx": {
                "nombre": "Soluciones Tecnológicas Hidalgo",
                "correo": "vinculacion@solucionestecnologicas.mx",
                "password": "Empresa2026!",
                "rol": "Empresa",
                "activo": True,
                "sector": "Industrial",
                "ubicacion": "Pachuca, Hidalgo",
                "rfc": "STH190812AB1",
                "verificada": True,
                "descripcion": "Integradora de infraestructura de red, soporte y sistemas para la región.",
            },
            "rrhh@innovahidalgo.com": {
                "nombre": "Innova Manufactura Hidalgo",
                "correo": "rrhh@innovahidalgo.com",
                "password": "Empresa2026!",
                "rol": "Empresa",
                "activo": True,
                "sector": "Industrial",
                "ubicacion": "Mineral de la Reforma, Hidalgo",
                "rfc": "IMH210405CD9",
                "verificada": False,
                "descripcion": "Planta de ensamble y control de calidad en proceso de validación institucional.",
            },
        }

    if "sesion" not in st.session_state:
        st.session_state.sesion = None

    if "vacantes" not in st.session_state:
        st.session_state.vacantes = [
            {
                "id": 1,
                "puesto": "Auxiliar de sistemas y redes",
                "empresa": "Soluciones Tecnológicas Hidalgo",
                "correo_empresa": "vinculacion@solucionestecnologicas.mx",
                "sector": "Industrial",
                "tipo": "Medio tiempo",
                "ubicacion": "Pachuca, Hidalgo",
                "salario": "$5,500 mensuales",
                "modalidad": "Presencial",
                "horario": "Matutino",
                "carreras": [
                    "Ingeniería en Tecnologías de la Información y Comunicaciones",
                    "Ingeniería Electromecánica",
                ],
                "area_interes": "Desarrollo y TI",
                "descripcion": "Apoyo en mantenimiento preventivo de equipos, cableado estructurado y soporte técnico.",
                "requisitos": "Conocimientos básicos de redes, sistemas operativos y atención a usuarios.",
                "activa": True,
            },
            {
                "id": 2,
                "puesto": "Desarrollador web y automatización junior",
                "empresa": "Soluciones Tecnológicas Hidalgo",
                "correo_empresa": "vinculacion@solucionestecnologicas.mx",
                "sector": "Servicios",
                "tipo": "Prácticas profesionales",
                "ubicacion": "Zona Metropolitana de Pachuca",
                "salario": "Apoyo económico $3,500",
                "modalidad": "Híbrido",
                "horario": "Vespertino",
                "carreras": [
                    "Ingeniería en Tecnologías de la Información y Comunicaciones",
                ],
                "area_interes": "Desarrollo y TI",
                "descripcion": "Desarrollo de módulos internos, tableros operativos y automatización de reportes.",
                "requisitos": "HTML, CSS, JavaScript o Python; deseable nociones de SQL.",
                "activa": True,
            },
            {
                "id": 3,
                "puesto": "Analista de datos y mejora continua",
                "empresa": "Soluciones Tecnológicas Hidalgo",
                "correo_empresa": "vinculacion@solucionestecnologicas.mx",
                "sector": "Servicios",
                "tipo": "Residencia profesional",
                "ubicacion": "Pachuca, Hidalgo",
                "salario": "Apoyo económico + liberación de residencia",
                "modalidad": "Híbrido",
                "horario": "Flexible",
                "carreras": [
                    "Ingeniería en Tecnologías de la Información y Comunicaciones",
                    "Ingeniería Industrial",
                    "Ingeniería en Gestión Empresarial",
                ],
                "area_interes": "Datos e Inteligencia Artificial",
                "descripcion": "Limpieza de bases de datos, indicadores de desempeño y propuesta de tablero ejecutivo.",
                "requisitos": "Manejo de Python, Excel avanzado o SQL; capacidad analítica.",
                "activa": True,
            },
            {
                "id": 4,
                "puesto": "Auxiliar de planeación y logística",
                "empresa": "Soluciones Tecnológicas Hidalgo",
                "correo_empresa": "vinculacion@solucionestecnologicas.mx",
                "sector": "Industrial",
                "tipo": "Medio tiempo",
                "ubicacion": "Mineral de la Reforma, Hidalgo",
                "salario": "$5,200 mensuales",
                "modalidad": "Presencial",
                "horario": "Matutino",
                "carreras": [
                    "Ingeniería Industrial",
                    "Ingeniería en Gestión Empresarial",
                    "Licenciatura en Administración",
                ],
                "area_interes": "Logística y Cadena de Suministro",
                "descripcion": "Control de inventarios, programación de rutas y seguimiento de entregas regionales.",
                "requisitos": "Organización, Excel intermedio y trabajo en equipo.",
                "activa": True,
            },
            {
                "id": 5,
                "puesto": "Residente de mantenimiento y eficiencia energética",
                "empresa": "Soluciones Tecnológicas Hidalgo",
                "correo_empresa": "vinculacion@solucionestecnologicas.mx",
                "sector": "Industrial",
                "tipo": "Residencia profesional",
                "ubicacion": "Pachuca, Hidalgo",
                "salario": "Apoyo económico",
                "modalidad": "Presencial",
                "horario": "Matutino",
                "carreras": [
                    "Ingeniería Electromecánica",
                    "Ingeniería Mecánica",
                    "Ingeniería Eléctrica",
                ],
                "area_interes": "Mantenimiento y Energía",
                "descripcion": "Levantamiento de cargas, bitácoras de mantenimiento y optimización energética.",
                "requisitos": "Estar cursando residencia profesional y conocer normatividad básica.",
                "activa": True,
            },
        ]

    if "postulaciones" not in st.session_state:
        st.session_state.postulaciones = [
            {
                "id": 101,
                "vacante_id": 3,
                "estudiante_correo": "l22200123@pachuca.tecnm.mx",
                "estudiante_nombre": "Ana Sofía Hernández",
                "empresa": "Soluciones Tecnológicas Hidalgo",
                "correo_empresa": "vinculacion@solucionestecnologicas.mx",
                "estado": "Entrevista",
                "fecha": "2026-11-18",
                "nota": "Entrevista técnica programada con vinculación.",
            }
        ]

    if "notificaciones" not in st.session_state:
        st.session_state.notificaciones = [
            {
                "destinatario": "l22200123@pachuca.tecnm.mx",
                "mensaje": "Tu postulación a 'Analista de datos y mejora continua' avanzó a estado: Entrevista.",
                "fecha": "2026-11-18",
            },
            {
                "destinatario": "admin@pachuca.tecnm.mx",
                "mensaje": "La empresa 'Innova Manufactura Hidalgo' solicita verificación institucional.",
                "fecha": "2026-11-20",
            },
        ]

    if "calificaciones" not in st.session_state:
        st.session_state.calificaciones = [
            {
                "autor_correo": "l22200123@pachuca.tecnm.mx",
                "autor_rol": "Estudiante",
                "objetivo_tipo": "Empresa",
                "objetivo_id": "Soluciones Tecnológicas Hidalgo",
                "puntuacion": 5,
                "comentario": "Proceso claro, acompañamiento real y enfoque formativo.",
                "fecha": "2026-11-19",
            }
        ]

    if "curriculums_por_usuario" not in st.session_state:
        st.session_state.curriculums_por_usuario = {}


init_state()

# ==========================================
# FUNCIONES AUXILIARES DE NEGOCIO Y SEGURIDAD
# ==========================================


def correo_institucional_valido(correo: str) -> bool:
    patron = r"^[^@\s]+@(pachuca\.tecnm\.mx|tecnm\.mx)$"
    return bool(re.match(patron, correo.strip().lower()))


def agregar_notificacion(destinatario: str, mensaje: str):
    st.session_state.notificaciones.insert(
        0,
        {
            "destinatario": destinatario.lower(),
            "mensaje": mensaje,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
        },
    )


def empresa_verificada(nombre_empresa: str) -> bool:
    for u in st.session_state.usuarios.values():
        if u.get("rol") == "Empresa" and u.get("nombre") == nombre_empresa:
            return bool(u.get("verificada", False))
    return False


def obtener_usuario_actual():
    correo = st.session_state.sesion
    if correo and correo in st.session_state.usuarios:
        return st.session_state.usuarios[correo]
    return None


def calcular_compatibilidad(vacante: dict, usuario: dict | None) -> tuple[bool, list[str]]:
    if not usuario or usuario.get("rol") != "Estudiante":
        return False, []
    motivos = []
    carrera = usuario.get("carrera", "")
    area = usuario.get("area_interes", "")
    if carrera and carrera in vacante.get("carreras", []):
        motivos.append("Carrera afín")
    if area and area == vacante.get("area_interes", ""):
        motivos.append("Área de interés")
    return len(motivos) > 0, motivos


def promedio_calificacion_empresa(nombre_empresa: str) -> tuple[float | None, int]:
    vals = [
        c["puntuacion"]
        for c in st.session_state.calificaciones
        if c["objetivo_tipo"] == "Empresa" and c["objetivo_id"] == nombre_empresa
    ]
    if not vals:
        return None, 0
    return round(sum(vals) / len(vals), 1), len(vals)


def promedio_calificacion_estudiante(correo_est: str) -> tuple[float | None, int]:
    vals = [
        c["puntuacion"]
        for c in st.session_state.calificaciones
        if c["objetivo_tipo"] == "Estudiante" and c["objetivo_id"] == correo_est.lower()
    ]
    if not vals:
        return None, 0
    return round(sum(vals) / len(vals), 1), len(vals)


def puede_calificar_empresa(correo_usuario: str, nombre_empresa: str) -> bool:
    return any(
        p["estudiante_correo"].lower() == correo_usuario.lower()
        and p["empresa"] == nombre_empresa
        for p in st.session_state.postulaciones
    )


def puede_calificar_estudiante(correo_empresa: str, nombre_empresa: str, correo_estudiante: str) -> bool:
    return any(
        p["estudiante_correo"].lower() == correo_estudiante.lower()
        and (
            p.get("correo_empresa", "").lower() == correo_empresa.lower()
            or p["empresa"] == nombre_empresa
        )
        for p in st.session_state.postulaciones
    )


usuario_actual = obtener_usuario_actual()
rol_actual = usuario_actual["rol"] if usuario_actual else "Visitante"


def exigir_estudiante_institucional():
    if (
        not usuario_actual
        or rol_actual != "Estudiante"
        or not correo_institucional_valido(usuario_actual.get("correo", ""))
    ):
        st.warning("🔒 Acceso restringido: este apartado requiere una cuenta de estudiante con correo institucional.")
        st.info("Ingresa desde **Acceso institucional** con tu cuenta @pachuca.tecnm.mx o @tecnm.mx.")
        st.stop()


# ==========================================
# ENCABEZADO INSTITUCIONAL
# ==========================================

st.markdown(f"""
<div class="gov-strip">
    <span>🇲🇽 Gobierno de México · Educación Pública Superior</span>
    <span>Rol activo: <b>{html.escape(rol_actual)}</b></span>
</div>
<div class="institution-header">
    <div class="brand-left">
        <div class="brand-icon">🎓</div>
        <div>
            <div class="brand-title">TECNM · INSTITUTO TECNOLÓGICO DE PACHUCA</div>
            <div class="brand-sub">ITP EMPLEO LOCAL · PORTAL UNIVERSITARIO DE VINCULACIÓN Y EMPLEO</div>
        </div>
    </div>
    <div class="badge-uni">Entorno Académico · Pachuca, Hgo.</div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# MENÚ LATERAL Y SESIÓN
# ==========================================

with st.sidebar:
    st.markdown("# 🎓 TECNM")
    st.markdown("### ITP EMPLEO LOCAL")
    st.markdown("Plataforma universitaria de vinculación")
    st.markdown("---")

    if usuario_actual:
        st.success(f"Sesión: {usuario_actual['nombre']}")
        st.caption(f"Correo: {usuario_actual['correo']} · Rol: {usuario_actual['rol']}")
        if st.button("Cerrar sesión", key="btn_logout"):
            st.session_state.sesion = None
            st.rerun()
    else:
        st.info("Modo visitante: inicia sesión o regístrate para postularte y usar funciones por rol.")

    st.markdown("---")

    opciones_menu = [
        "Inicio",
        "Acceso institucional",
        "Buscar empleo",
        "Prácticas y residencias",
        "Mi perfil y carreras",
        "Mi currículum",
        "Mis postulaciones",
        "Calificaciones mutuas",
        "Para empresas",
    ]
    if rol_actual == "Administrador":
        opciones_menu.append("Panel universitario")
    opciones_menu.append("Seguridad y acerca")

    pagina = st.radio("MENÚ PRINCIPAL", opciones_menu)

    st.markdown("---")
    st.caption("📍 Pachuca de Soto y zona metropolitana")
    st.caption("Instituto Tecnológico de Pachuca · Proyecto universitario")


# ==========================================
# COMPONENTE DE TARJETA DE VACANTE
# ==========================================


def mostrar_vacante(vacante: dict, contexto: str = "general"):
    verificada = empresa_verificada(vacante["empresa"])
    es_afin, motivos = calcular_compatibilidad(vacante, usuario_actual)
    prom_emp, n_emp = promedio_calificacion_empresa(vacante["empresa"])
    calif_texto = f"⭐ {prom_emp}/5 ({n_emp})" if prom_emp else "Sin calificación aún"

    esc = lambda valor: html.escape(str(valor if valor is not None else ""))
    carreras_str = ", ".join(vacante.get("carreras", [])) or "Abierta"
    badge_ver = (
        '<span class="tag-match">✔ Empresa verificada</span>'
        if verificada else '<span class="tag-ver">⏳ Verificación pendiente</span>'
    )
    badge_afin = (
        f'<span class="tag-match">🎯 Recomendada ({esc(", ".join(motivos))})</span>'
        if es_afin else ""
    )

    tarjeta = f"""
    <div class="job-card">
      <h3>💼 {esc(vacante.get('puesto'))}</h3>
      <div class="job-company">{esc(vacante.get('empresa'))} · {esc(calif_texto)}</div>
      <div style="margin-top:12px">{badge_ver} {badge_afin}</div>
      <div style="margin-top:8px">
        <span class="tag">{esc(vacante.get('sector'))}</span>
        <span class="tag">{esc(vacante.get('tipo'))}</span>
        <span class="tag">{esc(vacante.get('modalidad'))}</span>
        <span class="tag">{esc(vacante.get('area_interes', 'General'))}</span>
      </div>
      <p class="job-info">🎓 <b>Carreras afines:</b> {esc(carreras_str)}</p>
      <p class="job-info">📍 {esc(vacante.get('ubicacion'))} · 🕒 {esc(vacante.get('horario'))} · 💰 {esc(vacante.get('salario'))}</p>
      <p>{esc(vacante.get('descripcion'))}</p>
      <b>Requisitos:</b> {esc(vacante.get('requisitos'))}
    </div>
    """
    st.markdown(tarjeta, unsafe_allow_html=True)

    if not verificada:
        st.caption("Esta vacante no admite postulaciones hasta que la empresa sea verificada por administración.")
        return
    if not usuario_actual:
        st.info("Inicia sesión con tu correo institucional para postularte.")
        return
    if rol_actual != "Estudiante" or not correo_institucional_valido(usuario_actual.get("correo", "")):
        st.caption("La postulación está disponible únicamente para estudiantes con correo institucional.")
        return

    ya_postulado = any(
        p["vacante_id"] == vacante["id"]
        and p["estudiante_correo"].lower() == usuario_actual["correo"].lower()
        for p in st.session_state.postulaciones
    )
    if ya_postulado:
        st.success("Ya estás postulado a esta vacante. Revisa el avance en 'Mis postulaciones'.")
    elif st.button("Postularme a esta vacante", key=f"postular_{contexto}_{vacante['id']}_{usuario_actual['correo']}"):
        nuevo_id = max([p["id"] for p in st.session_state.postulaciones], default=100) + 1
        st.session_state.postulaciones.append({
            "id": nuevo_id,
            "vacante_id": vacante["id"],
            "estudiante_correo": usuario_actual["correo"],
            "estudiante_nombre": usuario_actual["nombre"],
            "empresa": vacante["empresa"],
            "correo_empresa": vacante.get("correo_empresa", ""),
            "estado": "Enviada",
            "fecha": datetime.now().strftime("%Y-%m-%d"),
            "nota": "Postulación enviada desde el portal universitario.",
        })
        agregar_notificacion(usuario_actual["correo"], f"Te postulaste a '{vacante['puesto']}' en {vacante['empresa']} (Estado: Enviada).")
        if vacante.get("correo_empresa"):
            agregar_notificacion(vacante["correo_empresa"], f"Nueva postulación de {usuario_actual['nombre']} ({usuario_actual.get('carrera', '')}) para '{vacante['puesto']}'.")
        st.success("¡Postulación registrada y notificada!")
        st.rerun()


# ==========================================
# PÁGINA: INICIO
# ==========================================

if pagina == "Inicio":
    st.markdown("""
    <div class="hero">
        <h1>Vinculación universitaria con oportunidades locales</h1>
        <p>
        Portal académico del Instituto Tecnológico de Pachuca para conectar estudiantes
        con empleos, prácticas profesionales y residencias verificadas en Pachuca y su zona metropolitana.
        </p>
    </div>
    """, unsafe_allow_html=True)

    empresas_verificadas_count = sum(
        1 for u in st.session_state.usuarios.values() if u.get("rol") == "Empresa" and u.get("verificada")
    )
    vacantes_activas = [v for v in st.session_state.vacantes if v.get("activa", True) and empresa_verificada(v["empresa"])]

    c1, c2, c3, c4 = st.columns(4)
    estadisticas = [
        ("💼", len(vacantes_activas), "Vacantes activas verificadas"),
        ("🏢", empresas_verificadas_count, "Empresas verificadas"),
        ("🎓", len(CARRERAS_ITP), "Programas educativos contemplados"),
        ("📋", len(st.session_state.postulaciones), "Postulaciones en seguimiento"),
    ]
    for col, dato in zip([c1, c2, c3, c4], estadisticas):
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div>{dato[0]}</div>
                <div class="stat-number">{dato[1]}</div>
                <div class="stat-label">{dato[2]}</div>
            </div>
            """, unsafe_allow_html=True)

    if usuario_actual:
        notifs = [
            n for n in st.session_state.notificaciones
            if n["destinatario"] == usuario_actual["correo"].lower() or rol_actual == "Administrador"
        ]
        if notifs:
            st.markdown('<p class="section-title">🔔 Notificaciones recientes</p>', unsafe_allow_html=True)
            for n in notifs[:3]:
                st.markdown(
                    f'<div class="notif-box"><b>{html.escape(n["fecha"])}</b> · {html.escape(n["mensaje"])}</div>',
                    unsafe_allow_html=True,
                )

    st.markdown('<p class="section-title">¿Cómo opera este portal universitario?</p>', unsafe_allow_html=True)
    a, b, c = st.columns(3)
    with a:
        st.markdown("### 🎓 Enfoque académico")
        st.write("Filtra por carrera, semestre, área de interés, prácticas profesionales y residencias.")
    with b:
        st.markdown("### 🛡️ Control y verificación")
        st.write("Las empresas pasan por revisión administrativa antes de publicar y los roles delimitan acciones.")
    with c:
        st.markdown("### 🔄 Seguimiento y evaluación")
        st.write("Consulta estados de postulación y evalúa mutuamente tras una postulación o experiencia registrada.")

    st.markdown("---")
    st.markdown('<p class="section-title">Vacantes destacadas</p>', unsafe_allow_html=True)

    if rol_actual == "Estudiante":
        ordenadas = sorted(
            vacantes_activas,
            key=lambda v: (1 if calcular_compatibilidad(v, usuario_actual)[0] else 0, v["id"]),
            reverse=True,
        )
    else:
        ordenadas = vacantes_activas

    for vacante in ordenadas[:3]:
        mostrar_vacante(vacante, contexto="inicio")


# ==========================================
# PÁGINA: ACCESO INSTITUCIONAL
# ==========================================

elif pagina == "Acceso institucional":
    st.markdown('<p class="section-title">🔐 Acceso institucional y registro de cuentas</p>', unsafe_allow_html=True)
    st.write("Autenticación por rol para Estudiantes, Empresas y Administradores universitarios.")

    tab_login, tab_reg_est, tab_reg_emp = st.tabs(
        ["Iniciar sesión", "Registro estudiante (Correo escolar)", "Registro empresa"]
    )

    with tab_login:
        with st.form("form_login"):
            correo_in = st.text_input("Correo electrónico")
            pass_in = st.text_input("Contraseña", type="password")
            enviar_login = st.form_submit_button("Ingresar")

            if enviar_login:
                c_norm = correo_in.strip().lower()
                usr = st.session_state.usuarios.get(c_norm)
                if usr and usr.get("password") == pass_in:
                    if usr.get("rol") == "Estudiante" and not correo_institucional_valido(c_norm):
                        st.error("Las cuentas de estudiante solo pueden ingresar con correo institucional @pachuca.tecnm.mx o @tecnm.mx.")
                    elif not usr.get("activo", True):
                        st.error("Esta cuenta se encuentra suspendida por administración.")
                    else:
                        st.session_state.sesion = c_norm
                        st.success(f"Bienvenido/a, {usr['nombre']} ({usr['rol']}).")
                        st.rerun()
                else:
                    st.error("Credenciales inválidas. Verifica tu correo y contraseña.")

        with st.expander("Cuentas de prueba disponibles en esta sesión"):
            st.write("- **Estudiante:** `l22200123@pachuca.tecnm.mx` / `Alumno2026!`")
            st.write("- **Empresa verificada:** `vinculacion@solucionestecnologicas.mx` / `Empresa2026!`")
            st.write("- **Empresa pendiente:** `rrhh@innovahidalgo.com` / `Empresa2026!`")
            st.write("- **Administrador:** `admin@pachuca.tecnm.mx` / `AdminITP2026!`")

    with tab_reg_est:
        st.caption("Se requiere correo institucional (@pachuca.tecnm.mx o @tecnm.mx) y contraseña de al menos 8 caracteres.")
        with st.form("form_reg_est"):
            nombre_est = st.text_input("Nombre completo del estudiante")
            correo_est = st.text_input("Correo institucional", placeholder="ej. l23200456@pachuca.tecnm.mx")
            pass_est = st.text_input("Contraseña (mín. 8 caracteres)", type="password")
            carrera_est = st.selectbox("Carrera", CARRERAS_ITP)
            semestre_est = st.selectbox(
                "Semestre", ["1°", "2°", "3°", "4°", "5°", "6°", "7°", "8°", "9°", "10°"]
            )
            area_est = st.selectbox("Área de interés principal", AREAS_INTERES)
            crear_est = st.form_submit_button("Registrar cuenta estudiantil")

            if crear_est:
                c_norm = correo_est.strip().lower()
                if not nombre_est.strip():
                    st.error("Ingresa tu nombre completo.")
                elif not correo_institucional_valido(c_norm):
                    st.error("Debes usar un correo escolar válido (@pachuca.tecnm.mx o @tecnm.mx).")
                elif len(pass_est) < 8:
                    st.error("La contraseña debe tener al menos 8 caracteres.")
                elif c_norm in st.session_state.usuarios:
                    st.warning("Ese correo ya está registrado.")
                else:
                    st.session_state.usuarios[c_norm] = {
                        "nombre": nombre_est.strip(),
                        "correo": c_norm,
                        "password": pass_est,
                        "rol": "Estudiante",
                        "activo": True,
                        "carrera": carrera_est,
                        "semestre": semestre_est,
                        "area_interes": area_est,
                        "habilidades": "",
                        "disponibilidad": "Flexible",
                        "telefono": "",
                    }
                    st.session_state.sesion = c_norm
                    agregar_notificacion(
                        "admin@pachuca.tecnm.mx",
                        f"Nuevo estudiante registrado: {nombre_est.strip()} ({carrera_est}).",
                    )
                    st.success("¡Cuenta estudiantil creada e iniciada!")
                    st.rerun()

    with tab_reg_emp:
        st.caption("Las empresas nuevas inician como NO VERIFICADAS hasta que un administrador valide sus datos.")
        with st.form("form_reg_emp"):
            nom_emp = st.text_input("Razón social o nombre comercial")
            rfc_emp = st.text_input("RFC (opcional en prueba)")
            correo_emp = st.text_input("Correo corporativo de contacto")
            pass_emp = st.text_input("Contraseña (mín. 8 caracteres)", type="password")
            sec_emp = st.selectbox("Sector económico", ["Industrial", "Comercial", "Servicios"])
            ubi_emp = st.text_input("Ubicación", value="Pachuca, Hidalgo")
            desc_emp = st.text_area("Descripción breve de la organización")
            crear_emp = st.form_submit_button("Solicitar registro de empresa")

            if crear_emp:
                c_norm = correo_emp.strip().lower()
                if not nom_emp.strip() or "@" not in c_norm:
                    st.error("Completa el nombre de la empresa y un correo válido.")
                elif len(pass_emp) < 8:
                    st.error("La contraseña debe tener al menos 8 caracteres.")
                elif c_norm in st.session_state.usuarios:
                    st.warning("Ese correo ya está registrado.")
                else:
                    st.session_state.usuarios[c_norm] = {
                        "nombre": nom_emp.strip(),
                        "correo": c_norm,
                        "password": pass_emp,
                        "rol": "Empresa",
                        "activo": True,
                        "sector": sec_emp,
                        "ubicacion": ubi_emp.strip() or "Pachuca, Hidalgo",
                        "rfc": rfc_emp.strip().upper() or "PENDIENTE",
                        "verificada": False,
                        "descripcion": desc_emp.strip(),
                    }
                    st.session_state.sesion = c_norm
                    agregar_notificacion(
                        "admin@pachuca.tecnm.mx",
                        f"Empresa '{nom_emp.strip()}' pendiente de verificación administrativa.",
                    )
                    st.success("Cuenta de empresa registrada en estado PENDIENTE de verificación.")
                    st.rerun()


# ==========================================
# PÁGINA: BUSCAR EMPLEO
# ==========================================

elif pagina == "Buscar empleo":
    st.markdown('<p class="section-title">🔎 Búsqueda de oportunidades</p>', unsafe_allow_html=True)
    st.write("Filtra por carrera, área de interés, sector, tipo y modalidad.")

    busqueda = st.text_input(
        "Buscar por puesto, empresa, habilidad o palabra clave",
        placeholder="Ej. datos, redes, logística, prácticas...",
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        carrera_filtro = st.selectbox("Carrera", ["Todas"] + CARRERAS_ITP)
    with col2:
        area_filtro = st.selectbox("Área de interés", ["Todas"] + AREAS_INTERES)
    with col3:
        sector_filtro = st.selectbox("Sector", ["Todos", "Industrial", "Comercial", "Servicios"])

    col4, col5, col6 = st.columns(3)
    with col4:
        tipo_filtro = st.selectbox(
            "Tipo de oportunidad",
            ["Todos", "Medio tiempo", "Prácticas profesionales", "Residencia profesional"],
        )
    with col5:
        modalidad_filtro = st.selectbox("Modalidad", ["Todas", "Presencial", "Híbrido", "Remoto"])
    with col6:
        solo_verificadas = st.checkbox("Solo empresas verificadas", value=True)
        solo_afines = st.checkbox(
            "Priorizar/filtrar afines a mi perfil",
            value=(rol_actual == "Estudiante"),
            disabled=(rol_actual != "Estudiante"),
        )

    resultados = []
    for v in st.session_state.vacantes:
        if not v.get("activa", True):
            continue
        verificada = empresa_verificada(v["empresa"])
        if solo_verificadas and not verificada:
            continue
        if carrera_filtro != "Todas" and carrera_filtro not in v.get("carreras", []):
            continue
        if area_filtro != "Todas" and v.get("area_interes") != area_filtro:
            continue
        if sector_filtro != "Todos" and v["sector"] != sector_filtro:
            continue
        if tipo_filtro != "Todos" and v["tipo"] != tipo_filtro:
            continue
        if modalidad_filtro != "Todas" and v["modalidad"] != modalidad_filtro:
            continue

        texto_buscable = (
            f"{v['puesto']} {v['empresa']} {v['descripcion']} {v['requisitos']} "
            f"{' '.join(v.get('carreras', []))} {v.get('area_interes', '')}"
        ).lower()
        if busqueda.strip() and busqueda.strip().lower() not in texto_buscable:
            continue

        es_afin, _ = calcular_compatibilidad(v, usuario_actual)
        if solo_afines and rol_actual == "Estudiante" and not es_afin:
            continue

        resultados.append(v)

    if rol_actual == "Estudiante":
        resultados.sort(
            key=lambda x: (1 if calcular_compatibilidad(x, usuario_actual)[0] else 0, x["id"]),
            reverse=True,
        )

    st.markdown("---")
    st.write(f"*{len(resultados)} oportunidades encontradas*")

    if resultados:
        for v in resultados:
            mostrar_vacante(v, contexto="buscar")
    else:
        st.warning("No se encontraron vacantes con los filtros seleccionados.")


# ==========================================
# PÁGINA: PRÁCTICAS Y RESIDENCIAS
# ==========================================

elif pagina == "Prácticas y residencias":
    st.markdown('<p class="section-title">🎓 Prácticas y residencias profesionales</p>', unsafe_allow_html=True)
    st.write(
        "Sección enfocada en vincular tu formación académica con proyectos reales "
        "y requisitos curriculares del Instituto Tecnológico de Pachuca."
    )

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="info-box">
            <h3>📘 Prácticas profesionales</h3>
            Experiencia supervisada para aplicar fundamentos técnicos, fortalecer habilidades
            profesionales y conocer la dinámica organizacional.
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="info-box">
            <h3>🏢 Residencias profesionales</h3>
            Desarrollo de un proyecto técnico o de mejora vinculado con la organización
            y alineado a tu plan de estudios y carrera.
        </div>
        """, unsafe_allow_html=True)

    modalidad_acad = st.radio(
        "Filtrar modalidad académica",
        ["Todas", "Prácticas profesionales", "Residencia profesional"],
        horizontal=True,
    )

    acad_vacantes = [
        v for v in st.session_state.vacantes
        if v.get("activa", True)
        and v["tipo"] in ["Prácticas profesionales", "Residencia profesional"]
        and (modalidad_acad == "Todas" or v["tipo"] == modalidad_acad)
    ]

    for v in acad_vacantes:
        mostrar_vacante(v, contexto="acad")


# ==========================================
# PÁGINA: MI PERFIL Y CARRERAS
# ==========================================

elif pagina == "Mi perfil y carreras":
    st.markdown('<p class="section-title">👤 Mi perfil académico y profesional</p>', unsafe_allow_html=True)
    exigir_estudiante_institucional()

    with st.form("formulario_perfil_est"):
        nombre = st.text_input("Nombre completo", value=usuario_actual.get("nombre", ""))
        st.text_input("Correo institucional", value=usuario_actual.get("correo", ""), disabled=True)
        carrera = st.selectbox(
            "Carrera",
            CARRERAS_ITP,
            index=CARRERAS_ITP.index(usuario_actual["carrera"])
            if usuario_actual.get("carrera") in CARRERAS_ITP
            else 0,
        )
        semestres = ["1°", "2°", "3°", "4°", "5°", "6°", "7°", "8°", "9°", "10°"]
        semestre = st.selectbox(
            "Semestre o periodo académico",
            semestres,
            index=semestres.index(usuario_actual["semestre"])
            if usuario_actual.get("semestre") in semestres
            else 0,
        )
        area_interes = st.selectbox(
            "Área de interés",
            AREAS_INTERES,
            index=AREAS_INTERES.index(usuario_actual["area_interes"])
            if usuario_actual.get("area_interes") in AREAS_INTERES
            else 0,
        )
        habilidades = st.text_area(
            "Habilidades técnicas y blandas",
            value=usuario_actual.get("habilidades", ""),
            placeholder="Ej. Python, SQL, SolidWorks, Lean Manufacturing, trabajo en equipo...",
        )
        disponibilidad = st.selectbox(
            "Disponibilidad de horario",
            ["Matutino", "Vespertino", "Nocturno", "Flexible", "Fines de semana"],
        )
        telefono = st.text_input("Teléfono de contacto (opcional)", value=usuario_actual.get("telefono", ""))
        guardar = st.form_submit_button("Guardar perfil")

        if guardar:
            if nombre.strip():
                usuario_actual.update(
                    {
                        "nombre": nombre.strip(),
                        "carrera": carrera,
                        "semestre": semestre,
                        "area_interes": area_interes,
                        "habilidades": habilidades.strip(),
                        "disponibilidad": disponibilidad,
                        "telefono": telefono.strip(),
                    }
                )
                st.success("Perfil actualizado correctamente.")
            else:
                st.error("El nombre completo no puede estar vacío.")

    st.markdown("---")
    st.markdown("### Resumen del perfil actual")
    for k in ["nombre", "correo", "carrera", "semestre", "area_interes", "disponibilidad", "habilidades", "telefono"]:
        st.write(f"**{k.replace('_', ' ').capitalize()}:** {usuario_actual.get(k, '—')}")


# ==========================================
# PÁGINA: MI CURRÍCULUM
# ==========================================

elif pagina == "Mi currículum":
    st.markdown('<p class="section-title">📄 Mi currículum vitae (PDF)</p>', unsafe_allow_html=True)
    exigir_estudiante_institucional()

    st.write("Sube tu CV en formato PDF para mantenerlo asociado a tu perfil durante la sesión.")
    archivo = st.file_uploader("Selecciona tu CV en PDF", type=["pdf"])

    if archivo is not None:
        if archivo.size > 5 * 1024 * 1024:
            st.error("El archivo excede el límite de 5 MB.")
        elif st.button("Guardar currículum"):
            os.makedirs("curriculums", exist_ok=True)
            safe_user = re.sub(r"[^a-zA-Z0-9_-]", "_", usuario_actual["correo"])
            nombre_archivo = f"CV_{safe_user}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            ruta = os.path.join("curriculums", nombre_archivo)
            with open(ruta, "wb") as f:
                f.write(archivo.getbuffer())
            st.session_state.curriculums_por_usuario[usuario_actual["correo"]] = nombre_archivo
            st.success("Currículum guardado correctamente.")

    cv_actual = st.session_state.curriculums_por_usuario.get(usuario_actual["correo"])
    if cv_actual:
        st.info(f"CV activo en esta sesión: **{cv_actual}**")
    else:
        st.caption("Aún no has guardado un CV en esta sesión.")


# ==========================================
# PÁGINA: MIS POSTULACIONES Y SEGUIMIENTO
# ==========================================

elif pagina == "Mis postulaciones":
    st.markdown('<p class="section-title">📋 Seguimiento de postulaciones</p>', unsafe_allow_html=True)

    if not usuario_actual:
        st.info("Inicia sesión para consultar y dar seguimiento a postulaciones.")
    else:
        if rol_actual == "Estudiante":
            lista_post = [
                p for p in st.session_state.postulaciones
                if p["estudiante_correo"].lower() == usuario_actual["correo"].lower()
            ]
        elif rol_actual == "Empresa":
            lista_post = [
                p for p in st.session_state.postulaciones
                if p.get("correo_empresa", "").lower() == usuario_actual["correo"].lower()
                or p["empresa"] == usuario_actual.get("nombre")
            ]
        else:
            lista_post = list(st.session_state.postulaciones)

        if not lista_post:
            st.info("No hay postulaciones registradas para tu vista actual.")
        else:
            vacantes_map = {v["id"]: v for v in st.session_state.vacantes}
            for p in lista_post:
                vac = vacantes_map.get(p["vacante_id"], {})
                puesto_nombre = vac.get("puesto", f"Vacante #{p['vacante_id']}")
                st.markdown(f"""
                <div class="info-box">
                    <h3>{html.escape(puesto_nombre)} · <span class="tag">{html.escape(p['estado'])}</span></h3>
                    <b>Empresa:</b> {html.escape(p['empresa'])} | <b>Estudiante:</b> {html.escape(p['estudiante_nombre'])} ({html.escape(p['estudiante_correo'])})<br>
                    <small>Fecha de registro: {html.escape(p['fecha'])} · Nota: {html.escape(p.get('nota', ''))}</small>
                </div>
                """, unsafe_allow_html=True)

                if rol_actual in ["Empresa", "Administrador"]:
                    c_est, c_nota, c_btn = st.columns([2, 3, 1])
                    with c_est:
                        nuevo_estado = st.selectbox(
                            "Estado",
                            ESTADOS_POSTULACION,
                            index=ESTADOS_POSTULACION.index(p["estado"])
                            if p["estado"] in ESTADOS_POSTULACION
                            else 0,
                            key=f"estado_sel_{p['id']}",
                        )
                    with c_nota:
                        nueva_nota = st.text_input(
                            "Observación de seguimiento",
                            value=p.get("nota", ""),
                            key=f"nota_inp_{p['id']}",
                        )
                    with c_btn:
                        st.write("")
                        if st.button("Actualizar", key=f"act_post_{p['id']}"):
                            p["estado"] = nuevo_estado
                            p["nota"] = nueva_nota.strip()
                            agregar_notificacion(
                                p["estudiante_correo"],
                                f"Actualización en '{puesto_nombre}' ({p['empresa']}): estado '{nuevo_estado}'.",
                            )
                            st.success("Estado actualizado y notificado al estudiante.")
                            st.rerun()


# ==========================================
# PÁGINA: CALIFICACIONES MUTUAS
# ==========================================

elif pagina == "Calificaciones mutuas":
    st.markdown('<p class="section-title">⭐ Calificaciones mutuas</p>', unsafe_allow_html=True)
    st.write(
        "Solo es posible calificar cuando existe una postulación o experiencia registrada "
        "entre el estudiante y la empresa."
    )

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### Calificaciones de empresas")
        empresas_lista = sorted(
            {u["nombre"] for u in st.session_state.usuarios.values() if u.get("rol") == "Empresa"}
        )
        for emp in empresas_lista:
            prom, cnt = promedio_calificacion_empresa(emp)
            ver = "✔ Verificada" if empresa_verificada(emp) else "⏳ Pendiente"
            st.write(f"**{emp}** ({ver}) — {f'{prom}/5 ({cnt} reseñas)' if prom else 'Sin calificaciones'}")

    with col_b:
        st.markdown("### Calificaciones de estudiantes (por experiencia/postulación)")
        estudiantes_lista = [
            u for u in st.session_state.usuarios.values() if u.get("rol") == "Estudiante"
        ]
        for est in estudiantes_lista:
            prom, cnt = promedio_calificacion_estudiante(est["correo"])
            st.write(
                f"**{est['nombre']}** ({est.get('carrera', '')}) — "
                f"{f'{prom}/5 ({cnt} evaluaciones)' if prom else 'Sin evaluaciones'}"
            )

    st.markdown("---")
    st.markdown("### Registrar evaluación")

    if not usuario_actual:
        st.info("Inicia sesión como Estudiante o Empresa para registrar una evaluación.")
    elif rol_actual == "Estudiante":
        empresas_elegibles = sorted(
            {
                p["empresa"]
                for p in st.session_state.postulaciones
                if p["estudiante_correo"].lower() == usuario_actual["correo"].lower()
            }
        )
        if not empresas_elegibles:
            st.warning("Aún no tienes postulaciones o experiencias registradas con ninguna empresa para calificar.")
        else:
            with st.form("form_calif_emp"):
                emp_obj = st.selectbox("Empresa a evaluar", empresas_elegibles)
                pts = st.slider("Puntuación", 1, 5, 5)
                com = st.text_area("Comentario sobre la experiencia o proceso")
                env_c = st.form_submit_button("Publicar calificación a empresa")
                if env_c:
                    if not puede_calificar_empresa(usuario_actual["correo"], emp_obj):
                        st.error("No existe postulación registrada con esta empresa.")
                    else:
                        st.session_state.calificaciones.append(
                            {
                                "autor_correo": usuario_actual["correo"],
                                "autor_rol": "Estudiante",
                                "objetivo_tipo": "Empresa",
                                "objetivo_id": emp_obj,
                                "puntuacion": pts,
                                "comentario": com.strip(),
                                "fecha": datetime.now().strftime("%Y-%m-%d"),
                            }
                        )
                        st.success("Calificación registrada.")
                        st.rerun()

    elif rol_actual == "Empresa":
        nombre_emp = usuario_actual.get("nombre", "")
        estudiantes_elegibles = sorted(
            {
                p["estudiante_correo"]
                for p in st.session_state.postulaciones
                if puede_calificar_estudiante(usuario_actual["correo"], nombre_emp, p["estudiante_correo"])
            }
        )
        if not estudiantes_elegibles:
            st.warning("Aún no tienes postulaciones o experiencias registradas con estudiantes para evaluar.")
        else:
            with st.form("form_calif_est"):
                est_obj = st.selectbox("Estudiante con postulación/experiencia registrada", estudiantes_elegibles)
                pts = st.slider("Puntuación", 1, 5, 5)
                com = st.text_area("Comentario sobre desempeño o participación")
                env_c = st.form_submit_button("Publicar evaluación al estudiante")
                if env_c:
                    if not puede_calificar_estudiante(usuario_actual["correo"], nombre_emp, est_obj):
                        st.error("Solo puedes evaluar a estudiantes con postulación o experiencia registrada.")
                    else:
                        st.session_state.calificaciones.append(
                            {
                                "autor_correo": usuario_actual["correo"],
                                "autor_rol": "Empresa",
                                "objetivo_tipo": "Estudiante",
                                "objetivo_id": est_obj.lower(),
                                "puntuacion": pts,
                                "comentario": com.strip(),
                                "fecha": datetime.now().strftime("%Y-%m-%d"),
                            }
                        )
                        agregar_notificacion(
                            est_obj,
                            f"La empresa '{nombre_emp}' registró una evaluación ({pts}/5) sobre tu postulación/experiencia.",
                        )
                        st.success("Evaluación registrada.")
                        st.rerun()
    else:
        st.info("El rol Administrador supervisa las evaluaciones y no emite calificaciones directas.")

    st.markdown("### Historial de evaluaciones recientes")
    for c in reversed(st.session_state.calificaciones[-8:]):
        st.markdown(
            f'<div class="info-box"><b>{html.escape(c["objetivo_tipo"])}:</b> {html.escape(c["objetivo_id"])} · '
            f'<b>{"⭐" * c["puntuacion"]} ({c["puntuacion"]}/5)</b><br>'
            f'<small>Por {html.escape(c["autor_rol"])} ({html.escape(c["autor_correo"])}) · {html.escape(c["fecha"])}</small><br>'
            f'{html.escape(c.get("comentario", ""))}</div>',
            unsafe_allow_html=True,
        )


# ==========================================
# PÁGINA: PARA EMPRESAS
# ==========================================

elif pagina == "Para empresas":
    st.markdown('<p class="section-title">🏢 Espacio para empresas y vinculación</p>', unsafe_allow_html=True)

    if rol_actual == "Empresa" and usuario_actual:
        verificada = bool(usuario_actual.get("verificada", False))
        if verificada:
            st.success("Tu empresa está **VERIFICADA** por administración. Puedes publicar vacantes.")
        else:
            st.warning(
                "Tu empresa está en estado **PENDIENTE DE VERIFICACIÓN**. "
                "Un administrador debe aprobar tu cuenta antes de publicar vacantes activas."
            )

        with st.form("form_publicar_vacante"):
            puesto = st.text_input("Nombre del puesto o proyecto")
            sector = st.selectbox("Sector económico", ["Industrial", "Comercial", "Servicios"])
            tipo = st.selectbox(
                "Tipo de oportunidad",
                ["Medio tiempo", "Prácticas profesionales", "Residencia profesional"],
            )
            modalidad = st.selectbox("Modalidad", ["Presencial", "Híbrido", "Remoto"])
            horario = st.selectbox("Horario", ["Matutino", "Vespertino", "Flexible"])
            ubicacion = st.text_input("Ubicación", value=usuario_actual.get("ubicacion", "Pachuca, Hidalgo"))
            salario = st.text_input("Compensación o apoyo", value="Apoyo económico")
            carreras_sel = st.multiselect("Carreras afines", CARRERAS_ITP, default=[CARRERAS_ITP[0]])
            area_sel = st.selectbox("Área de interés", AREAS_INTERES)
            descripcion = st.text_area("Descripción de actividades")
            requisitos = st.text_area("Requisitos académicos o técnicos")
            publicar = st.form_submit_button("Publicar vacante", disabled=not verificada)

            if publicar:
                if not verificada:
                    st.error("Solo empresas verificadas pueden publicar oportunidades.")
                elif not puesto.strip() or not descripcion.strip():
                    st.error("Completa al menos el puesto y la descripción.")
                else:
                    nuevo_id = max([v["id"] for v in st.session_state.vacantes], default=0) + 1
                    st.session_state.vacantes.append(
                        {
                            "id": nuevo_id,
                            "puesto": puesto.strip(),
                            "empresa": usuario_actual["nombre"],
                            "correo_empresa": usuario_actual["correo"],
                            "sector": sector,
                            "tipo": tipo,
                            "ubicacion": ubicacion.strip() or "Pachuca, Hidalgo",
                            "salario": salario.strip() or "A convenir",
                            "modalidad": modalidad,
                            "horario": horario,
                            "carreras": carreras_sel or ["Abierta"],
                            "area_interes": area_sel,
                            "descripcion": descripcion.strip(),
                            "requisitos": requisitos.strip() or "Por definir en entrevista.",
                            "activa": True,
                        }
                    )
                    agregar_notificacion(
                        "admin@pachuca.tecnm.mx",
                        f"Empresa '{usuario_actual['nombre']}' publicó la vacante '{puesto.strip()}'.",
                    )
                    st.success("Vacante publicada en el portal.")
                    st.rerun()
    else:
        st.write(
            "Las empresas se registran en **Acceso institucional**, pasan por verificación administrativa "
            "y posteriormente publican empleos, prácticas y residencias para estudiantes del ITP."
        )
        st.markdown("""
        <div class="info-box">
            <h3>🛡️ Proceso de incorporación</h3>
            1. Registro de cuenta empresarial.<br>
            2. Revisión y verificación por vinculación / administración del portal.<br>
            3. Publicación de vacantes segmentadas por carrera, seguimiento y evaluación mutua.
        </div>
        """, unsafe_allow_html=True)


# ==========================================
# PÁGINA: PANEL UNIVERSITARIO (ADMIN)
# ==========================================

elif pagina == "Panel universitario":
    st.markdown('<p class="section-title">🏛️ Panel universitario de administración</p>', unsafe_allow_html=True)

    if rol_actual != "Administrador":
        st.error("Acceso restringido: esta sección requiere rol de **Administrador**.")
    else:
        total_est = sum(1 for u in st.session_state.usuarios.values() if u.get("rol") == "Estudiante")
        total_emp = sum(1 for u in st.session_state.usuarios.values() if u.get("rol") == "Empresa")
        pendientes_ver = [
            u for u in st.session_state.usuarios.values()
            if u.get("rol") == "Empresa" and not u.get("verificada", False)
        ]

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Estudiantes", total_est)
        m2.metric("Empresas", total_emp)
        m3.metric("Empresas por verificar", len(pendientes_ver))
        m4.metric("Vacantes registradas", len(st.session_state.vacantes))

        st.markdown("### 1. Verificación y gestión de empresas")
        for correo_u, u in list(st.session_state.usuarios.items()):
            if u.get("rol") == "Empresa":
                estado_ver = "Verificada ✔" if u.get("verificada") else "Pendiente ⏳"
                estado_cta = "Activa" if u.get("activo", True) else "Suspendida"
                c1, c2, c3 = st.columns([4, 1, 1])
                with c1:
                    st.write(
                        f"**{u['nombre']}** ({correo_u}) · Sector: {u.get('sector', '')} · "
                        f"Verificación: **{estado_ver}** · Cuenta: **{estado_cta}**"
                    )
                with c2:
                    if not u.get("verificada"):
                        if st.button("Verificar", key=f"ver_emp_{correo_u}"):
                            u["verificada"] = True
                            agregar_notificacion(
                                correo_u,
                                f"Tu empresa '{u['nombre']}' ha sido VERIFICADA por administración.",
                            )
                            st.success(f"{u['nombre']} verificada.")
                            st.rerun()
                with c3:
                    etiqueta_cta = "Suspender" if u.get("activo", True) else "Activar"
                    if st.button(etiqueta_cta, key=f"cta_emp_{correo_u}"):
                        u["activo"] = not u.get("activo", True)
                        st.rerun()

        st.markdown("---")
        st.markdown("### 2. Control de publicaciones (vacantes)")
        for v in st.session_state.vacantes:
            c1, c2 = st.columns([5, 1])
            with c1:
                st.write(
                    f"**#{v['id']} · {v['puesto']}** — {v['empresa']} ({v['tipo']}) · "
                    f"Estado: **{'Activa' if v.get('activa', True) else 'Oculta'}**"
                )
            with c2:
                accion_v = "Ocultar" if v.get("activa", True) else "Activar"
                if st.button(accion_v, key=f"toggle_vac_{v['id']}"):
                    v["activa"] = not v.get("activa", True)
                    st.rerun()

        st.markdown("---")
        st.markdown("### 3. Estadísticas de postulaciones por estado")
        if st.session_state.postulaciones:
            df_post = pd.DataFrame(st.session_state.postulaciones)
            resumen_estados = df_post["estado"].value_counts().reset_index()
            resumen_estados.columns = ["Estado", "Cantidad"]
            st.dataframe(resumen_estados, width="stretch", hide_index=True)
            st.bar_chart(resumen_estados.set_index("Estado"))
        else:
            st.info("Sin datos de postulaciones aún.")

        st.markdown("---")
        st.markdown("### 4. Gestión de usuarios registrados")
        df_users = pd.DataFrame(
            [
                {
                    "Nombre": u.get("nombre"),
                    "Correo": u.get("correo"),
                    "Rol": u.get("rol"),
                    "Carrera": u.get("carrera", "—"),
                    "Verificada": u.get("verificada", "—"),
                    "Activa": u.get("activo", True),
                }
                for u in st.session_state.usuarios.values()
            ]
        )
        st.dataframe(df_users, width="stretch", hide_index=True)


# ==========================================
# PÁGINA: SEGURIDAD Y ACERCA DEL PROYECTO
# ==========================================

elif pagina == "Seguridad y acerca":
    st.markdown('<p class="section-title">🛡️ Seguridad, permisos y acerca de la plataforma</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        <h3>🔐 Controles implementados en el prototipo</h3>
        • <b>Validación de correo institucional:</b> restringe el registro y acceso de estudiantes a dominios institucionales (@pachuca.tecnm.mx / @tecnm.mx).<br>
        • <b>Permisos por rol:</b> separa acciones de Visitante, Estudiante, Empresa y Administrador.<br>
        • <b>Verificación previa de empresas:</b> impide que empresas no verificadas publiquen ofertas activas.<br>
        • <b>Evaluaciones condicionadas:</b> exige postulación o experiencia registrada para habilitar calificaciones mutuas.<br>
        • <b>Escape HTML y control de publicaciones:</b> escapa entradas dinámicas en tarjetas HTML y permite activar/ocultar vacantes o suspender cuentas.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Descripción del proyecto")
    st.write(
        "ITP Empleo Local es una plataforma universitaria concebida para el Instituto Tecnológico de Pachuca "
        "con el objetivo de vincular a estudiantes con empleos, prácticas profesionales y residencias "
        "en Pachuca de Soto y su zona metropolitana bajo criterios académicos y de control institucional."
    )

    st.markdown("### Sectores contemplados")
    x, y, z = st.columns(3)
    with x:
        st.markdown("#### 🏭 Industrial")
        st.write("Producción, logística, mantenimiento, calidad y tecnología.")
    with y:
        st.markdown("#### 🛍️ Comercial")
        st.write("Administración, operaciones comerciales y atención.")
    with z:
        st.markdown("#### 💻 Servicios")
        st.write("Desarrollo de software, análisis de datos y consultoría.")

# ==========================================
# PIE DE PÁGINA
# ==========================================

st.markdown("""
<div class="footer">
    <b>ITP EMPLEO LOCAL</b><br>
    Instituto Tecnológico de Pachuca · Portal Universitario de Vinculación y Empleo<br>
    Conectando talento estudiantil con oportunidades locales.
</div>
""", unsafe_allow_html=True)