import glob
import rlcompleter
import readline

import PyPDF2

def path_completer(text, state):
    line = readline.get_line_buffer().split()

    if '~' in text:
        text = os.path.expanduser('~')

    return [x for x in glob.glob(text+'*')][state]
readline.parse_and_bind('tab: complete')
readline.set_completer(path_completer)

if __name__ == "__main__":
    pdf = input('Enter PDF: ')
    src_pdf = PyPDF2.PdfFileReader(pdf)
    if src_pdf.isEncrypted:
        pswd = input('Enter PASSWORD: ')
        src_pdf.decrypt(pswd)
        print(src_pdf.documentInfo)

        dst_pdf = PyPDF2.PdfFileWriter()
        dst_pdf.cloneReaderDocumentRoot(src_pdf)

        d = {key: src_pdf.documentInfo[key] for key in src_pdf.documentInfo.keys()}
        dst_pdf.addMetadata(d)

        with open(pdf, 'wb') as f:
            dst_pdf.write(f)

    else:
        print("'"+pdf+"' is not encrypted.")
