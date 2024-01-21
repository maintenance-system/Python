import pdfplumber
import io
from bidi.algorithm import get_display
import re


# r'H:\Final Project\בטיחות.pdf'
def readFileAndNumberPage(path):
    with open(path, 'rb') as file:
        pdf_data = file.read()
        with pdfplumber.open(io.BytesIO(pdf_data)) as pdf:
            text = ""
            num_pages = len(pdf.pages)
            for page in pdf.pages:
                page_text = page.extract_text()
                rtl_text = get_display(page_text)
                text += rtl_text
                new_text = text.replace("Ê", " ")

    return new_text, num_pages


def readFile(path):
    with open(path, 'rb') as file:
        pdf_data = file.read()
        with pdfplumber.open(io.BytesIO(pdf_data)) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                rtl_text = get_display(page_text)
                text += rtl_text
                new_text = text.replace("Ê", " ")

    return new_text
#def a

def sortText():
    # Deleting header and footer
    sentence_to_remove = " מדינת ישראל"
    result = text.replace(sentence_to_remove, "")
    sentence_to_remove = f"משרד החינוך תאריך הדפסה:{getDate()} "
    result = result.replace(sentence_to_remove, "")
    sentence_to_remove = f"המוסד: {getSymbole()} עץ הדעת {getNeighborhood()}  מפקח בטיחות: חרדי"
    result = result.replace(sentence_to_remove, "")
    num = 1
    while num <= num_pages:
        sentence_to_remove = f"עמוד {num} מתוך {num_pages}"
        result = result.replace(sentence_to_remove, "")
        num += 1

    # Deleting the beginning of the file
    start_word = "ממצאים לפי תחומי בדיקה וקדימות טיפול"
    end_word = "פירוט הממצאים"
    start_index = result.find(start_word)
    end_index = result.find(end_word) + len(end_word)
    result = result[:start_index] + result[end_index:]

    # Deleting the end of the file
    split_text = result.split("הערה לפרטי המסגרת:")
    result = split_text[0]
    return result


# function to get the print date
def getDate(text):
    patterndate = r'תאריך הדפסה:(\d{2}/\d{2}/\d{4})'

    match = re.search(patterndate, text)
    date = ""
    if match:
        date = match.group(1)
    return date


# function to get the symbole
def getSymbole():
    semelMosad = r'המוסד:\s*(.*?)(?=\s+עץ הדעת)'
    match = re.findall(semelMosad, text)
    return match[0]


# function to get address and symbole
def getAddressAndSymbole():
    pattern = r'המוסד:\s*(.*?)(?=\s+מנהל המוסד)'
    match = re.search(pattern, text).group(1)
    return match


# get only the neighborhood
def getNeighborhood():
    pattern = r'עץ הדעת (.*?),'
    match = re.search(pattern, getAddressAndSymbole())
    if match:
        extracted_text = match.group(1)
        return extracted_text
    else:
        return "Pattern not found in the text."


def selectedPrecedence(src, dest, text):
    start_tag = f'קדימות{src} :'
    end_tag = f'קדימות{dest} :'

    start_index = text.find(start_tag)
    end_index = text.find(end_tag)

    if start_index != -1:  # and end_index != -1:
        # extracted_text = text[start_index + len(start_tag):end_index].strip()
        if end_index != -1:
            extracted_text = text[start_index + len(start_tag):end_index].strip()
        else:
            extracted_text = text[start_index + len(start_tag):].strip()
        return extracted_text
    else:
        return ""


def numerAProblemsFromPrecedence(text):
    pattern = r"(?<!\d )\d+ [^\n]+(?:\n.+)??"
    matches = re.findall(pattern, text)
    output_array = []
    # Print the extracted sections
    for match in matches:
        if match.strip() not in ['2 מתוך 4 מדינת ישראל', '632083 עץ הדעת קהילות יעקב  מפקח בטיחות: חרדי', '1 :']:
            output_array.append(match.strip())
    # print(output_array)
    return len(output_array)


def getNumberProblems():
    #numberProblems = 0
    #precedenceZero = selectedPrecedence(0, 1, text)
    #if precedenceZero != "":
    #    numberProblems += numerAProblemsFromPrecedence(precedenceZero)
    #precedenceOne = selectedPrecedence(1, 2, text)
    #if precedenceOne != "":
    #    numberProblems += numerAProblemsFromPrecedence(precedenceOne)
    # print("1111111111", precedenceOne)
    #precedenceTwo = selectedPrecedence(2, 3, text)
    #if precedenceTwo != "":
    #    numberProblems += numerAProblemsFromPrecedence(precedenceTwo)
    return 10


if __name__ == '__main__':
    # num pages - number a pages in the file
    # text - the text from the file
    text, num_pages = readFile()
    # print(text)
    # date - is a print date
    date = getDate(text)
    # print(date)
    # symbole - is Institution symbol
    symbol = getSymbole()
    # print(symbol)
    # addressSymbol - the full address and symbol
    addressSymbol = getAddressAndSymbole()
    # print(addressSymbol)
    # neighborhood - the neighborhood
    neighborhood = getNeighborhood()
    # print(neighborhood)
    # sort the text
    text = sortText()
    print(text)
    # Precedence 0/1/2
    precedenceZero = selectedPrecedence(0, 1)
    # print("00000000", precedenceZero)
    numberProblems = 0
    if precedenceZero != "":
        numberProblems += numerAProblemsFromPrecedence(precedenceZero)

    precedenceOne = selectedPrecedence(1, 2)
    if precedenceOne != "":
        numberProblems += numerAProblemsFromPrecedence(precedenceOne)
    # print("1111111111", precedenceOne)
    precedenceTwo = selectedPrecedence(2, 3)
    if precedenceTwo != "":
        numberProblems += numerAProblemsFromPrecedence(precedenceTwo)
    # print("2222222222222", precedenceTwo)
    print(numberProblems)
    # print(text)
