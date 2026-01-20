# Wikipedia Magazine Layout Generator

A professional magazine layout generator that creates stunning A4 spread designs from Wikipedia content using DrawBot.

## 🎨 Overview

This project demonstrates high-end graphic design capabilities by automatically generating 10 unique magazine-style PDF layouts, each featuring a different Wikipedia article with professional typography, balanced composition, and modern editorial design principles.

## 🖼️ Layout Gallery

### 01. Quantum Entanglement - Minimalist Typography
![Layout 01](previews/layout_01_Quantum_Entanglement-1.png)
*Clean, bold headlines with generous whitespace and strong accent lines*

### 02. Art Nouveau Architecture - Grid Modern
![Layout 02](previews/layout_02_Art_Nouveau_Architecture-1.png)
*Three-column layout with centered title and geometric accents*

### 03. The Viking Age - Asymmetric Bold
![Layout 03](previews/layout_03_The_Viking_Age-1.png)
*Dynamic rotated elements with offset columns and geometric shapes*

### 04. Bioluminescence - Classic Editorial
![Layout 04](previews/layout_04_Bioluminescence-1.png)
*Traditional drop cap with serif typography and ornamental elements*

### 05. Baroque Music - Contemporary Geometric
![Layout 05](previews/layout_05_Baroque_Music-1.png)
*Modern shapes with mixed column widths and geometric framing*

### 06. The Silk Road - Swiss Style
![Layout 06](previews/layout_06_The_Silk_Road-1.png)
*International Typographic Style with grid precision and clean lines*

### 07. Artificial Intelligence - Bold Brutalist
![Layout 07](previews/layout_07_Artificial_Intelligence-1.png)
*Raw, powerful design with high contrast and bold blocks*

### 08. Gothic Cathedrals - Elegant Serif
![Layout 08](previews/layout_08_Gothic_Cathedrals-1.png)
*Refined, classical approach with ornamental details and decorative flourishes*

### 09. Coffee Culture - Modern Tech
![Layout 09](previews/layout_09_Coffee_Culture-1.png)
*Futuristic aesthetic with diagonal elements and tech-inspired brackets*

### 10. The Northern Lights - Magazine Editorial
![Layout 10](previews/layout_10_The_Northern_Lights-1.png)
*High-end editorial with pullquotes and feature numbers*

## ✨ Features

- **10 Distinct Design Styles**: Each layout showcases a different editorial design approach
- **A4 Spread Format**: Professional double-page layouts (1190.56 x 841.89 points)
- **Modern Typography**: Carefully selected typeface combinations
- **Color Palettes**: 10 curated color schemes for visual variety
- **Balanced Layouts**: Grid-based design with proper margins and spacing

## 🎯 Design Styles

1. **Minimalist Typography** - Clean, bold headlines with generous whitespace
2. **Grid Modern** - Three-column layout with centered title
3. **Asymmetric Bold** - Dynamic rotated elements and offset columns
4. **Classic Editorial** - Traditional drop cap with serif typography
5. **Contemporary Geometric** - Modern shapes and mixed column widths
6. **Swiss Style** - International Typographic Style with grid precision
7. **Bold Brutalist** - Raw, powerful design with high contrast
8. **Elegant Serif** - Refined, classical approach with ornamental details
9. **Modern Tech** - Futuristic aesthetic with tech-inspired elements
10. **Magazine Editorial** - High-end editorial with pullquotes and feature numbers

## 📚 Featured Articles

1. Quantum Entanglement
2. Art Nouveau Architecture
3. The Viking Age
4. Bioluminescence
5. Baroque Music
6. The Silk Road
7. Artificial Intelligence
8. Gothic Cathedrals
9. Coffee Culture
10. The Northern Lights

## 🛠 Technical Stack

- **DrawBot-skia**: Cross-platform version of DrawBot for PDF generation
- **Python 3.11**: Core programming language
- **Libraries**: Pillow, Requests, BeautifulSoup4, NumPy

## 📁 Project Structure

```
.
├── generate_layouts.py          # Main layout generator
├── text_helpers.py              # Text rendering utilities
├── wikipedia_content.json       # Curated Wikipedia content
├── output/                      # Generated PDF files
│   ├── layout_01_Quantum_Entanglement.pdf
│   ├── layout_02_Art_Nouveau_Architecture.pdf
│   └── ... (10 total PDFs)
├── previews/                    # PNG preview images
│   ├── layout_01_Quantum_Entanglement-1.png
│   ├── layout_02_Art_Nouveau_Architecture-1.png
│   └── ... (10 total previews)
├── wikipedia_magazine_layouts.zip  # Complete archive
└── README.md                    # This file
```

## 🚀 Usage

Generate all magazine layouts:

```bash
python3 generate_layouts.py
```

This will create 10 PDF files in the `output/` directory.

## 🎨 Design Principles Applied

### Typography
- Hierarchy through size and weight
- Mix of serif (Georgia) and sans-serif (Helvetica) typefaces
- Proper line height and kerning
- Strategic use of uppercase for emphasis

### Layout
- Grid-based systems for consistency
- Balanced whitespace
- Visual flow from title to body
- Column structures for readability

### Color
- Restrained color palettes
- High contrast for readability
- Accent colors for visual interest
- Professional, modern schemes

### Composition
- Asymmetric balance
- Rule of thirds application
- Visual hierarchy
- Strategic element placement

## 📊 Output Specifications

- **Format**: PDF
- **Size**: A4 Spread (420mm × 297mm or 1190.56 × 841.89 points)
- **Resolution**: 72 DPI (vector graphics)
- **File Size**: ~20-24 KB per layout
- **Total**: 10 unique designs

## 🎯 Key Features by Layout

| Layout | Style | Key Features |
|--------|-------|--------------|
| 01 | Minimalist | Large typography, accent lines, justified text |
| 02 | Grid | Three-column system, centered title |
| 03 | Asymmetric | Rotated title, offset columns, geometric shapes |
| 04 | Editorial | Drop cap, ornamental elements, serif typography |
| 05 | Geometric | Background shapes, geometric framing |
| 06 | Swiss | Four-column grid, mathematical precision |
| 07 | Brutalist | High contrast, bold blocks, raw aesthetic |
| 08 | Elegant | Refined serif, decorative flourishes |
| 09 | Modern | Tech aesthetic, diagonal elements, brackets |
| 10 | Magazine | Feature numbers, pullquotes, editorial style |

## 💡 Design Inspiration

This project draws inspiration from:
- Swiss International Typographic Style
- Bauhaus design principles
- Contemporary magazine editorial design
- Brutalist web design movement
- Art Nouveau's organic forms
- Modernist architecture

## 🔧 Dependencies

Install required packages:

```bash
pip3 install drawbot-skia pillow requests beautifulsoup4 lxml
```

System requirements:
```bash
apt-get install libegl1 libgles2 libgl1
```

## 📝 Implementation Details

### Text Rendering
Custom `textBox()` function implements word wrapping and alignment for drawbot-skia compatibility.

### Color Management
10 distinct color palettes with primary, accent, and background colors for visual variety.

### Layout Engine
Modular design system with separate style functions for each layout approach.

## 🌟 Highlights

- **Professional Quality**: Magazine-ready layouts suitable for print
- **Diverse Styles**: Each layout demonstrates different design approaches
- **Typography Excellence**: Careful attention to typeface selection and hierarchy
- **Balanced Composition**: Grid systems and whitespace management
- **Modern Aesthetics**: Contemporary design trends and principles

## 📖 Content Curation

Articles were selected to showcase diverse topics:
- Science (Quantum Entanglement, Bioluminescence)
- History (Viking Age, Silk Road)
- Art & Architecture (Art Nouveau, Gothic Cathedrals)
- Technology (Artificial Intelligence)
- Culture (Coffee Culture, Baroque Music)
- Nature (Northern Lights)

## 🎓 Educational Value

This project demonstrates:
- Professional graphic design principles
- Editorial layout techniques
- Typography mastery
- Grid system implementation
- Color theory application
- Programmatic design generation

## 🏆 Results

Successfully generated:
- **10 PDF layouts** (~225KB total) - Professional magazine-quality editorial designs
- **10 PNG previews** (~688KB total) - High-quality preview images for each layout
- **Complete ZIP archive** (~208KB) - All PDFs bundled for easy download

Each layout showcases unique typographic treatments and balanced compositions suitable for print publication.

---

**Created with DrawBot-skia** | **2026**
