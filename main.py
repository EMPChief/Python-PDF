from fpdf import FPDF
import csv

OUTPUT_FILE = "output.pdf"
INPUT_FILE = "data.csv"


class PDFGenerator(FPDF):
    def __init__(self, orientation='p', unit='mm', format='A4'):
        super().__init__(orientation=orientation, unit=unit, format=format)
        self.set_auto_page_break(auto=True, margin=15)
        self.set_font("Arial", size=12)

    def header(self):
        self.cell(0, 10, "EMP Corp", 0, 1, "C")

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()} - Made by EMP Corp", 0, 0, "C")

    def content(self, content_text):
        self.cell(0, 10, content_text, ln=True)

    def generate_pdf(self, data):
        self.set_y(15)

        for row in data:
            topic, pages = row[1], int(row[2])

            for _ in range(pages):
                self.add_page()
                
                self.set_font("Arial", style="B")
                self.cell(0, 10, f"Topic: {topic}", ln=True)
                self.cell(0, 1, "", ln=True, border="T")

                self.content("This is a sample content.")

    def save_pdf(self, filename):
        self.output(filename)

def read_csv(file_path):
    data = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            data.append(row)
    return data

if __name__ == "__main__":
    data = read_csv(INPUT_FILE)

    pdf_generator = PDFGenerator(orientation='p', unit='mm', format='A4')
    pdf_generator.generate_pdf(data)
    pdf_generator.save_pdf(OUTPUT_FILE)
