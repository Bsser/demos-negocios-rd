"""Videos de ejemplo por sector para la página de servicios (usa el motor de Shorts del repo privado). Uso: python videos.py"""
import pathlib, sys
sys.path.insert(0, r"C:\Users\Jonathan Garcia\ClaudeProyects\redes-rd\privado\marketing")
from shorts import generar

V = pathlib.Path(__file__).parent / "v"
V.mkdir(exist_ok=True)
PIE = "Video de ejemplo · Jarvis Digital RD"
VIDEOS = {
    "demo-restaurante": {"color": "#b33a1b", "marca": "Tu restaurante aquí", "url": PIE, "slides": [
        ("El almuerzo más rico de la zona", "¿No sabes dónde almorzar hoy? Aquí te tenemos lo tuyo."),
        ("Plato del día con jugo natural", "Todos los días, plato del día con su jugo natural."),
        ("Abierto de lunes a sábado", "Abrimos de lunes a sábado, desde temprano."),
        ("Delivery en tu zona", "Y si no puedes venir, te lo llevamos."),
        ("Pide por WhatsApp", "Escríbenos por WhatsApp y haz tu pedido."),
    ]},
    "demo-salon": {"color": "#8a2c6b", "marca": "Tu salón aquí", "url": PIE, "slides": [
        ("¿Lista para el fin de semana?", "¿Lista para el fin de semana? Ven y te ponemos linda."),
        ("Cortes, tintes, mechas y uñas", "Cortes, tintes, mechas, manicure y pedicure."),
        ("Citas el mismo día", "Tenemos citas el mismo día."),
        ("Productos profesionales", "Trabajamos con productos profesionales."),
        ("Reserva tu cita por WhatsApp", "Reserva tu cita por WhatsApp. Te esperamos."),
    ]},
    "demo-inmobiliaria": {"color": "#0d47a1", "marca": "Tu inmobiliaria aquí", "url": PIE, "slides": [
        ("Apartamento en venta en Santo Domingo", "Apartamento en venta en Santo Domingo."),
        ("3 habitaciones · 2 baños · parqueo", "Tres habitaciones, dos baños y parqueo."),
        ("Área social con piscina", "Con área social y piscina."),
        ("Cerca de supermercados y colegios", "Cerca de supermercados, colegios y avenidas principales."),
        ("Agenda tu visita por WhatsApp", "Agenda tu visita por WhatsApp hoy mismo."),
    ]},
}
if __name__ == "__main__":
    for clave, s in VIDEOS.items():
        generar(clave, s, V)
    for f in [*V.glob("*-[0-9].*"), *V.glob("*.txt")]:
        f.unlink()  # solo quedan los .mp4 finales
