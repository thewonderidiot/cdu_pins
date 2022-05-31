from flask import render_template, g
import sqlite3
import json

from cdu_pins import app

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['delphi'])
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return render_template('pin_inspector.html')

@app.route('/pins/pin/<conn>/<int:pin>')
def get_pin_info(conn, pin):
    c = get_db().cursor()
    res = c.execute('SELECT IOTYPE, NET, DESCRIPTION FROM PINS WHERE CONNECTOR=? AND PIN=?', (conn, pin))
    try:
        iotype, net, desc = res.fetchone()
    except:
        return '???'

    pin_data = {}
    pin_data['net'] = {}
    pin_data['net']['name'] = net
    pin_data['net']['description'] = desc
    pin_data['iotype'] = iotype
    pin_data['connections'] = []

    if net is not None and iotype not in ["SPARE", "NC", "UNK"]:
        for net_conn, net_pin in c.execute('SELECT CONNECTOR, PIN FROM PINS WHERE NET=? AND NOT ((IOTYPE="NC") OR (CONNECTOR=? AND PIN=?))', (net, conn, pin)):
            pin_data['connections'].append({'connector': net_conn, 'pin': net_pin})

    return json.dumps(pin_data)

@app.route('/pins/pin_classes/<tray>')
def get_pin_classes(tray):
    c = get_db().cursor()

    pin_classes = {}
    pin_classes['pin_classes'] = []
    for conn, pin, net, iotype, desc in c.execute('SELECT CONNECTOR, PIN, NET, IOTYPE, DESCRIPTION FROM PINS WHERE CONNECTOR LIKE ?', (tray+'%',)):
        if iotype == 'UNK' or 'UNK' in desc:
            pin_class = "UNK"
        elif net in ['_CHASS', '+4VLO'] or net.endswith('SIGGR') or ("shield" in desc.lower()):
            pin_class = '+4VLO'
        elif iotype in ['NC', 'SPARE', 'BP']:
            pin_class = iotype
        elif net in ['+4VHI']:
            pin_class = net
        elif '+28' in net:
            pin_class = '+28V'
        else:
            pin_class = 'DATA'

        pin_classes['pin_classes'].append({'connector': conn, 'pin': pin, 'pin_class': pin_class, 'description': desc})

    return json.dumps(pin_classes)

@app.route('/pins/net/<path:net>')
def get_net_pins(net):
    c = get_db().cursor()

    net_data = {
        'description': '',
        'connections': [],
    }

    res = c.execute('SELECT DESCRIPTION FROM NETS WHERE NET=?', (net,)).fetchone()
    if res is not None:
        net_data['description'] = res[0]
        net_data['connections'] = []

        for net_conn, net_pin in c.execute('SELECT CONNECTOR, PIN FROM PINS WHERE NET=? AND NOT IOTYPE="SPARE"', (net,)):
            net_data['connections'].append({'connector': net_conn, 'pin': net_pin})

    return json.dumps(net_data)

