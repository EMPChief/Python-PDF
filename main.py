from fpdf import FPDF
import csv
OUTPUT_FILE = "output.pdf"
INPUT_FILE = "data.csv"


class PDFGenerator(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.set_font("Arial", size=12)

    def generate_pdf(self, data):
        for row in data:
            topic, pages = row[1], int(row[2])

            for _ in range(pages):
                self.add_page()
                self.cell(0, 10, f"Topic: {topic}", ln=True)
                self.cell(0, 1, "", ln=True, border="T")

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
    
    pdf_generator = PDFGenerator()
    pdf_generator.generate_pdf(data)
    pdf_generator.save_pdf(OUTPUT_FILE)
