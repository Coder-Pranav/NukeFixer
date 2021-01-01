import nuke
import sys

print('hi')
print(str(sys.argv[1]))

nuke.scriptOpen(sys.argv[1])
node = nuke.allNodes()
for i in node:
    try:
        i['disable'].setValue(True)
        print 'Disabled: ' + (i['name'].value())
    except:
        pass

new_workfile_name = nuke.root().name().split('.')[0] + '_disabled' + '.nk'
nuke.scriptSaveAs(new_workfile_name,overwrite=1)
print('File Saved: ' + new_workfile_name)
