import sqlite3
import json
import sys

def dump_list(nets, category):
    print('-----------------------------')
    print('%s (%u)' % (category, len(nets)))
    print('-----------------------------')
    for net in nets:
        print(net['net'][0])
        for pin in net['pins']:
            print('    %s-%u (%s)' % pin)

def check_connections(dbf):
    db = sqlite3.connect(dbf)
    c = db.cursor()

    connected_ncs = []
    connected_spares = []
    double_outs = []
    no_outs = []
    no_ins = []

    nets = c.execute('SELECT NET FROM NETS').fetchall()
    for tray in 'XS':
        for net in nets:
            pin_infos = c.execute('SELECT CONNECTOR, PIN, IOTYPE FROM PINS WHERE NET=? AND CONNECTOR LIKE ?', (net[0], tray+'%')).fetchall()
            if len(pin_infos) == 0:
                continue

            conns = [p[0] for p in pin_infos]
            pins = [p[1] for p in pin_infos]
            ios = [p[2] for p in pin_infos]

            if 'NC' in ios and any([io != 'NC' for io in ios]):
                connected_ncs.append({
                    'net': net,
                    'pins': tuple(zip(conns, pins, ios))
                })

            if 'SPARE' in ios:
                connected_spares.append({
                    'net': net,
                    'pins': tuple(zip(conns, pins, ios))
                })

            if 'NC' in ios or 'SPARE' in ios:
                continue

            if ios.count('OUT') > 1 and (net[0] not in ['+4VHI', '+4VLO', 'K+28VH', 'U+28VH', 'CARPSA',
                                                        'ALCECL', 'BLCECL', 'CLCECL', 'DLCECL', 'ELCECL']):
                double_outs.append({
                    'net': net,
                    'pins': tuple(zip(conns, pins, ios))
                })

            if 'OUT' not in ios and ('TEMPH' not in net[0] and 'TEMPL' not in net[0]):
                no_outs.append({
                    'net': net,
                    'pins': tuple(zip(conns, pins, ios))
                })

            if 'IN' not in ios:
                no_ins.append({
                    'net': net,
                    'pins': tuple(zip(conns, pins, ios))
                })

    db.close()

    dump_list(connected_ncs, 'Connected NCs')
    dump_list(connected_spares, 'Connected Spares')
    dump_list(double_outs, 'Multiple Outputs')
    dump_list(no_outs, 'No Outputs')
    dump_list(no_ins, 'No Inputs')

if __name__ == '__main__':
    check_connections(sys.argv[1])

