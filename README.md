# Wikipedia Magazine Layout Generator

A professional magazine layout generator that creates stunning A4 spread designs from Wikipedia content using DrawBot.

## 🎨 Overview

This project demonstrates high-end graphic design capabilities by automatically generating 10 unique magazine-style PDF layouts, each featuring a different Wikipedia article with professional typography, balanced composition, and modern editorial design principles.

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

Successfully generated 10 stunning PDF layouts totaling ~225KB, each showcasing professional magazine-quality editorial design with unique typographic treatments and balanced compositions.

---

**Created with DrawBot-skia** | **2026**
