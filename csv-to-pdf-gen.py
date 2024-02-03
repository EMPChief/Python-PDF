import pandas as pd
from fpdf import FPDF

"""
Generates a PDF report from a CSV file.

Reads data from a CSV file, iterates through the rows, and generates a PDF 
report with a title, content, and page footer for each row of data.

The PDFGenerator class handles creating the PDF and adding pages, headers, 
footers and content. The read_csv function reads the data from the CSV file.

The main execution generates the PDFGenerator instance, reads the CSV data, 
generates the PDF report, and saves it to file.
"""
OUTPUT_FILE = "output.pdf"
INPUT_FILE = "data.csv"


class PDFGenerator:
    def __init__(self, orientation='p', unit='mm', format='A4'):
        self.pdf = FPDF(orientation=orientation, unit=unit, format=format)
        self.pdf.set_auto_page_break(auto=True, margin=15)
        self.pdf.set_font("Arial", size=12)

    def header(self):
        self.pdf.cell(0, 10, "EMP Corp", 0, 1, "C")

    def footer(self):
        self.pdf.set_y(-15)
        self.pdf.set_font("Arial", "I", 8)
        self.pdf.cell(
            0, 10, f"Page {self.pdf.page_no()} - Made by EMP Corp", 0, 0, "C")

    def content(self, content_text):
        self.pdf.cell(0, 10, content_text, ln=True)

    def generate_pdf(self, data):
        self.pdf.set_y(15)

        for row in data.itertuples(index=False):
            topic, pages, description = row[1], int(
                row[2]), str(row[3])

            for _ in range(pages):
                self.pdf.add_page()

                self.pdf.set_font("Arial", style="B")
                self.pdf.cell(0, 10, f"Topic: {topic}", ln=True)
                self.pdf.cell(0, 1, "", ln=True, border="T")

                if description:
                    self.content(description)
                else:
                    self.content("This is a sample content.")

    def save_pdf(self, filename):
        self.pdf.output(filename)


def read_csv(file_path):
    data = pd.read_csv(file_path)
    return data


if __name__ == "__main__":
    data = read_csv(INPUT_FILE)

    pdf_generator = PDFGenerator(orientation='p', unit='mm', format='A4')
    pdf_generator.generate_pdf(data)
    pdf_generator.save_pdf(OUTPUT_FILE)
