#!/usr/bin/env python3
"""
Wikipedia Magazine Layout Generator
Creates stunning A4 spread layouts from random Wikipedia articles
"""

import requests
import json
import os
import random
from bs4 import BeautifulSoup
from urllib.parse import urljoin, unquote
from pathlib import Path
import re

# DrawBot imports
from drawbot_skia.drawbot import *

class WikipediaArticleFetcher:
    """Fetches and parses random Wikipedia articles"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Magazine Layout Bot/1.0)'
        })
        self.base_url = "https://en.wikipedia.org"

    def get_random_articles(self, count=10):
        """Fetch random Wikipedia articles"""
        articles = []

        for i in range(count):
            try:
                # Use Wikipedia's random page API
                url = f"{self.base_url}/api/rest_v1/page/random/summary"
                response = self.session.get(url, timeout=10)

                if response.status_code == 200:
                    data = response.json()
                    article = {
                        'title': data.get('title', ''),
                        'extract': data.get('extract', ''),
                        'description': data.get('description', ''),
                        'thumbnail': data.get('thumbnail', {}).get('source') if 'thumbnail' in data else None,
                        'url': data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                        'page_id': data.get('pageid', '')
                    }

                    # Get full content
                    full_content = self.get_full_article_content(data.get('title', ''))
                    article['full_content'] = full_content
                    article['images'] = self.get_article_images(data.get('title', ''))

                    articles.append(article)
                    print(f"✓ Fetched: {article['title']}")
                else:
                    print(f"✗ Failed to fetch article {i+1}")

            except Exception as e:
                print(f"✗ Error fetching article {i+1}: {e}")

        return articles

    def get_full_article_content(self, title):
        """Get full article text content"""
        try:
            # Use Wikipedia API to get article content
            api_url = f"{self.base_url}/w/api.php"
            params = {
                'action': 'query',
                'format': 'json',
                'titles': title,
                'prop': 'extracts',
                'explaintext': True,
                'exsectionformat': 'plain'
            }

            response = self.session.get(api_url, params=params, timeout=10)
            data = response.json()

            pages = data.get('query', {}).get('pages', {})
            for page_id, page_data in pages.items():
                extract = page_data.get('extract', '')
                # Split into paragraphs and clean up
                paragraphs = [p.strip() for p in extract.split('\n\n') if p.strip()]
                return paragraphs[:15]  # Limit to first 15 paragraphs

        except Exception as e:
            print(f"  Error getting full content: {e}")

        return []

    def get_article_images(self, title):
        """Get images from article"""
        try:
            api_url = f"{self.base_url}/w/api.php"
            params = {
                'action': 'query',
                'format': 'json',
                'titles': title,
                'prop': 'images|imageinfo',
                'iiprop': 'url',
                'imlimit': 10
            }

            response = self.session.get(api_url, params=params, timeout=10)
            data = response.json()

            images = []
            pages = data.get('query', {}).get('pages', {})

            for page_id, page_data in pages.items():
                for img in page_data.get('images', []):
                    img_title = img.get('title', '')
                    # Filter out common icons and logos
                    if not any(skip in img_title.lower() for skip in ['icon', 'logo', 'flag', 'svg']):
                        img_url = self.get_image_url(img_title)
                        if img_url:
                            images.append(img_url)

            return images[:3]  # Limit to 3 images

        except Exception as e:
            print(f"  Error getting images: {e}")

        return []

    def get_image_url(self, image_title):
        """Get direct URL for an image"""
        try:
            api_url = f"{self.base_url}/w/api.php"
            params = {
                'action': 'query',
                'format': 'json',
                'titles': image_title,
                'prop': 'imageinfo',
                'iiprop': 'url'
            }

            response = self.session.get(api_url, params=params, timeout=10)
            data = response.json()

            pages = data.get('query', {}).get('pages', {})
            for page_id, page_data in pages.items():
                imageinfo = page_data.get('imageinfo', [])
                if imageinfo:
                    return imageinfo[0].get('url')

        except Exception as e:
            pass

        return None

    def download_image(self, url, save_path):
        """Download an image from URL"""
        try:
            response = self.session.get(url, timeout=15)
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                return True
        except Exception as e:
            print(f"  Error downloading image: {e}")
        return False


class MagazineLayoutDesigner:
    """Creates stunning magazine layouts using DrawBot"""

    def __init__(self, output_dir="output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.image_dir = self.output_dir / "images"
        self.image_dir.mkdir(exist_ok=True)

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
            {'primary': (0.1, 0.1, 0.15), 'accent': (0.9, 0.3, 0.3), 'bg': (0.98, 0.98, 0.96)},
            {'primary': (0.05, 0.15, 0.25), 'accent': (0.2, 0.6, 0.8), 'bg': (0.99, 0.99, 0.98)},
            {'primary': (0.15, 0.1, 0.1), 'accent': (0.8, 0.5, 0.2), 'bg': (0.97, 0.96, 0.95)},
            {'primary': (0.1, 0.15, 0.1), 'accent': (0.4, 0.7, 0.4), 'bg': (0.98, 0.99, 0.97)},
            {'primary': (0.2, 0.1, 0.15), 'accent': (0.9, 0.4, 0.6), 'bg': (0.99, 0.97, 0.98)},
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

        # Choose layout style randomly
        layout_styles = [
            self.layout_style_1,
            self.layout_style_2,
            self.layout_style_3,
            self.layout_style_4,
            self.layout_style_5
        ]

        layout_func = layout_styles[index % len(layout_styles)]
        layout_func(article, palette)

        # Save PDF
        output_file = self.output_dir / f"layout_{index+1:02d}_{self.sanitize_filename(article['title'])}.pdf"
        saveImage(str(output_file))

        endDrawing()

        print(f"✓ Created layout: {output_file.name}")

        return output_file

    def layout_style_1(self, article, palette):
        """Minimalist with large typography"""

        # Large title on left page
        fill(*palette['primary'])
        font("Helvetica-Bold", 72)

        title_box = (self.margin, self.page_height * 0.4,
                    self.column_width, self.page_height * 0.4)
        textBox(article['title'].upper(), title_box, align="left")

        # Accent line
        fill(*palette['accent'])
        rect(self.margin, self.page_height * 0.35, 120, 6)

        # Description/summary on left
        fill(*palette['primary'])
        font("Helvetica", 16)
        desc_box = (self.margin, self.page_height * 0.15,
                   self.column_width, self.page_height * 0.15)
        textBox(article.get('extract', '')[:300], desc_box, align="left")

        # Body text on right page
        right_x = self.page_width / 2 + self.margin

        font("Georgia", 11)
        leading = 16

        y_position = self.page_height - self.margin - 100

        # Add body paragraphs
        paragraphs = article.get('full_content', [])[:8]

        for para in paragraphs:
            if y_position < self.margin + 100:
                break

            # Calculate text height
            text_h = 200  # Approximate

            text_box = (right_x, y_position - text_h,
                       self.column_width - self.margin, text_h)

            overflow = textBox(para, text_box, align="left")

            y_position -= text_h + 20

        # Page number
        fill(*palette['accent'])
        font("Helvetica", 10)
        text(f"{random.randint(10, 99)}",
             (self.page_width - self.margin - 30, self.margin))

    def layout_style_2(self, article, palette):
        """Image-focused with overlay text"""

        # Try to use article image
        images = article.get('images', [])

        # Large image spanning left page
        if images:
            img_path = self.download_and_get_image(images[0], 0)
            if img_path and os.path.exists(img_path):
                save()

                # Image on left page
                img_w = self.page_width / 2 - self.margin
                img_h = self.page_height - 2 * self.margin

                translate(self.margin, self.margin)

                # Clip to bounds
                clipPath = BezierPath()
                clipPath.rect(0, 0, img_w, img_h)
                clipPath(clipPath)

                image(img_path, (0, 0), alpha=0.85)

                restore()

        # White overlay box for title
        fill(1, 1, 1, 0.95)
        overlay_h = 200
        rect(self.margin, self.page_height - self.margin - overlay_h,
             self.page_width / 2 - 2 * self.margin, overlay_h)

        # Title in overlay
        fill(*palette['primary'])
        font("Helvetica-Bold", 48)
        title_box = (self.margin + 30, self.page_height - self.margin - overlay_h + 40,
                    self.page_width / 2 - 2 * self.margin - 60, 140)
        textBox(article['title'], title_box, align="left")

        # Body text on right page in two columns
        right_x = self.page_width / 2 + self.margin

        fill(*palette['primary'])
        font("Georgia", 10)

        # Extract text
        extract = article.get('extract', '')

        col_w = (self.column_width - self.margin - 30) / 2

        # Left column on right page
        text_box_1 = (right_x, self.margin + 50,
                     col_w, self.page_height - 2 * self.margin - 100)
        overflow = textBox(extract[:800], text_box_1, align="justified")

        # Right column on right page
        text_box_2 = (right_x + col_w + 30, self.margin + 50,
                     col_w, self.page_height - 2 * self.margin - 100)
        textBox(extract[800:1600], text_box_2, align="justified")

        # Accent element
        fill(*palette['accent'])
        oval(right_x - 40, self.page_height / 2 - 40, 80, 80)

    def layout_style_3(self, article, palette):
        """Grid-based with multiple images"""

        # Title at top spanning both pages
        fill(*palette['accent'])
        font("Helvetica-Bold", 64)

        title_box = (self.margin, self.page_height - self.margin - 120,
                    self.page_width - 2 * self.margin, 100)
        textBox(article['title'].upper(), title_box, align="center")

        # Decorative line
        fill(*palette['primary'])
        rect(self.page_width / 2 - 200, self.page_height - self.margin - 140,
             400, 2)

        # Three column layout for text
        col_w = (self.page_width - 2 * self.margin - 60) / 3
        y_start = self.page_height - self.margin - 180

        fill(*palette['primary'])
        font("Georgia", 10)

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

        # Image grid at bottom
        images = article.get('images', [])
        if images:
            img_h = 150
            img_w = (self.page_width - 2 * self.margin - 60) / 3

            for i, img_url in enumerate(images[:3]):
                img_path = self.download_and_get_image(img_url, i)
                if img_path and os.path.exists(img_path):
                    x = self.margin + i * (img_w + 30)
                    y = self.margin - 20

                    save()
                    translate(x, y)

                    clipPath = BezierPath()
                    clipPath.rect(0, 0, img_w, img_h)
                    clipPath(clipPath)

                    image(img_path, (0, 0))
                    restore()

    def layout_style_4(self, article, palette):
        """Asymmetric modern layout"""

        # Large title rotated on left edge
        save()
        fill(*palette['accent'])
        font("Helvetica-Bold", 56)

        translate(self.margin + 20, self.page_height / 2)
        rotate(90)
        text(article['title'].upper(), (0, 0))
        restore()

        # Main content area
        content_x = self.margin + 100
        content_w = self.page_width - self.margin - content_x - self.margin

        # Description box with background
        fill(*palette['accent'], alpha=0.1)
        desc_h = 150
        rect(content_x, self.page_height - self.margin - desc_h - 50,
             content_w * 0.6, desc_h)

        fill(*palette['primary'])
        font("Helvetica", 14)
        desc_box = (content_x + 20, self.page_height - self.margin - desc_h - 30,
                   content_w * 0.6 - 40, desc_h - 40)
        textBox(article.get('extract', '')[:400], desc_box, align="left")

        # Body text in offset columns
        font("Georgia", 10)

        col1_w = content_w * 0.55
        col2_w = content_w * 0.4

        y_start = self.page_height - self.margin - desc_h - 100

        paragraphs = article.get('full_content', [])

        # Column 1
        text_box = (content_x, self.margin + 80,
                   col1_w, y_start - self.margin - 80)
        textBox('\n\n'.join(paragraphs[:5]), text_box, align="justified")

        # Column 2 (offset lower)
        col2_x = content_x + col1_w + 40
        text_box = (col2_x, self.margin + 50,
                   col2_w, y_start - self.margin - 200)
        textBox('\n\n'.join(paragraphs[5:8]), text_box, align="justified")

        # Geometric accent
        fill(*palette['accent'])
        rect(col2_x - 20, self.page_height - self.margin - 80,
             4, 60)

    def layout_style_5(self, article, palette):
        """Classic editorial with drop cap"""

        # Title centered at top
        fill(*palette['primary'])
        font("Georgia-Bold", 56)

        title_box = (self.margin + 100, self.page_height - self.margin - 150,
                    self.page_width - 2 * self.margin - 200, 120)
        textBox(article['title'], title_box, align="center")

        # Subtitle/description
        fill(*palette['accent'])
        font("Georgia-Italic", 16)

        desc_box = (self.margin + 100, self.page_height - self.margin - 180,
                   self.page_width - 2 * self.margin - 200, 30)
        textBox(article.get('description', ''), desc_box, align="center")

        # Decorative elements
        fill(*palette['accent'])
        line_y = self.page_height - self.margin - 200

        # Left ornament
        oval(self.page_width / 2 - 250, line_y - 2, 4, 4)
        rect(self.page_width / 2 - 240, line_y, 200, 0.5)

        # Right ornament
        rect(self.page_width / 2 + 40, line_y, 200, 0.5)
        oval(self.page_width / 2 + 246, line_y - 2, 4, 4)

        # Body text in two columns
        col_w = (self.page_width - 2 * self.margin - 100) / 2
        y_start = self.page_height - self.margin - 250

        paragraphs = article.get('full_content', [])

        # Get first paragraph for drop cap
        if paragraphs:
            first_para = paragraphs[0]
            rest_text = '\n\n'.join(paragraphs[1:])

            # Drop cap
            if first_para:
                fill(*palette['accent'])
                font("Georgia-Bold", 90)
                text(first_para[0], (self.margin + 50, y_start - 80))

                # Rest of first paragraph
                fill(*palette['primary'])
                font("Georgia", 11)

                first_para_rest = first_para[1:]

                # Column 1
                text_box = (self.margin + 130, y_start - 100,
                           col_w - 80, y_start - self.margin - 100)
                overflow = textBox(first_para_rest + '\n\n' + rest_text[:1000],
                                 text_box, align="justified")

                # Column 2
                text_box = (self.page_width / 2 + 50, y_start - 100,
                           col_w, y_start - self.margin - 100)
                textBox(rest_text[1000:2000], text_box, align="justified")

        # Page info at bottom
        fill(*palette['primary'])
        font("Helvetica", 9)
        text(f"WIKIPEDIA MAGAZINE · {article.get('title', '').upper()[:30]}",
             (self.margin + 50, self.margin + 20))

        font("Helvetica-Bold", 9)
        text(f"{random.randint(1, 150)}",
             (self.page_width - self.margin - 50, self.margin + 20))

    def download_and_get_image(self, url, index):
        """Download image and return local path"""
        if not url:
            return None

        try:
            img_path = self.image_dir / f"img_{index}_{hash(url) % 10000}.jpg"

            if not img_path.exists():
                response = requests.get(url, timeout=15)
                if response.status_code == 200:
                    with open(img_path, 'wb') as f:
                        f.write(response.content)

            return str(img_path)

        except Exception as e:
            print(f"  Error with image: {e}")

        return None

    @staticmethod
    def sanitize_filename(filename):
        """Sanitize filename for filesystem"""
        # Remove or replace invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        filename = filename.replace(' ', '_')
        return filename[:50]  # Limit length


def main():
    """Main execution function"""

    print("=" * 60)
    print("WIKIPEDIA MAGAZINE LAYOUT GENERATOR")
    print("=" * 60)
    print()

    # Initialize fetcher
    print("📡 Fetching random Wikipedia articles...")
    fetcher = WikipediaArticleFetcher()
    articles = fetcher.get_random_articles(10)

    print(f"\n✓ Fetched {len(articles)} articles\n")

    # Initialize designer
    print("🎨 Creating magazine layouts...")
    designer = MagazineLayoutDesigner()

    # Create layouts
    pdf_files = []
    for i, article in enumerate(articles):
        print(f"\n[{i+1}/10] Creating layout for: {article['title']}")
        pdf_file = designer.create_layout(article, i)
        pdf_files.append(pdf_file)

    print("\n" + "=" * 60)
    print("✓ ALL LAYOUTS COMPLETE!")
    print("=" * 60)
    print(f"\nGenerated {len(pdf_files)} PDF layouts in: output/")
    print()

    for pdf in pdf_files:
        print(f"  • {pdf.name}")

    print()


if __name__ == "__main__":
    main()
