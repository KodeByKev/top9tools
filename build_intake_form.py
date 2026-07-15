"""
build_intake_form.py
Run with:  py -3 build_intake_form.py
Generates Top9Tools_Client_Intake_Form.pdf in the same folder (website/).
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas as pdfgen_canvas
from reportlab.platypus.flowables import Flowable

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_PATH   = os.path.join(SCRIPT_DIR, "Top9Tools_Client_Intake_Form.pdf")
LOGO_PATH  = os.path.join(SCRIPT_DIR, "Logo.png")

# ── Brand colours ──────────────────────────────────────────────────────────────
NAVY       = colors.HexColor("#0D1B2A")
BLUE       = colors.HexColor("#4A90D9")
BLUE_LIGHT = colors.HexColor("#6AAEE8")
WHITE      = colors.white
OFF_WHITE  = colors.HexColor("#F4F7FB")
MUTED      = colors.HexColor("#5A6A7A")
BLACK      = colors.black
RULE       = colors.HexColor("#CCCCCC")

PW, PH = letter
MARGIN = 0.6 * inch
CW     = PW - 2 * MARGIN   # content width


def build():
    c = pdfgen_canvas.Canvas(OUT_PATH, pagesize=letter)
    c.setTitle("Top 9 Tools – Client Intake Form")
    c.setAuthor("Top 9 Tools")

    # ── helpers ────────────────────────────────────────────────────────────────

    def section_bar(y, text):
        """Dark navy banner with white label."""
        h = 0.22 * inch
        c.setFillColor(NAVY)
        c.rect(MARGIN, y - h, CW, h, stroke=0, fill=1)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 9.5)
        c.drawString(MARGIN + 8, y - h + 6, text)
        return y - h - 10   # return y below the bar with a small gap

    def field_line(y, label, width=None, indent=0):
        """Bold label + underline field."""
        w = width or CW - indent
        x = MARGIN + indent
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(BLACK)
        lw = c.stringWidth(label + "  ", "Helvetica-Bold", 9)
        c.drawString(x, y, label)
        c.setStrokeColor(RULE)
        c.setLineWidth(0.75)
        c.line(x + lw, y - 1, x + w, y - 1)
        return y - 18

    def two_fields(y, label1, label2):
        """Two labeled fields side by side."""
        half = CW / 2 - 8
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(BLACK)
        lw1 = c.stringWidth(label1 + "  ", "Helvetica-Bold", 9)
        c.drawString(MARGIN, y, label1)
        c.setStrokeColor(RULE)
        c.setLineWidth(0.75)
        c.line(MARGIN + lw1, y - 1, MARGIN + half, y - 1)
        rx = MARGIN + half + 16
        lw2 = c.stringWidth(label2 + "  ", "Helvetica-Bold", 9)
        c.setFillColor(BLACK)
        c.drawString(rx, y, label2)
        c.line(rx + lw2, y - 1, MARGIN + CW, y - 1)
        return y - 18

    def checkbox(x, y, label, size=10):
        """Single checkbox with label."""
        c.setStrokeColor(NAVY)
        c.setFillColor(WHITE)
        c.setLineWidth(0.75)
        c.rect(x, y - 1, size, size, stroke=1, fill=1)
        c.setFont("Helvetica", 9)
        c.setFillColor(BLACK)
        c.drawString(x + size + 5, y + 1, label)
        return x + size + 5 + c.stringWidth(label, "Helvetica", 9) + 18

    def ruled_area(y, lines=5, label=None):
        """Optional label then N ruled writing lines."""
        if label:
            c.setFont("Helvetica-Bold", 9)
            c.setFillColor(BLACK)
            c.drawString(MARGIN, y, label)
            y -= 14
        c.setStrokeColor(RULE)
        c.setLineWidth(0.5)
        for _ in range(lines):
            c.line(MARGIN, y, MARGIN + CW, y)
            y -= 16
        return y - 4

    def note(y, text, size=7.5):
        c.setFont("Helvetica-Oblique", size)
        c.setFillColor(MUTED)
        c.drawString(MARGIN, y, text)
        return y - 12

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 1
    # ══════════════════════════════════════════════════════════════════════════

    # ── Header band ────────────────────────────────────────────────────────────
    HDR_H = 1.0 * inch
    hdr_y = PH - HDR_H
    c.setFillColor(NAVY)
    c.rect(0, hdr_y, PW, HDR_H, stroke=0, fill=1)

    LOGO_SIZE = HDR_H - 0.12 * inch
    if os.path.exists(LOGO_PATH):
        c.drawImage(LOGO_PATH,
                    MARGIN,
                    hdr_y + (HDR_H - LOGO_SIZE) / 2,
                    width=LOGO_SIZE, height=LOGO_SIZE,
                    preserveAspectRatio=True, mask="auto")

    tx = MARGIN + LOGO_SIZE + 0.18 * inch
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(tx, hdr_y + HDR_H * 0.55, "Top 9 Tools")
    c.setFillColor(BLUE_LIGHT)
    c.setFont("Helvetica", 12)
    c.drawString(tx, hdr_y + HDR_H * 0.25, "Client Intake Form")

    # Return address / contact (right side of header)
    c.setFillColor(WHITE)
    c.setFont("Helvetica", 8)
    right_x = PW - MARGIN
    c.drawRightString(right_x, hdr_y + HDR_H * 0.62, "kevin.donohue24@gmail.com")
    c.drawRightString(right_x, hdr_y + HDR_H * 0.42, "847-772-4639")

    y = hdr_y - 0.28 * inch

    # ── Intro note ─────────────────────────────────────────────────────────────
    c.setFont("Helvetica", 8.5)
    c.setFillColor(MUTED)
    intro = ("Please complete this form and return it to kevin.donohue24@gmail.com. "
             "Fields marked with an asterisk (*) are required.")
    c.drawString(MARGIN, y, intro)
    y -= 0.28 * inch

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 1 — Contact Information
    # ══════════════════════════════════════════════════════════════════════════
    y = section_bar(y, "1.  CONTACT INFORMATION")
    y = field_line(y, "Organization Name: *")
    y -= 4
    y = two_fields(y, "Contact Name: *", "Title / Role:")
    y -= 4
    y = two_fields(y, "Phone Number:", "Email Address: *")
    y -= 10

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 2 — Services
    # ══════════════════════════════════════════════════════════════════════════
    y = section_bar(y, "2.  SERVICES NEEDED  (check all that apply)")

    services = [
        ("Custom App",      "Browser-based analytics tool built for your athletes"),
        ("Custom API",      "Data pipeline — move & structure your data in a new place"),
        ("Custom Document", "Fillable branded PDFs (forms, reports, review sheets)"),
        ("Custom Website",  "Fully branded website for your program or organization"),
    ]

    for svc, desc in services:
        # Checkbox
        c.setStrokeColor(NAVY)
        c.setFillColor(WHITE)
        c.setLineWidth(0.75)
        c.rect(MARGIN, y, 11, 11, stroke=1, fill=1)
        # Service name
        c.setFont("Helvetica-Bold", 9.5)
        c.setFillColor(NAVY)
        c.drawString(MARGIN + 17, y + 1, svc)
        nw = c.stringWidth(svc, "Helvetica-Bold", 9.5)
        # Description
        c.setFont("Helvetica", 8.5)
        c.setFillColor(MUTED)
        c.drawString(MARGIN + 17 + nw + 8, y + 1, f"— {desc}")
        y -= 20

    y -= 6

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 3 — Data & Project Details
    # ══════════════════════════════════════════════════════════════════════════
    y = section_bar(y, "3.  PROJECT & DATA DETAILS")

    # 3a — Variables
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(BLACK)
    c.drawString(MARGIN, y, "a)  What variables (columns) exist in your data?")
    y -= 4
    y = note(y, "      e.g.  Athlete Name,  Pitch Type,  Velocity,  Vertical Break,  Date,  Game/Bullpen ...")
    y = ruled_area(y, lines=4)

    # 3b — Display preference
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(BLACK)
    c.drawString(MARGIN, y, "b)  How do you want these variables organized or displayed?")
    y -= 4
    y = note(y, "      e.g.  Group by athlete,  show averages per pitch type,  export as PDF,  live dashboard by date ...")
    y = ruled_area(y, lines=4)

    # 3c — Row estimate + deadline side by side
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(BLACK)
    c.drawString(MARGIN, y, "c)  Rough estimate of data points (rows):")
    lw = c.stringWidth("c)  Rough estimate of data points (rows):", "Helvetica-Bold", 9) + 8
    c.setStrokeColor(RULE)
    c.setLineWidth(0.75)
    half_right = MARGIN + CW / 2 - 16
    c.line(MARGIN + lw, y - 1, half_right, y - 1)

    rx = MARGIN + CW / 2 + 8
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(BLACK)
    c.drawString(rx, y, "d)  Project deadline (if any):")
    lw2 = c.stringWidth("d)  Project deadline (if any):", "Helvetica-Bold", 9) + 8
    c.line(rx + lw2, y - 1, MARGIN + CW, y - 1)
    y -= 20

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 4 — Additional Notes
    # ══════════════════════════════════════════════════════════════════════════
    y -= 4
    y = section_bar(y, "4.  ADDITIONAL NOTES / QUESTIONS")
    y = ruled_area(y, lines=5)

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 5 — Signature
    # ══════════════════════════════════════════════════════════════════════════
    y -= 4
    y = section_bar(y, "5.  SIGNATURE")

    sig_w = CW * 0.60
    date_w = CW * 0.28
    date_x = MARGIN + sig_w + CW * 0.12

    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(BLACK)
    c.drawString(MARGIN, y, "Signature:")
    sw = c.stringWidth("Signature:", "Helvetica-Bold", 9) + 8
    c.setStrokeColor(RULE)
    c.setLineWidth(0.75)
    c.line(MARGIN + sw, y - 1, MARGIN + sig_w, y - 1)

    c.drawString(date_x, y, "Date:")
    dw = c.stringWidth("Date:", "Helvetica-Bold", 9) + 8
    c.line(date_x + dw, y - 1, MARGIN + CW, y - 1)
    y -= 22

    # Printed name
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(BLACK)
    c.drawString(MARGIN, y, "Printed Name:")
    pw2 = c.stringWidth("Printed Name:", "Helvetica-Bold", 9) + 8
    c.setStrokeColor(RULE)
    c.line(MARGIN + pw2, y - 1, MARGIN + sig_w, y - 1)
    y -= 28

    # ── Footer ─────────────────────────────────────────────────────────────────
    c.setStrokeColor(NAVY)
    c.setLineWidth(0.75)
    c.line(MARGIN, MARGIN + 0.22 * inch, PW - MARGIN, MARGIN + 0.22 * inch)

    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(MARGIN, MARGIN + 0.08 * inch, "Top 9 Tools")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 7.5)
    c.drawCentredString(PW / 2, MARGIN + 0.08 * inch,
                        "kevin.donohue24@gmail.com  \u2022  847-772-4639")
    c.setFillColor(MUTED)
    c.drawRightString(PW - MARGIN, MARGIN + 0.08 * inch,
                      "Custom Apps, APIs, Documents & Websites")

    c.save()
    print("Done: Top9Tools_Client_Intake_Form.pdf")


if __name__ == "__main__":
    build()
