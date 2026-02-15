from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def export_pdf(text, path="final_report.pdf"):
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4

    y = height - 40
    for line in text.split("\n"):
        if y < 40:
            c.showPage()
            y = height - 40
        c.drawString(40, y, line[:100])
        y -= 14

    c.save()
    return path
