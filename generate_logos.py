"""Generate authentic classic automotive SVG logos"""

logos = {
    "suzuki.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="100%" height="100%">
  <rect width="100%" height="100%" fill="#ffffff"/>
  <g transform="translate(50, 15) scale(0.9)">
    <!-- Suzuki iconic S emblem -->
    <path d="M 175.7,2.8 L 52.8,2.8 L 41.5,41.9 L 140.2,41.9 L 41.5,123.5 L 41.5,164.7 L 165.4,164.7 L 176.7,125.6 L 77.0,125.6 L 175.7,44.0 Z" fill="#E31B23"/>
    <text x="110" y="195" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="19" font-weight="800" letter-spacing="4" fill="#1f2937" text-anchor="middle">MARUTI SUZUKI</text>
  </g>
</svg>''',

    "honda.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="100%" height="100%">
  <rect width="100%" height="100%" fill="#ffffff"/>
  <g transform="translate(60, 15) scale(0.9)">
    <!-- Honda classic trapezoid badge with H -->
    <path d="M 25,20 C 12,20 5,28 8,45 L 28,145 C 31,160 40,168 55,168 L 145,168 C 160,168 169,160 172,145 L 192,45 C 195,28 188,20 175,20 Z" fill="none" stroke="#2563eb" stroke-width="8"/>
    <path d="M 52,40 L 68,148 L 84,148 L 88,102 C 88,96 92,92 100,92 C 108,92 112,96 112,102 L 116,148 L 132,148 L 148,40 L 130,40 L 122,86 C 120,90 115,92 108,92 L 92,92 C 85,92 80,90 78,86 L 70,40 Z" fill="#2563eb"/>
    <text x="100" y="195" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="20" font-weight="800" letter-spacing="5" fill="#1f2937" text-anchor="middle">HONDA</text>
  </g>
</svg>''',

    "hyundai.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="100%" height="100%">
  <rect width="100%" height="100%" fill="#ffffff"/>
  <g transform="translate(50, 20) scale(0.9)">
    <!-- Hyundai classic oval ring -->
    <ellipse cx="110" cy="85" rx="100" ry="60" fill="none" stroke="#002c5f" stroke-width="9"/>
    <!-- Slanted italic H -->
    <path d="M 52,122 C 55,108 65,72 75,50 C 78,45 84,45 88,46 L 98,48 C 94,56 86,76 80,94 L 125,78 C 129,72 135,56 142,42 C 145,38 152,38 156,40 L 165,42 C 158,58 145,95 138,125 C 135,129 130,130 125,128 L 115,126 C 118,118 124,100 128,88 L 85,104 C 82,109 76,124 70,136 C 68,140 60,140 56,138 Z" fill="#002c5f"/>
    <text x="110" y="185" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="20" font-weight="800" letter-spacing="4" fill="#1f2937" text-anchor="middle">HYUNDAI</text>
  </g>
</svg>''',

    "toyota.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="100%" height="100%">
  <rect width="100%" height="100%" fill="#ffffff"/>
  <g transform="translate(50, 18) scale(0.9)">
    <!-- Toyota classic 3-oval emblem -->
    <ellipse cx="110" cy="85" rx="98" ry="62" fill="none" stroke="#eb0a1e" stroke-width="8"/>
    <ellipse cx="110" cy="62" rx="60" ry="26" fill="none" stroke="#eb0a1e" stroke-width="7"/>
    <ellipse cx="110" cy="86" rx="24" ry="58" fill="none" stroke="#eb0a1e" stroke-width="7"/>
    <text x="110" y="190" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="20" font-weight="800" letter-spacing="5" fill="#1f2937" text-anchor="middle">TOYOTA</text>
  </g>
</svg>''',

    "classic_badge.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="32" height="32">
  <rect x="2" y="2" width="60" height="60" rx="14" fill="#1f2937"/>
  <path d="M12 40 L20 22 C22 18 26 16 30 16 L34 16 C38 16 42 18 44 22 L52 40 C54 44 51 48 46 48 L18 48 C13 48 10 44 12 40 Z" fill="none" stroke="#60a5fa" stroke-width="3" stroke-linecap="round"/>
  <circle cx="22" cy="44" r="4" fill="#ffffff"/>
  <circle cx="42" cy="44" r="4" fill="#ffffff"/>
  <path d="M22 28 L42 28" stroke="#93c5fd" stroke-width="2.5" stroke-linecap="round"/>
</svg>'''
}

import os
for name, content in logos.items():
    with open(f"/Users/SujalSingh/Machine_Learnig_1/static/logos/{name}", "w") as f:
        f.write(content)
print("Logos created successfully!")
