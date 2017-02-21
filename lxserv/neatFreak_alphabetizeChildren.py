#python

import lx, lxu, modo, traceback

NAME_CMD = 'neatFreak.alphabetizeChildren'

# Standard command implementation
class CMD_neatFreak(lxu.command.BasicCommand):

    _first_run = True

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_POSTCMD | lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def basic_Execute(self, msg, flags):
        try:
            # For each selected item sort children and move to new position
            for item in modo.Scene().selected:
                for child in sorted(item.children(), key=lambda x: x.name, reverse = True):
                    child.setParent(child.parent, 0)

        except:
            traceback.print_exc()

lx.bless(CMD_neatFreak, NAME_CMD)
