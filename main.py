from flask import Flask, render_template, url_for, request, redirect
import yaml, subprocess
from os import listdir, environ
from os.path import isfile, join

app = Flask(__name__)

@app.route('/')
def index():
    onlyfiles = [f for f in listdir('sw_vars/data_v2') if isfile(join('sw_vars/data_v2', f))]
    return render_template('index.html', onlyfiles=onlyfiles)


@app.route('/errors/')
def errors():
    onlyfiles = [f for f in listdir('sw_vars/errors') if isfile(join('sw_vars/errors', f))]
    return render_template('errors.html', onlyfiles=onlyfiles)

@app.route("/errors/<string:file>")
def errors_file(file):
    ip,hostname = ip_host(file)
    with open('sw_vars/errors/'+file, 'r', encoding="utf-8") as f:
        data = f.read().split('\n')
        # yaml.full_load(f)
    return render_template('errors_file.html', file=file, data=data, ip=ip, hostname=hostname)

@app.route('/conf/')
def conf():
    onlyfiles = [f for f in listdir('sw_vars/conf_v3') if isfile(join('sw_vars/conf_v3', f))]
    return render_template('conf.html', onlyfiles=onlyfiles)

def ip_host(file):
    hostname = '_'.join(file.split('_')[1:-1])
    ip = file.split('_')[0]
    return ip,hostname

@app.route("/conf/<string:file>")
def conf_file(file):
    ip,hostname = ip_host(file)
    with open('sw_vars/conf_v3/'+file, 'r', encoding="utf-8") as f:
        data = f.read().split('\n')
    return render_template('conf_file.html', file=file, data=data, ip=ip, hostname=hostname)

@app.route('/data/<string:file>', methods=['POST', 'GET'])
def data_table(file):
    ip,hostname = ip_host(file)
    with open('sw_vars/data_v2/'+file, 'r') as f:
        data = yaml.safe_load(f)
    if request.method == "GET":
        return render_template('data_table.html', data=data, file=file, ip=ip, hostname=hostname)
    # elif request.method == 'POST':
    #     # data_dict = request.form.to_dict()
    #     hostname = '_'.join(file.split('_')[1:-1])
    #     command = [
    #         'docker', 'run', '--rm', '-v', f'{environ["PWD"]}/sw_vars:/home/user/sw_vars',
    #         'ansible-docker', 'ansible-playbook', '7-change_vlan_to_access_or_trunk_v2.yml', '-e', f'ip={hostname}',
    #         '-e', 'usr=username', '-e', 'pwd=password', '-i', 'inventory.yml'
    #     ]
    #     result = subprocess.run(command, stdout=subprocess.PIPE, encoding='utf-8')
    #     if result.returncode == 0:
    #         with open('sw_vars/data_v2/' + file, 'r') as f:
    #             new_data = yaml.safe_load(f)
    #         return render_template('conf_file.html', file=file, data=new_data)
    #     else:
    #         return f'Error, file {file}' + result.stdout

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
    with open('sw_vars/data_v2/'+file, 'r') as f:
        data = yaml.safe_load(f)
    if request.method == "GET":
        return render_template('data.html', data=data['interfaces'], file=file, interface=interface)
    elif request.method == "POST":
        data_dict = request.form.to_dict()
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
        with open('sw_vars/data_v2/' + file, 'w') as f:
            s = yaml.dump(data).replace('null', '').replace("'", "")
            f.write(s)

    return redirect("/data/" + file, code=302)

if __name__ == '__main__':
    app.run(debug=True)