from pypdf import PdfReader

reader = PdfReader("C://Users//ChenPen//Desktop//AEC Tech 2024//GENN_APD_112_AIA_ARC_PLA_N1_B_Plan N1.pdf")
number_of_pages = len(reader.pages)
page = reader.pages[0]
text = page.extract_text()
print (text)