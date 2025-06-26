import streamlit as st
import google.generativeai as genai
from fpdf import FPDF

# 🔐 Configure Gemini API
genai.configure(api_key="AIzaSyCeIrInbnkuJJBAqP_TBe69IwnQ9ethDBE")  # Use your Gemini API key

# 📄 Gemini Model
model = genai.GenerativeModel("gemini-2.0-flash")

# 📤 PDF Export Function
def save_to_pdf(email_content, filename="generated_email.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    for line in email_content.split('\n'):
        pdf.multi_cell(0, 10, txt=line)
    
    pdf.output(filename)
    return filename

# 🖥 Streamlit App Interface
st.set_page_config(page_title="AI Email Generator", layout="centered")
st.title("📧 AI Email Generator")

st.markdown("Generate professional emails in seconds!")

# 🌐 Input Fields
name = st.text_input("👤 Your Name")
purpose = st.text_area("🎯 Email Purpose", placeholder="e.g., Applying for internship...")
tone = st.selectbox("🎭 Tone of Email", ["Formal", "Friendly", "Persuasive", "Apologetic", "Grateful"])

email_text = ""

# ✍ Generate Email Button
if st.button("Generate Email"):
    if not name or not purpose:
        st.warning("Please fill in all the fields.")
    else:
        with st.spinner("Generating email using Gemini AI..."):
            prompt = f"""
            Write a {tone.lower()} email.
            Name of sender: {name}
            Purpose: {purpose}
            Format it as a professional email with proper salutation, body, and sign-off.
            """
            response = model.generate_content(prompt)
            email_text = response.text.strip()

        st.subheader("📬 Generated Email")
        st.markdown(email_text.replace('\n', '  \n'))  # Ensures clean line breaks in Markdown

        # 📥 Download PDF
        file_path = save_to_pdf(email_text)
        with open(file_path, "rb") as f:
            st.download_button("📄 Download as PDF", f, file_name="email_output.pdf", mime="application/pdf")