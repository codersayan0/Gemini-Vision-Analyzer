# 🔍 Gemini Vision Analyzer

A Streamlit web app that uses Google's Gemini 1.5 Flash model to analyze uploaded images and answer custom questions about them.

## 🚀 Features

- 📷 Upload and validate image files (JPG, PNG, JPEG, WebP)
- ❓ Ask any question related to the uploaded image
- 🤖 Get intelligent responses using Gemini Vision API (Gemini 1.5 Flash)
- 🧠 Google API Key integration via sidebar
- 📝 Download analysis report as a PDF
- 🧰 Clean UI with success and error message boxes

---

## 📸 Demo

> [Insert a screenshot or a GIF demo here if available]

---

## 🧑‍💻 Tech Stack

- [Streamlit](https://streamlit.io/)
- [Google Generative AI (Gemini API)](https://ai.google.dev/)
- [Pillow (PIL)](https://pillow.readthedocs.io/en/stable/)
- [ReportLab](https://www.reportlab.com/) *(for PDF generation)*

---

## 🧪 How It Works

1. User uploads an image (max 10MB, supported: PNG, JPG, JPEG, WebP)
2. User enters a question (e.g., "What is happening in this image?")
3. The app sends the image and question to Gemini via API
4. Gemini analyzes and responds intelligently
5. User can download the result as a PDF report

---

## 🔐 Setup Instructions

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/gemini-vision-analyzer.git
   cd gemini-vision-analyzer
