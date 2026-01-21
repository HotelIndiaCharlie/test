#!/usr/bin/env python3
"""
Professional Wikipedia Magazine Layouts
Editorial-quality typesetting with Google sans-serif fonts
"""

import json
from pathlib import Path
import re

from drawbot_skia.drawbot import *
from text_helpers import textBox


class ProfessionalMagazineDesigner:
    """Creates professional magazine layouts with proper typography"""

    def __init__(self):
        # A4 spread dimensions: two portrait pages side by side
        # A4 portrait = 595.28 x 841.89 points
        self.width = 595.28 * 2  # 1190.56 points (420mm)
        self.height = 841.89     # 841.89 points (297mm)

        # Professional margins (in points)
        self.margin_outer = 72   # 1 inch outer margin
        self.margin_inner = 54   # 0.75 inch inner margin
        self.margin_top = 72     # 1 inch top
        self.margin_bottom = 72  # 1 inch bottom

        # Typography settings
        self.body_size = 10.5
        self.body_leading = 14    # 1.33 line height for readability
        self.max_chars = 75       # Maximum characters per line

        # Calculate column widths for 75 char limit
        # Average char width at 10.5pt ≈ 6 points
        self.optimal_column = 450  # ~75 chars at 10.5pt

        # Color palettes - sophisticated editorial
        self.palettes = [
            {'name': 'Classic', 'primary': (0.1, 0.1, 0.12), 'accent': (0.85, 0.15, 0.15), 'bg': (0.99, 0.99, 0.98)},
            {'name': 'Ocean', 'primary': (0.08, 0.12, 0.16), 'accent': (0.15, 0.45, 0.75), 'bg': (0.99, 0.995, 1.0)},
            {'name': 'Forest', 'primary': (0.08, 0.12, 0.10), 'accent': (0.25, 0.55, 0.35), 'bg': (0.98, 0.99, 0.98)},
            {'name': 'Burgundy', 'primary': (0.12, 0.08, 0.10), 'accent': (0.65, 0.15, 0.25), 'bg': (0.995, 0.985, 0.99)},
            {'name': 'Navy', 'primary': (0.06, 0.08, 0.14), 'accent': (0.20, 0.30, 0.60), 'bg': (0.99, 0.99, 0.995)},
            {'name': 'Slate', 'primary': (0.15, 0.15, 0.17), 'accent': (0.45, 0.50, 0.55), 'bg': (0.98, 0.98, 0.98)},
            {'name': 'Crimson', 'primary': (0.12, 0.10, 0.10), 'accent': (0.75, 0.20, 0.20), 'bg': (0.99, 0.98, 0.98)},
            {'name': 'Teal', 'primary': (0.08, 0.12, 0.12), 'accent': (0.20, 0.60, 0.60), 'bg': (0.98, 0.995, 0.995)},
            {'name': 'Charcoal', 'primary': (0.14, 0.14, 0.15), 'accent': (0.50, 0.50, 0.52), 'bg': (0.985, 0.985, 0.985)},
            {'name': 'Plum', 'primary': (0.12, 0.08, 0.12), 'accent': (0.55, 0.25, 0.45), 'bg': (0.995, 0.985, 0.995)},
        ]

        # Font configurations (Google fonts)
        self.fonts = {
            'roboto_light': 'Roboto-Light',
            'roboto_regular': 'Roboto-Regular',
            'roboto_medium': 'Roboto-Medium',
            'roboto_bold': 'Roboto-Bold',
            'roboto_black': 'Roboto-Black',
            'opensans_regular': 'OpenSans-Regular',
            'opensans_semibold': 'OpenSans-SemiBold',
            'opensans_bold': 'OpenSans-Bold',
            'noto_regular': 'NotoSans-Regular',
            'noto_bold': 'NotoSans-Bold',
        }

        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)

    def calculate_text_width(self, text, font_name, font_size):
        """Calculate pixel width of text"""
        font(font_name, font_size)
        w, h = textSize(text)
        return w

    def create_professional_layout(self, article, index):
        """Create a professional magazine layout"""

        palette = self.palettes[index % len(self.palettes)]

        newDrawing()
        newPage(self.width, self.height)

        # Background
        fill(*palette['bg'])
        rect(0, 0, self.width, self.height)

        # Select layout style
        styles = [
            self.layout_editorial_feature,
            self.layout_news_magazine,
            self.layout_longform,
            self.layout_review_style,
            self.layout_feature_spread,
            self.layout_cultural,
            self.layout_investigative,
            self.layout_profile,
            self.layout_modern_editorial,
            self.layout_prestige,
        ]

        styles[index % len(styles)](article, palette, index)

        # Save
        filename = f"layout_{index+1:02d}_{self.clean(article['title'])}.pdf"
        saveImage(str(self.output_dir / filename))
        endDrawing()

        return filename

    def layout_editorial_feature(self, article, pal, idx):
        """Feature article - classic magazine editorial"""

        # Left page - title and intro
        left_x = self.margin_outer
        left_w = self.width/2 - self.margin_outer - self.margin_inner/2

        # Section label
        fill(*pal['accent'])
        font(self.fonts['roboto_bold'], 9)
        text("FEATURE", (left_x, self.height - self.margin_top + 10))

        # Title - bold, large
        fill(*pal['primary'])
        font(self.fonts['roboto_black'], 56)
        lineHeight(60)

        title_box = (left_x, self.height - self.margin_top - 280, left_w, 260)
        textBox(article['title'].upper(), title_box, align="left")

        # Deck/subtitle
        fill(*pal['accent'])
        font(self.fonts['roboto_light'], 18)
        lineHeight(26)

        deck_box = (left_x, self.height - self.margin_top - 380, left_w, 80)
        textBox(article.get('description', ''), deck_box, align="left")

        # Intro paragraph - larger
        fill(*pal['primary'])
        font(self.fonts['roboto_regular'], 13)
        lineHeight(19)

        intro_box = (left_x, self.margin_bottom + 200, left_w, self.height - self.margin_top - 440)
        textBox(article['extract'], intro_box, align="left")

        # Byline
        fill(*pal['primary'])
        font(self.fonts['roboto_medium'], 9)
        text("WIKIPEDIA COLLECTION", (left_x, self.margin_bottom + 160))

        # Right page - body text in columns
        right_x = self.width/2 + self.margin_inner/2
        right_w = self.width - right_x - self.margin_outer

        # Two columns
        col_w = (right_w - 24) / 2  # 24pt gutter

        fill(*pal['primary'])
        font(self.fonts['roboto_regular'], self.body_size)
        lineHeight(self.body_leading)

        paras = article['full_content']
        body = '\n\n'.join(paras[:8])

        # Column 1
        col1_box = (right_x, self.margin_bottom + 60, col_w, self.height - self.margin_top - 80)
        textBox(body[:2500], col1_box, align="justified")

        # Column 2
        col2_x = right_x + col_w + 24
        col2_box = (col2_x, self.margin_bottom + 60, col_w, self.height - self.margin_top - 80)
        textBox(body[2500:5000], col2_box, align="justified")

        # Page number
        fill(*pal['accent'])
        font(self.fonts['roboto_medium'], 10)
        text(f"{idx + 10}", (self.width - self.margin_outer - 20, self.margin_bottom))

    def layout_news_magazine(self, article, pal, idx):
        """News magazine style - TIME/Newsweek inspired"""

        # Title across top
        fill(*pal['accent'])
        font(self.fonts['roboto_bold'], 72)
        lineHeight(76)

        title_box = (self.margin_outer, self.height - self.margin_top - 120,
                    self.width - 2*self.margin_outer, 110)
        textBox(article['title'].upper(), title_box, align="center")

        # Divider line
        fill(*pal['accent'])
        rect(self.width/2 - 150, self.height - self.margin_top - 140, 300, 2)

        # Subtitle
        fill(*pal['primary'])
        font(self.fonts['roboto_light'], 16)
        lineHeight(22)

        subtitle_box = (self.margin_outer + 100, self.height - self.margin_top - 190,
                       self.width - 2*self.margin_outer - 200, 40)
        textBox(article.get('description', ''), subtitle_box, align="center")

        # Three columns
        col_w = (self.width - 2*self.margin_outer - 48) / 3
        y_top = self.height - self.margin_top - 220

        fill(*pal['primary'])
        font(self.fonts['roboto_regular'], self.body_size)
        lineHeight(self.body_leading)

        paras = article['full_content']

        # Column 1
        col1_x = self.margin_outer
        textBox('\n\n'.join(paras[:3]),
               (col1_x, self.margin_bottom + 60, col_w, y_top - self.margin_bottom - 60),
               align="justified")

        # Column 2
        col2_x = self.margin_outer + col_w + 24
        textBox('\n\n'.join(paras[3:6]),
               (col2_x, self.margin_bottom + 60, col_w, y_top - self.margin_bottom - 60),
               align="justified")

        # Column 3
        col3_x = self.margin_outer + 2*(col_w + 24)
        textBox('\n\n'.join(paras[6:9]),
               (col3_x, self.margin_bottom + 60, col_w, y_top - self.margin_bottom - 60),
               align="justified")

        # Footer
        fill(*pal['accent'])
        font(self.fonts['roboto_bold'], 8)
        text(f"VOLUME 1 · PAGE {idx + 20}", (self.width/2 - 50, self.margin_bottom + 20))

    def layout_longform(self, article, pal, idx):
        """Longform journalism - New Yorker inspired"""

        left_x = self.margin_outer + 60
        right_w = self.width - self.margin_outer - 60

        # Title - elegant and large
        fill(*pal['primary'])
        font(self.fonts['opensans_bold'], 64)
        lineHeight(72)

        title_box = (left_x, self.height - self.margin_top - 200,
                    right_w - left_x, 180)
        textBox(article['title'], title_box, align="left")

        # Author/intro bar
        fill(*pal['accent'])
        rect(left_x, self.height - self.margin_top - 230, 120, 2)

        # Intro
        fill(*pal['primary'])
        font(self.fonts['opensans_regular'], 14)
        lineHeight(21)

        intro_box = (left_x, self.height - self.margin_top - 330,
                    right_w - left_x, 90)
        textBox(article['extract'][:400], intro_box, align="left")

        # Body text - two columns
        col_w = (right_w - left_x - 30) / 2
        y_top = self.height - self.margin_top - 360

        fill(*pal['primary'])
        font(self.fonts['opensans_regular'], self.body_size)
        lineHeight(self.body_leading)

        paras = article['full_content']
        body = '\n\n'.join(paras)

        # Column 1
        textBox(body[:3000],
               (left_x, self.margin_bottom + 80, col_w, y_top - self.margin_bottom - 80),
               align="justified")

        # Column 2
        col2_x = left_x + col_w + 30
        textBox(body[3000:6000],
               (col2_x, self.margin_bottom + 80, col_w, y_top - self.margin_bottom - 80),
               align="justified")

        # Page marker
        fill(*pal['accent'])
        font(self.fonts['opensans_bold'], 9)
        text(f"{idx + 30}", (self.width/2 - 10, self.margin_bottom + 30))

    def layout_review_style(self, article, pal, idx):
        """Review/critique style"""

        # Left column - narrow for pull quotes
        left_x = self.margin_outer
        left_w = 220

        # Large number
        fill(*pal['accent'], 0.15)
        font(self.fonts['roboto_black'], 200)
        text(f"{idx+1}", (left_x, self.height - 280))

        # Title vertical
        fill(*pal['primary'])
        font(self.fonts['roboto_bold'], 24)

        # Draw title vertically on left
        with savedState():
            translate(left_x + 140, self.height - self.margin_top - 100)
            rotate(90)
            text(article['title'][:40].upper(), (0, 0))

        # Main content area - right
        main_x = self.margin_outer + left_w + 40
        main_w = self.width - main_x - self.margin_outer

        # Subtitle
        fill(*pal['accent'])
        font(self.fonts['roboto_medium'], 20)
        lineHeight(28)

        subtitle_box = (main_x, self.height - self.margin_top - 100, main_w, 80)
        textBox(article.get('description', ''), subtitle_box, align="left")

        # Intro
        fill(*pal['primary'])
        font(self.fonts['roboto_regular'], 13)
        lineHeight(19)

        intro_box = (main_x, self.height - self.margin_top - 210, main_w, 100)
        textBox(article['extract'], intro_box, align="left")

        # Body - two columns
        col_w = (main_w - 24) / 2
        y_top = self.height - self.margin_top - 240

        fill(*pal['primary'])
        font(self.fonts['roboto_regular'], self.body_size)
        lineHeight(self.body_leading)

        paras = article['full_content']

        textBox('\n\n'.join(paras[:5]),
               (main_x, self.margin_bottom + 60, col_w, y_top - self.margin_bottom - 60),
               align="justified")

        col2_x = main_x + col_w + 24
        textBox('\n\n'.join(paras[5:9]),
               (col2_x, self.margin_bottom + 60, col_w, y_top - self.margin_bottom - 60),
               align="justified")

    def layout_feature_spread(self, article, pal, idx):
        """Classic magazine feature spread"""

        # Left page - visual emphasis
        left_x = self.margin_outer
        left_w = self.width/2 - self.margin_outer - self.margin_inner/2

        # Category
        fill(*pal['accent'])
        font(self.fonts['roboto_bold'], 11)
        text("IN DEPTH", (left_x, self.height - self.margin_top + 15))

        # Title
        fill(*pal['primary'])
        font(self.fonts['roboto_black'], 62)
        lineHeight(68)

        title_box = (left_x, self.height - self.margin_top - 300, left_w, 280)
        textBox(article['title'], title_box, align="left")

        # Deck
        fill(*pal['primary'])
        font(self.fonts['roboto_light'], 16)
        lineHeight(24)

        deck_box = (left_x, self.height - self.margin_top - 400, left_w, 80)
        textBox(article.get('description', ''), deck_box, align="left")

        # Accent line
        fill(*pal['accent'])
        rect(left_x, self.height - self.margin_top - 420, 100, 4)

        # Intro paragraph
        fill(*pal['primary'])
        font(self.fonts['roboto_regular'], 12)
        lineHeight(18)

        intro_box = (left_x, self.margin_bottom + 120, left_w,
                    self.height - self.margin_top - 460)
        textBox(article['extract'], intro_box, align="left")

        # Right page - body text
        right_x = self.width/2 + self.margin_inner/2
        right_w = self.width - right_x - self.margin_outer

        # Single column for readability
        fill(*pal['primary'])
        font(self.fonts['roboto_regular'], self.body_size)
        lineHeight(self.body_leading)

        paras = article['full_content']
        body = '\n\n'.join(paras)

        textBox(body,
               (right_x + 40, self.margin_bottom + 80, right_w - 80,
                self.height - self.margin_top - 100),
               align="justified")

        # Page number
        fill(*pal['accent'])
        font(self.fonts['roboto_bold'], 11)
        text(f"{idx + 40}", (self.width - self.margin_outer - 25, self.margin_bottom + 25))

    def layout_cultural(self, article, pal, idx):
        """Cultural magazine style"""

        # Header
        fill(*pal['accent'])
        font(self.fonts['opensans_bold'], 10)
        text("CULTURE · ARTS · IDEAS", (self.margin_outer, self.height - self.margin_top + 15))

        # Title - centered, elegant
        fill(*pal['primary'])
        font(self.fonts['opensans_bold'], 58)
        lineHeight(64)

        title_box = (self.margin_outer + 80, self.height - self.margin_top - 160,
                    self.width - 2*self.margin_outer - 160, 140)
        textBox(article['title'], title_box, align="center")

        # Subtitle centered
        fill(*pal['accent'])
        font(self.fonts['opensans_regular'], 15)
        lineHeight(22)

        subtitle_box = (self.margin_outer + 120, self.height - self.margin_top - 200,
                       self.width - 2*self.margin_outer - 240, 30)
        textBox(article.get('description', ''), subtitle_box, align="center")

        # Decorative element
        fill(*pal['accent'])
        rect(self.width/2 - 60, self.height - self.margin_top - 220, 120, 1)

        # Body - three columns
        col_w = (self.width - 2*self.margin_outer - 48) / 3
        y_top = self.height - self.margin_top - 250

        fill(*pal['primary'])
        font(self.fonts['opensans_regular'], self.body_size)
        lineHeight(self.body_leading)

        paras = article['full_content']

        col1_x = self.margin_outer
        textBox('\n\n'.join(paras[:3]),
               (col1_x, self.margin_bottom + 80, col_w, y_top - self.margin_bottom - 80),
               align="justified")

        col2_x = self.margin_outer + col_w + 24
        textBox('\n\n'.join(paras[3:6]),
               (col2_x, self.margin_bottom + 80, col_w, y_top - self.margin_bottom - 80),
               align="justified")

        col3_x = self.margin_outer + 2*(col_w + 24)
        textBox('\n\n'.join(paras[6:9]),
               (col3_x, self.margin_bottom + 80, col_w, y_top - self.margin_bottom - 80),
               align="justified")

        # Footer
        fill(*pal['primary'])
        font(self.fonts['opensans_bold'], 9)
        text(f"PAGE {idx + 50} · WIKIPEDIA QUARTERLY",
             (self.width/2 - 80, self.margin_bottom + 30))

    def layout_investigative(self, article, pal, idx):
        """Investigative journalism style"""

        # Bold header
        fill(*pal['accent'])
        font(self.fonts['roboto_black'], 14)
        text("SPECIAL REPORT", (self.margin_outer, self.height - self.margin_top + 20))

        # Title - impactful
        fill(*pal['primary'])
        font(self.fonts['roboto_black'], 68)
        lineHeight(72)

        title_box = (self.margin_outer, self.height - self.margin_top - 180,
                    self.width - 2*self.margin_outer, 170)
        textBox(article['title'].upper(), title_box, align="left")

        # Heavy accent line
        fill(*pal['accent'])
        rect(self.margin_outer, self.height - self.margin_top - 200,
             self.width - 2*self.margin_outer, 6)

        # Intro - prominent
        fill(*pal['primary'])
        font(self.fonts['roboto_medium'], 15)
        lineHeight(22)

        intro_box = (self.margin_outer, self.height - self.margin_top - 300,
                    self.width - 2*self.margin_outer, 90)
        textBox(article['extract'], intro_box, align="left")

        # Body - wide columns
        col_w = (self.width - 2*self.margin_outer - 30) / 2
        y_top = self.height - self.margin_top - 330

        fill(*pal['primary'])
        font(self.fonts['roboto_regular'], self.body_size)
        lineHeight(self.body_leading)

        paras = article['full_content']

        col1_x = self.margin_outer
        textBox('\n\n'.join(paras[:5]),
               (col1_x, self.margin_bottom + 80, col_w, y_top - self.margin_bottom - 80),
               align="justified")

        col2_x = self.margin_outer + col_w + 30
        textBox('\n\n'.join(paras[5:9]),
               (col2_x, self.margin_bottom + 80, col_w, y_top - self.margin_bottom - 80),
               align="justified")

        # Page
        fill(*pal['accent'])
        font(self.fonts['roboto_black'], 11)
        text(f"{idx + 60}", (self.margin_outer, self.margin_bottom + 25))

    def layout_profile(self, article, pal, idx):
        """Profile/portrait style"""

        # Title on left side
        left_x = self.margin_outer
        left_w = 280

        fill(*pal['primary'])
        font(self.fonts['opensans_bold'], 52)
        lineHeight(56)

        title_box = (left_x, self.height - self.margin_top - 400, left_w, 380)
        textBox(article['title'], title_box, align="left")

        # Category label
        fill(*pal['accent'])
        font(self.fonts['opensans_bold'], 9)
        text("PROFILE", (left_x, self.height - self.margin_top + 10))

        # Main content area
        main_x = left_x + left_w + 50
        main_w = self.width - main_x - self.margin_outer

        # Lead paragraph
        fill(*pal['primary'])
        font(self.fonts['opensans_semibold'], 13)
        lineHeight(20)

        lead_box = (main_x, self.height - self.margin_top - 120, main_w, 100)
        textBox(article['extract'][:500], lead_box, align="left")

        # Body text
        font(self.fonts['opensans_regular'], self.body_size)
        lineHeight(self.body_leading)

        paras = article['full_content']
        body = '\n\n'.join(paras)

        textBox(body,
               (main_x, self.margin_bottom + 80, main_w,
                self.height - self.margin_top - 240),
               align="justified")

        # Accent bar
        fill(*pal['accent'])
        rect(main_x, self.height - self.margin_top - 140, 80, 3)

    def layout_modern_editorial(self, article, pal, idx):
        """Modern editorial magazine"""

        # Header bar
        fill(*pal['accent'])
        rect(0, self.height - 80, self.width, 80)

        # Title in header
        fill(1, 1, 1)
        font(self.fonts['roboto_bold'], 48)
        lineHeight(52)

        title_box = (self.margin_outer + 20, self.height - 70,
                    self.width - 2*self.margin_outer - 40, 60)
        textBox(article['title'].upper(), title_box, align="left")

        # Subtitle below header
        fill(*pal['primary'])
        font(self.fonts['roboto_light'], 18)
        lineHeight(26)

        subtitle_box = (self.margin_outer, self.height - 140,
                       self.width - 2*self.margin_outer, 50)
        textBox(article.get('description', ''), subtitle_box, align="left")

        # Body - two main columns
        col_w = (self.width - 2*self.margin_outer - 36) / 2
        y_top = self.height - 170

        fill(*pal['primary'])
        font(self.fonts['roboto_regular'], self.body_size)
        lineHeight(self.body_leading)

        paras = article['full_content']

        # Add drop cap effect to first paragraph
        first_para = paras[0] if paras else ""
        rest_paras = paras[1:]

        # Column 1 - with intro
        col1_x = self.margin_outer

        # Intro paragraph larger
        font(self.fonts['roboto_medium'], 12)
        lineHeight(18)
        intro_box = (col1_x, y_top - 100, col_w, 90)
        textBox(article['extract'][:300], intro_box, align="left")

        # Rest of column 1
        font(self.fonts['roboto_regular'], self.body_size)
        lineHeight(self.body_leading)
        textBox('\n\n'.join(rest_paras[:4]),
               (col1_x, self.margin_bottom + 80, col_w, y_top - 120 - self.margin_bottom - 80),
               align="justified")

        # Column 2
        col2_x = self.margin_outer + col_w + 36
        textBox('\n\n'.join(rest_paras[4:8]),
               (col2_x, self.margin_bottom + 80, col_w, y_top - 20 - self.margin_bottom - 80),
               align="justified")

        # Page number
        fill(*pal['accent'])
        font(self.fonts['roboto_bold'], 10)
        text(f"{idx + 70}", (self.width/2 - 10, self.margin_bottom + 30))

    def layout_prestige(self, article, pal, idx):
        """Prestige magazine style - Vogue/Vanity Fair inspired"""

        # Minimal header
        fill(*pal['accent'])
        font(self.fonts['opensans_semibold'], 9)
        text("FEATURE STORY", (self.margin_outer, self.height - self.margin_top + 12))

        # Title - elegant, large, centered
        fill(*pal['primary'])
        font(self.fonts['opensans_bold'], 66)
        lineHeight(72)

        title_box = (self.margin_outer + 60, self.height - self.margin_top - 200,
                    self.width - 2*self.margin_outer - 120, 180)
        textBox(article['title'], title_box, align="center")

        # Thin decorative line
        fill(*pal['accent'])
        rect(self.width/2 - 100, self.height - self.margin_top - 220, 200, 0.5)

        # Deck - centered
        fill(*pal['primary'])
        font(self.fonts['opensans_regular'], 14)
        lineHeight(21)

        deck_box = (self.margin_outer + 100, self.height - self.margin_top - 280,
                   self.width - 2*self.margin_outer - 200, 50)
        textBox(article.get('description', ''), deck_box, align="center")

        # Body - elegant two-column
        col_w = (self.width - 2*self.margin_outer - 120) / 2
        col_gap = 36
        y_top = self.height - self.margin_top - 320

        fill(*pal['primary'])
        font(self.fonts['opensans_regular'], self.body_size)
        lineHeight(self.body_leading)

        paras = article['full_content']
        body = '\n\n'.join(paras)

        # Column 1
        col1_x = self.margin_outer + 60
        textBox(body[:3500],
               (col1_x, self.margin_bottom + 100, col_w, y_top - self.margin_bottom - 100),
               align="justified")

        # Column 2
        col2_x = col1_x + col_w + col_gap
        textBox(body[3500:7000],
               (col2_x, self.margin_bottom + 100, col_w, y_top - self.margin_bottom - 100),
               align="justified")

        # Page number - elegant
        fill(*pal['accent'])
        font(self.fonts['opensans_regular'], 9)
        text(f"— {idx + 80} —", (self.width/2 - 20, self.margin_bottom + 40))

    @staticmethod
    def clean(name):
        """Clean filename"""
        name = re.sub(r'[<>:"/\\|?*]', '', name)
        return name.replace(' ', '_')[:40]


def main():
    print("\n" + "=" * 75)
    print("           PROFESSIONAL WIKIPEDIA MAGAZINE LAYOUTS")
    print("          Editorial-Quality Typography & Design")
    print("=" * 75 + "\n")

    # Load articles
    with open('wikipedia_content.json', 'r') as f:
        articles = json.load(f)

    print(f"📚 {len(articles)} articles loaded\n")
    for i, art in enumerate(articles, 1):
        print(f"  {i:2d}. {art['title']}")

    print("\n" + "─" * 75)
    print("🎨 Generating professional magazine layouts...")
    print("─" * 75 + "\n")

    designer = ProfessionalMagazineDesigner()

    files = []
    for i, art in enumerate(articles):
        filename = designer.create_professional_layout(art, i)
        files.append(filename)
        palette_name = designer.palettes[i % len(designer.palettes)]['name']
        print(f"✓ [{i+1:2d}/10] {palette_name:10s} | {art['title'][:45]:<45} → {filename}")

    print("\n" + "=" * 75)
    print("✓ ALL PROFESSIONAL LAYOUTS COMPLETE!")
    print("=" * 75)
    print(f"\n📁 Location: output/")
    print(f"📄 Files: {len(files)} PDF layouts\n")


if __name__ == "__main__":
    main()
