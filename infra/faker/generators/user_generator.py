from faker import Faker
from typing import Dict, List
import random
import string
import re

class UserGenerator:
    def __init__(self, locale: str = 'pt_BR'):
        self.faker = Faker(locale)
        self._init_patterns()

    def _init_patterns(self):
        """Inicializa padrões para geração de dados"""
        self.email_patterns = [
            "{first}.{last}@{domain}",
            "{first}_{last}@{domain}",
            "{first}{year}@{domain}",
            "{first[0]}{last}@{domain}",
            "{last}.{first}@{domain}"
        ]
        
        self.username_patterns = [
            "{first}.{last}",
            "{first}_{last}",
            "{first}{year}",
            "{first[0]}{last}",
            "{last}.{first}"
        ]
        
        self.password_requirements = {
            'min_length': 8,
            'max_length': 20,
            'require_upper': True,
            'require_lower': True,
            'require_digits': True,
            'require_special': True
        }
        
        self.common_domains = [
            'gmail.com', 'yahoo.com', 'hotmail.com',
            'outlook.com', 'protonmail.com', 'icloud.com'
        ]

    def generate_user(self) -> Dict[str, str]:
        """Gera dados de usuário aleatórios"""
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        year = str(random.randint(1970, 2000))
        domain = random.choice(self.common_domains)
        
        pattern_data = {
            'first': first_name.lower(),
            'last': last_name.lower(),
            'year': year,
            'domain': domain
        }
        
        email_pattern = random.choice(self.email_patterns)
        username_pattern = random.choice(self.username_patterns)
        
        email = self._format_pattern(email_pattern, pattern_data)
        username = self._format_pattern(username_pattern, pattern_data)
        
        return {
            'username': username,
            'email': email,
            'password': self._generate_strong_password(),
            'full_name': f"{first_name} {last_name}"
        }

    def generate_invalid_data(self) -> Dict[str, str]:
        """Gera dados inválidos para testes negativos"""
        invalid_types = [
            self._generate_empty_data,
            self._generate_whitespace_data,
            self._generate_malformed_email,
            self._generate_weak_password,
            self._generate_long_data
        ]
        
        return random.choice(invalid_types)()

    def _format_pattern(self, pattern: str, data: Dict[str, str]) -> str:
        """Formata um padrão com os dados fornecidos"""
        result = pattern
        
        # Substituição básica
        for key, value in data.items():
            result = result.replace(f"{{{key}}}", value)
        
        # Substituição com slice
        slice_pattern = re.compile(r'\{(\w+)\[(\d+)\]\}')
        matches = slice_pattern.finditer(result)
        
        for match in matches:
            key, index = match.groups()
            if key in data:
                value = data[key][int(index)]
                result = result.replace(match.group(0), value)
        
        return result

    def _generate_strong_password(self, length: int = 12) -> str:
        """Gera uma senha forte que atende aos requisitos"""
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        special = "!@#$%^&*"
        
        # Garantir pelo menos um de cada tipo
        password = [
            random.choice(lowercase),
            random.choice(uppercase),
            random.choice(digits),
            random.choice(special)
        ]
        
        # Completar com caracteres aleatórios
        all_chars = lowercase + uppercase + digits + special
        for _ in range(length - 4):
            password.append(random.choice(all_chars))
            
        random.shuffle(password)
        return ''.join(password)

    def _generate_empty_data(self) -> Dict[str, str]:
        """Gera dados vazios"""
        return {
            'username': '',
            'email': '',
            'password': '',
            'full_name': ''
        }

    def _generate_whitespace_data(self) -> Dict[str, str]:
        """Gera dados com espaços em branco"""
        return {
            'username': '   ',
            'email': '   ',
            'password': '   ',
            'full_name': '   '
        }

    def _generate_malformed_email(self) -> Dict[str, str]:
        """Gera emails mal formados"""
        malformed_emails = [
            'invalid.email',
            'invalid@',
            '@domain.com',
            'invalid@domain',
            'invalid@domain.',
            '.invalid@domain.com',
            'invalid@.com',
            'invalid@domain..com'
        ]
        
        return {
            'username': self.faker.user_name(),
            'email': random.choice(malformed_emails),
            'password': self._generate_strong_password(),
            'full_name': self.faker.name()
        }

    def _generate_weak_password(self) -> Dict[str, str]:
        """Gera senhas fracas"""
        weak_passwords = [
            '123456',
            'password',
            'qwerty',
            'abc123',
            'letmein',
            'admin',
            'welcome',
            'monkey123',
            'q1w2e3'
        ]
        
        return {
            'username': self.faker.user_name(),
            'email': self.faker.email(),
            'password': random.choice(weak_passwords),
            'full_name': self.faker.name()
        }

    def _generate_long_data(self) -> Dict[str, str]:
        """Gera dados muito longos"""
        long_string = 'a' * 256
        
        return {
            'username': long_string,
            'email': f"{long_string}@domain.com",
            'password': long_string,
            'full_name': long_string
        }
