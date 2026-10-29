from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

# Tus 5 ramos de prueba
RAMOS = [
    {"id": 1, "nombre": "Ramo de Rosas Rojas (12 pzs)", "precio": 450, "imagen": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=300"},
    {"id": 2, "nombre": "Bouquet de Girasoles", "precio": 380, "imagen": "https://images.unsplash.com/photo-1597848212624-a19eb35e2651?w=300"},
    {"id": 3, "nombre": "Arreglo de Tulipanes", "precio": 600, "imagen": "https://images.unsplash.com/photo-1563245372-f21724e3856d?w=300"},
    {"id": 4, "nombre": "Mix Silvestre de Temporada", "precio": 420, "imagen": "https://images.unsplash.com/photo-1526047932273-341f2a7631f9?w=300"},
    {"id": 5, "nombre": "Orquídea Blanca Elegante", "precio": 850, "imagen": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=300"}
]

@app.route('/')
def index():
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Mi Florería - Catálogo</title>
        <style>
            body { font-family: Arial, sans-serif; background: #f4f4f4; text-align: center; padding: 20px; }
            .grid { display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; }
            .card { background: white; border-radius: 8px; width: 250px; padding: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
            .card img { width: 100%; height: 180px; object-fit: cover; border-radius: 5px; }
            button { background: #28a745; color: white; border: none; padding: 10px 15px; border-radius: 5px; cursor: pointer; }
            button:hover { background: #218838; }
        </style>
    </head>
    <body>
        <h1>🌸 Catálogo de la Florería 🌸</h1>
        <div class="grid">
            {% for ramo in ramos %}
            <div class="card">
                <img src="{{ ramo.imagen }}" alt="{{ ramo.nombre }}">
                <h3>{{ ramo.nombre }}</h3>
                <p><b>${{ ramo.precio }} MXN</b></p>
                <form action="/checkout" method="GET">
                    <input type="hidden" name="ramo_id" value="{{ ramo.id }}">
                    <button type="submit">Comprar</button>
                </form>
            </div>
            {% endfor %}
        </div>
    </body>
    </html>
    """
    return render_template_string(html, ramos=RAMOS)

@app.route('/checkout')
def checkout():
    ramo_id = int(request.args.get('ramo_id', 1))
    ramo_seleccionado = next((r for r in RAMOS if r['id'] == ramo_id), RAMOS[0])
    
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Datos de Envío</title>
        <style>
            body { font-family: Arial, sans-serif; background: #f4f4f4; padding: 20px; }
            form { background: white; max-width: 400px; margin: 0 auto; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
            input, label { display: block; width: 100%; margin-bottom: 10px; }
            input { padding: 8px; box-sizing: border-box; }
            button { background: #007bff; color: white; border: none; padding: 10px; width: 100%; border-radius: 5px; cursor: pointer; }
        </style>
    </head>
    <body>
        <form action="/procesar-pago" method="POST">
            <h2>Completa tus datos</h2>
            <p>Estás comprando: <b>{{ ramo.nombre }} (${{ ramo.precio }})</b></p>
            <input type="hidden" name="ramo_nombre" value="{{ ramo.nombre }}">
            <input type="hidden" name="ramo_precio" value="{{ ramo.precio }}">
            
            <label>Nombre completo:</label>
            <input type="text" name="nombre" required>
            
            <label>Teléfono (WhatsApp):</label>
            <input type="text" name="telefono" placeholder="Ej: 521722XXXXXXXX" required>
            
            <label>Correo electrónico:</label>
            <input type="email" name="correo" required>
            
            <label>Fecha y hora deseada de entrega:</label>
            <input type="datetime-local" name="fecha" required>
            
            <button type="submit">Simular Pago y Enviar Pedido</button>
        </form>
    </body>
    </html>
    """
    return render_template_string(html, ramo=ramo_seleccionado)

@app.route('/procesar-pago', methods=['POST'])
def procesar_pago():
    nombre = request.form['nombre']
    telefono = request.form['telefono']
    correo = request.form['correo']
    fecha = request.form['fecha']
    ramo = request.form['ramo_nombre']
    precio = request.form['ramo_precio']

    # 1. Armamos el mensaje para la florería
    texto_mensaje = (
        f"🚨 *¡NUEVO PEDIDO DE FLORES!* 🚨\n\n"
        f"🌸 Ramo: {ramo} (${precio} MXN)\n"
        f"👤 Cliente: {nombre}\n"
        f"📱 Tel: {telefono}\n"
        f"📧 Email: {correo}\n"
        f"📅 Para fecha: {fecha}\n\n"
        f"_¡Entra al sistema para calcular y enviarle su tiempo estimado!_"
    )

    # --- TUS CREDENCIALES DE GREEN API ---
    id_instance = "710722785267"
    api_token = "da8d5f53af854cf2b5344d9a449a22593c3899d2130447bd87"
    chat_id = "5217221573060@c.us" 

    # Enviamos el mensaje automáticamente por la API
    url = f"https://api.green-api.com/waInstance{id_instance}/SendMessage/{api_token}"
    payload = {
        "chatId": chat_id,
        "message": texto_mensaje
    }
    requests.post(url, json=payload)

    return """
    <h2 style="text-align:center; color:green; font-family:Arial;">¡Pago Exitoso! 🎉</h2>
    <p style="text-align:center; color:family-sans; font-family:Arial;">Gracias por tu compra. El pedido ha sido procesado y enviado a tu WhatsApp automáticamente.</p>
    <p style="text-align:center;"><a href="/">Regresar al catálogo</a></p>
    """

if __name__ == '__main__':
    app.run(debug=True, port=5000)