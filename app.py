from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- PRECIOS BASE (Estrategia Portafolio) ---
PRECIOS = {
    'landing': 35000,       # Base accesible
    'corporativa': 75000,   # Pymes
    'ecommerce': 150000,    # Tienda
    'webapp': 200000        # App
}

EXTRAS = {
    'seo': 15000,
    'hosting': 15000,
    'admin': 30000
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cotizar', methods=['POST'])
def cotizar():
    data = request.get_json()
    
    # 1. Precio Base
    tipo_sitio = data.get('tipo', 'landing')
    total = PRECIOS.get(tipo_sitio, 0)
    
    # 2. Factor de Diseño (AQUI ESTÁ EL CAMBIO)
    # Estandar = x1.0
    # Premium = x1.5 (50% más caro, pero incluye más cosas)
    if data.get('diseno') == 'premium':
        total = int(total * 1.5) 
    
    # 3. Extras
    servicios_extra = data.get('extras', [])
    for servicio in servicios_extra:
        total += EXTRAS.get(servicio, 0)
    
    # Formateo moneda chilena
    precio_formateado = f"${total:,.0f}".replace(",", ".")
    
    return jsonify({
        'precio': precio_formateado,
        'mensaje': 'Precio promocional por construcción de portafolio.'
    })

if __name__ == '__main__':
    app.run(debug=True)