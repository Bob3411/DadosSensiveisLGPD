import os
import pandas as pd
import docx
import PyPDF2
import re


def is_personal_data(text):
    # Expressões regulares para identificar dados pessoais
    patterns = [
        r'\b[A-Z][a-z]+\s[A-Z][a-z]+\b',  # Nome completo
        r'\b\d{2}.\d{3}.\d{3}-\d{1}\b',  # RG
        r'\b\d{3}.\d{3}.\d{3}-\d{2}\b',  # CPF
        r'\b(Masculino|Feminino|Outro)\b',  # Gênero
        r'\b\d{2}/\d{2}/\d{4}\b',  # Data de nascimento (DD/MM/AAAA)
        r'\b[A-Z][a-z]+\s[A-Z][a-z]+,\s[A-Z][a-z]+\b',  # Local de nascimento
        r'\b\d{4,5}-\d{4}\b',  # Telefone
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
        r'\b[A-Z]{3}-\d{4}\b',  # Placa de automóvel (ABC-1234)
        r'\b\d{4}\s\d{4}\s\d{4}\s\d{4}\b',  # Cartão bancário (16 dígitos)
        r'\b(Branco|Negro|Pardo|Indígena|Amarelo)\b',  # Origem racial ou étnica
        r'\b(Católica|Evangélica|Ateísta|Agnóstica)\b',  # Convicção religiosa
        r'\b(Liberal|Conservador|Socialista|Anarquista)\b',  # Opinião política
        r'\b[Sindicato|Organização]+\b',  # Filiação a sindicato ou organização
        r'\b(Saúde|Vida Sexual)\b',  # Dado referente à saúde ou à vida sexual
        r'\bGenético|Biométrico\b',  # Dado genético ou biométrico
    ]
    for pattern in patterns:
        if re.search(pattern, text):
            return True
    return False

# def is_personal_data(text):
    # Expressões regulares para identificar informações pessoais
#    patterns = [
#        r'\b\d{3}.\d{3}.\d{3}-\d{2}\b',  # CPF
#       r'\b\d{2}.\d{3}.\d{3}/\d{4}-\d{2}\b',  # CNPJ
#        r'\b\d{4,5}-\d{4}\b',  # Telefone
#        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
#    ]
#    for pattern in patterns:
#        if re.search(pattern, text):
#            return True
#    return False


def process_file(file_path):
    if file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            if is_personal_data(text):
                return 'Dados Pessoais'
            else:
                return 'Não Dados Pessoais'
    elif file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
        for column in df.columns:
            if any(df[column].apply(lambda x: is_personal_data(str(x)))):
                return 'Dados Pessoais'
        return 'Não Dados Pessoais'
    elif file_path.endswith('.pdf'):
        pdf_file = open(file_path, 'rb')
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        text = ''
        for page_num in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_num)
            text += page.extractText()
        pdf_file.close()
        if is_personal_data(text):
            return 'Dados Pessoais'
        else:
            return 'Não Dados Pessoais'
    elif file_path.endswith('.docx'):
        doc = docx.Document(file_path)
        text = ''
        for para in doc.paragraphs:
            text += para.text
        if is_personal_data(text):
            return 'Dados Pessoais'
        else:
            return 'Não Dados Pessoais'
    else:
        return 'Formato de arquivo não suportado'


def classify_files(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            classification = process_file(file_path)
            print(f'{file_name}: {classification}')

# Exemplo de uso
folder_path = 'C:\\Users\\Fabio\\Documents\\Teste'
classify_files(folder_path)
