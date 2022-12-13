from flask import Flask, render_template, url_for, request
import yaml
from os import listdir
from os.path import isfile, join

app = Flask(__name__)

@app.route('/')
def index():
    onlyfiles = [f for f in listdir('data') if isfile(join('data', f))]
    return render_template('index.html', onlyfiles=onlyfiles)

@app.route('/data/<string:file>', methods=['POST', 'GET'])
def data_file(file):
    with open('data/'+file, 'r') as f:
        data = yaml.safe_load(f)
    if request.method == "GET":
        return render_template('data.html', data=data)
    elif request.method == "POST":
        data_dict = request.form.to_dict()
        print(data_dict['descr'])
        intf = data_dict["interface"]
        if not 'Vlan' in intf:
            if not data_dict["descr"] and data['interfaces'][intf].get('description'):
                del data['interfaces'][intf]['description']
            elif data_dict["descr"]:
                data['interfaces'][intf]['description'] = data_dict["descr"]

            if not request.form["mode"] and data['interfaces'][intf].get('mode'):
                data['interfaces'][intf]['mode'] = ''
            elif request.form["mode"]:
                data['interfaces'][intf]['mode'] = request.form["mode"]

            if not request.form["vlan_access"] and data['interfaces'][intf].get('vlan_access'):
                data['interfaces'][intf]['vlan_access'] = ''
            elif request.form["vlan_access"]:
                data['interfaces'][intf]['vlan_access'] = request.form["vlan_access"]

            if not request.form["vlan_trunk"] and data['interfaces'][intf].get('vlan_trunk'):
                data['interfaces'][intf]['vlan_trunk'] = ''
            elif request.form["vlan_trunk"]:
                data['interfaces'][intf]['vlan_trunk'] = request.form["vlan_trunk"]

            if not request.form["vlan_voice"] and data['interfaces'][intf].get('vlan_voice'):
                data['interfaces'][intf]['vlan_voice'] = ''
            elif request.form["vlan_voice"]:
                data['interfaces'][intf]['vlan_voice'] = request.form["vlan_voice"]

            if not request.form["vlan_native"] and data['interfaces'][intf].get('vlan_native'):
                data['interfaces'][intf]['vlan_native'] = ''
            elif request.form["vlan_native"]:
                data['interfaces'][intf]['vlan_native'] = request.form["vlan_native"]

            if not request.form["encapsulation"] and data['interfaces'][intf].get('encapsulation'):
                del data['interfaces'][intf]['encapsulation']
            elif request.form["encapsulation"]:
                data['interfaces'][intf]['encapsulation'] = request.form["encapsulation"]

            if not request.form["arp_inspection"] and data['interfaces'][intf].get('arp_inspection'):
                del data['interfaces'][intf]['arp_inspection']
            elif request.form["arp_inspection"]:
                data['interfaces'][intf]['arp_inspection'] = request.form["arp_inspection"]

            if not request.form["dhcp_snooping"] and data['interfaces'][intf].get('dhcp_snooping'):
                del data['interfaces'][intf]['dhcp_snooping']
            elif request.form["dhcp_snooping"]:
                data['interfaces'][intf]['dhcp_snooping'] = request.form["dhcp_snooping"]

            if not request.form["load_interval"] and data['interfaces'][intf].get('load_interval'):
                del data['interfaces'][intf]['load_interval']
            elif request.form["load_interval"]:
                data['interfaces'][intf]['load_interval'] = request.form["load_interval"]

            if not request.form["portfast"] and data['interfaces'][intf].get('portfast'):
                del data['interfaces'][intf]['portfast']
            elif request.form["portfast"]:
                data['interfaces'][intf]['portfast'] = request.form["portfast"]

            if not request.form["bpdufilter"] and data['interfaces'][intf].get('bpdufilter'):
                del data['interfaces'][intf]['bpdufilter']
            elif request.form["bpdufilter"]:
                data['interfaces'][intf]['bpdufilter'] = request.form["bpdufilter"]

            if not request.form["channel_group"] and data['interfaces'][intf].get('channel_group'):
                del data['interfaces'][intf]['channel_group']
            elif request.form["channel_group"]:
                data['interfaces'][intf]['channel_group'] = request.form["channel_group"]

        elif "Vlan" in intf:

            if not request.form["status"] and data['interfaces'][intf].get('status'):
                del data['interfaces'][intf]['status']
            elif request.form["status"]:
                data['interfaces'][intf]['status'] = request.form["status"]

            if not request.form["ip"] and data['interfaces'][intf].get('ip'):
                del data['interfaces'][intf]['ip']
            elif request.form["ip"]:
                data['interfaces'][intf]['ip'] = request.form["ip"]

            if not data_dict["descr"] and data['interfaces'][intf].get('description'):
                del data['interfaces'][intf]['description']
            elif data_dict["descr"]:
                data['interfaces'][intf]['description'] = data_dict["descr"]

    return data

if __name__ == '__main__':
    app.run(debug=True)