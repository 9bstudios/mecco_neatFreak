#python

import lx, lxu, modo, traceback

NAME_CMD = 'neatFreak.superMeshCleanup'

class CMD_neatFreak(lxu.command.BasicCommand):

    _first_run = True

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add ("mTolerance", lx.symbol.sTYPE_DISTANCE)

    def cmd_Flags(self):
        return lx.symbol.fCMD_POSTCMD | lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_DialogInit(self):
        if self._first_run:
            self.attr_SetFlt(0, 1.0)
            self.after_first_run()

    @classmethod
    def after_first_run(cls):
        cls._first_run = False

    def basic_Execute(self, msg, flags):
        try:
            merging_tolerance = self.dyna_Float(0)

            lx.eval("select.polygon add type subdiv 1")
            lx.eval("poly.convert face subdiv false")
            lx.eval("select.polygon add type psubdiv 2")
            lx.eval("poly.convert face psubdiv false")

            for i in range(3):
                lx.eval("!!vert.merge fixed false %s false true" % merging_tolerance)
                lx.eval("!!mesh.cleanup true true true true true true true true true true")
                lx.eval("!!poly.align")

            lx.eval('vertMap.updateNormals')
        except:
            traceback.print_exc()


lx.bless(CMD_neatFreak, NAME_CMD)
