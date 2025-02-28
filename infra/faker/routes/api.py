from flask import Blueprint, jsonify, request
import logging
import random
from generators.sql_generator import SQLGenerator
from generators.xss_generator import XSSGenerator
from generators.cmd_generator import CommandGenerator
from generators.buffer_generator import BufferGenerator
from generators.path_generate import PathGenerator
from generators.url_generator import URLGenerator
from generators.svg_generator import SVGGenerator
from generators.unicode_generator import UnicodeGenerator
from generators.user_generator import UserGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api = Blueprint('api', __name__)

class AttackGenerator:
    def __init__(self, generator):
        self.generator = generator
        
    def generate_attack(self):
        # Default implementation for generators that don't have generate_attack
        if hasattr(self.generator, 'generate_attack'):
            return self.generator.generate_attack()
        elif hasattr(self.generator, 'generate'):
            return self.generator.generate()
        else:
            return self.generator.generate_user()  # Fallback for UserGenerator

generators = {
    'sql': AttackGenerator(SQLGenerator()),
    'xss': AttackGenerator(XSSGenerator()),
    'cmd': AttackGenerator(CommandGenerator()),
    'buffer': AttackGenerator(BufferGenerator()),
    'path': AttackGenerator(PathGenerator()),
    'url': AttackGenerator(URLGenerator()),
    'svg': AttackGenerator(SVGGenerator()),
    'unicode': AttackGenerator(UnicodeGenerator()),
    'user': AttackGenerator(UserGenerator())
}

@api.route('/', defaults={'path': ''})
@api.route('/<path:path>')
def catch_all(path):
    """Root endpoint and catch-all route - mirrors the health check"""
    return health_check()

@api.route('/generate/user', methods=['GET'])
def generate_user():
    """Endpoint para gerar dados de usuário"""
    try:
        quantity = int(request.args.get('quantity', 1))
        invalid = request.args.get('invalid', 'false').lower() == 'true'

        if quantity < 1 or quantity > 100:
            return jsonify({'error': 'Quantity must be between 1 and 100'}), 400

        users = []
        for _ in range(quantity):
            if invalid:
                users.append(generators['user'].generate_attack())
            else:
                users.append(generators['user'].generate_attack())

        return jsonify(users)

    except Exception as e:
        logger.error(f"Error generating user data: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api.route('/generate/attack/<attack_type>', methods=['GET'])
def generate_specific_attack(attack_type):
    """Endpoint para gerar um tipo específico de ataque"""
    try:
        quantity = int(request.args.get('quantity', 1))
        if quantity < 1 or quantity > 100:
            return jsonify({'error': 'Quantity must be between 1 and 100'}), 400

        if attack_type not in generators:
            return jsonify({'error': f'Invalid attack type. Available types: {list(generators.keys())}'}), 400

        generator = generators[attack_type]
        attacks = [generator.generate_attack() for _ in range(quantity)]
        
        return jsonify({
            'type': attack_type,
            'quantity': quantity,
            'attacks': attacks
        })

    except Exception as e:
        logger.error(f"Error generating {attack_type} attack: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api.route('/generate/attack', methods=['GET'])
def generate_attack():
    """Endpoint para gerar ataques aleatórios ou específicos"""
    try:
        attack_type = request.args.get('type', 'random')
        quantity = int(request.args.get('quantity', 1))
        
        if quantity < 1 or quantity > 100:
            return jsonify({'error': 'Quantity must be between 1 and 100'}), 400

        attacks = []
        for _ in range(quantity):
            if attack_type == 'random':
                selected_type = random.choice(list(generators.keys()))
                generator = generators[selected_type]
                attack_data = generator.generate_attack()
                attacks.append({
                    'type': selected_type,
                    'data': attack_data
                })
            elif attack_type in generators:
                generator = generators[attack_type]
                attacks.append({
                    'type': attack_type,
                    'data': generator.generate_attack()
                })
            else:
                return jsonify({
                    'error': f'Invalid attack type: {attack_type}',
                    'available_types': list(generators.keys())
                }), 400

        return jsonify({
            'quantity': quantity,
            'attacks': attacks
        })

    except Exception as e:
        logger.error(f"Error generating attack data: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api.route('/generate/mixed', methods=['GET'])
def generate_mixed():
    """Endpoint para gerar ataques mistos"""
    try:
        quantity = int(request.args.get('quantity', 1))
        fields = request.args.get('fields', 'username,email,password,full_name').split(',')
        
        if quantity < 1 or quantity > 100:
            return jsonify({'error': 'Quantity must be between 1 and 100'}), 400

        mixed_attacks = []
        for _ in range(quantity):
            attack = {}
            for field in fields:
                field = field.strip()
                generator_type = random.choice(list(generators.keys()))
                generator = generators[generator_type]
                attack_data = generator.generate_attack()
                attack[field] = {
                    'value': attack_data,
                    'type': generator_type
                }
            mixed_attacks.append(attack)

        return jsonify({
            'quantity': quantity,
            'fields': fields,
            'attacks': mixed_attacks
        })

    except Exception as e:
        logger.error(f"Error generating mixed attack data: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api.route('/attacks/types', methods=['GET'])
def get_attack_types():
    """Endpoint para listar todos os tipos de ataques disponíveis"""
    return jsonify({
        'available_types': list(generators.keys()),
        'total': len(generators)
    })

@api.route('/health', methods=['GET'])
def health_check():
    """Endpoint de verificação de saúde"""
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'generators': list(generators.keys()),
        'endpoints': [
            '/generate/attack',
            '/generate/attack/<attack_type>',
            '/generate/mixed',
            '/generate/user',
            '/attacks/types',
            '/health'
        ]
    })
