from pdfminer.high_level import extract_text

def extract_text_from_pdf(pdf_path):
    text =extract_text(pdf_path)
    return text
if __name__ == '__main__':

    sample_path = "CV_Floresida_Tare_SHQ.pdf"
    result = extract_text_from_pdf(sample_path)
    print(result)