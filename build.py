"""Páginas de muestra para negocios de RD (prospectos). Genera docs/<id>/ desde demos.json + docs/index.html (servicios y precios).
Todas llevan noindex y un aviso de "página de muestra, no oficial". Si un negocio pide quitarla, bórrala de demos.json y reconstruye.
Uso: python build.py"""
import html, json, pathlib, shutil, urllib.parse

SITIO = "https://bsser.github.io/demos-negocios-rd"
RAIZ = pathlib.Path(__file__).parent
SALIDA = RAIZ / "docs"
e = html.escape

COLOR = {"restaurante": ("#b33a1b", "#fff4ec"), "salon": ("#8a2c6b", "#fbf0f7"), "inmobiliaria": ("#0d47a1", "#eef4fc"),
         "tienda": ("#1d6b3a", "#eef7f1"), "otro": ("#4a3aa8", "#f2f0fc")}
SECCIONES = {  # texto genérico de ejemplo; se marca como ejemplo en la página
    "restaurante": ("Nuestro menú", ["Plato del día", "Desayunos dominicanos", "Jugos naturales", "Postres"]),
    "salon": ("Servicios", ["Corte y peinado", "Tinte y mechas", "Manicure y pedicure", "Tratamientos"]),
    "inmobiliaria": ("Propiedades destacadas", ["Apartamento en venta", "Casa en alquiler", "Solar en venta", "Local comercial"]),
    "tienda": ("Lo que ofrecemos", ["Productos principales", "Ofertas de la semana", "Pedidos por WhatsApp", "Entrega a domicilio"]),
    "otro": ("Servicios", ["Servicio principal", "Planes y precios", "Reservas por WhatsApp", "Promociones"]),
}

CSS = """*{box-sizing:border-box}body{margin:0;font:17px/1.6 system-ui,"Segoe UI",Arial,sans-serif;color:#1b1f24;background:#fff}
.aviso{background:#fff6d6;color:#5b4a00;font-size:13px;text-align:center;padding:6px 12px}
.hero{background:var(--c);color:#fff;padding:56px 16px 48px;text-align:center}
.hero h1{font-size:clamp(30px,7vw,52px);line-height:1.1;margin:0 0 10px}.hero p{font-size:19px;opacity:.95;margin:0 auto 22px;max-width:640px}
.btn{display:inline-block;background:#25d366;color:#08311a;font-weight:800;padding:14px 24px;border-radius:999px;text-decoration:none;margin:4px}
.btn.sec{background:#fff;color:var(--c)}
main{max-width:900px;margin:0 auto;padding:8px 16px 40px}h2{color:var(--c);margin-top:36px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:14px;padding:0;list-style:none}
.grid li{background:var(--f);border-radius:14px;padding:18px;font-weight:700}.grid small{display:block;font-weight:400;color:#5b6470}
.info{background:var(--f);border-radius:14px;padding:18px 20px}.info p{margin:6px 0}
footer{text-align:center;color:#5b6470;font-size:13px;padding:24px 16px 40px;border-top:1px solid #e3e6ea}
.precios td,.precios th{border-bottom:1px solid #e3e6ea;padding:10px 8px;text-align:left;vertical-align:top}.precios{border-collapse:collapse;width:100%}
video{width:100%;max-width:320px;border-radius:14px;display:block;margin:10px 0}"""


def wa(tel):
    d = "".join(c for c in tel if c.isdigit())
    if len(d) == 10:
        d = "1" + d  # RD: +1 809/829/849
    return f"https://wa.me/{d}" if len(d) == 11 else ""


def doc(titulo, color, fondo, cuerpo, base):
    return (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<meta name="robots" content="noindex,nofollow"><title>{e(titulo)}</title><link rel="stylesheet" href="{base}e.css">'
            f'<style>:root{{--c:{color};--f:{fondo}}}</style></head><body>{cuerpo}</body></html>')


def demo(n):
    c, f = COLOR.get(n["sector"], COLOR["otro"])
    titulo_sec, items = SECCIONES.get(n["sector"], SECCIONES["otro"])
    w = wa(n.get("telefono", ""))
    mapa = "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(f"{n['nombre']} {n.get('direccion') or n['ciudad']}")
    tel = "".join(c for c in n.get("telefono", "") if c.isdigit())
    botones = (f"<a class='btn' href='{w}'>Escríbenos por WhatsApp</a>" if w and n.get("wa") else f"<a class='btn' href='tel:+1{tel}'>Llámanos</a>" if tel else "") + f"<a class='btn sec' href='{mapa}'>Cómo llegar</a>"
    info = "".join(f"<p><b>{k}:</b> {e(v)}</p>" for k, v in [("Dirección", n.get("direccion", "")), ("Horario", n.get("horario", "")),
                                                          ("Teléfono", n.get("telefono", "")), ("Instagram", n.get("instagram", ""))] if v)
    cuerpo = (f"<div class='aviso'>Página de muestra hecha por Jarvis Digital RD para {e(n['nombre'])}. No es su sitio oficial.</div>"
              f"<section class='hero'><h1>{e(n['nombre'])}</h1><p>{e(n.get('especialidad') or '')}</p>{botones}</section><main>"
              f"<h2>{titulo_sec}</h2><ul class='grid'>" + "".join(f"<li>{e(i)}<small>Ejemplo: aquí va tu foto, descripción y precio</small></li>" for i in items) + "</ul>"
              f"<h2>Visítanos</h2><div class='info'>{info}</div></main>"
              "<footer>Así se vería tu página: rápida, lista para el celular, con botón de WhatsApp y ubicación. "
              "<a href='../'>Ver precios y ejemplos de videos</a></footer>")
    return doc(f"{n['nombre']} (muestra)", c, f, cuerpo, "../")


def portada(videos):
    vids = "".join(f"<div><b>{e(t)}</b><video src='v/{v}' controls preload='none' playsinline></video></div>" for t, v in videos)
    filas = [("Página web sencilla", "Tu negocio en internet y en el celular: servicios, horario, ubicación y botón de WhatsApp. Hosting gratis incluido.", "RD$5,000 (pago único)"),
             ("Videos para Instagram, TikTok y estado de WhatsApp", "Videos verticales de 20-40 s con tus fotos, texto y voz dominicana.", "RD$1,500 c/u · 4 por RD$4,000"),
             ("Menú digital con código QR", "Tu menú en el celular del cliente; cuando cambies precios, te lo actualizamos. Te damos el QR para imprimir.", "RD$2,500"),
             ("Video de propiedad (inmobiliarias)", "Video vertical con fotos, precio, metraje y contacto.", "RD$1,500 por propiedad")]
    tabla = "<table class='precios'><tr><th>Servicio</th><th>Qué incluye</th><th>Precio</th></tr>" + "".join(
        f"<tr><td><b>{a}</b></td><td>{b}</td><td>{p}</td></tr>" for a, b, p in filas) + "</table>"
    cuerpo = ("<section class='hero'><h1>Jarvis Digital RD</h1><p>Páginas web, videos y menús QR para negocios dominicanos. "
              "Rápido, a buen precio, y sin que tengas que saber de tecnología.</p></section><main>"
              f"<h2>Precios</h2>{tabla}<h2>Cómo trabajamos</h2><ol><li>Nos mandas tus fotos y datos por correo o WhatsApp.</li>"
              "<li>En 24-48 horas te enviamos el trabajo para que lo revises (1 ronda de cambios incluida).</li>"
              "<li>Pagas por transferencia cuando lo apruebas.</li></ol>"
              + (f"<h2>Ejemplos de videos</h2><div class='grid'>{vids}</div>" if vids else "")
              + "</main><footer>Para pedir un trabajo, responde al correo que te enviamos.</footer>")
    return doc("Jarvis Digital RD: páginas web, videos y menús QR para negocios", "#1b1f24", "#f3f4f6", cuerpo, "")


if __name__ == "__main__":
    datos = json.loads((RAIZ / "demos.json").read_text(encoding="utf-8"))
    if SALIDA.exists():
        shutil.rmtree(SALIDA)
    SALIDA.mkdir()
    (SALIDA / "e.css").write_text(CSS, encoding="utf-8")
    if (RAIZ / "v").exists():
        shutil.copytree(RAIZ / "v", SALIDA / "v")
    videos = [(t, v) for t, v in datos.get("videos", []) if (SALIDA / "v" / v).exists()]
    (SALIDA / "index.html").write_text(portada(videos), encoding="utf-8")
    for n in datos["negocios"]:
        (SALIDA / n["id"]).mkdir()
        (SALIDA / n["id"] / "index.html").write_text(demo(n), encoding="utf-8")
    (SALIDA / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")
    (SALIDA / ".nojekyll").write_text("")
    assert wa("809-555-1234") == "https://wa.me/18095551234" and wa("") == ""
    for n in datos["negocios"]:
        assert "noindex" in (SALIDA / n["id"] / "index.html").read_text(encoding="utf-8")
    print(f"OK: {len(datos['negocios'])} muestras, {len(videos)} videos en docs/")
