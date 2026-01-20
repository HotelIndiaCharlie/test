#!/usr/bin/env python3
"""
Magazine Layout Generator - Creates stunning A4 spread layouts
Optimized for drawbot-skia
"""

import json
import random
from pathlib import Path
import re

from drawbot_skia.drawbot import *
from text_helpers import textBox


class MagazineDesigner:
    """Creates stunning magazine layouts"""

    def __init__(self):
        # A4 spread dimensions (in points at 72 DPI)
        self.width = 595.28 * 2  # Double page
        self.height = 841.89
        self.margin = 60

        # Color palettes
        self.palettes = [
            {'primary': (0.1, 0.1, 0.15), 'accent': (0.9, 0.3, 0.3), 'bg': (0.98, 0.98, 0.96)},
            {'primary': (0.05, 0.15, 0.25), 'accent': (0.2, 0.6, 0.8), 'bg': (0.99, 0.99, 0.98)},
            {'primary': (0.15, 0.1, 0.1), 'accent': (0.8, 0.5, 0.2), 'bg': (0.97, 0.96, 0.95)},
            {'primary': (0.1, 0.15, 0.1), 'accent': (0.4, 0.7, 0.4), 'bg': (0.98, 0.99, 0.97)},
            {'primary': (0.2, 0.1, 0.15), 'accent': (0.9, 0.4, 0.6), 'bg': (0.99, 0.97, 0.98)},
            {'primary': (0.08, 0.08, 0.12), 'accent': (0.6, 0.4, 0.9), 'bg': (0.98, 0.98, 0.99)},
            {'primary': (0.15, 0.1, 0.05), 'accent': (0.95, 0.7, 0.3), 'bg': (0.99, 0.98, 0.96)},
            {'primary': (0.05, 0.12, 0.15), 'accent': (0.3, 0.8, 0.8), 'bg': (0.97, 0.99, 0.99)},
            {'primary': (0.12, 0.08, 0.12), 'accent': (0.8, 0.3, 0.5), 'bg': (0.99, 0.97, 0.98)},
            {'primary': (0.08, 0.10, 0.08), 'accent': (0.5, 0.6, 0.3), 'bg': (0.98, 0.99, 0.97)},
        ]

        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)

    def create(self, article, index):
        """Create layout for an article"""

        palette = self.palettes[index % len(self.palettes)]

        newDrawing()
        newPage(self.width, self.height)

        # Background
        fill(*palette['bg'])
        rect(0, 0, self.width, self.height)

        # Select layout style
        layouts = [
            self.style_minimalist,
            self.style_grid,
            self.style_asymmetric,
            self.style_editorial,
            self.style_geometric,
            self.style_swiss,
            self.style_bold,
            self.style_elegant,
            self.style_modern,
            self.style_magazine,
        ]

        layouts[index % len(layouts)](article, palette, index)

        # Save
        filename = f"layout_{index+1:02d}_{self.clean(article['title'])}.pdf"
        saveImage(str(self.output_dir / filename))
        endDrawing()

        return filename

    def style_minimalist(self, article, pal, idx):
        """Minimalist typography"""

        # Large title
        fill(*pal['primary'])
        font("Helvetica-Bold", 72)
        textBox(article['title'].upper(),
               (self.margin, self.height * 0.4, self.width * 0.4, self.height * 0.4),
               align="left")

        # Accent line
        fill(*pal['accent'])
        rect(self.margin, self.height * 0.35, 120, 8)

        # Extract
        fill(*pal['primary'])
        font("Helvetica", 16)
        textBox(article['extract'],
               (self.margin, self.height * 0.12, self.width * 0.4, self.height * 0.18))

        # Body
        font("Georgia", 11)
        body = '\n\n'.join(article['full_content'][:6])
        textBox(body,
               (self.width/2 + self.margin, self.margin + 80,
                self.width * 0.4, self.height - 2*self.margin - 120),
               align="justified")

        # Page number
        fill(*pal['accent'])
        font("Helvetica-Bold", 11)
        text(f"{idx + 12}", (self.width - self.margin - 30, self.margin + 10))

    def style_grid(self, article, pal, idx):
        """Grid layout"""

        # Title
        fill(*pal['accent'])
        font("Helvetica-Bold", 64)
        textBox(article['title'].upper(),
               (self.margin, self.height - self.margin - 120,
                self.width - 2*self.margin, 100),
               align="center")

        # Line
        fill(*pal['primary'])
        rect(self.width/2 - 200, self.height - self.margin - 140, 400, 3)

        # Three columns
        col_w = (self.width - 2*self.margin - 60) / 3
        y_start = self.height - self.margin - 180

        fill(*pal['primary'])
        font("Georgia", 11)

        paras = article['full_content']

        for i in range(3):
            x = self.margin + i * (col_w + 30)
            text_content = '\n\n'.join(paras[i*3:i*3+3])
            textBox(text_content,
                   (x, self.margin + 100, col_w, y_start - self.margin - 100),
                   align="justified")

        fill(*pal['accent'])
        rect(self.width/2 - 60, self.margin + 30, 120, 4)

    def style_asymmetric(self, article, pal, idx):
        """Asymmetric design"""

        # Rotated title
        with savedState():
            fill(*pal['accent'])
            font("Helvetica-Bold", 56)
            translate(self.margin + 30, self.height/2 + 200)
            rotate(90)
            text(article['title'].upper()[:30], (0, 0))

        # Description box
        content_x = self.margin + 100
        content_w = self.width - self.margin - content_x - self.margin

        fill(*pal['accent'], 0.1)
        desc_h = 150
        rect(content_x, self.height - self.margin - desc_h - 50,
             content_w * 0.65, desc_h)

        fill(*pal['primary'])
        font("Helvetica", 15)
        textBox(article['extract'],
               (content_x + 20, self.height - self.margin - desc_h - 30,
                content_w * 0.65 - 40, desc_h - 40))

        # Body text
        font("Georgia", 11)

        col1_w = content_w * 0.55
        col2_w = content_w * 0.4
        y_start = self.height - self.margin - desc_h - 100

        paras = article['full_content']

        textBox('\n\n'.join(paras[:5]),
               (content_x, self.margin + 80, col1_w, y_start - self.margin - 80),
               align="justified")

        col2_x = content_x + col1_w + 40
        textBox('\n\n'.join(paras[5:8]),
               (col2_x, self.margin + 50, col2_w, y_start - self.margin - 200),
               align="justified")

        # Accent elements
        fill(*pal['accent'])
        rect(col2_x - 20, self.height - self.margin - 80, 4, 60)
        oval(content_x - 50, self.height/2 - 40, 80, 80)

    def style_editorial(self, article, pal, idx):
        """Classic editorial"""

        # Title
        fill(*pal['primary'])
        font("Georgia-Bold", 56)
        textBox(article['title'],
               (self.margin + 100, self.height - self.margin - 180,
                self.width - 2*self.margin - 200, 140),
               align="center")

        # Description
        fill(*pal['accent'])
        font("Georgia-Italic", 16)
        if article.get('description'):
            textBox(article['description'].upper(),
                   (self.margin + 100, self.height - self.margin - 210,
                    self.width - 2*self.margin - 200, 30),
                   align="center")

        # Decorative elements
        fill(*pal['accent'])
        line_y = self.height - self.margin - 230
        oval(self.width/2 - 260, line_y - 2, 5, 5)
        rect(self.width/2 - 245, line_y, 200, 1)
        rect(self.width/2 + 45, line_y, 200, 1)
        oval(self.width/2 + 255, line_y - 2, 5, 5)

        # Body text
        col_w = (self.width - 2*self.margin - 100) / 2
        y_start = self.height - self.margin - 280

        paras = article['full_content']

        if paras:
            # Drop cap
            fill(*pal['accent'])
            font("Georgia-Bold", 90)
            text(paras[0][0], (self.margin + 50, y_start - 80))

            # Text
            fill(*pal['primary'])
            font("Georgia", 12)

            textBox(paras[0][1:] + '\n\n' + '\n\n'.join(paras[1:]),
                   (self.margin + 130, self.margin + 80,
                    col_w - 80, y_start - self.margin - 80),
                   align="justified")

            # Second column
            body2 = '\n\n'.join(paras[5:])
            textBox(body2,
                   (self.width/2 + 50, self.margin + 80,
                    col_w, y_start - self.margin - 80),
                   align="justified")

        # Footer
        fill(*pal['primary'])
        font("Helvetica", 9)
        text(f"WIKIPEDIA · {article['title'].upper()[:35]}",
             (self.margin + 50, self.margin + 25))
        font("Helvetica-Bold", 10)
        text(f"{idx + 48}", (self.width - self.margin - 50, self.margin + 25))

    def style_geometric(self, article, pal, idx):
        """Geometric shapes"""

        # Background shapes
        fill(*pal['accent'], 0.08)
        oval(self.width * 0.1, self.height * 0.6, 300, 300)
        rect(self.width * 0.7, self.height * 0.1, 250, 400)

        # Title frame
        fill(*pal['accent'])
        rect(self.margin, self.height - self.margin - 200, 8, 150)

        fill(*pal['primary'])
        font("Helvetica-Bold", 58)
        textBox(article['title'].upper(),
               (self.margin + 40, self.height - self.margin - 180,
                self.width * 0.45, 150))

        # Description
        fill(*pal['accent'], 0.15)
        rect(self.margin + 40, self.height - self.margin - 250,
             self.width * 0.4, 50)

        fill(*pal['primary'])
        font("Helvetica", 13)
        textBox(article.get('description', '').upper(),
               (self.margin + 55, self.height - self.margin - 238,
                self.width * 0.4 - 30, 35))

        # Body text
        font("Georgia", 11)
        paras = article['full_content']

        # Wide column
        textBox('\n\n'.join(paras[:4]),
               (self.margin + 40, self.margin + 100,
                self.width * 0.35, self.height - self.margin - 380),
               align="justified")

        # Two narrow columns
        col_w = (self.width - self.margin - (self.margin + 40 + self.width * 0.35) - 60) / 2
        right_start = self.margin + 40 + self.width * 0.35 + 40

        textBox('\n\n'.join(paras[4:7]),
               (right_start, self.margin + 100,
                col_w, self.height - self.margin - 380),
               align="justified")

        textBox('\n\n'.join(paras[7:9]),
               (right_start + col_w + 30, self.margin + 100,
                col_w, self.height - self.margin - 380),
               align="justified")

        fill(*pal['accent'])
        rect(right_start, self.height - self.margin - 280, col_w * 2 + 30, 3)

    def style_swiss(self, article, pal, idx):
        """Swiss style"""

        # Title
        fill(*pal['primary'])
        font("Helvetica", 52)
        textBox(article['title'].upper(),
               (self.margin, self.height - self.margin - 140,
                self.width * 0.5, 120))

        # Accent bar
        fill(*pal['accent'])
        rect(self.margin, self.height - self.margin - 160, self.width * 0.4, 8)

        # Info
        font("Helvetica", 11)
        text(article.get('description', '').upper(),
             (self.margin, self.height - self.margin - 180))

        # Four columns
        font("Helvetica", 10)
        paras = article['full_content']

        col_w = (self.width - 2*self.margin - 90) / 4
        y_start = self.height - self.margin - 220

        for i in range(4):
            if i * 2 < len(paras):
                col_x = self.margin + i * (col_w + 30)
                textBox('\n\n'.join(paras[i*2:i*2+2]),
                       (col_x, self.margin + 60, col_w, y_start - self.margin - 60))

        # Grid markers
        fill(*pal['accent'])
        for i in range(5):
            x = self.margin + i * (col_w + 30)
            rect(x, self.margin + 40, 1, 10)

    def style_bold(self, article, pal, idx):
        """Bold brutalist"""

        # Black header
        fill(0, 0, 0)
        rect(0, self.height - 280, self.width * 0.5, 280)

        # Title in white
        fill(1, 1, 1)
        font("Helvetica-Bold", 68)
        textBox(article['title'].upper(),
               (self.margin, self.height - 240,
                self.width * 0.5 - 2*self.margin, 200))

        # Accent block
        fill(*pal['accent'])
        rect(self.width * 0.5, self.height - 180, self.width * 0.2, 180)

        # Description
        fill(*pal['primary'])
        font("Helvetica-Bold", 14)
        extract = article['extract'][:200].upper()
        textBox(extract,
               (self.width * 0.5 + 30, self.height - 150,
                self.width * 0.2 - 60, 140))

        # Body
        fill(*pal['primary'])
        font("Courier", 10)
        body = '\n\n'.join(article['full_content'])
        textBox(body,
               (self.margin, self.margin + 80,
                self.width - 2*self.margin, self.height - 400))

        # Bold line
        fill(*pal['accent'])
        rect(0, self.margin + 40, self.width, 4)

    def style_elegant(self, article, pal, idx):
        """Elegant serif"""

        # Title
        fill(*pal['primary'])
        font("Georgia-Bold", 64)
        textBox(article['title'],
               (self.width * 0.15, self.height - self.margin - 200,
                self.width * 0.7, 160),
               align="center")

        # Ornament
        fill(*pal['accent'])
        rect(self.width/2 - 150, self.height - self.margin - 220, 100, 0.5)
        rect(self.width/2 + 50, self.height - self.margin - 220, 100, 0.5)
        oval(self.width/2 - 3, self.height - self.margin - 222, 6, 6)

        # Introduction
        font("Georgia-Italic", 14)
        textBox(article['extract'],
               (self.width * 0.2, self.height - self.margin - 320,
                self.width * 0.6, 90),
               align="center")

        # Body
        font("Georgia", 11)
        paras = article['full_content']

        col_w = (self.width * 0.8 - 40) / 2

        textBox('\n\n'.join(paras[:5]),
               (self.width * 0.1, self.margin + 100,
                col_w, self.height - self.margin - 450),
               align="justified")

        textBox('\n\n'.join(paras[5:9]),
               (self.width * 0.1 + col_w + 40, self.margin + 100,
                col_w, self.height - self.margin - 450),
               align="justified")

        # Footer ornament
        fill(*pal['accent'])
        oval(self.width/2 - 2, self.margin + 60, 4, 4)
        font("Georgia-Italic", 10)
        text(f"— {idx + 72} —", (self.width/2 - 20, self.margin + 40))

    def style_modern(self, article, pal, idx):
        """Modern tech"""

        # Diagonal stripe
        fill(*pal['accent'], 0.2)
        with savedState():
            translate(self.width * 0.3, self.height * 0.8)
            rotate(-15)
            rect(-200, -600, 800, 1200)

        # Title
        fill(*pal['accent'])
        font("Helvetica-Bold", 24)
        text("// " + article.get('description', '').upper()[:40],
             (self.margin, self.height - self.margin - 50))

        fill(*pal['primary'])
        font("Helvetica-Bold", 66)
        textBox(article['title'].upper(),
               (self.margin, self.height - self.margin - 180,
                self.width * 0.55, 120))

        # Brackets
        fill(*pal['accent'])
        font("Helvetica-Bold", 80)
        text("[", (self.margin - 15, self.height - self.margin - 180))
        text("]", (self.margin + self.width * 0.55 - 20, self.height - self.margin - 90))

        # Body
        fill(*pal['primary'])
        font("Helvetica", 10)
        paras = article['full_content']

        col_w = (self.width - 2*self.margin - 60) / 3

        for i in range(3):
            col_x = self.margin + i * (col_w + 30)

            fill(*pal['accent'])
            rect(col_x, self.height - self.margin - 230, col_w, 1)

            fill(*pal['primary'])
            if i * 3 < len(paras):
                textBox('\n\n'.join(paras[i*3:i*3+3]),
                       (col_x, self.margin + 80,
                        col_w, self.height - self.margin - 260))

        fill(*pal['accent'])
        font("Courier", 8)
        text(f"[DOC_{idx:03d}] // WIKIPEDIA // PAGE_{idx+1}",
             (self.margin, self.margin + 35))

    def style_magazine(self, article, pal, idx):
        """Magazine editorial"""

        # Feature number
        fill(*pal['accent'], 0.15)
        font("Helvetica-Bold", 280)
        text(f"{idx+1}", (self.margin - 20, self.height - 350))

        # Section label
        fill(*pal['accent'])
        font("Helvetica-Bold", 11)
        text("FEATURE", (self.margin, self.height - self.margin - 30))

        # Title
        fill(*pal['primary'])
        font("Georgia-Bold", 72)
        textBox(article['title'],
               (self.margin, self.height - self.margin - 240,
                self.width * 0.5, 200))

        # Pullquote
        fill(*pal['accent'])
        rect(self.width * 0.5 + 40, self.height - self.margin - 180, 4, 120)

        fill(*pal['primary'])
        font("Georgia-Italic", 24)
        first_sentence = article['extract'].split('.')[0] + '.'
        textBox(first_sentence,
               (self.width * 0.5 + 70, self.height - self.margin - 180,
                self.width * 0.35, 120))

        # Body
        font("Georgia", 11)
        paras = article['full_content']

        textBox('\n\n'.join(paras[:4]),
               (self.margin, self.margin + 100,
                self.width * 0.28, self.height - self.margin - 380),
               align="justified")

        col_w = (self.width - self.margin - (self.margin + self.width * 0.28) - 60) / 2
        right_start = self.margin + self.width * 0.28 + 40

        textBox('\n\n'.join(paras[4:7]),
               (right_start, self.margin + 100,
                col_w, self.height - self.margin - 380),
               align="justified")

        textBox('\n\n'.join(paras[7:9]),
               (right_start + col_w + 30, self.margin + 100,
                col_w, self.height - self.margin - 380),
               align="justified")

        # Byline
        fill(*pal['accent'])
        font("Helvetica", 9)
        text("WIKIPEDIA COLLECTION 2026", (self.margin, self.margin + 50))

    @staticmethod
    def clean(name):
        """Clean filename"""
        name = re.sub(r'[<>:"/\\|?*]', '', name)
        return name.replace(' ', '_')[:40]


def main():
    print("\n" + "=" * 70)
    print(" " * 15 + "WIKIPEDIA MAGAZINE LAYOUT GENERATOR")
    print("=" * 70 + "\n")

    # Load articles
    with open('wikipedia_content.json', 'r') as f:
        articles = json.load(f)

    print(f"📖 Loaded {len(articles)} articles\n")
    for i, art in enumerate(articles, 1):
        print(f"  {i:2d}. {art['title']}")

    print("\n" + "─" * 70)
    print("🎨 Creating magazine layouts...")
    print("─" * 70 + "\n")

    designer = MagazineDesigner()

    files = []
    for i, art in enumerate(articles):
        filename = designer.create(art, i)
        files.append(filename)
        print(f"✓ [{i+1:2d}/10] {art['title'][:45]:<45} → {filename}")

    print("\n" + "=" * 70)
    print("✓ ALL LAYOUTS COMPLETE!")
    print("=" * 70)
    print(f"\n📁 Location: output/")
    print(f"📄 Files: {len(files)}")
    print()


if __name__ == "__main__":
    main()
