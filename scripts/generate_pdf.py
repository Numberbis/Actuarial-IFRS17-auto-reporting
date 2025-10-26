#!/usr/bin/env python3
"""
Script to convert IFRS 17 Markdown report to professional HTML and PDF
"""

import sys
from pathlib import Path
import re


def markdown_to_html(md_content: str) -> str:
    """Simple markdown to HTML converter for our specific report format"""

    html_lines = []
    in_table = False
    table_lines = []

    lines = md_content.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i]

        # Headers
        if line.startswith('# '):
            html_lines.append(f'<h1>{line[2:]}</h1>')
        elif line.startswith('## '):
            html_lines.append(f'<h2>{line[3:]}</h2>')
        elif line.startswith('### '):
            html_lines.append(f'<h3>{line[4:]}</h3>')
        elif line.startswith('#### '):
            html_lines.append(f'<h4>{line[5:]}</h4>')

        # Horizontal rules
        elif line.strip() == '---' or line.strip().startswith('==='):
            html_lines.append('<hr>')

        # Tables
        elif '|' in line and line.strip().startswith('|'):
            if not in_table:
                in_table = True
                table_lines = []
            table_lines.append(line)

            # Check if next line is not a table line
            if i + 1 >= len(lines) or '|' not in lines[i + 1]:
                # Process the complete table
                html_lines.append(convert_table(table_lines))
                in_table = False
                table_lines = []

        # Lists
        elif line.strip().startswith('- '):
            # Start of a list
            list_items = []
            while i < len(lines) and lines[i].strip().startswith('- '):
                item = lines[i].strip()[2:]
                list_items.append(f'<li>{process_inline(item)}</li>')
                i += 1
            html_lines.append('<ul>')
            html_lines.extend(list_items)
            html_lines.append('</ul>')
            i -= 1  # Back one step because we'll increment at the end

        # Paragraphs
        elif line.strip():
            html_lines.append(f'<p>{process_inline(line)}</p>')

        # Empty lines
        else:
            if html_lines and html_lines[-1] != '':
                html_lines.append('')

        i += 1

    return '\n'.join(html_lines)


def process_inline(text: str) -> str:
    """Process inline markdown elements like bold, italic, code"""
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Code
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    # Italic
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    return text


def convert_table(table_lines: list) -> str:
    """Convert markdown table to HTML"""
    if len(table_lines) < 2:
        return ''

    html = ['<table>']

    # Header row
    header = table_lines[0]
    cells = [cell.strip() for cell in header.split('|')[1:-1]]  # Remove first and last empty
    html.append('<thead><tr>')
    for cell in cells:
        html.append(f'<th>{process_inline(cell)}</th>')
    html.append('</tr></thead>')

    # Body rows (skip the separator line)
    html.append('<tbody>')
    for row in table_lines[2:]:
        if row.strip():
            cells = [cell.strip() for cell in row.split('|')[1:-1]]
            html.append('<tr>')
            for cell in cells:
                html.append(f'<td>{process_inline(cell)}</td>')
            html.append('</tr>')
    html.append('</tbody>')

    html.append('</table>')
    return '\n'.join(html)


def create_html_document(body_html: str, css_path: Path) -> str:
    """Create a complete HTML document with CSS"""

    # Read CSS file
    css_content = css_path.read_text()

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IFRS 17 Actuarial Report</title>
    <style>
{css_content}
    </style>
</head>
<body>
{body_html}
</body>
</html>"""

    return html


def main():
    # Paths
    md_path = Path('reports/ifrs17_report.md')
    html_path = Path('reports/ifrs17_report.html')
    pdf_path = Path('reports/ifrs17_report.pdf')
    css_path = Path('templates/report-style.css')

    if not md_path.exists():
        print(f"Error: {md_path} not found")
        sys.exit(1)

    if not css_path.exists():
        print(f"Error: {css_path} not found")
        sys.exit(1)

    print("Converting Markdown to HTML...")
    md_content = md_path.read_text(encoding='utf-8')
    body_html = markdown_to_html(md_content)
    full_html = create_html_document(body_html, css_path)

    # Save HTML
    html_path.write_text(full_html, encoding='utf-8')
    print(f"✓ HTML saved to {html_path}")

    # Convert HTML to PDF using WeasyPrint
    print("Converting HTML to PDF with WeasyPrint...")
    try:
        from weasyprint import HTML
        HTML(string=full_html, base_url='.').write_pdf(pdf_path)
        print(f"✓ PDF saved to {pdf_path}")
        print(f"\n✅ Report generation complete!")
        print(f"   - Markdown: {md_path}")
        print(f"   - HTML: {html_path}")
        print(f"   - PDF: {pdf_path}")
    except Exception as e:
        print(f"Error generating PDF: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
