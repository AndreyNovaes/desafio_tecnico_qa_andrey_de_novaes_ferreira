from typing import Dict
import random
import string

class BufferGenerator:
    def __init__(self):
        self.basic_overflow = [
            "A" * 1000,
            "B" * 5000,
            "C" * 10000,
            "D" * 0xFFFF,
            "E" * 65535
        ]
        
        self.format_string = [
            "%x" * 1000,
            "%s" * 1000,
            "%n" * 100,
            "%p" * 500,
            "%.1000x"
        ]
        
        self.null_bytes = [
            "\x00" * 1000,
            "\xff" * 1000,
            "\x90" * 1000,  # NOP sled
            "\xcc" * 1000,  # INT3
            "\xcd\x03" * 500  # INT3 with argument
        ]
        
        self.unicode_overflow = [
            "🔥" * 1000,
            "💣" * 1000,
            "🚀" * 1000,
            "👾" * 1000,
            "⚡" * 1000
        ]
        
        self.special_chars = [
            "../" * 1000,
            "<!--" * 1000,
            "-->" * 1000,
            "]]>" * 1000,
            "<![CDATA[" * 500
        ]

    def generate_attack(self) -> Dict[str, str]:
        """Gera um ataque de buffer overflow aleatório"""
        all_overflow = (
            self.basic_overflow +
            self.format_string +
            self.null_bytes +
            self.unicode_overflow +
            self.special_chars
        )
        
        overflow = random.choice(all_overflow)
        return {
            'username': overflow,
            'email': f"{overflow[:10]}@overflow.com",
            'password': overflow,
            'full_name': overflow
        }

    def generate_shellcode_pattern(self, length: int = 1000) -> Dict[str, str]:
        """Gera um padrão cíclico para encontrar offsets"""
        pattern = ''
        for i in range(length):
            pattern += string.ascii_uppercase[i % 26]
            pattern += string.ascii_lowercase[i % 26]
            pattern += string.digits[i % 10]
            
        return {
            'username': pattern,
            'password': pattern
        }

    def generate_heap_spray(self) -> Dict[str, str]:
        """Gera um ataque de heap spray"""
        nop_sled = "\x90" * 1000
        payload = "A" * 100
        padding = "B" * (5000 - len(nop_sled) - len(payload))
        
        spray = nop_sled + payload + padding
        
        return {
            'username': spray,
            'password': spray
        }

    def generate_format_string(self) -> Dict[str, str]:
        """Gera ataques de format string"""
        formats = [
            "%x." * 100,
            "%n" * 50,
            "%s%s%s%s%s",
            "%x%n%x%n%x",
            "%.1000d"
        ]
        return {
            'username': random.choice(formats),
            'password': random.choice(formats)
        }
