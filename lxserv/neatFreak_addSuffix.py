#python

import lx, lxu, modo, traceback

NAME_CMD = 'neatFreak.addSuffix'

class CMD_neatFreak(lxu.command.BasicCommand):

    _first_run = True

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add ("suffix", lx.symbol.sTYPE_STRING)

    def cmd_Flags(self):
        return lx.symbol.fCMD_POSTCMD | lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_DialogInit(self):
        if self._first_run:
            self.attr_SetString(0, "")
            self.after_first_run()

    @classmethod
    def after_first_run(cls):
        cls._first_run = False

    def basic_Execute(self, msg, flags):
        try:
            suffix = self.dyna_String(0)
            # If suffix string is empty throw warning and return
            if suffix == "":
                modo.dialogs.alert("Empty Suffix", "Suffix is empty", dtype='warning')
                return

            # Check if selection exists
            scene = modo.Scene()
            if len(scene.selected) == 0:
                modo.dialogs.alert("No Selection", "No items selected", dtype='warning')
                return

            # Add suffix to all selected items
            for item in scene.selected:
                item.name = item.name + suffix
        except:
            traceback.print_exc()


lx.bless(CMD_neatFreak, NAME_CMD)
