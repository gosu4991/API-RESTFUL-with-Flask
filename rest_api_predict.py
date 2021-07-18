from flask import Flask
from flask_restful import Resource, Api, reqparse
from werkzeug.datastructures import FileStorage
from predict_resnet50 import predict
import tempfile
import json
import pprint

app = Flask(__name__)
app.logger.setLevel('INFO')

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
        ofile, ofname = tempfile.mkstemp()
        the_file.save(ofname)
        results = predict(ofname)[0]
        output = {'categories':[]}
        for _, categ, score in results:
            output['categories'].append(("Categories: "+categ))
            output['categories'].append(("Accuracy: "+str(float(score))))
        
        return output


api.add_resource(Hello, '/hello')
api.add_resource(Image, '/image')

if __name__ == '__main__':
    app.run(debug=True)
