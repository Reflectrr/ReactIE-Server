from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from ReactIE.run_ReactIE import get_extraction
from utils import save_json
from PDFConversion.xmlParser import runParser
import json

app = Flask(__name__)
cors = CORS(app) 
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/extraction')
@cross_origin()
def request_extraction():
    basePath = './json/'
    filename = request.args.get('filename')
    if not filename.endswith('.json'):
        return jsonify({'error':'Invalid file type'}), 400
    # check if reactions have already been extracted
    try:
        with open(f'./reactions/result_{filename}') as f:
            reactions = json.load(f)
            return jsonify(reactions), 200
    except:
        reactions = get_extraction(f'{basePath}{filename}')
        save_json(filename, reactions)
        return jsonify(reactions), 200

# process user request to run PDF Converter on the uploaded pdf
@app.route('/parse', methods=['POST'])
@cross_origin()
def parsePDF():
    file = request.files['file']
    file.save(f'./upload/{file.filename}')
    jsonFile = file.filename.replace('.pdf', '.json')
    # check if json file exists
    try:
        with open(f'./json/{jsonFile}') as f:
            data = json.load(f)
            return jsonify({'fullText':data['fullText']}), 200
    except:
        runParser(f'./upload/{file.filename}')
        with open(f'./json/{jsonFile}') as f:
            data = json.load(f)
            return jsonify({'fullText':data['fullText']}), 200

@app.route('/test')
@app.route('/')
@cross_origin()
def hello_world():
    return '<p>Hello, World!</p>'