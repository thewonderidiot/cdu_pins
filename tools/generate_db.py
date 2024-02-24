import csv
import glob
import sqlite3
import argparse

def expand_net(net, axis, vehicle):
    if net in ('_CHASS',):
        return net

    if axis in ['IG', 'MG', 'OG']:
        group = 'ISS'
        vgroup = 'U'
        r1group = 'U'
    elif axis == 'TRUN':
        group = 'TRN'
        vgroup = 'O'
        r1group = 'T' if vehicle != 'LEM' else 'S'
    else:
        group = 'SH'
        vgroup = 'O'
        r1group = 'S'

    if '___' in net:
        return net.replace('___', group)

    axis_letters = {
        'IG': 'A',
        'MG': 'B',
        'OG': 'C',
        'SHFT': 'D',
        'TRUN': 'E',
    }

    if '_' in net:
        if '+28V' in net or 'INHRC' in net or '28RF' in net:
            return net.replace('_', vgroup)
        elif 'REF1' in net:
            return net.replace('_', r1group)
        elif 'P+HI' in net or 'P-HI' in net:
            return net.replace('_', axis[0])
        else:
            return net.replace('_', axis_letters[axis])

    return net


def decode(nets, ios, descs, vehicle, axis):
    netlist = [n.strip() for n in nets.split('|')]
    iolist = [i.strip() for i in ios.split('|')]
    desclist = [d.strip() for d in descs.split('|')]

    if len(iolist) == 1:
        return expand_net(nets, axis, vehicle), ios, descs

    all_ios = []
    io_groups = []
    for io in iolist:
        io_str = io[io.find('(')+1:io.find(')')]
        ios = io_str.split('/')
        io_groups.append(ios)
        all_ios.extend(ios)

    if axis in ['IG', 'MG', 'OG']:
        group = 'IMU'
    elif vehicle == 'LEM':
        group = 'RR'
    else:
        group = 'OPTX'

    for i,ios in enumerate(io_groups):
        if vehicle in ios or group in ios or (axis in ios and group not in all_ios) or ((vehicle+'+'+group) in ios):
            if len(netlist) == 1:
                net = netlist[0]
            else:
                net = netlist[i]

            if len(desclist) == 1:
                desc = desclist[0]
            else:
                desc = desclist[i]

            net = expand_net(net, axis, vehicle)
            io = iolist[i].split(' ')[0]
            return (net, io, desc)

    return ''

def generate_db(vehicle):
    db = sqlite3.connect('cdu_' + vehicle.lower() + '.db')
    c = db.cursor()

    c.execute('CREATE TABLE IOTYPES(IOTYPE TEXT NOT NULL PRIMARY KEY)')
    c.execute('CREATE TABLE NETS(NET TEXT NOT NULL PRIMARY KEY, DESCRIPTION TEXT NOT NULL)')
    c.execute('CREATE TABLE CONNECTORS(CONNECTOR TEXT NOT NULL PRIMARY KEY, NAME TEXT NOT NULL, PINS INTEGER, DESCRIPTION TEXT NOT NULL)')
    c.execute('CREATE TABLE PINS(CONNECTOR TEXT NOT NULL REFERENCES CONNECTORS(CONNECTOR), PIN INTEGER NOT NULL, IOTYPE TEXT NOT NULL REFERENCES IOTYPES(IOTYPE), NET TEXT REFERENCES NETS(NET), DESCRIPTION TEXT, PRIMARY KEY (CONNECTOR, PIN))')
    c.execute('CREATE INDEX PIN_NETS ON PINS(NET)')

    c.execute('INSERT INTO IOTYPES VALUES ("IN")')
    c.execute('INSERT INTO IOTYPES VALUES ("OUT")')
    c.execute('INSERT INTO IOTYPES VALUES ("NC")')
    c.execute('INSERT INTO IOTYPES VALUES ("SPARE")')

    c.execute('INSERT INTO CONNECTORS VALUES ("X01", "MODE", 142, "")')
    c.execute('INSERT INTO CONNECTORS VALUES ("X02", "DIGITAL MODE", 142, "")')
    c.execute('INSERT INTO CONNECTORS VALUES ("X03", "INTERROGATE", 142, "")')
    c.execute('INSERT INTO CONNECTORS VALUES ("X04", "POWER SUPPLY", 124, "")')
    c.execute('INSERT INTO CONNECTORS VALUES ("X05", "D/A CONVERTER", 142, "")')
    c.execute('INSERT INTO CONNECTORS VALUES ("X06", "ERROR ANGLE COUNTER & LOGIC", 142, "")')
    c.execute('INSERT INTO CONNECTORS VALUES ("X07", "COARSE SYSTEM", 142, "")')
    c.execute('INSERT INTO CONNECTORS VALUES ("X08", "READ COUNTER", 142, "")')
    c.execute('INSERT INTO CONNECTORS VALUES ("X09", "MSA & QUADRATURE REJECTION", 142, "")')
    c.execute('INSERT INTO CONNECTORS VALUES ("X10", "QUADRANT SELECTOR", 142, "")')
    c.execute('INSERT INTO CONNECTORS VALUES ("X11", "D/A CONVERTER", 142, "")')
    c.execute('INSERT INTO CONNECTORS VALUES ("X12", "ERROR ANGLE COUNTER & LOGIC", 142, "")')
    c.execute('INSERT INTO CONNECTORS VALUES ("X13", "COARSE SYSTEM", 142, "")')
    c.execute('INSERT INTO CONNECTORS VALUES ("X14", "READ COUNTER", 142, "")')
    c.execute('INSERT INTO CONNECTORS VALUES ("X15", "MSA & QUADRATURE REJECTION", 142, "")')
    c.execute('INSERT INTO CONNECTORS VALUES ("X16", "QUADRANT SELECTOR", 142, "")')
    c.execute('INSERT INTO CONNECTORS VALUES ("X51", "INTERTRAY CONNECTOR", 213, "")')
    c.execute('INSERT INTO CONNECTORS VALUES ("X52", "TEST CONNECTOR", 36, "")')
    c.execute('INSERT INTO CONNECTORS VALUES ("X53", "MAIN CONNECTOR", 300, "")')
    c.execute('INSERT INTO CONNECTORS VALUES ("S01", "D/A CONVERTER", 142, "")')
    c.execute('INSERT INTO CONNECTORS VALUES ("S02", "ERROR ANGLE COUNTER & LOGIC", 142, "")')
    c.execute('INSERT INTO CONNECTORS VALUES ("S03", "COARSE SYSTEM", 142, "")')
    c.execute('INSERT INTO CONNECTORS VALUES ("S04", "READ COUNTER", 142, "")')
    c.execute('INSERT INTO CONNECTORS VALUES ("S05", "MSA & QUADRATURE REJECTION", 142, "")')
    c.execute('INSERT INTO CONNECTORS VALUES ("S06", "QUADRANT SELECTOR", 142, "")')
    c.execute('INSERT INTO CONNECTORS VALUES ("S07", "D/A CONVERTER", 142, "")')
    c.execute('INSERT INTO CONNECTORS VALUES ("S08", "ERROR ANGLE COUNTER & LOGIC", 142, "")')
    c.execute('INSERT INTO CONNECTORS VALUES ("S09", "COARSE SYSTEM", 142, "")')
    c.execute('INSERT INTO CONNECTORS VALUES ("S10", "READ COUNTER", 142, "")')
    c.execute('INSERT INTO CONNECTORS VALUES ("S11", "MSA & QUADRATURE REJECTION", 142, "")')
    c.execute('INSERT INTO CONNECTORS VALUES ("S12", "QUADRANT SELECTOR", 142, "")')
    c.execute('INSERT INTO CONNECTORS VALUES ("S13", "D/A CONVERTER", 142, "")')
    c.execute('INSERT INTO CONNECTORS VALUES ("S14", "ERROR ANGLE COUNTER & LOGIC", 142, "")')
    c.execute('INSERT INTO CONNECTORS VALUES ("S15", "COARSE SYSTEM", 142, "")')
    c.execute('INSERT INTO CONNECTORS VALUES ("S16", "READ COUNTER", 142, "")')
    c.execute('INSERT INTO CONNECTORS VALUES ("S17", "MSA & QUADRATURE REJECTION", 142, "")')
    c.execute('INSERT INTO CONNECTORS VALUES ("S18", "QUADRANT SELECTOR", 142, "")')
    c.execute('INSERT INTO CONNECTORS VALUES ("S51", "INTERTRAY CONNECTOR", 213, "")')

    tsvs = sorted(glob.glob('*.tsv'))
    for tsv in tsvs:
        module_num = int(tsv[1:3])

        with open(tsv, 'r') as f:
            rd = csv.reader(f, delimiter='\t')
            data = list(rd)
        module_pins = []
        rows = len(data[0]) // 4
        for row in range(rows):
            for col in data:
                pin_info = col[row*4:(row+1)*4]
                module_pins.append(pin_info)

        modules = []
        if module_num >= 5 and module_num <= 10:
            module_offset = module_num  - 4
            modules.append(('X%02u' % (module_num), 'SHFT'))
            modules.append(('X%02u' % (module_num+6), 'TRUN'))
            modules.append(('S%02u' % (module_offset), 'OG'))
            modules.append(('S%02u' % (module_offset+6), 'MG'))
            modules.append(('S%02u' % (module_offset+12), 'IG'))
        else:
            modules.append(('X%02u' % (module_num), '-'))

        for module, axis in modules:
            for pin in module_pins:
                if not pin[0]:
                    continue
                net, io, desc = decode(pin[1], pin[2], pin[3], vehicle, axis)
                io = io.upper()
                if net and not c.execute('SELECT NET FROM NETS WHERE NET=?', (net,)).fetchone():
                    c.execute('INSERT INTO NETS VALUES (?, "")', (net,))
                if io not in ['SPARE', 'IN', 'OUT', 'NC', 'BP']:
                    raise RuntimeError(io)

                c.execute('INSERT INTO PINS VALUES (?, ?, ?, ?, ?)', (module, pin[0], io, net, desc))
                if module == 'X51':
                    if io == 'IN':
                        s51_io = 'OUT'
                    elif io == 'OUT':
                        s51_io = 'IN'
                    else:
                        s51_io = io
                    c.execute('INSERT INTO PINS VALUES ("S51", ?, ?, ?, ?)', (pin[0], s51_io, net, desc))

    db.commit()
    db.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CDU Backplane DB Generator')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-l', '--lem', action='store_true', help='Generate for LEM')
    group.add_argument('-c', '--csm', action='store_true', help='Generate for CSM')
    args = parser.parse_args()

    vehicle = 'LEM' if args.lem else 'CSM'
    generate_db(vehicle)
