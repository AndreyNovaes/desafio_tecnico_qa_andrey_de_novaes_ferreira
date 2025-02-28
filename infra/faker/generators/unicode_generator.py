from typing import Dict
import random

class UnicodeGenerator:
    def __init__(self):
        self.rtl_chars = [
            "\u200F",  # RTL Mark
            "\u061C",  # ALM
            "\u202E",  # RTL Override
            "\u202B",  # RTL Embedding
            "\u202D"   # LTR Override
        ]
        
        self.zero_width = [
            "\u200B",  # Zero Width Space
            "\u200C",  # Zero Width Non-Joiner
            "\u200D",  # Zero Width Joiner
            "\uFEFF",  # Zero Width No-Break Space
            "\u2060"   # Word Joiner
        ]
        
        self.homographs = [
            ("a", "а"),  # Latin 'a' vs Cyrillic 'а'
            ("e", "е"),  # Latin 'e' vs Cyrillic 'е'
            ("o", "о"),  # Latin 'o' vs Cyrillic 'о'
            ("p", "р"),  # Latin 'p' vs Cyrillic 'р'
            ("s", "ѕ")   # Latin 's' vs Cyrillic 'ѕ'
        ]
        
        self.combining_chars = [
            "\u0300",  # Combining Grave Accent
            "\u0301",  # Combining Acute Accent
            "\u0302",  # Combining Circumflex
            "\u0303",  # Combining Tilde
            "\u0304"   # Combining Macron
        ]
        
        self.special_spaces = [
            "\u2000",  # En Quad
            "\u2001",  # Em Quad
            "\u2002",  # En Space
            "\u2003",  # Em Space
            "\u2004",  # Three-Per-Em Space
            "\u2005",  # Four-Per-Em Space
            "\u2006",  # Six-Per-Em Space
            "\u2007",  # Figure Space
            "\u2008",  # Punctuation Space
            "\u2009"   # Thin Space
        ]
        
        self.math_symbols = [
            "∀", "∁", "∂", "∃", "∄",
            "∅", "∆", "∇", "∈", "∉",
            "∊", "∋", "∌", "∍", "∎"
        ]
        
        self.arrows = [
            "←", "↑", "→", "↓", "↔",
            "↕", "↖", "↗", "↘", "↙"
        ]

    def generate_attack(self) -> Dict[str, str]:
        """Gera um ataque com caracteres Unicode maliciosos"""
        attack_types = [
            self._generate_rtl_attack,
            self._generate_zero_width_attack,
            self._generate_homograph_attack,
            self._generate_combining_attack,
            self._generate_space_attack,
            self._generate_math_attack,
            self._generate_arrow_attack
        ]
        
        attack_func = random.choice(attack_types)
        return attack_func()

    def _generate_rtl_attack(self) -> Dict[str, str]:
        """Gera um ataque usando caracteres RTL"""
        username = f"admin{random.choice(self.rtl_chars)}rotartsinimda"
        password = f"pass{random.choice(self.rtl_chars)}word"
        
        return {
            'username': username,
            'email': f"{username}@kappapride.com",
            'password': password,
            'full_name': f"Admin{random.choice(self.rtl_chars)}User"
        }

    def _generate_zero_width_attack(self) -> Dict[str, str]:
        """Gera um ataque usando caracteres de largura zero"""
        zwc = random.choice(self.zero_width)
        username = f"a{zwc}d{zwc}m{zwc}i{zwc}n"
        password = f"p{zwc}a{zwc}s{zwc}s"
        
        return {
            'username': username,
            'email': f"{username}@kappapride.com",
            'password': password,
            'full_name': f"Admin{zwc}User"
        }

    def _generate_homograph_attack(self) -> Dict[str, str]:
        """Gera um ataque usando homógrafos"""
        word = "admin"
        homograph_word = ""
        
        for c in word:
            for latin, cyrillic in self.homographs:
                if c == latin:
                    homograph_word += cyrillic
                    break
            else:
                homograph_word += c
        
        return {
            'username': homograph_word,
            'email': f"{homograph_word}@kappapride.com",
            'password': homograph_word,
            'full_name': f"Admin User"
        }

    def _generate_combining_attack(self) -> Dict[str, str]:
        """Gera um ataque usando caracteres combinantes"""
        username = "admin"
        combined = ""
        
        for c in username:
            combined += c + random.choice(self.combining_chars)
        
        return {
            'username': combined,
            'email': f"admin@kappapride.com",
            'password': combined,
            'full_name': combined
        }

    def _generate_space_attack(self) -> Dict[str, str]:
        """Gera um ataque usando diferentes tipos de espaço"""
        spaces = random.sample(self.special_spaces, 3)
        username = f"admin{spaces[0]}user{spaces[1]}name{spaces[2]}"
        
        return {
            'username': username,
            'email': f"admin@kappapride.com",
            'password': username,
            'full_name': username
        }

    def _generate_math_attack(self) -> Dict[str, str]:
        """Gera um ataque usando símbolos matemáticos"""
        symbols = random.sample(self.math_symbols, 3)
        attack = f"admin{symbols[0]}{symbols[1]}{symbols[2]}"
        
        return {
            'username': attack,
            'email': f"{attack}@kappapride.com",
            'password': attack,
            'full_name': attack
        }

    def _generate_arrow_attack(self) -> Dict[str, str]:
        """Gera um ataque usando setas Unicode"""
        arrows = random.sample(self.arrows, 3)
        attack = f"admin{arrows[0]}{arrows[1]}{arrows[2]}"
        
        return {
            'username': attack,
            'email': f"{attack}@kappapride.com",
            'password': attack,
            'full_name': attack
        }
