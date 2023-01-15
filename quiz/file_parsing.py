import openpyxl


def excel_parser(name_file):
    wb = openpyxl.load_workbook(name_file)
    wb.active = 0
    sheet = wb.active
    # получим макс количество строк в документе
    rows = sheet.max_row
    print(rows)
    # проходим по всем значениям колонки B
    questions = []
    question = []
    for num in range(1, rows):
        cell = sheet['C' + str(num)]
        if cell.value:
            questions.append(question)
            question = []
            description = cell.value
            cell_name_a = 'B' + str(num)
            question_text = sheet[cell_name_a].value
            question_text = str(question_text).replace('\xa0', ' ')
            question.append(question_text)
            description = str(description).replace('\xa0', ' ')
            question.append(description)
        else:
            cell_name_b = 'B' + str(num)
            choice = []
            choice_text = sheet[cell_name_b].value
            choice_text = str(choice_text).replace('\xa0', ' ')
            choice.append(choice_text)
            choice.append(sheet['A' + str(num)].value)
            question.append(choice)
    return questions[1:]


if __name__ == "__main__":
    excel_parser('questions.xlsx')
