from pathlib import Path
from PIL import Image

ROOT = Path('/home/ubuntu/lets-dance-mvp/assets/images')
TARGETS = [
    'icon.png',
    'android-icon-foreground.png',
    'favicon.png',
    'splash-icon.png',
]

for name in TARGETS:
    path = ROOT / name
    with Image.open(path) as img:
        img = img.convert('RGBA')
        img.thumbnail((1024, 1024))
        img.save(path, format='PNG', optimize=True)
        print(f'optimized {name}: {path.stat().st_size} bytes')
