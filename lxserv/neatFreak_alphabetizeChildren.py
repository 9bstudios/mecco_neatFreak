#python

import lx, lxu, modo, traceback

NAME_CMD = 'neatFreak.alphabetizeChildren'

class CMD_neatFreak(lxu.command.BasicCommand):

    _first_run = True

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def basic_Execute(self, msg, flags):
        try:
            for item in modo.Scene().selected:
                for child in sorted(item.children(), key=lambda x: x.name, reverse = True):
                    child.setParent(child.parent, 0)

        except:
            traceback.print_exc()

lx.bless(CMD_neatFreak, NAME_CMD)
