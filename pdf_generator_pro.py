#!/usr/bin/env python3
"""
Professional PDF Resume Generator for Resume Retool
Creates ATS-friendly, beautifully styled PDF resumes
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import os

class ProfessionalResumePDF:
    """
    Generate beautiful, ATS-friendly PDF resumes
    Following best practices for executive resume design
    """
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.colors = {
            'primary': colors.HexColor('#2C3E50'),      # Dark blue-gray for headers
            'secondary': colors.HexColor('#34495E'),    # Medium gray for subheaders
            'accent': colors.HexColor('#3498DB'),       # Blue accent for lines
            'text': colors.HexColor('#2C3E50'),         # Dark text for readability
            'light': colors.HexColor('#7F8C8D'),        # Light gray for secondary info
        }
        self._create_professional_styles()
    
    def _create_professional_styles(self):
        """Create elegant, ATS-friendly styles"""
        
        # Name style - Large, bold, centered
        self.styles.add(ParagraphStyle(
            name='Name',
            parent=self.styles['Title'],
            fontSize=24,
            leading=28,
            textColor=self.colors['primary'],
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Contact style - Clean, centered, smaller
        self.styles.add(ParagraphStyle(
            name='Contact',
            parent=self.styles['Normal'],
            fontSize=10,
            leading=12,
            textColor=self.colors['secondary'],
            alignment=TA_CENTER,
            spaceAfter=4,
            fontName='Helvetica'
        ))
        
        # Professional title
        self.styles.add(ParagraphStyle(
            name='ProfessionalTitle',
            parent=self.styles['Normal'],
            fontSize=12,
            leading=14,
            textColor=self.colors['primary'],
            alignment=TA_CENTER,
            spaceAfter=12,
            spaceBefore=4,
            fontName='Helvetica-Bold'
        ))
        
        # Section headers - Clean with subtle accent
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading1'],
            fontSize=13,
            leading=16,
            textColor=self.colors['primary'],
            spaceAfter=8,
            spaceBefore=14,
            fontName='Helvetica-Bold',
            alignment=TA_LEFT
        ))
        
        # Company/Organization name
        self.styles.add(ParagraphStyle(
            name='Company',
            parent=self.styles['Normal'],
            fontSize=11,
            leading=13,
            textColor=self.colors['primary'],
            spaceAfter=2,
            fontName='Helvetica-Bold'
        ))
        
        # Job title/Position
        self.styles.add(ParagraphStyle(
            name='JobTitle',
            parent=self.styles['Normal'],
            fontSize=10,
            leading=12,
            textColor=self.colors['secondary'],
            spaceAfter=6,
            fontName='Helvetica-Oblique'
        ))
        
        # Date style - Right aligned
        self.styles.add(ParagraphStyle(
            name='Dates',
            parent=self.styles['Normal'],
            fontSize=10,
            leading=12,
            textColor=self.colors['light'],
            alignment=TA_RIGHT,
            fontName='Helvetica'
        ))
        
        # Bullet points - Clean and readable
        self.styles.add(ParagraphStyle(
            name='Bullet',
            parent=self.styles['Normal'],
            fontSize=10,
            leading=13,
            textColor=self.colors['text'],
            leftIndent=15,
            spaceAfter=3,
            fontName='Helvetica',
            alignment=TA_JUSTIFY
        ))
        
        # Professional summary
        self.styles.add(ParagraphStyle(
            name='Summary',
            parent=self.styles['Normal'],
            fontSize=10,
            leading=13,
            textColor=self.colors['text'],
            spaceAfter=12,
            alignment=TA_JUSTIFY,
            fontName='Helvetica'
        ))
        
        # Skills style
        self.styles.add(ParagraphStyle(
            name='Skill',
            parent=self.styles['Normal'],
            fontSize=10,
            leading=12,
            textColor=self.colors['text'],
            fontName='Helvetica'
        ))
        
        # Education style
        self.styles.add(ParagraphStyle(
            name='Education',
            parent=self.styles['Normal'],
            fontSize=10,
            leading=12,
            textColor=self.colors['text'],
            spaceAfter=4,
            fontName='Helvetica'
        ))
    
    def create_header_line(self):
        """Create a subtle line separator"""
        line = HRFlowable(
            width="100%",
            thickness=1,
            lineCap='round',
            color=self.colors['accent'],
            spaceBefore=2,
            spaceAfter=8
        )
        return line
    
    def format_contact_info(self, contact):
        """Format contact information with proper separators"""
        # Clean format with bullet separators
        parts = contact.split('|')
        if len(parts) > 1:
            formatted = " • ".join([p.strip() for p in parts])
            return formatted
        return contact
    
    def generate_pdf(self, resume_data, output_path):
        """
        Generate a professional PDF resume
        
        Args:
            resume_data: Dictionary with resume information
            output_path: Path for the output PDF
        """
        # Create document with proper margins for ATS scanning
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        # Build the resume content
        story = []
        
        # HEADER SECTION
        # Name
        story.append(Paragraph(resume_data.get('full_name', ''), self.styles['Name']))
        
        # Contact information
        contact = self.format_contact_info(resume_data.get('contact', ''))
        story.append(Paragraph(contact, self.styles['Contact']))
        
        # Professional title (if provided)
        if resume_data.get('title'):
            story.append(Paragraph(resume_data['title'], self.styles['ProfessionalTitle']))
        
        # Subtle separator line
        story.append(self.create_header_line())
        
        # PROFESSIONAL SUMMARY
        if resume_data.get('summary'):
            story.append(Paragraph('PROFESSIONAL SUMMARY', self.styles['SectionHeader']))
            story.append(Paragraph(resume_data['summary'], self.styles['Summary']))
        
        # CORE COMPETENCIES / SKILLS
        if resume_data.get('skills'):
            story.append(Paragraph('CORE COMPETENCIES', self.styles['SectionHeader']))
            
            skills = resume_data['skills']
            
            # Create a 3-column layout for skills
            skill_data = []
            num_cols = 3
            num_rows = (len(skills) + num_cols - 1) // num_cols
            
            for row in range(num_rows):
                row_data = []
                for col in range(num_cols):
                    idx = row + col * num_rows
                    if idx < len(skills):
                        # Add bullet point
                        skill_text = f"• {skills[idx]}"
                        row_data.append(Paragraph(skill_text, self.styles['Skill']))
                    else:
                        row_data.append("")
                skill_data.append(row_data)
            
            if skill_data:
                skill_table = Table(
                    skill_data,
                    colWidths=[2.2*inch, 2.2*inch, 2.2*inch],
                    style=TableStyle([
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                        ('LEFTPADDING', (0, 0), (-1, -1), 0),
                        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                        ('TOPPADDING', (0, 0), (-1, -1), 2),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                    ])
                )
                story.append(skill_table)
                story.append(Spacer(1, 0.15*inch))
        
        # PROFESSIONAL EXPERIENCE
        if resume_data.get('experience'):
            story.append(Paragraph('PROFESSIONAL EXPERIENCE', self.styles['SectionHeader']))
            
            for exp in resume_data['experience']:
                # Keep experience together on same page
                exp_content = []
                
                # Company and dates on same line using table
                company_date_data = [[
                    Paragraph(exp.get('company', ''), self.styles['Company']),
                    Paragraph(exp.get('dates', ''), self.styles['Dates'])
                ]]
                
                company_date_table = Table(
                    company_date_data,
                    colWidths=[4.5*inch, 2*inch],
                    style=TableStyle([
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                        ('LEFTPADDING', (0, 0), (0, 0), 0),
                        ('RIGHTPADDING', (-1, -1), (-1, -1), 0),
                        ('TOPPADDING', (0, 0), (-1, -1), 0),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                    ])
                )
                exp_content.append(company_date_table)
                
                # Job title
                exp_content.append(Paragraph(exp.get('title', ''), self.styles['JobTitle']))
                
                # Bullet points
                for bullet in exp.get('bullets', []):
                    # Clean bullet text
                    bullet_text = bullet.strip()
                    if not bullet_text.startswith('•'):
                        bullet_text = f"• {bullet_text}"
                    exp_content.append(Paragraph(bullet_text, self.styles['Bullet']))
                
                exp_content.append(Spacer(1, 0.1*inch))
                
                # Keep experience section together
                story.append(KeepTogether(exp_content))
        
        # EDUCATION
        if resume_data.get('education'):
            story.append(Paragraph('EDUCATION', self.styles['SectionHeader']))
            
            for edu in resume_data['education']:
                edu_text = f"<b>{edu.get('degree', '')}</b>"
                if edu.get('school'):
                    edu_text += f" | {edu['school']}"
                if edu.get('year'):
                    edu_text += f" | {edu['year']}"
                story.append(Paragraph(edu_text, self.styles['Education']))
        
        # Build the PDF
        doc.build(story)
        return output_path
    
    def generate_from_text(self, resume_text, output_path):
        """Convert plain text resume to professional PDF"""
        # Parse the text into structured data
        resume_data = self._parse_resume_text(resume_text)
        return self.generate_pdf(resume_data, output_path)
    
    def _parse_resume_text(self, text):
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
        
        current_section = None
        current_exp = None
        summary_lines = []
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            if not line:
                i += 1
                continue
            
            # Parse sections based on keywords
            if i == 0:  # First line is name
                resume_data['full_name'] = line
            elif i == 1:  # Second line is contact
                resume_data['contact'] = line
            elif i == 2 and ('|' in line or 'Candidate' in line):  # Title line
                resume_data['title'] = line
            elif 'PROFESSIONAL SUMMARY' in line.upper():
                current_section = 'summary'
                summary_lines = []
            elif 'CORE COMPETENCIES' in line.upper() or 'SKILLS' in line.upper():
                current_section = 'skills'
                if summary_lines and not resume_data['summary']:
                    resume_data['summary'] = ' '.join(summary_lines)
            elif 'PROFESSIONAL EXPERIENCE' in line.upper() or 'WORK EXPERIENCE' in line.upper():
                current_section = 'experience'
            elif 'EDUCATION' in line.upper():
                current_section = 'education'
                if current_exp:
                    resume_data['experience'].append(current_exp)
                    current_exp = None
            else:
                # Process content based on current section
                if current_section == 'summary':
                    if not any(keyword in line.upper() for keyword in ['CORE COMPETENCIES', 'SKILLS', 'PROFESSIONAL EXPERIENCE']):
                        summary_lines.append(line)
                
                elif current_section == 'skills':
                    if line.startswith('•'):
                        skill = line[1:].strip()
                        resume_data['skills'].append(skill)
                    elif line and not any(keyword in line.upper() for keyword in ['PROFESSIONAL', 'EXPERIENCE', 'EDUCATION']):
                        # Handle skills without bullets
                        resume_data['skills'].append(line)
                
                elif current_section == 'experience':
                    # Detect new company (usually has dates like "2020 - 2023")
                    if any(year in line for year in ['2020', '2021', '2022', '2023', '2024', '2025']) and '–' in line:
                        if current_exp:
                            resume_data['experience'].append(current_exp)
                        
                        # Parse company and dates
                        parts = line.rsplit(' ', 4)  # Split from right to get dates
                        dates = ''
                        company = line
                        
                        # Try to extract dates
                        for j in range(len(parts)):
                            if '–' in parts[j] or '-' in parts[j]:
                                dates = ' '.join(parts[j:])
                                company = ' '.join(parts[:j])
                                break
                        
                        current_exp = {
                            'company': company.strip(),
                            'dates': dates.strip(),
                            'title': '',
                            'bullets': []
                        }
                    elif current_exp and not current_exp['title'] and not line.startswith('•'):
                        # This is likely the job title
                        current_exp['title'] = line
                    elif current_exp and line.startswith('•'):
                        # Bullet point
                        current_exp['bullets'].append(line[1:].strip())
                
                elif current_section == 'education':
                    # Parse education entries
                    edu_entry = {'degree': '', 'school': '', 'year': ''}
                    
                    if '|' in line:
                        parts = line.split('|')
                        edu_entry['degree'] = parts[0].strip()
                        if len(parts) > 1:
                            edu_entry['school'] = parts[1].strip()
                        if len(parts) > 2:
                            edu_entry['year'] = parts[2].strip()
                    else:
                        edu_entry['degree'] = line
                    
                    resume_data['education'].append(edu_entry)
            
            i += 1
        
        # Add final experience if exists
        if current_exp:
            resume_data['experience'].append(current_exp)
        
        # Add summary if not already added
        if summary_lines and not resume_data['summary']:
            resume_data['summary'] = ' '.join(summary_lines)
        
        return resume_data


# Standalone function for easy integration
def create_professional_pdf(resume_text_or_data, output_path):
    """
    Create a professional PDF resume from text or structured data
    
    Args:
        resume_text_or_data: Either plain text resume or structured dict
        output_path: Where to save the PDF
    
    Returns:
        Path to generated PDF
    """
    generator = ProfessionalResumePDF()
    
    if isinstance(resume_text_or_data, str):
        # Plain text input
        return generator.generate_from_text(resume_text_or_data, output_path)
    else:
        # Structured data input
        return generator.generate_pdf(resume_text_or_data, output_path)


# Example usage
if __name__ == "__main__":
    # Test with sample resume data
    sample_data = {
        'full_name': 'Your Name',
        'contact': 'your.email@example.com | Your Location | LinkedIn',
        'title': 'Vice President Strategic Initiatives Candidate',
        'summary': 'Highly accomplished executive with 20+ years driving strategic initiatives and operational excellence in complex organizational environments. Proven track record of translating enterprise-wide strategies into actionable implementation plans, leading cross-functional teams, and delivering measurable business outcomes. Expert in change management, digital transformation, and scalable solution deployment.',
        'skills': [
            'Strategic Planning & Execution',
            'Change Management',
            'Healthcare Transformation',
            'Cross-functional Leadership',
            'Operations Excellence',
            'P&L Management ($70M+)',
            'Digital Transformation',
            'Stakeholder Engagement',
            'Program Management',
            'Process Optimization',
            'Team Development (30+)',
            'Agile & Waterfall'
        ],
        'experience': [
            {
                'company': 'TBWA WH, NEW YORK, NY',
                'dates': '2023 – Present',
                'title': 'SVP, Director of Integrated Delivery/Project + Program Management',
                'bullets': [
                    'Lead enterprise-wide strategic initiatives across $70M portfolio, ensuring alignment with organizational objectives and measurable business outcomes',
                    'Drive operational transformation and change management initiatives for department of 30+ project managers',
                    'Partner with executive leadership to identify, prioritize, and monitor strategic priorities that align with core business differentiators',
                    'Design and implement scalable frameworks for cross-functional execution and governance structures',
                    'Optimize program performance through comprehensive KPI tracking, budget management, and resource allocation',
                    'Champion digital transformation and AI adoption across project management operations'
                ]
            },
            {
                'company': 'ACCENTURE, NEW YORK, NY',
                'dates': '2020 – 2023',
                'title': 'Marketing and Communications Brand Delivery Lead',
                'bullets': [
                    'Managed strategic change initiatives across Healthcare, Financial Services, and Technology sectors',
                    'Led cross-functional transformation programs impacting multiple markets and business units',
                    'Developed scalable operational frameworks and best practices for enterprise-wide implementation',
                    'Mentored and developed team of 8-12 project managers while managing P&L across portfolio',
                    'Drove measurable improvements in operational efficiency and stakeholder satisfaction',
                    'Promoted from NY Brand Delivery Lead to NA and Canada Brand Delivery Lead'
                ]
            }
        ],
        'education': [
            {
                'degree': 'MFA, Literature, Fiction, Writing',
                'school': 'City University of New York-Brooklyn College',
                'year': ''
            },
            {
                'degree': 'B.A., Literature and Creative Writing',
                'school': 'Binghamton University',
                'year': ''
            }
        ]
    }
    
    # Generate PDF
    output_file = 'sample_resume_professional.pdf'
    create_professional_pdf(sample_data, output_file)
    print(f"✅ Professional PDF resume generated: {output_file}")