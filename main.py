import pandas as pd
from fpdf import FPDF
import glob
from datetime import datetime, timedelta


class ProfessionalInvoiceGenerator:
    def __init__(self, filepaths, output_folder="invoices_pdf/", company_name="Your Company", card_number="XXXX-XXXX-XXXX-XXXX", card_reference="1234"):
        self.filepaths = filepaths
        self.output_folder = output_folder
        self.company_name = company_name
        self.card_number = card_number
        self.card_reference = card_reference

    def generate_invoices(self):
        for filepath in self.filepaths:
            df = pd.read_excel(filepath, sheet_name="Sheet 1")
            pdf = FPDF(orientation='p', unit='mm', format='A4')
            pdf.add_page()

            # Header
            pdf.set_font("Arial", style="B", size=16)
            pdf.cell(0, 10, f"Invoice from {self.company_name}", 0, 1, "C")

            # Customer Details
            pdf.set_font("Arial", size=12)
            pdf.cell(0, 10, f"Invoice Number: 123812", 0, 1, "L")
            pdf.cell(0, 10, f"Customer Name: Artur", 0, 1, "L")
            pdf.cell(0, 10, f"Customer Address: Lovund 8764", 0, 1, "L")
            pdf.cell(0, 10, f"Customer Email: admin@empchief.com", 0, 1, "L")

            # Company Details
            pdf.ln(10)
            pdf.cell(0, 10, f"Company Name: {self.company_name}", 0, 1, "L")
            pdf.cell(0, 10, f"Card Number: {self.card_number}", 0, 1, "L")
            pdf.cell(
                0, 10, f"Card Reference: {self.card_reference}", 0, 1, "L")

            # Line break
            pdf.ln(10)

            # Table Header
            pdf.set_font("Arial", style="B", size=12)
            col_widths = [40, 60, 30, 30, 30]
            headers = ["Item", "Description",
                       "Quantity", "Unit Price", "Total"]

            for i, header in enumerate(headers):
                pdf.cell(col_widths[i], 10, header, 1)
            pdf.ln(10)

            # Invoice Items
            pdf.set_font("Arial", size=12)
            for index, row in df.iterrows():
                for i, col in enumerate(["product_id", "product_name", "amount_purchased", "price_per_unit", "total_price"]):
                    pdf.cell(col_widths[i], 10, str(row[col]), 1)
                pdf.ln(10)

            # Total Amount
            pdf.cell(col_widths[0] + col_widths[1] +
                     col_widths[2], 10, "Total Amount:", 1)
            pdf.cell(col_widths[3] + col_widths[4], 10,
                     f"{df['total_price'].sum():.2f}", 1)

            # Date generated and Pay by date
            generated_date = datetime.now().strftime("%Y-%m-%d")
            pay_by_date = (datetime.now() + timedelta(days=30)
                           ).strftime("%Y-%m-%d")

            pdf.ln(10)
            pdf.set_font("Arial", style="B", size=12)
            pdf.cell(col_widths[0] + col_widths[1], 10,
                     f"Date Generated: {generated_date}", 1)
            pdf.cell(col_widths[2] + col_widths[3] +
                     col_widths[4], 10, f"Pay By Date: {pay_by_date}", 1)

            # Save the PDF
            output_filename = f"{self.output_folder}invoice_{df.iloc[0, 0]}.pdf"
            pdf.output(output_filename)

        print("PDFs generated successfully.")


filepaths = glob.glob("invoices/*.xlsx")
invoice_generator = ProfessionalInvoiceGenerator(
    filepaths, company_name="EMPCorp", card_number="XXXX-XXXX-XXXX-XXXX", card_reference="123124457812")
invoice_generator.generate_invoices()
