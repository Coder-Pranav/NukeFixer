from __future__ import division

import sys
import time

import nuke

sys.stdout.write((str(sys.argv[1])))


def flush_then_wait():
    sys.stdout.flush()
    sys.stderr.flush()
    time.sleep(0.1)


nuke.scriptOpen(sys.argv[1])
node = [nod for nod in nuke.allNodes() if not nod.Class() == 'Viewer'
        and not nod.Class() == 'BackdropNode']
total_nodes = len(node)

for index, item in enumerate(node):
    try:
        progress = int(((index + 1) / total_nodes) * 100)
        item['disable'].setValue(True)
        sys.stdout.write('Disabled: ' + (item['name'].value() + '\n'))
        sys.stderr.write("Total complete: {}%\n".format(progress))
        flush_then_wait()
    except:
        pass
new_workfile_name = nuke.root().name().split('.')[0] + '_disabled' + '.nk'
nuke.scriptSaveAs(new_workfile_name, overwrite=1)
sys.stdout.write(('File Saved: ' + new_workfile_name))
