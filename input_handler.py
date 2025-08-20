#!/usr/bin/env python3
"""
Input Handler for Multiple Job Posting Formats
Handles: Screenshots (OCR), URLs (web scraping), PDFs, and text
"""

import os
import re
import requests
from typing import Optional, Dict
from PIL import Image
import pytesseract
import PyPDF2
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class JobPostingExtractor:
    """
    Extracts job posting text from various sources
    Supports: Screenshots, URLs, PDFs, and raw text
    """
    
    def __init__(self):
        self.supported_formats = {
            'screenshot': ['.png', '.jpg', '.jpeg', '.gif', '.bmp'],
            'pdf': ['.pdf'],
            'text': ['.txt', '.md'],
            'url': ['http://', 'https://']
        }
    
    def extract_from_source(self, source: str) -> Dict:
        """
        Main entry point - automatically detects source type and extracts text
        
        Args:
            source: Can be a file path, URL, or raw text
            
        Returns:
            Dict with job_text and metadata
        """
        result = {
            'job_text': '',
            'source_type': '',
            'company': '',
            'position': '',
            'extraction_method': '',
            'success': False,
            'error': None
        }
        
        try:
            # Detect source type
            if self._is_url(source):
                result = self._extract_from_url(source)
            elif os.path.isfile(source):
                ext = os.path.splitext(source)[1].lower()
                if ext in self.supported_formats['screenshot']:
                    result = self._extract_from_screenshot(source)
                elif ext in self.supported_formats['pdf']:
                    result = self._extract_from_pdf(source)
                elif ext in self.supported_formats['text']:
                    result = self._extract_from_text_file(source)
            else:
                # Assume it's raw text
                result = self._extract_from_text(source)
            
            # Extract company and position from text
            if result['success']:
                result['company'] = self._extract_company(result['job_text'])
                result['position'] = self._extract_position(result['job_text'])
                
        except Exception as e:
            result['error'] = str(e)
            result['success'] = False
        
        return result
    
    def _is_url(self, source: str) -> bool:
        """Check if source is a URL"""
        return source.startswith('http://') or source.startswith('https://')
    
    def _extract_from_screenshot(self, image_path: str) -> Dict:
        """Extract text from screenshot using OCR"""
        print(f"📸 Extracting text from screenshot: {image_path}")
        
        try:
            # Open image
            image = Image.open(image_path)
            
            # Use Tesseract OCR to extract text
            text = pytesseract.image_to_string(image)
            
            # Clean up OCR output
            text = self._clean_ocr_text(text)
            
            return {
                'job_text': text,
                'source_type': 'screenshot',
                'extraction_method': 'OCR (Tesseract)',
                'success': True,
                'error': None
            }
            
        except Exception as e:
            return {
                'job_text': '',
                'source_type': 'screenshot',
                'extraction_method': 'OCR (Tesseract)',
                'success': False,
                'error': f"OCR extraction failed: {str(e)}"
            }
    
    def _extract_from_url(self, url: str) -> Dict:
        """Extract job posting from URL"""
        print(f"🌐 Extracting job posting from URL: {url}")
        
        try:
            # Detect job board and use appropriate extraction
            domain = urlparse(url).netloc
            
            if 'linkedin.com' in domain:
                return self._extract_from_linkedin(url)
            elif 'indeed.com' in domain:
                return self._extract_from_indeed(url)
            elif 'glassdoor.com' in domain:
                return self._extract_from_glassdoor(url)
            else:
                # Generic extraction
                return self._extract_generic_webpage(url)
                
        except Exception as e:
            return {
                'job_text': '',
                'source_type': 'url',
                'extraction_method': 'web_scraping',
                'success': False,
                'error': f"URL extraction failed: {str(e)}"
            }
    
    def _extract_from_linkedin(self, url: str) -> Dict:
        """Extract from LinkedIn job posting"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # LinkedIn-specific selectors
        job_text = ""
        
        # Try to find job description section
        description_section = soup.find('div', class_='description__text')
        if not description_section:
            description_section = soup.find('div', {'class': re.compile('job-description')})
        
        if description_section:
            job_text = description_section.get_text(separator='\n', strip=True)
        
        # Extract company and title
        company = ""
        position = ""
        
        company_elem = soup.find('a', {'class': re.compile('company-name')})
        if company_elem:
            company = company_elem.get_text(strip=True)
        
        title_elem = soup.find('h1', {'class': re.compile('job-title')})
        if title_elem:
            position = title_elem.get_text(strip=True)
        
        return {
            'job_text': job_text,
            'source_type': 'url',
            'extraction_method': 'LinkedIn scraping',
            'company': company,
            'position': position,
            'success': bool(job_text),
            'error': None if job_text else "Could not extract job description"
        }
    
    def _extract_generic_webpage(self, url: str) -> Dict:
        """Generic webpage extraction"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text
        text = soup.get_text(separator='\n', strip=True)
        
        # Clean up text
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        text = '\n'.join(lines)
        
        return {
            'job_text': text,
            'source_type': 'url',
            'extraction_method': 'Generic web scraping',
            'success': bool(text),
            'error': None if text else "Could not extract content"
        }
    
    def _extract_from_pdf(self, pdf_path: str) -> Dict:
        """Extract text from PDF"""
        print(f"📄 Extracting text from PDF: {pdf_path}")
        
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()
            
            return {
                'job_text': text,
                'source_type': 'pdf',
                'extraction_method': 'PyPDF2',
                'success': True,
                'error': None
            }
            
        except Exception as e:
            return {
                'job_text': '',
                'source_type': 'pdf',
                'extraction_method': 'PyPDF2',
                'success': False,
                'error': f"PDF extraction failed: {str(e)}"
            }
    
    def _extract_from_text_file(self, file_path: str) -> Dict:
        """Extract from text file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        return {
            'job_text': text,
            'source_type': 'text_file',
            'extraction_method': 'Direct file read',
            'success': True,
            'error': None
        }
    
    def _extract_from_text(self, text: str) -> Dict:
        """Handle raw text input"""
        return {
            'job_text': text,
            'source_type': 'raw_text',
            'extraction_method': 'Direct input',
            'success': True,
            'error': None
        }
    
    def _clean_ocr_text(self, text: str) -> str:
        """Clean up OCR output"""
        # Fix common OCR errors
        replacements = {
            '|': 'I',  # Pipe often confused with I
            '0': 'O',  # Zero/O confusion in certain contexts
            '§': 'S',  # Section symbol confused with S
        }
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Fix line breaks
        text = re.sub(r'(?<=[a-z])\s+(?=[a-z])', ' ', text)
        
        return text.strip()
    
    def _extract_company(self, text: str) -> str:
        """Try to extract company name from job text"""
        patterns = [
            r'(?:Company|Employer|Organization)[\s:]+([A-Z][A-Za-z\s&,]+)',
            r'About\s+([A-Z][A-Za-z\s&,]+)',
            r'Join\s+([A-Z][A-Za-z\s&,]+)',
            r'([A-Z][A-Za-z\s&,]+)\s+is\s+(?:seeking|hiring|looking)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                company = match.group(1).strip()
                # Clean up common suffixes
                company = re.sub(r'\s+(Inc|LLC|Ltd|Corp|Corporation)\.?$', '', company)
                return company
        
        return ""
    
    def _extract_position(self, text: str) -> str:
        """Try to extract position title from job text"""
        patterns = [
            r'(?:Position|Title|Role)[\s:]+([A-Za-z\s,\-]+)',
            r'(?:Job\s+Title)[\s:]+([A-Za-z\s,\-]+)',
            r'^([A-Z][A-Za-z\s,\-]+)(?:\n|$)',  # Often first line
            r'(?:Seeking|Hiring)\s+(?:a\s+)?([A-Z][A-Za-z\s,\-]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.MULTILINE)
            if match:
                position = match.group(1).strip()
                # Remove common artifacts
                position = position.replace('\n', ' ').strip()
                if len(position) > 5 and len(position) < 100:  # Sanity check
                    return position
        
        return ""

# Example usage
if __name__ == "__main__":
    extractor = JobPostingExtractor()
    
    # Test with different input types
    test_inputs = [
        "/Users/noahworkman/Downloads/job_screenshot.png",  # Screenshot
        "https://www.linkedin.com/jobs/view/123456",       # URL
        "/Users/noahworkman/Downloads/job_description.pdf", # PDF
        "Vice President position at Centene..."             # Raw text
    ]
    
    for input_source in test_inputs:
        print(f"\nTesting: {input_source[:50]}...")
        result = extractor.extract_from_source(input_source)
        
        if result['success']:
            print(f"✅ Extracted successfully via {result['extraction_method']}")
            print(f"   Company: {result['company']}")
            print(f"   Position: {result['position']}")
            print(f"   Text length: {len(result['job_text'])} characters")
        else:
            print(f"❌ Extraction failed: {result['error']}")