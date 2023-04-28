import base64
import xml.etree.ElementTree as ET
from collections import defaultdict
import pandas as pd

# takes in string XML and turn into ???
def parse(base64_str):
    base64_str = base64_str[21:]
    # Decode the Base64 encoded string
    decoded_data = base64.b64decode(base64_str)

    # Convert the decoded bytes to a string
    decoded_string = decoded_data.decode('utf-8')

    # Parse the XML string
    root = ET.fromstring(decoded_string)

    # Convert root to string
    root_as_string = ET.tostring(root, encoding='utf8').decode('utf8')
    # print(root_as_string)

    # extract payor / payee info to build entities
    payments_preview, individual_entity_information, corporate_entity_information, data, corporate_accounts = convert_to_table(root)

    return payments_preview, individual_entity_information, corporate_entity_information, data, corporate_accounts

def convert_to_table(root):
    data = []
    corporate_accounts = defaultdict()
    corporate_entity_information = {}
    haveCorporateInformation = False
    
    for transaction in root.findall('row'):
        if not haveCorporateInformation:
            corporate_entity_information["Name"] = transaction[1][3].text
            corporate_entity_information["DBA"] = transaction[1][4].text
            corporate_entity_information["EIN"] = transaction[1][5].text
            corporate_entity_information["Address Line 1"] = transaction[1][6][0].text
            corporate_entity_information["City"] = transaction[1][6][1].text
            corporate_entity_information["State"] = transaction[1][6][2].text
            corporate_entity_information["Zip"] = transaction[1][6][3].text
            haveCorporateInformation = True

        row = {}

        # Employee / Payee rows
        row['E: Dunkin ID'] = transaction[0][0].text
        row['E: Dunkin Branch'] = transaction[0][1].text
        row['E: First Name'] = transaction[0][2].text
        row['E: Last Name'] = transaction[0][3].text
        row['E: DOB'] = transaction[0][4].text
        row['E: Phone Number'] = transaction[0][5].text
        row['E: Payee Plaid Id'] = transaction[2][0].text
        row['E: Payee Loan Account #'] = transaction[2][1].text

        # Payor rows
        if transaction[1][0].text not in corporate_accounts:
            corporate_accounts[transaction[1][0].text] = (int(transaction[1][1].text),int(transaction[1][2].text))

        row['Payor: Dunkin ID'] = transaction[1][0].text
        row['Payor: ABARouting'] = transaction[1][1].text
        row['Payor: Account Number'] = transaction[1][2].text
        row['Payor: Name'] = transaction[1][3].text
        row['Payor: EIN'] = transaction[1][5].text
        row['Payor: Address'] = transaction[1][6][0].text + ', ' + transaction[1][6][1].text + ', ' + transaction[1][6][2].text + ', ' + transaction[1][6][3].text

        row['Amount'] = transaction[3].text
        data.append(row)

    individual_entity_information = filter_individual_entities(data)

    # convert data to viewable dataframe for testing purposes
    df = pd.DataFrame(data)
    sorted_df = df.sort_values(by=['E: Dunkin ID'])
    sorted_df.to_csv('method_data.csv', index=False)

    # create payment staging preview
    payments_preview = create_payment_staging_preview(data)

    return payments_preview, individual_entity_information, corporate_entity_information, data, corporate_accounts

def filter_individual_entities(data):
    # Load the original table
    df = pd.DataFrame(data)

    # Concatenate first name and last name to create a full name column
    df['Full Name'] = df['E: First Name'] + ' ' + df['E: Last Name']

    # Group the data by full name and apply an aggregate function to select a single record for each group
    filtered_df = df.groupby('Full Name').first().reset_index()

    # Save the filtered dataframe as a CSV file
    # filtered_df.to_csv('individual_entities.csv', index=False)

    data_dict = df.to_dict('list')

    return data_dict

def create_payment_staging_preview(data):
    # Load the original table
    df = pd.DataFrame(data)

    # Convert the 'Amount' column to numeric type
    df['Amount'] = pd.to_numeric(df['Amount'].str.replace('$', '')).round(2)

    # Concatenate first name and last name to create a full name column
    df['Name'] = df['E: First Name'] + ' ' + df['E: Last Name']

    # Group the data by full name and apply an aggregate function to select a single record for each group
    filtered_df = df.groupby('Name')['Amount'].sum().reset_index()

    # Save the filtered dataframe as a CSV file
    filtered_df.to_csv('filtered_table.csv', index=False)

    # Convert the filtered dataframe to a dictionary and return it
    data_dict = filtered_df.to_dict('list')
    return data_dict