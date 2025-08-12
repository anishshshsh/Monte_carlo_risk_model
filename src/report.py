from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image  
from reportlab.lib.styles import getSampleStyleSheet
import os

def create_pdf_report(output_pdf_path, title, summary_text, image_paths):
    """
    Create a PDF report with the given title, summary text, and images.
    """
    doc = SimpleDocTemplate(output_pdf_path, pagesize=A4)  # Create PDF document
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph(f"<b>{title}</b>", styles['Title']))
    story.append(Spacer(1,12))
    for line in summary_text.split('\n'):  # Split summary text into lines
        story.append(Paragraph(line, styles['Normal']))
        story.append(Spacer(1,6))
    story.append(Spacer(1,12))
    for img in image_paths:  # Add images to the story
        if os.path.exists(img):
            story.append(Image(img, width=480, height=240))
            story.append(Spacer(1,12))
    doc.build(story)
