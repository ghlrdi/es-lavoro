import os
import re
import requests
import json

base_dir = 'abc/File copiati'
os.makedirs(base_dir, exist_ok=True)
url = "https://test.register"
pattern = r'^-> \{([^}]+)\} (\S+) (\S+)$'

for t in os.listdir('abc'):
    file_path = os.path.join('abc', t)
    
    if os.path.isfile(file_path):
        with open(file_path) as curFile:
            text = ""
            title = None  
            number = None
            matricola_dir = None 
            TupText = []

            for line in curFile:
                line = line.strip()
                print(f"Processing line: {line}")  

                match = re.match(pattern, line)
                if match:
                    print(f"Match found: {match.groups()}") 

                    if title is not None and text:
                        full_text = f"{number}\n{text}\n"
                        matricola_path = os.path.join(base_dir, matricola_dir)
                        os.makedirs(matricola_path, exist_ok=True)

                        if not os.path.exists(os.path.join(matricola_path, title)):
                            with open(os.path.join(matricola_path, title), 'w+') as file:
                                file.write(full_text)
                        else:
                            print(f"The file {title} already exists in {matricola_path}")

                    title = match.group(2) + '.txt'
                    number = match.group(3)
                    matricola_dir = match.group(1)
                    text = ""
                else:
                    if line:  
                        text += line + '\n'

            if title is not None and text:
                full_text = f"{number}\n{text}\n"
                matricola_path = os.path.join(base_dir, matricola_dir)
                os.makedirs(matricola_path, exist_ok=True)

                if not os.path.exists(os.path.join(matricola_path, title)):
                    with open(os.path.join(matricola_path, title), 'w+') as file:
                        file.write(full_text)
                else:
                    print(f"The file {title} already exists in {matricola_path}")

            if matricola_dir and number:
                TupText.append({
                    "matricola": matricola_dir,
                    "number": number,
                    "text": text.strip()
                })
                print(f"Data to send: {TupText[-1]}")  
            else:
                print(f"Missing data for file: {t}, Matricola: {matricola_dir}, Number: {number}")

            try:
                if TupText:
                    response = requests.post(url, json=TupText)
                    print(f"Response: {response.status_code}, {response.text}")
                else:
                    print("No valid data to send.")

            except requests.RequestException as e:
                print(f"Error during request: {e}")
