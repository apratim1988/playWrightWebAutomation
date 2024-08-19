import openpyxl
from faker import Faker

def read_test_data(file_path, sheet_name):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook[sheet_name]
    data = []

    headers = [cell.value for cell in sheet[1]]
    fake = Faker()

    for row in sheet.iter_rows(min_row=2, values_only=True):
        test_data = dict(zip(headers, row))

        # Add dynamically generated data
        test_data['first_name'] = fake.first_name()
        test_data['last_name'] = fake.last_name()
        test_data['zipcode'] = fake.zipcode()

        data.append(test_data)

    return data
