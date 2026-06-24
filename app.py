"""
=====================================================================
 Plantillas de Mensajes para Citas
 ConfiguroWeb · 2026 · Python real en el navegador (PyScript)
=====================================================================
"""
from pyscript import document, window
from js import localStorage
import json
import math

APP_CLAVE = "python_plantillas_mensajes_citas_datos"
VERSION = "1.0.0"


# =====================================================================
#  Lógica de negocio
# =====================================================================
class Calculadora:
    """Modelo de cálculo de Plantillas de Mensajes para Citas."""

    def __init__(self, tipo, cliente, fecha, hora):
        self.tipo = float(tipo)
        self.cliente = float(cliente)
        self.fecha = float(fecha)
        self.hora = float(hora)

    def calcular(self):
        """Ejecuta el cálculo principal y devuelve un dict de resultados."""

        t = str(self.tipo).lower().strip()
        if "confir" in t:
            msg = (f"Estimado/a {self.cliente}, confirmamos su cita para el "
                   f"{self.fecha} a las {self.hora}. Gracias por su preferencia.")
        elif "reagen" in t or "camb" in t:
            msg = (f"Hola {self.cliente}, necesitamos reagendar su cita del {self.fecha} "
                   f"a las {self.hora}. ¿Le queda bien o prefiere otro horario?")
        else:
            msg = (f"Estimado/a {self.cliente}, lamentamos informarle que debemos "
                   f"cancelar su cita del {self.fecha}. Agendaremos una nueva pronto.")
        return {"mensaje": msg, "caracteres": len(msg)}


    def diagnostico(self, resultados):
        """Texto explicativo del resultado."""
        return "✅ Mensaje listo para copiar y enviar."


# =====================================================================
#  Formateadores
# =====================================================================
def fmt_moneda(v):
    if v is None:
        return "—"
    if math.isinf(v):
        return "∞"
    return f"${v:,.0f}"

def fmt_num(v):
    if v is None:
        return "—"
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return f"{v:,}"

def fmt_pct(v):
    if v is None:
        return "—"
    return f"{v:.1f}%"


# =====================================================================
#  Persistencia localStorage
# =====================================================================
def cargar_guardado():
    try:
        raw = localStorage.getItem(APP_CLAVE)
        if raw:
            return json.loads(raw)
    except Exception:
        pass
    return None

def guardar_ls(datos):
    try:
        localStorage.setItem(APP_CLAVE, json.dumps(datos))
        return True
    except Exception:
        return False


# =====================================================================
#  UI helpers
# =====================================================================
def input_float(eid):
    el = document.querySelector(f"#{eid}")
    if not el or not el.value:
        return 0.0
    try:
        return float(el.value)
    except (ValueError, TypeError):
        return 0.0

def mostrar(html, clase=""):
    caja = document.querySelector("#resultado")
    caja.innerHTML = html
    caja.classList.remove("hidden", "is-error", "is-success")
    if clase:
        caja.classList.add(clase)


# =====================================================================
#  Handlers
# =====================================================================
def calcular_handler(event=None):
    """Lee inputs, instancia, calcula y muestra."""

    c = Calculadora(
        document.querySelector("#tipo").value or "",
        document.querySelector("#cliente").value or "",
        document.querySelector("#fecha").value or "",
        document.querySelector("#hora").value or "",
    )
    r = c.calcular()
    html = f"""
      <div class="result-value">💬 Mensaje generado</div>
      <p style="white-space:pre-wrap;background:#fff;padding:1rem;border-radius:8px;border:1px solid var(--cweb-border);">{r["mensaje"]}</p>
      <p class="result-detail">{r["caracteres"]} caracteres · {c.diagnostico(r)}</p>
    """
    mostrar(html, clase="is-success")



def guardar_datos(event=None):
    datos = {
            "tipo": input_float("tipo"),
            "cliente": input_float("cliente"),
            "fecha": input_float("fecha"),
            "hora": input_float("hora"),
        "version": VERSION,
    }
    ok = guardar_ls(datos)
    if ok:
        mostrar("💾 Datos guardados en este navegador.", clase="is-success")
    else:
        mostrar("❌ No se pudieron guardar los datos.", clase="is-error")


def cargar_al_inicio():
    datos = cargar_guardado()
    if not datos:
        return
    try:
        if "tipo" in datos:
            document.querySelector("#tipo").value = datos["tipo"]
        if "cliente" in datos:
            document.querySelector("#cliente").value = datos["cliente"]
        if "fecha" in datos:
            document.querySelector("#fecha").value = datos["fecha"]
        if "hora" in datos:
            document.querySelector("#hora").value = datos["hora"]
        aviso = document.querySelector("#resultado")
        aviso.innerHTML = "📂 Datos cargados. Pulsa <em>Calcular</em>."
        aviso.classList.remove("hidden")
    except Exception:
        pass


def inicializar():
    cargar_al_inicio()
    window.dispatchEvent(window.Event.new("py:ready"))

inicializar()
