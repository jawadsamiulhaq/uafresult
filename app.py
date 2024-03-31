from flask import Flask, request, jsonify
import requests
import json
from flask_cors import CORS
app = Flask(__name__)
CORS(app, origins='*')

def process_request(ag_number, errors_list):
    try:
        session_requests = requests.session()
        html1 = session_requests.get("http://lms.uaf.edu.pk/login/index.php", params={'url': 'http://lms.uaf.edu.pk/login/index.php'})
        html = html1.text
        a = html.split("document.getElementById(\'token\').value=\'")[1]
        b = a.split("'")[0]
        payload = {'Register': ag_number, 'token': b}
        html = session_requests.post(f"http://lms.uaf.edu.pk/course/uaf_student_result.php", data=payload)
        html = html.text
        #file_path = "file.html"
        #with open(file_path, "w", encoding="utf-8") as file:
          #  file.write(html)
        payload=json.dumps({"reg":ag_number})
        response = session_requests.post(f"https://jawadsamiulhaq.com/uafresults/", data=json.dumps({"html":html}),headers={"Content-Type": "application/json"})
        # print(response.json())
        return response.json()
    except Exception as e:
        return {'error': str(e)}

@app.route('/uafresult', methods=["POST"])
def calculate_cgpa():
    try:
        data = request.get_json()

        if 'reg' not in data:
            return jsonify({'error': 'Missing reg parameter'}), 400

        ag_number = data['reg']
        errors_list = []  # Reset errors_list for each request

        result = process_request(ag_number, errors_list)

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

