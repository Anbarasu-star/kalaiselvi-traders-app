import streamlit as st
from fpdf import FPDF
import base64
import os
from datetime import datetime

# Constants
RATE_PER_KG = 35
ITEMS = ['Coconut', 'Gingelly', 'Groundnut']
HEADER_COLOR = (0, 51, 102)

# PDF Class
class PDF(FPDF):
    def header(self):
        self.set_fill_color(*HEADER_COLOR)
        self.set_text_color(255, 255, 255)

        if os.path.exists("logo.png"):
            self.image("logo.png", 10, 8, 20)

        self.set_font("Arial", 'B', 18)
        self.cell(0, 10, "Kalaiselvi Traders", ln=True, align='C', fill=True)

        self.set_font("Arial", '', 12)
        self.cell(0, 10, "267, EH Road, Vysarpadi, Chennai - 39", ln=True, align='C', fill=True)
        self.ln(5)

        self.set_text_color(0, 0, 0)
        self.set_font("Arial", '', 11)
        self.cell(0, 10, f"Date: {datetime.now().strftime('%d-%m-%Y')}", ln=True, align='R')
        self.ln(5)

    def footer(self):
        self.set_y(-30)
        self.set_font("Arial", 'I', 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, "Thank you for your business. Have a great day!", ln=True, align='C')

        self.set_y(-20)
        self.set_font("Arial", '', 10)
        self.cell(0, 10, f"Generated on: {datetime.now().strftime('%d-%m-%Y %H:%M')}", ln=True, align='L')

        self.set_y(-10)
        self.cell(0, 10, "Signature: __________________________", ln=True, align='R')

# Page Config
st.set_page_config(page_title="கலைசெல்வி டிரேடர்ஸ் - செக்கு எண்ணெய்", layout="centered")

# Styling
st.markdown("""
    <style>
        h1 {
            color: #003366;
            text-align: center;
        }
        .btn-download {
            background-color: #003366;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            text-decoration: none;
            font-size: 16px;
            text-align: center;
        }
        .btn-download:hover {
            background-color: #00509e;
        }
    </style>
""", unsafe_allow_html=True)

# Title and Address
st.markdown("<h1>🧾 கலைசெல்வி டிரேடர்ஸ் - செக்கு எண்ணெய்</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 16px;'>267, EH Road, Vysarpadi, Chennai - 39</p>", unsafe_allow_html=True)

# Optional Logo
if os.path.exists("logo.png"):
    st.image("logo.png", width=80)

# Inputs
item = st.selectbox("Select Item", ITEMS)
weight = st.number_input("Enter Weight (kg)", min_value=0.0, step=0.5)
payment_status = st.radio("Payment Status", ["Paid", "Not Paid"])

# Show Total
if weight > 0:
    amount = weight * RATE_PER_KG
    st.success(f"💰 Total Amount: ₹ {amount:.2f}")

# PDF Generation
if st.button("Generate Bill"):
    amount = weight * RATE_PER_KG
    pdf = PDF()
    pdf.add_page()

    # Table Header
    pdf.set_fill_color(*HEADER_COLOR)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(60, 10, "Item", 1, 0, 'C', True)
    pdf.cell(40, 10, "Weight (kg)", 1, 0, 'C', True)
    pdf.cell(40, 10, "Rate/kg", 1, 0, 'C', True)
    pdf.cell(40, 10, "Amount", 1, 1, 'C', True)

    # Table Row
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 12)
    pdf.cell(60, 10, item, 1, 0, 'C')
    pdf.cell(40, 10, f"{weight:.2f}", 1, 0, 'C')
    pdf.cell(40, 10, f"Rs. {RATE_PER_KG}", 1, 0, 'C')
    pdf.cell(40, 10, f"Rs. {amount:.2f}", 1, 1, 'C')

    # Total Row
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(140, 10, "Total", 1, 0, 'R')
    pdf.cell(40, 10, f"Rs. {amount:.2f}", 1, 1, 'C')

    # Payment Status
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"Payment Status: {payment_status}", ln=True, align='L')

    # Save and Show
    output_path = "kalaiselvi_bill.pdf"
    pdf.output(output_path)

    with open(output_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="500" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

    # Download Link
    st.markdown(
        f"<a href='data:application/octet-stream;base64,{base64_pdf}' download='kalaiselvi_bill.pdf' class='btn-download'>📥 Download Bill</a>",
        unsafe_allow_html=True
    )
