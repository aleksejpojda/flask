from flask import Flask, render_template, url_for, request
import yaml
from os import listdir
from os.path import isfile, join

app = Flask(__name__)

@app.route('/')
def index():
    onlyfiles = [f for f in listdir('data') if isfile(join('data', f))]
    return render_template('index.html', onlyfiles=onlyfiles)

@app.route('/data/<string:file>') #, methods=['POST', 'GET'])
def data_table(file):
    with open('data/'+file, 'r') as f:
        data = yaml.safe_load(f)
    if request.method == "GET":
        return render_template('data_table.html', data=data, file=file)

@app.route('/data/<string:file>/<string:interface>', methods=['POST', 'GET'])
def data_file(file, interface):
    interface = interface.replace('_', '/')
    param_del = [
        "description",
        "encapsulation",
        "arp_inspection",
        "dhcp_snooping",
        "load_interval",
        "portfast",
        "bpdufilter",
        "channel_group",
        "status",
        ]
    param_not_del = [
        "mode",
        "vlan_access",
        "vlan_trunk",
        "vlan_voice",
        "vlan_native"
    ]
    param_vlan = [
        "ip",
        "description",
        "status"
    ]
    with open('data/'+file, 'r') as f:
        data = yaml.safe_load(f)
    if request.method == "GET":
        return render_template('data.html', data=data['interfaces'], file=file, interface=interface)
    elif request.method == "POST":
        data_dict = request.form.to_dict()
        # print(data_dict['description'])
        intf = data_dict["interface"]
        if not 'Vlan' in intf:
            for param in param_not_del:
                if not request.form[param] and data['interfaces'][intf].get(param):
                    data['interfaces'][intf][param] = ''
                elif request.form[param]:
                    data['interfaces'][intf][param] = request.form[param]

            for param in param_del:
                if not data_dict[param] and data['interfaces'][intf].get(param):
                    del data['interfaces'][intf][param]
                elif data_dict[param]:
                    data['interfaces'][intf][param] = data_dict[param]

        elif "Vlan" in intf:
            for param in param_vlan:
                if not request.form.get(param) and data['interfaces'][intf].get(param):
                    del data['interfaces'][intf][param]
                elif request.form.get(param):
                    data['interfaces'][intf][param] = request.form[param]
        with open('data/' + file, 'w') as f:
            s = yaml.dump(data).replace('null', '').replace("'", "")
            f.write(s)

    return render_template('data_table.html', data=data, file=file)

if __name__ == '__main__':
    app.run(debug=True)