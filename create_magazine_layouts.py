#!/usr/bin/env python3
"""
Magazine Layout Generator - Creates stunning A4 spread layouts
"""

import json
import os
import random
from pathlib import Path
import re

# DrawBot imports
from drawbot_skia.drawbot import *
from text_helpers import textBox, simpleTextBox


class MagazineLayoutDesigner:
    """Creates stunning magazine layouts using DrawBot"""

    def __init__(self, output_dir="output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # A4 dimensions in points (at 72 DPI)
        # A4 = 210mm x 297mm = 595.28 x 841.89 points
        # For spread: 2 x width
        self.page_width = 595.28 * 2  # Double page spread
        self.page_height = 841.89

        # Margins and grid
        self.margin = 60
        self.gutter = 30
        self.column_width = (self.page_width - 2 * self.margin - self.gutter) / 2

        # Color palettes (modern editorial colors)
        self.color_palettes = [
            {'primary': (0.1, 0.1, 0.15), 'accent': (0.9, 0.3, 0.3), 'bg': (0.98, 0.98, 0.96), 'name': 'Crimson'},
            {'primary': (0.05, 0.15, 0.25), 'accent': (0.2, 0.6, 0.8), 'bg': (0.99, 0.99, 0.98), 'name': 'Ocean'},
            {'primary': (0.15, 0.1, 0.1), 'accent': (0.8, 0.5, 0.2), 'bg': (0.97, 0.96, 0.95), 'name': 'Amber'},
            {'primary': (0.1, 0.15, 0.1), 'accent': (0.4, 0.7, 0.4), 'bg': (0.98, 0.99, 0.97), 'name': 'Forest'},
            {'primary': (0.2, 0.1, 0.15), 'accent': (0.9, 0.4, 0.6), 'bg': (0.99, 0.97, 0.98), 'name': 'Rose'},
            {'primary': (0.08, 0.08, 0.12), 'accent': (0.6, 0.4, 0.9), 'bg': (0.98, 0.98, 0.99), 'name': 'Violet'},
            {'primary': (0.15, 0.1, 0.05), 'accent': (0.95, 0.7, 0.3), 'bg': (0.99, 0.98, 0.96), 'name': 'Gold'},
            {'primary': (0.05, 0.12, 0.15), 'accent': (0.3, 0.8, 0.8), 'bg': (0.97, 0.99, 0.99), 'name': 'Teal'},
            {'primary': (0.12, 0.08, 0.12), 'accent': (0.8, 0.3, 0.5), 'bg': (0.99, 0.97, 0.98), 'name': 'Magenta'},
            {'primary': (0.08, 0.10, 0.08), 'accent': (0.5, 0.6, 0.3), 'bg': (0.98, 0.99, 0.97), 'name': 'Olive'},
        ]

    def create_layout(self, article, index):
        """Create a magazine spread layout for an article"""

        # Select color palette
        palette = self.color_palettes[index % len(self.color_palettes)]

        # Create new drawing
        newDrawing()

        # Create new page (spread)
        newPage(self.page_width, self.page_height)

        # Background
        fill(*palette['bg'])
        rect(0, 0, self.page_width, self.page_height)

        # Choose layout style
        layout_styles = [
            self.layout_minimalist_typography,
            self.layout_grid_modern,
            self.layout_asymmetric_bold,
            self.layout_classic_editorial,
            self.layout_contemporary_geometric,
            self.layout_swiss_style,
            self.layout_brutalist,
            self.layout_elegant_serif,
            self.layout_futuristic,
            self.layout_magazine_editorial,
        ]

        layout_func = layout_styles[index % len(layout_styles)]
        layout_func(article, palette, index)

        # Save PDF
        output_file = self.output_dir / f"layout_{index+1:02d}_{self.sanitize_filename(article['title'])}.pdf"
        saveImage(str(output_file))

        endDrawing()

        print(f"✓ Layout {index+1:2d}: {palette['name']:12s} | {article['title'][:40]}")

        return output_file

    def layout_minimalist_typography(self, article, palette, index):
        """Minimalist with large typography"""

        # Large title on left page
        fill(*palette['primary'])
        font("Helvetica-Bold", 72)

        title_box = (self.margin, self.page_height * 0.4,
                    self.column_width - self.margin, self.page_height * 0.4)
        textBox(article['title'].upper(), title_box, align="left")

        # Accent line
        fill(*palette['accent'])
        rect(self.margin, self.page_height * 0.35, 120, 8)

        # Description/summary on left
        fill(*palette['primary'])
        font("Helvetica", 16)
        desc_box = (self.margin, self.page_height * 0.12,
                   self.column_width - self.margin, self.page_height * 0.18)
        textBox(article.get('extract', ''), desc_box, align="left")

        # Body text on right page
        right_x = self.page_width / 2 + self.margin

        fill(*palette['primary'])
        font("Georgia", 11)
        lineHeight(16)

        # Add body paragraphs
        paragraphs = article.get('full_content', [])
        body_text = '\n\n'.join(paragraphs[:6])

        text_box = (right_x, self.margin + 80,
                   self.column_width - self.margin, self.page_height - 2 * self.margin - 120)
        textBox(body_text, text_box, align="justified")

        # Page number
        fill(*palette['accent'])
        font("Helvetica-Bold", 11)
        text(f"{index + 12}",
             (self.page_width - self.margin - 30, self.margin + 10))

    def layout_grid_modern(self, article, palette, index):
        """Grid-based modern layout"""

        # Title at top spanning both pages
        fill(*palette['accent'])
        font("Helvetica-Bold", 64)

        title_box = (self.margin, self.page_height - self.margin - 120,
                    self.page_width - 2 * self.margin, 100)
        textBox(article['title'].upper(), title_box, align="center")

        # Decorative line
        fill(*palette['primary'])
        rect(self.page_width / 2 - 200, self.page_height - self.margin - 140,
             400, 3)

        # Three column layout for text
        col_w = (self.page_width - 2 * self.margin - 60) / 3
        y_start = self.page_height - self.margin - 180

        fill(*palette['primary'])
        font("Georgia", 11)
        lineHeight(15)

        paragraphs = article.get('full_content', [])

        # Column 1
        if len(paragraphs) > 0:
            text_box = (self.margin, self.margin + 100,
                       col_w, y_start - self.margin - 100)
            textBox('\n\n'.join(paragraphs[:3]), text_box, align="justified")

        # Column 2
        if len(paragraphs) > 3:
            text_box = (self.margin + col_w + 30, self.margin + 100,
                       col_w, y_start - self.margin - 100)
            textBox('\n\n'.join(paragraphs[3:6]), text_box, align="justified")

        # Column 3
        if len(paragraphs) > 6:
            text_box = (self.margin + 2 * (col_w + 30), self.margin + 100,
                       col_w, y_start - self.margin - 100)
            textBox('\n\n'.join(paragraphs[6:9]), text_box, align="justified")

        # Geometric accent at bottom
        fill(*palette['accent'])
        rect(self.page_width / 2 - 60, self.margin + 30, 120, 4)

    def layout_asymmetric_bold(self, article, palette, index):
        """Asymmetric modern layout"""

        # Large title rotated on left edge
        save()
        fill(*palette['accent'])
        font("Helvetica-Bold", 56)

        translate(self.margin + 30, self.page_height / 2 + 200)
        rotate(90)
        text(article['title'].upper()[:30], (0, 0))
        restore()

        # Main content area
        content_x = self.margin + 100
        content_w = self.page_width - self.margin - content_x - self.margin

        # Description box with background
        fill(*palette['accent'])
        opacity(0.1)
        desc_h = 150
        rect(content_x, self.page_height - self.margin - desc_h - 50,
             content_w * 0.65, desc_h)

        opacity(1.0)
        fill(*palette['primary'])
        font("Helvetica", 15)
        lineHeight(22)
        desc_box = (content_x + 20, self.page_height - self.margin - desc_h - 30,
                   content_w * 0.65 - 40, desc_h - 40)
        textBox(article.get('extract', ''), desc_box, align="left")

        # Body text in offset columns
        font("Georgia", 11)
        lineHeight(16)

        col1_w = content_w * 0.55
        col2_w = content_w * 0.4

        y_start = self.page_height - self.margin - desc_h - 100

        paragraphs = article.get('full_content', [])

        # Column 1
        text_box = (content_x, self.margin + 80,
                   col1_w, y_start - self.margin - 80)
        textBox('\n\n'.join(paragraphs[:5]), text_box, align="justified")

        # Column 2 (offset)
        col2_x = content_x + col1_w + 40
        text_box = (col2_x, self.margin + 50,
                   col2_w, y_start - self.margin - 200)
        textBox('\n\n'.join(paragraphs[5:8]), text_box, align="justified")

        # Geometric accent
        fill(*palette['accent'])
        rect(col2_x - 20, self.page_height - self.margin - 80,
             4, 60)

        # Circle accent
        oval(content_x - 50, self.page_height / 2 - 40, 80, 80)

    def layout_classic_editorial(self, article, palette, index):
        """Classic editorial with drop cap"""

        # Title centered at top
        fill(*palette['primary'])
        font("Georgia-Bold", 56)
        lineHeight(64)

        title_box = (self.margin + 100, self.page_height - self.margin - 180,
                    self.page_width - 2 * self.margin - 200, 140)
        textBox(article['title'], title_box, align="center")

        # Subtitle/description
        fill(*palette['accent'])
        font("Georgia-Italic", 16)

        desc_box = (self.margin + 100, self.page_height - self.margin - 210,
                   self.page_width - 2 * self.margin - 200, 30)
        desc = article.get('description', '')
        if desc:
            textBox(desc.upper(), desc_box, align="center")

        # Decorative elements
        fill(*palette['accent'])
        line_y = self.page_height - self.margin - 230

        # Ornamental lines
        oval(self.page_width / 2 - 260, line_y - 2, 5, 5)
        rect(self.page_width / 2 - 245, line_y, 200, 1)

        rect(self.page_width / 2 + 45, line_y, 200, 1)
        oval(self.page_width / 2 + 255, line_y - 2, 5, 5)

        # Body text in two columns
        col_w = (self.page_width - 2 * self.margin - 100) / 2
        y_start = self.page_height - self.margin - 280

        paragraphs = article.get('full_content', [])

        # Drop cap from first paragraph
        if paragraphs:
            first_para = paragraphs[0]
            rest_text = '\n\n'.join(paragraphs[1:])

            if first_para:
                # Drop cap
                fill(*palette['accent'])
                font("Georgia-Bold", 90)
                text(first_para[0], (self.margin + 50, y_start - 80))

                # Rest of text
                fill(*palette['primary'])
                font("Georgia", 12)
                lineHeight(18)

                first_para_rest = first_para[1:]

                # Column 1
                text_box = (self.margin + 130, self.margin + 80,
                           col_w - 80, y_start - self.margin - 80)
                textBox(first_para_rest + '\n\n' + rest_text, text_box, align="justified")

                # Column 2
                col2_remaining = len(rest_text) * 0.6
                text_box = (self.page_width / 2 + 50, self.margin + 80,
                           col_w, y_start - self.margin - 80)
                textBox(rest_text[int(col2_remaining):], text_box, align="justified")

        # Footer
        fill(*palette['primary'])
        font("Helvetica", 9)
        text(f"WIKIPEDIA COLLECTION · {article.get('title', '').upper()[:35]}",
             (self.margin + 50, self.margin + 25))

        font("Helvetica-Bold", 10)
        text(f"{index + 48}",
             (self.page_width - self.margin - 50, self.margin + 25))

    def layout_contemporary_geometric(self, article, palette, index):
        """Contemporary with geometric shapes"""

        # Background geometric shapes
        fill(*palette['accent'])
        opacity(0.08)

        # Large circle
        oval(self.page_width * 0.1, self.page_height * 0.6, 300, 300)

        # Rectangle
        rect(self.page_width * 0.7, self.page_height * 0.1, 250, 400)

        opacity(1.0)

        # Title with geometric frame
        fill(*palette['accent'])
        rect(self.margin, self.page_height - self.margin - 200, 8, 150)

        fill(*palette['primary'])
        font("Helvetica-Bold", 58)
        lineHeight(66)

        title_box = (self.margin + 40, self.page_height - self.margin - 180,
                    self.page_width * 0.45, 150)
        textBox(article['title'].upper(), title_box, align="left")

        # Description in box
        fill(*palette['accent'])
        opacity(0.15)
        rect(self.margin + 40, self.page_height - self.margin - 250,
             self.page_width * 0.4, 50)

        opacity(1.0)
        fill(*palette['primary'])
        font("Helvetica", 13)
        desc_box = (self.margin + 55, self.page_height - self.margin - 238,
                   self.page_width * 0.4 - 30, 35)
        textBox(article.get('description', '').upper(), desc_box, align="left")

        # Body text - mixed column widths
        fill(*palette['primary'])
        font("Georgia", 11)
        lineHeight(16)

        paragraphs = article.get('full_content', [])

        # Left column - wide
        text_box = (self.margin + 40, self.margin + 100,
                   self.page_width * 0.35, self.page_height - self.margin - 380)
        textBox('\n\n'.join(paragraphs[:4]), text_box, align="justified")

        # Right section - narrow columns
        col_w = (self.page_width - self.margin - (self.margin + 40 + self.page_width * 0.35) - 60) / 2

        right_start = self.margin + 40 + self.page_width * 0.35 + 40

        # Right col 1
        text_box = (right_start, self.margin + 100,
                   col_w, self.page_height - self.margin - 380)
        textBox('\n\n'.join(paragraphs[4:7]), text_box, align="justified")

        # Right col 2
        text_box = (right_start + col_w + 30, self.margin + 100,
                   col_w, self.page_height - self.margin - 380)
        textBox('\n\n'.join(paragraphs[7:9]), text_box, align="justified")

        # Accent elements
        fill(*palette['accent'])
        rect(right_start, self.page_height - self.margin - 280, col_w * 2 + 30, 3)

    def layout_swiss_style(self, article, palette, index):
        """Swiss/International Typographic Style"""

        # Grid system - strict alignment
        grid_unit = 20

        # Title - flush left, mathematical precision
        fill(*palette['primary'])
        font("Helvetica", 52)
        lineHeight(56)

        title_box = (self.margin, self.page_height - self.margin - 140,
                    self.page_width * 0.5, 120)
        textBox(article['title'].upper(), title_box, align="left")

        # Red accent bar
        fill(*palette['accent'])
        rect(self.margin, self.page_height - self.margin - 160,
             self.page_width * 0.4, 8)

        # Information hierarchy
        fill(*palette['primary'])
        font("Helvetica", 11)
        text(article.get('description', '').upper(), (self.margin, self.page_height - self.margin - 180))

        # Body text - precise grid
        font("Helvetica", 10)
        lineHeight(14)

        paragraphs = article.get('full_content', [])

        # Four column grid
        col_w = (self.page_width - 2 * self.margin - 90) / 4
        y_start = self.page_height - self.margin - 220

        for i in range(4):
            if i * 2 < len(paragraphs):
                col_x = self.margin + i * (col_w + 30)
                text_box = (col_x, self.margin + 60,
                           col_w, y_start - self.margin - 60)
                textBox('\n\n'.join(paragraphs[i*2:i*2+2]), text_box, align="left")

        # Mathematical grid markers
        fill(*palette['accent'])
        for i in range(5):
            x = self.margin + i * (col_w + 30)
            rect(x, self.margin + 40, 1, 10)

    def layout_brutalist(self, article, palette, index):
        """Brutalist design - raw and bold"""

        # Heavy black background block
        fill(0, 0, 0)
        rect(0, self.page_height - 280, self.page_width * 0.5, 280)

        # Title in white on black
        fill(1, 1, 1)
        font("Helvetica-Bold", 68)
        lineHeight(72)

        title_box = (self.margin, self.page_height - 240,
                    self.page_width * 0.5 - 2 * self.margin, 200)
        textBox(article['title'].upper(), title_box, align="left")

        # Accent color block
        fill(*palette['accent'])
        rect(self.page_width * 0.5, self.page_height - 180,
             self.page_width * 0.2, 180)

        # Description on accent
        fill(*palette['primary'])
        font("Helvetica-Bold", 14)
        lineHeight(20)
        desc_box = (self.page_width * 0.5 + 30, self.page_height - 150,
                   self.page_width * 0.2 - 60, 140)
        textBox(article.get('extract', '')[:200].upper(), desc_box, align="left")

        # Body text - raw, unadorned
        fill(*palette['primary'])
        font("Courier", 10)
        lineHeight(14)

        paragraphs = article.get('full_content', [])

        # Single wide column
        text_box = (self.margin, self.margin + 80,
                   self.page_width - 2 * self.margin, self.page_height - 400)
        textBox('\n\n'.join(paragraphs), text_box, align="left")

        # Bold graphic elements
        fill(*palette['accent'])
        rect(0, self.margin + 40, self.page_width, 4)

        # Corner marks
        fill(0, 0, 0)
        rect(self.margin, self.page_height - self.margin - 20, 20, 2)
        rect(self.margin, self.page_height - self.margin - 20, 2, 20)

    def layout_elegant_serif(self, article, palette, index):
        """Elegant serif-based layout"""

        # Ornate title treatment
        fill(*palette['primary'])
        font("Georgia-Bold", 64)
        lineHeight(72)

        # Center alignment for elegance
        title_box = (self.page_width * 0.15, self.page_height - self.margin - 200,
                    self.page_width * 0.7, 160)
        textBox(article['title'], title_box, align="center")

        # Decorative flourish
        fill(*palette['accent'])
        # Top flourish
        rect(self.page_width / 2 - 150, self.page_height - self.margin - 220, 100, 0.5)
        rect(self.page_width / 2 + 50, self.page_height - self.margin - 220, 100, 0.5)
        oval(self.page_width / 2 - 3, self.page_height - self.margin - 222, 6, 6)

        # Introduction paragraph - larger
        fill(*palette['primary'])
        font("Georgia-Italic", 14)
        lineHeight(22)

        intro_box = (self.page_width * 0.2, self.page_height - self.margin - 320,
                    self.page_width * 0.6, 90)
        textBox(article.get('extract', ''), intro_box, align="center")

        # Body text - elegant two-column
        font("Georgia", 11)
        lineHeight(17)

        paragraphs = article.get('full_content', [])

        col_w = (self.page_width * 0.8 - 40) / 2

        # Column 1
        text_box = (self.page_width * 0.1, self.margin + 100,
                   col_w, self.page_height - self.margin - 450)
        textBox('\n\n'.join(paragraphs[:5]), text_box, align="justified")

        # Column 2
        text_box = (self.page_width * 0.1 + col_w + 40, self.margin + 100,
                   col_w, self.page_height - self.margin - 450)
        textBox('\n\n'.join(paragraphs[5:9]), text_box, align="justified")

        # Footer ornament
        fill(*palette['accent'])
        oval(self.page_width / 2 - 2, self.margin + 60, 4, 4)

        # Page number
        font("Georgia-Italic", 10)
        text(f"— {index + 72} —", (self.page_width / 2 - 20, self.margin + 40))

    def layout_futuristic(self, article, palette, index):
        """Futuristic tech-inspired layout"""

        # Diagonal accent stripe
        fill(*palette['accent'])
        opacity(0.2)

        save()
        translate(self.page_width * 0.3, self.page_height * 0.8)
        rotate(-15)
        rect(-200, -600, 800, 1200)
        restore()

        opacity(1.0)

        # Title with tech aesthetic
        fill(*palette['accent'])
        font("Helvetica-Bold", 24)
        text("// " + article.get('description', '').upper()[:40], (self.margin, self.page_height - self.margin - 50))

        fill(*palette['primary'])
        font("Helvetica-Bold", 66)
        lineHeight(70)

        title_box = (self.margin, self.page_height - self.margin - 180,
                    self.page_width * 0.55, 120)
        textBox(article['title'].upper(), title_box, align="left")

        # Tech-style brackets
        fill(*palette['accent'])
        font("Helvetica-Bold", 80)
        text("[", (self.margin - 15, self.page_height - self.margin - 180))
        text("]", (self.margin + self.page_width * 0.55 - 20, self.page_height - self.margin - 90))

        # Body text in columns with tech spacing
        fill(*palette['primary'])
        font("Helvetica", 10)
        lineHeight(15)

        paragraphs = article.get('full_content', [])

        # Three columns
        col_w = (self.page_width - 2 * self.margin - 60) / 3

        for i in range(3):
            col_x = self.margin + i * (col_w + 30)

            # Column header line
            fill(*palette['accent'])
            rect(col_x, self.page_height - self.margin - 230, col_w, 1)

            # Text
            fill(*palette['primary'])
            text_box = (col_x, self.margin + 80,
                       col_w, self.page_height - self.margin - 260)

            if i * 3 < len(paragraphs):
                textBox('\n\n'.join(paragraphs[i*3:i*3+3]), text_box, align="left")

        # Tech footer
        fill(*palette['accent'])
        font("Courier", 8)
        text(f"[DOCUMENT_{index:03d}] // WIKIPEDIA_ARCHIVE // PAGE_{index+1}", (self.margin, self.margin + 35))

    def layout_magazine_editorial(self, article, palette, index):
        """High-end magazine editorial style"""

        # Large feature number
        fill(*palette['accent'])
        opacity(0.15)
        font("Helvetica-Bold", 280)
        text(f"{index+1}", (self.margin - 20, self.page_height - 350))

        opacity(1.0)

        # Section label
        fill(*palette['accent'])
        font("Helvetica-Bold", 11)
        text("FEATURE", (self.margin, self.page_height - self.margin - 30))

        # Title - editorial style
        fill(*palette['primary'])
        font("Georgia-Bold", 72)
        lineHeight(76)

        title_box = (self.margin, self.page_height - self.margin - 240,
                    self.page_width * 0.5, 200)
        textBox(article['title'], title_box, align="left")

        # Pullquote/highlight
        fill(*palette['accent'])
        rect(self.page_width * 0.5 + 40, self.page_height - self.margin - 180,
             4, 120)

        fill(*palette['primary'])
        font("Georgia-Italic", 24)
        lineHeight(32)

        quote_box = (self.page_width * 0.5 + 70, self.page_height - self.margin - 180,
                    self.page_width * 0.35, 120)
        extract = article.get('extract', '')
        # Get first sentence as pullquote
        first_sentence = extract.split('.')[0] + '.'
        textBox(first_sentence, quote_box, align="left")

        # Body text - magazine column structure
        fill(*palette['primary'])
        font("Georgia", 11)
        lineHeight(17)

        paragraphs = article.get('full_content', [])

        # Left side - single column
        text_box = (self.margin, self.margin + 100,
                   self.page_width * 0.28, self.page_height - self.margin - 380)
        textBox('\n\n'.join(paragraphs[:4]), text_box, align="justified")

        # Right side - two columns
        col_w = (self.page_width - self.margin - (self.margin + self.page_width * 0.28) - 60) / 2
        right_start = self.margin + self.page_width * 0.28 + 40

        # Col 1
        text_box = (right_start, self.margin + 100,
                   col_w, self.page_height - self.margin - 380)
        textBox('\n\n'.join(paragraphs[4:7]), text_box, align="justified")

        # Col 2
        text_box = (right_start + col_w + 30, self.margin + 100,
                   col_w, self.page_height - self.margin - 380)
        textBox('\n\n'.join(paragraphs[7:9]), text_box, align="justified")

        # Byline
        fill(*palette['accent'])
        font("Helvetica", 9)
        text("WIKIPEDIA COLLECTION 2026", (self.margin, self.margin + 50))

    @staticmethod
    def sanitize_filename(filename):
        """Sanitize filename for filesystem"""
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        filename = filename.replace(' ', '_')
        return filename[:40]


def main():
    """Main execution function"""

    print("\n" + "=" * 70)
    print(" " * 15 + "WIKIPEDIA MAGAZINE LAYOUT GENERATOR")
    print("=" * 70)
    print()

    # Load articles from JSON
    print("📖 Loading Wikipedia articles...")
    with open('wikipedia_content.json', 'r') as f:
        articles = json.load(f)

    print(f"✓ Loaded {len(articles)} articles\n")

    # List articles
    print("Articles:")
    for i, article in enumerate(articles, 1):
        print(f"  {i:2d}. {article['title']}")

    print("\n" + "─" * 70)
    print("🎨 Creating stunning magazine layouts...")
    print("─" * 70 + "\n")

    # Initialize designer
    designer = MagazineLayoutDesigner()

    # Create layouts
    pdf_files = []
    for i, article in enumerate(articles):
        pdf_file = designer.create_layout(article, i)
        pdf_files.append(pdf_file)

    print("\n" + "=" * 70)
    print("✓ ALL LAYOUTS COMPLETE!")
    print("=" * 70)
    print(f"\nGenerated {len(pdf_files)} stunning PDF layouts in: output/")
    print("\nFiles created:")

    for pdf in pdf_files:
        print(f"  • {pdf.name}")

    print(f"\nTotal size: {sum(pdf.stat().st_size for pdf in pdf_files) / 1024:.1f} KB")
    print()


if __name__ == "__main__":
    main()
