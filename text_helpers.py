"""
Helper functions for text layout in drawbot-skia
"""

from drawbot_skia.drawbot import *


def textBox(txt, box, align="left"):
    """
    Simulate textBox functionality for drawbot-skia

    Args:
        txt: Text to render
        box: Tuple of (x, y, width, height)
        align: Alignment ("left", "right", "center", "justified")

    Returns:
        Overflow text (not currently implemented)
    """
    x, y, width, height = box

    if not txt:
        return ""

    # Split text into words
    words = txt.split()

    # Get current font size for line spacing
    lines = []
    current_line = []
    current_width = 0

    # Simple word wrapping
    for word in words:
        word_width, word_height = textSize(word + " ")

        if current_width + word_width <= width:
            current_line.append(word)
            current_width += word_width
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
            current_width = word_width

    if current_line:
        lines.append(" ".join(current_line))

    # Calculate line height (use global or default)
    line_height = 1.2
    try:
        # Try to get the current line height setting
        # This is a simplified approach
        line_height = 1.4  # Default spacing
    except:
        pass

    # Get approximate line height from font size
    if lines:
        _, char_height = textSize("Ay")
        line_spacing = char_height * line_height
    else:
        return ""

    # Render lines from top to bottom
    current_y = y + height - char_height

    for line in lines:
        if current_y < y:
            break  # Out of bounds

        # Calculate x position based on alignment
        line_width, _ = textSize(line)

        if align == "center":
            text_x = x + (width - line_width) / 2
        elif align == "right":
            text_x = x + width - line_width
        elif align == "justified" and line != lines[-1]:
            # Simple justified text (just left-align for simplicity)
            text_x = x
        else:  # left or default
            text_x = x

        text(line, (text_x, current_y))
        current_y -= line_spacing

    # Return empty string (overflow not calculated)
    return ""


def simpleTextBox(txt, box, align="left", line_limit=None):
    """
    Even simpler text box - just truncates text and renders

    Args:
        txt: Text to render
        box: Tuple of (x, y, width, height)
        align: Alignment
        line_limit: Maximum number of lines to render
    """
    x, y, width, height = box

    if not txt:
        return

    # Get character height
    _, char_height = textSize("Ay")
    line_spacing = char_height * 1.5

    # Split into paragraphs first
    paragraphs = txt.split('\n')

    current_y = y + height - char_height
    lines_rendered = 0

    for para in paragraphs:
        if current_y < y:
            break

        # Simple wrapping for each paragraph
        words = para.split()
        current_line = []

        for word in words:
            test_line = " ".join(current_line + [word])
            test_width, _ = textSize(test_line)

            if test_width <= width:
                current_line.append(word)
            else:
                # Render current line
                if current_line:
                    line_text = " ".join(current_line)
                    line_width, _ = textSize(line_text)

                    if align == "center":
                        text_x = x + (width - line_width) / 2
                    elif align == "right":
                        text_x = x + width - line_width
                    else:
                        text_x = x

                    text(line_text, (text_x, current_y))
                    current_y -= line_spacing
                    lines_rendered += 1

                    if line_limit and lines_rendered >= line_limit:
                        return

                    if current_y < y:
                        return

                current_line = [word]

        # Render last line of paragraph
        if current_line:
            line_text = " ".join(current_line)
            line_width, _ = textSize(line_text)

            if align == "center":
                text_x = x + (width - line_width) / 2
            elif align == "right":
                text_x = x + width - line_width
            else:
                text_x = x

            text(line_text, (text_x, current_y))
            current_y -= line_spacing * 1.3  # Extra space after paragraph
            lines_rendered += 1

            if line_limit and lines_rendered >= line_limit:
                return
