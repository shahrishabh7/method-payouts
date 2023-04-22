import base64
import xml.etree.ElementTree as ET

# takes in string XML and turn into ???
def parse(base64_str):
    base64_str = base64_str[21:]
    # Decode the Base64 encoded string
    decoded_data = base64.b64decode(base64_str)

    # Convert the decoded bytes to a string
    decoded_string = decoded_data.decode('utf-8')

    # Parse the XML string
    root = ET.fromstring(decoded_string)

    # Print the root element
    root_as_string = ET.tostring(root, encoding='utf8').decode('utf8')
    # print(root_as_string)

    # Put XML into table so can read it
    convert_to_table(root)

def convert_to_table(root):
    data = {}
    for child in root:
        print(child[0][0].text)
        break
        # data[child.tag] = child.text
    
    return data