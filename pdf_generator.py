import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_advance_packet(pitcher_name, pitch_mix_df, key_insights):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle', parent=styles['Heading1'], fontSize=18, leading=22, textColor=colors.HexColor('#0F172A')
    )
    section_style = ParagraphStyle(
        'SectionStyle', parent=styles['Heading2'], fontSize=12, leading=16, textColor=colors.HexColor('#1E3A8A'), spaceBefore=10
    )
    body_style = styles['Normal']
    
    story = []
    
    # Document Header
    story.append(Paragraph(f"ADVANCE SCOUTING REPORT: {pitcher_name.upper()}", title_style))
    story.append(Paragraph("MiLB Series Game Prep | Video & Technology Department", body_style))
    story.append(Spacer(1, 10))
    
    # Pitch Mix Table
    story.append(Paragraph("Pitch Arsenal Breakdown", section_style))
    table_data = [["Pitch Type", "Usage %", "Avg Velo (mph)", "Max Velo (mph)"]]
    
    for _, row in pitch_mix_df.iterrows():
        table_data.append([
            str(row["PitchType"]),
            f"{row['Usage%']:.1f}%",
            f"{row['AvgVelo']:.1f}",
            f"{row['MaxVelo']:.1f}"
        ])
        
    t = Table(table_data, colWidths=[130, 120, 130, 130])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#F8FAFC')),
    ]))
    story.append(t)
    story.append(Spacer(1, 12))
    
    # Key Game Plan Insights
    story.append(Paragraph("Coaching Directives & Video Triggers", section_style))
    for insight in key_insights:
        story.append(Paragraph(f"- {insight}", body_style))
        story.append(Spacer(1, 4))
        
    doc.build(story)
    buffer.seek(0)
    return buffer