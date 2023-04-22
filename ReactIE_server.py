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
    reactions = get_extraction(f'{basePath}{filename}')
    save_json(reactions)
    return jsonify(reactions), 200

@app.route('/test')
@cross_origin()
def hello_world():
    return '<p>Hello, World!</p>'


# process user request to run PDF Converter on the uploaded pdf
@app.route('/parse', methods=['POST'])
@cross_origin()
def parsePDF():
    file = request.files['file']
    file.save(f'./upload/{file.filename}')
    runParser(f'./upload/{file.filename}')
    jsonFile = file.filename.replace('.pdf', '.json')
    with open(f'./json/{jsonFile}') as f:
        data = json.load(f)
        return jsonify({'fullText':data['fullText']}), 200