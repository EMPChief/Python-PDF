import pandas as pd
from fpdf import FPDF
import glob


class SimpleInvoiceGenerator:
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

            pdf.set_font("Arial", size=12)
            pdf.set_font("Arial", style="B", size=16)
            pdf.cell(0, 10, "Invoice from EMPCorp", 0, 1, "C")

            # Customer Details
            pdf.set_font("Arial", size=12)
            pdf.cell(0, 10, "Invoice Number: " + str(df.iloc[0, 0]), 0, 1, "L")
            pdf.cell(0, 10, "Invoice Date: " + str(df.iloc[0, 1]), 0, 1, "L")
            pdf.cell(0, 10, "Customer Name: " + str(df.iloc[0, 2]), 0, 1, "L")
            pdf.cell(0, 10, "Customer Address: " +
                     str(df.iloc[0, 3]), 0, 1, "L")
            pdf.cell(0, 10, "Customer Email: " + str(df.iloc[0, 4]), 0, 1, "L")

            # Company Details
            pdf.ln(10)
            pdf.cell(0, 10, "Company Name: " + self.company_name, 0, 1, "L")
            pdf.cell(0, 10, "Card Number: " + self.card_number, 0, 1, "L")
            pdf.cell(0, 10, "Card Reference: " +
                     self.card_reference, 0, 1, "L")

            pdf.ln(10)
            pdf.set_font("Arial", style="B", size=12)
            col_widths = [40, 60, 30, 30, 30]

            for i, header in enumerate(["Item", "Description", "Quantity", "Unit Price", "Total"]):
                pdf.cell(col_widths[i], 10, header, 1)
            pdf.ln(10)

            for index, row in df.iterrows():
                for i, col in enumerate(["product_id", "product_name", "amount_purchased", "price_per_unit", "total_price"]):
                    pdf.cell(col_widths[i], 10, str(row[col]), 1)
                pdf.ln(10)

            pdf.cell(col_widths[0] + col_widths[1] +
                     col_widths[2], 10, "Total Amount:", 1)
            pdf.cell(col_widths[3] + col_widths[4], 10,
                     str(df['total_price'].sum()), 1)

            output_filename = f"{self.output_folder}invoice_{df.iloc[0, 0]}.pdf"
            pdf.output(output_filename)

        print("PDFs generated successfully.")


filepaths = glob.glob("invoices/*.xlsx")
invoice_generator = SimpleInvoiceGenerator(
    filepaths, company_name="EMPCorp", card_number="XXXX-XXXX-XXXX-XXXX", card_reference="123124457812")
invoice_generator.generate_invoices()
