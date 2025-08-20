# Nana's Resume Builder 🎯

AI-powered resume customization tool that tailors resumes to job descriptions while maintaining 100% factual accuracy.

## 🛡️ Core Principle: No Fabrication

This tool **NEVER** adds experience, skills, or qualifications you don't have. It only:
- Rewords existing experience to match job keywords
- Reorders content for better relevance
- Emphasizes transferable skills
- Optimizes for ATS systems

## ✨ Features

- 📸 **Screenshot Input**: Take a screenshot of any job posting
- 🌐 **URL Support**: Direct LinkedIn, Indeed, or any job board URL
- 📄 **PDF Support**: Upload job description PDFs
- 🔍 **Smart Keyword Matching**: Identifies and matches relevant keywords
- ✅ **Fact Checking**: Never adds experience you don't have
- 📊 **Match Analysis**: Shows what keywords were/weren't matched
- 📑 **PDF Export**: Professional PDF output

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/NoahWorkman/nana-resume-builder.git
cd nana-resume-builder

# Install dependencies
pip install -r requirements.txt

# For OCR support (screenshots)
# Mac: brew install tesseract
# Linux: sudo apt-get install tesseract-ocr
# Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
```

### Usage

```bash
# Screenshot input
python main.py /path/to/job_screenshot.png

# URL input
python main.py "https://www.linkedin.com/jobs/view/123456789"

# PDF input
python main.py /path/to/job_description.pdf

# Text input
python main.py "Paste the job description text here..."
```

### Output

The tool generates:
1. **Customized Resume** (`.txt` and `.pdf`)
2. **Analysis Report** (`.json`) showing:
   - Keywords found
   - Match rate
   - What was optimized
   - What couldn't be matched

## 📁 Project Structure

```
nana-resume-builder/
├── main.py              # Main application entry point
├── input_handler.py     # Handles screenshots, URLs, PDFs
├── keyword_optimizer.py # Keyword matching engine
├── resume_builder.py    # Resume generation logic
├── pdf_generator.py     # PDF creation
├── requirements.txt     # Python dependencies
└── output/             # Generated resumes and reports
```

## 🔍 How It Works

### 1. Input Processing
- **Screenshots**: OCR with Tesseract
- **URLs**: Web scraping with BeautifulSoup
- **PDFs**: Text extraction with PyPDF2

### 2. Keyword Analysis
```python
Job Posting → Extract Keywords → Match to Experience → Rewrite (Never Add)
```

### 3. Optimization Rules

✅ **Allowed**:
- "Managed" → "Strategically led" (same meaning)
- Reorder skills to match job priorities
- Emphasize relevant experience

❌ **Not Allowed**:
- Adding certifications not earned
- Claiming experience not possessed
- Inventing skills or technologies

### 4. Example Transformation

**Job Requires**: "Healthcare strategic planning experience"

**Nana Has**: "Strategic planning at Accenture with healthcare clients"

**Output**: "Led strategic planning initiatives for healthcare sector clients at Accenture"

**NOT**: "10 years dedicated healthcare strategic planning" (would be false)

## 📊 Sample Output

```
✨ Optimization Summary:
==================================================

✅ Keywords Successfully Matched:
   • strategic planning → Highlight enterprise strategy work at TBWA
   • change management → Direct experience
   • cross-functional → Managing 30+ PMs across disciplines

💡 Optimization Suggestions:
   • For 'healthcare': Emphasize Accenture healthcare client work

⚠️  Cannot Add (No Experience):
   • Clinical operations: No direct clinical experience
   • HIPAA compliance: No specific HIPAA certification

🛡️  Integrity Check: All content is 100% based on actual experience
```

## 🎯 Use Cases

Perfect for:
- Tailoring resumes to specific job postings
- Ensuring ATS keyword optimization
- Maintaining multiple resume versions
- Quick application to similar roles

## ⚠️ Important Notes

1. **Always Review**: Check the output before submitting
2. **Factual Only**: The tool will never add false information
3. **Supplement**: This tool helps optimize, not replace, your judgment

## 🤝 Contributing

This is a private repository for Nana's use. For questions or improvements, please contact Noah.

## 📝 License

Private repository - All rights reserved

---

Built with ❤️ for Nana's job search success!