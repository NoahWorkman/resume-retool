#!/usr/bin/env python3
"""
PDF Generator for Nana's Resume Builder
Creates professional PDF resumes from optimized text
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfgen import canvas
from datetime import datetime
import os

class ResumePDFGenerator:
    """Generate professional PDF resumes"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Create custom styles for resume sections"""
        
        # Name style
        self.styles.add(ParagraphStyle(
            name='ResumeName',
            parent=self.styles['Title'],
            fontSize=20,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=6,
            alignment=TA_CENTER
        ))
        
        # Contact style
        self.styles.add(ParagraphStyle(
            name='Contact',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#34495E'),
            alignment=TA_CENTER,
            spaceAfter=12
        ))
        
        # Title style
        self.styles.add(ParagraphStyle(
            name='ResumeTitle',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#2C3E50'),
            alignment=TA_CENTER,
            spaceAfter=18,
            fontName='Helvetica-Bold'
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=8,
            spaceBefore=12,
            fontName='Helvetica-Bold',
            borderColor=colors.HexColor('#3498DB'),
            borderWidth=0,
            borderPadding=0
        ))
        
        # Company/School name style
        self.styles.add(ParagraphStyle(
            name='Organization',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=2,
            fontName='Helvetica-Bold'
        ))
        
        # Job title style
        self.styles.add(ParagraphStyle(
            name='JobTitle',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#34495E'),
            spaceAfter=4,
            fontName='Helvetica-Oblique'
        ))
        
        # Bullet point style
        self.styles.add(ParagraphStyle(
            name='BulletPoint',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#2C3E50'),
            leftIndent=20,
            spaceAfter=4
        ))
        
        # Summary style
        self.styles.add(ParagraphStyle(
            name='Summary',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=12,
            alignment=TA_LEFT
        ))
    
    def generate_pdf(self, resume_data: dict, output_path: str):
        """
        Generate PDF from resume data
        
        Args:
            resume_data: Dictionary containing resume information
            output_path: Path for output PDF file
        """
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )
        
        story = []
        
        # Name
        story.append(Paragraph(resume_data['full_name'], self.styles['ResumeName']))
        
        # Contact
        story.append(Paragraph(resume_data['contact'], self.styles['Contact']))
        
        # Title
        if 'customized_title' in resume_data:
            story.append(Paragraph(resume_data['customized_title'], self.styles['ResumeTitle']))
        elif 'title' in resume_data:
            story.append(Paragraph(resume_data['title'], self.styles['ResumeTitle']))
        
        # Professional Summary
        story.append(Paragraph('PROFESSIONAL SUMMARY', self.styles['SectionHeader']))
        story.append(Paragraph(resume_data['summary'], self.styles['Summary']))
        
        # Core Competencies
        story.append(Paragraph('CORE COMPETENCIES', self.styles['SectionHeader']))
        
        # Create skills in columns
        skills_data = []
        skills = resume_data.get('skills', [])
        
        # Split skills into 3 columns
        cols = 3
        rows = len(skills) // cols + (1 if len(skills) % cols else 0)
        
        for i in range(rows):
            row = []
            for j in range(cols):
                idx = i + j * rows
                if idx < len(skills):
                    row.append(f"• {skills[idx]}")
                else:
                    row.append("")
            skills_data.append(row)
        
        if skills_data:
            skills_table = Table(skills_data, colWidths=[2.3*inch, 2.3*inch, 2.3*inch])
            skills_table.setStyle(TableStyle([
                ('FONT', (0, 0), (-1, -1), 'Helvetica', 9),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2C3E50')),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 2),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ]))
            story.append(skills_table)
            story.append(Spacer(1, 0.2*inch))
        
        # Professional Experience
        story.append(Paragraph('PROFESSIONAL EXPERIENCE', self.styles['SectionHeader']))
        
        for exp in resume_data.get('experience', []):
            # Company and dates on same line
            exp_header = f"<b>{exp['company']}</b> <i>{exp.get('dates', '')}</i>"
            story.append(Paragraph(exp_header, self.styles['Organization']))
            
            # Job title
            story.append(Paragraph(exp['title'], self.styles['JobTitle']))
            
            # Bullets
            for bullet in exp.get('bullets', []):
                story.append(Paragraph(f"• {bullet}", self.styles['BulletPoint']))
            
            story.append(Spacer(1, 0.1*inch))
        
        # Education
        story.append(Paragraph('EDUCATION', self.styles['SectionHeader']))
        
        for edu in resume_data.get('education', []):
            edu_text = f"<b>{edu['degree']}</b> | {edu['school']}"
            story.append(Paragraph(edu_text, self.styles['Normal']))
        
        # Build PDF
        doc.build(story)
        
        return output_path
    
    def text_to_pdf(self, resume_text: str, output_path: str):
        """
        Convert plain text resume to PDF
        
        Args:
            resume_text: Plain text resume
            output_path: Path for output PDF
        """
        # Parse text into structured data
        resume_data = self._parse_resume_text(resume_text)
        
        # Generate PDF
        return self.generate_pdf(resume_data, output_path)
    
    def _parse_resume_text(self, text: str) -> dict:
        """Parse plain text resume into structured format"""
        lines = text.strip().split('\n')
        
        resume_data = {
            'full_name': '',
            'contact': '',
            'title': '',
            'summary': '',
            'skills': [],
            'experience': [],
            'education': []
        }
        
        # Simple parsing logic
        current_section = None
        current_exp = None
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            if not line:
                continue
            
            # First line is name
            if i == 0:
                resume_data['full_name'] = line
            elif i == 1:
                resume_data['contact'] = line
            elif i == 2 and '|' in line:
                resume_data['title'] = line
            elif 'PROFESSIONAL SUMMARY' in line:
                current_section = 'summary'
            elif 'CORE COMPETENCIES' in line:
                current_section = 'skills'
            elif 'PROFESSIONAL EXPERIENCE' in line:
                current_section = 'experience'
            elif 'EDUCATION' in line:
                current_section = 'education'
            else:
                # Add content to current section
                if current_section == 'summary':
                    resume_data['summary'] += line + ' '
                elif current_section == 'skills' and line.startswith('•'):
                    resume_data['skills'].append(line[1:].strip())
                elif current_section == 'experience':
                    if not line.startswith('•') and len(line) > 20:
                        # New company
                        if current_exp:
                            resume_data['experience'].append(current_exp)
                        
                        # Try to parse company and dates
                        parts = line.rsplit(' ', 3)
                        if len(parts) >= 2 and '–' in parts[-1]:
                            current_exp = {
                                'company': ' '.join(parts[:-1]),
                                'dates': parts[-1],
                                'title': '',
                                'bullets': []
                            }
                        else:
                            current_exp = {
                                'company': line,
                                'dates': '',
                                'title': '',
                                'bullets': []
                            }
                    elif current_exp and not current_exp['title'] and not line.startswith('•'):
                        current_exp['title'] = line
                    elif current_exp and line.startswith('•'):
                        current_exp['bullets'].append(line[1:].strip())
                elif current_section == 'education':
                    resume_data['education'].append({
                        'degree': line.split('|')[0].strip() if '|' in line else line,
                        'school': line.split('|')[1].strip() if '|' in line else ''
                    })
        
        # Add last experience
        if current_exp:
            resume_data['experience'].append(current_exp)
        
        return resume_data

# Example usage
if __name__ == "__main__":
    generator = ResumePDFGenerator()
    
    # Test with sample data
    sample_resume = {
        'full_name': 'Ji Myung Nana Sheppard',
        'contact': '917.513.6060 | nobermann@gmail.com | New Jersey | LinkedIn',
        'title': 'Vice President Strategic Initiatives Candidate',
        'summary': 'Highly accomplished executive with 20+ years driving strategic initiatives and operational excellence.',
        'skills': [
            'Strategic Planning',
            'Change Management',
            'Project Management',
            'Healthcare Transformation',
            'Cross-functional Leadership',
            'Operations Excellence'
        ],
        'experience': [
            {
                'company': 'TBWA WH, NEW YORK, NY',
                'dates': '2023 – Present',
                'title': 'SVP, Director of Integrated Delivery',
                'bullets': [
                    'Lead strategic initiatives across $70M portfolio',
                    'Drive enterprise-wide transformation programs'
                ]
            }
        ],
        'education': [
            {
                'degree': 'MFA, Literature',
                'school': 'City University of New York'
            }
        ]
    }
    
    output_file = 'sample_resume.pdf'
    generator.generate_pdf(sample_resume, output_file)
    print(f"✅ PDF generated: {output_file}")