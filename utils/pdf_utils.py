# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# #ranking based system with recomentation Hari 
# def generate_pdf(candidates, output_path, job_description):

#     c = canvas.Canvas(output_path, pagesize=letter)
#     c.setFont("Helvetica", 12)
#     c.drawString(100, 780, "Candidate Evaluation Report")
#     c.line(100, 775, 500, 775)
#     c.drawString(100, 750, f"Job Description: {job_description[:100]}...")  # Show snippet

#     # Sort candidates by score
#     candidates = sorted(candidates, key=lambda x: x['score'], reverse=True)
#     y = 700
#     for rank, candidate in enumerate(candidates, 1):
#         c.drawString(100, y, f"Rank #{rank}: {candidate['name']}")
#         c.drawString(100, y - 20, f"Skills: {', '.join(candidate['skills'])}")
#         c.drawString(100, y - 40, f"Score: {candidate['score']}%")
#         # Recommendation
#         if candidate['score'] >= 80:
#             recommendation = "Strong Match"
#         elif 50 <= candidate['score'] < 80:
#             recommendation = "Moderate Match - Needs Review"
#         else:
#             recommendation = "Weak Match - Consider Alternative"
        
#         c.drawString(100, y - 60, f"Recommendation: {recommendation}")
        
#         y -= 80
#         if y < 100:  # Add a new page if needed
#             c.showPage()
#             y = 750

#     c.save()

# This file handles PDF generation for the recruiter report.
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(candidates, report_path):
    doc = SimpleDocTemplate(report_path, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    title = Paragraph("<b>Candidate Report</b>", styles["Title"])
    elements.append(title)

    data = [["Rank", "Candidate Name", "Skills", "Score", "Recommendation"]]

    candidates_sorted = sorted(candidates, key=lambda x: x["score"], reverse=True)

    for rank, candidate in enumerate(candidates_sorted, start=1):
        name = Paragraph(candidate["name"], styles["Normal"])
        skills = Paragraph(", ".join(candidate["skills"]) if candidate["skills"] else "N/A", styles["Normal"])  # Wrap skills text
        score = candidate["score"]

        # Recommendation based on score threshold
        recommendation_text = "Highly Recommended" if score >= 80 else "Consider" if score >= 50 else "Weak Match - Consider Alternative"
        recommendation = Paragraph(recommendation_text, styles["Normal"])

        data.append([rank, name, skills, score, recommendation])

    page_width, _ = letter
    col_widths = [page_width * 0.1, page_width * 0.25, page_width * 0.35, page_width * 0.1, page_width * 0.2]

    table = Table(data, colWidths=col_widths)

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('WORDWRAP', (0, 1), (-1, -1), 'CJK')  # word wrap
    ]))

    elements.append(table)
    doc.build(elements)
