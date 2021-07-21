from flask import Flask, render_template, request, jsonify
from flask_restful import Resource, Api, reqparse
from werkzeug.datastructures import FileStorage
from predict_resnet50 import predict
import tempfile
import json
import pprint
import requests
import json

app = Flask(__name__)
app.logger.setLevel('INFO')
url='http://class-catdog.herokuapp.com/image'

api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('file',
                    type=FileStorage,
                    location='files',
                    required=True,
                    help='provide a file')

class Hello(Resource):

    def get(self):
        return {'word': '[tiger_cat,0.5858129858970642],[Egyptian_cat,0.210690438747406],'}




class Image(Resource):

    def post(self):
        args = parser.parse_args()
        the_file = args['file']
        # save a temporary copy of the file
        ofile, ofname = tempfile.mkstemp()
        the_file.save(ofname)
        # predict
        results = predict(ofname)[0]
        # formatting the results as a JSON-serializable structure:
        output = {'top_categories': []}
        out = {'categories': []}
        for _, categ, score in results:
            out['categories'] += (([categ+str(': ')+str(float(score))]))

        return [out]



# routes
@app.route("/index.html", methods=['GET', 'POST'])
def main():
    return render_template("index.html")

@app.route("/submit", methods = ['POST'])
def get_output():
    if request.method == 'POST':
        img = request.files['my_image']
        img_path = img.filename
        files = {'file': img.read()}
        prediction = requests.post(url,files=files) 
        data = prediction.content
        json_data = json.loads(data)


    return render_template("index.html",data=json_data, img_path = img_path)

api.add_resource(Hello, '/hello')
api.add_resource(Image, '/image')

if __name__ == '__main__':
    app.run(debug=True)