from flask import Flask, request, jsonify
import yaml
from os import listdir
from os.path import isfile, join

app = Flask(__name__)


@app.route('/api')
def index():
    onlyfiles = files('sw_vars/data_v2')
    return jsonify({'files': onlyfiles})


@app.route('/api/errors/')
def errors():
    onlyfiles = files('sw_vars/errors')
    return jsonify({"files": onlyfiles})


@app.route("/api/errors/<string:file>")
def errors_file(file):
    with open('sw_vars/errors/'+file, 'r', encoding="utf-8") as f:
        data = f.read().split('\n')
    return jsonify({file: data})


@app.route('/api/conf/')
def conf():
    onlyfiles = files('sw_vars/conf_v3')
    return jsonify({"files": onlyfiles})


def files(path):
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    return onlyfiles


@app.route("/api/conf/<string:file>")
def conf_file(file):
    with open('sw_vars/conf_v3/'+file, 'r', encoding="utf-8") as f:
        data = f.read().split('\n')
    return jsonify({file: data})


@app.route('/api/data/<string:file>', methods=['POST', 'GET'])
def data_table(file):
    with open('sw_vars/data_v2/'+file, 'r') as f:
        data = yaml.safe_load(f)
    if request.method == "GET":
        return jsonify({file: data})


@app.route('/api/data/<string:file>/<string:interface>', methods=['POST', 'GET'])
def data_file(file, interface):
    interface = interface.replace('_', '/')
    with open('sw_vars/data_v2/'+file, 'r') as f:
        data = yaml.safe_load(f)
    if request.method == "GET":
        return jsonify({file: {interface: data['interfaces'][interface]}})
    elif request.method == "POST":
        data['interfaces'][interface].update(
            request.json[file]['interfaces'][interface])
        with open('sw_vars/data_v2/' + file, 'w') as f:
            s = yaml.dump(data).replace('null', '').replace("'", "")
            f.write(s)
    return 'ok'


if __name__ == '__main__':
    app.run(debug=True)
