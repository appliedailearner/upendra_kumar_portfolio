import zipfile
import xml.etree.ElementTree as ET

def read_docx(file_path):
    with zipfile.ZipFile(file_path) as docx:
        tree = ET.fromstring(docx.read('word/document.xml'))
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        text = '\n'.join(''.join(node.text for node in p.iterfind('.//w:t', ns) if node.text) for p in tree.iterfind('.//w:p', ns) if list(p.iterfind('.//w:t', ns)))
        with open('docx_content.txt', 'w', encoding='utf-8') as f:
            f.write(text)

read_docx(r'C:\MyResumePortfolio\azurewebapp\ICTSI_AppService_PrivateOnly_SOP_Option2.docx')
