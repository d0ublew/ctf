from flask import Flask, render_template, url_for ,request
import os
import defusedxml.ElementTree as ET

app = Flask(__name__)

CONFIG = {
    "SECRET_KEY" : os.urandom(24),
    "FLAG" : open("/flag.txt").read()
}

app.secret_key = CONFIG["SECRET_KEY"]

class PetDetails: 
    def __init__(self, name, price, description, image_path, gender, size): 
        self.name = name 
        self.price = price 
        self.description = description 
        self.image_path = image_path 
        self.gender = gender 
        self.size = size 

def parse_store_xml_file(xml_file="store.xml"):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        items = []
        for item_element in root.findall('item'):
            name = item_element.find('name').text
            price = float(item_element.find('price').text)
            description = item_element.find('description').text
            image_path = item_element.find('image_path').text
            gender = item_element.find('gender').text
            size = item_element.find('size').text

            item_data = (name, price, description, image_path, gender, size)
            items.append(item_data)

        return items
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
    return None

def parse_xml(xml):
    try:
        tree = ET.fromstring(xml)
        name = tree.find("item")[0].text
        price = float(tree.find("item")[1].text)
        description = tree.find("item")[2].text
        image_path = tree.find("item")[3].text
        gender = tree.find("item")[4].text
        size = tree.find("item")[5].text
        details = PetDetails(name,price,description,image_path,gender,size)
        combined_items = ("{0.name};"+str(details.price)+";{0.description};"+details.image_path+";{0.gender};{0.size}").format(details)
        return [combined_items]
    except:
        print("Malformed xml, skipping")
        return []

# Index
@app.route('/')
def index():
    return render_template('index.html',value=parse_store_xml_file())

@app.route('/view')
def view():
    xml = request.args.get('xml')
    list_results = parse_xml(xml)
    if list_results:
        items = list_results[0].split(";")
        return render_template('view.html',value=items)
    else:
        return render_template('error.html')

# Main Function
if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0")
        

