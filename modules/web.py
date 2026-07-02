from flask import Blueprint, render_template, jsonify, request
from modules.scanner import NetworkScanner
import yaml

web_bp = Blueprint('web', __name__)

# Cargar configuración
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Inicializar el escáner
scanner = NetworkScanner(config['network']['target'])

@web_bp.route('/')
def index():
    return render_template('index.html')

@web_bp.route('/api/scan', methods=['GET'])
def scan_network():
    """Endpoint para escanear la red y devolver dispositivos en JSON"""
    devices = scanner.scan_network()
    return jsonify({'devices': devices})

@web_bp.route('/api/scan_ports', methods=['POST'])
def scan_ports():
    """Endpoint para escanear puertos de una IP específica"""
    data = request.get_json()
    ip = data.get('ip')
    if ip:
        open_ports = scanner.scan_ports(ip)
        return jsonify({'ip': ip, 'open_ports': open_ports})
    return jsonify({'error': 'IP no proporcionada'}), 400
