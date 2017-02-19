#python

import lx, lxu, modo, traceback, re

NAME_CMD = 'neatFreak.findAndReplace'

# Replace all leftmost occurrences of 'search' by 'replace'. Function is case sensitive
def replaceStringCase(string, search, replace):
    return string.replace(search, replace)

# Replace all leftmost occurrences of regexp pattern 'search' by 'replace'. Function is case sensitive
def replaceRegexpCase(string, search, replace):
    pattern = re.compile(search)
    return pattern.sub(replace, string)

# Replace all leftmost occurrences of 'search' by 'replace'. Function ignores case
def replaceStringIgnoreCase(string, search, replace):
    # There is no standard Python function for this. Have to implement it.
    idx = 0
    while idx < len(string):
        pos = string.lower().find(search.lower(), idx)
        if pos == -1:
            break
        string = string[:pos] + replace + string[pos + len(search):]
  	idx = pos + len(replace)
    return string

# Replace all leftmost occurrences of regexp pattern 'search' by 'replace'. Function ignores case
def replaceRegexpIgnoreCase(string, search, replace):
    pattern = re.compile(search, re.IGNORECASE)
    return pattern.sub(replace, string)

class CMD_neatFreak(lxu.command.BasicCommand):

    _first_run = True

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add ('fr_search', lx.symbol.sTYPE_STRING)
        self.dyna_Add ('fr_replace', lx.symbol.sTYPE_STRING)
        self.dyna_Add('fr_ignore_case', lx.symbol.sTYPE_BOOLEAN)
        self.dyna_Add('fr_regexp', lx.symbol.sTYPE_BOOLEAN)

    def cmd_Flags(self):
        return lx.symbol.fCMD_POSTCMD | lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def arg_UIHints(self, index, hints):
        if index == 0:
            hints.Label("Search")
        elif index == 1:
            hints.Label("Replace")
        elif index == 2:
            hints.Label("Ignore case")
        elif index == 3:
            hints.Label("Use regexp")
        

    def cmd_DialogInit(self):
        if self._first_run:
            self.attr_SetInt(0, 1)
            self.attr_SetInt(1, 1)
            self.attr_SetInt(2, 1)
            self.attr_SetInt(3, 1)
            self.after_first_run()

    @classmethod
    def after_first_run(cls):
        cls._first_run = False

    def basic_Execute(self, msg, flags):
        try:
            search_string = self.dyna_String(0)
            replace_string = self.dyna_String(1)
            ignore_case = True if self.dyna_String(2) == 'true' else False
            use_regexp = True if self.dyna_String(3) == 'true' else False

            # Building replace function based of ignore_case and use_regexp flags
            if ignore_case:
                if use_regexp:
                    replace = replaceRegexpIgnoreCase
                else:
                    replace = replaceStringIgnoreCase
            else:
                if use_regexp:
                    replace = replaceRegexpCase
                else:
                    replace = replaceStringCase

            # Replacing search_string in item names by replace_string.
            scene = modo.Scene()
            for item in scene.iterItems():
                newName = replace(item.name, search_string, replace_string)
                # Assigning if name really changed. (Assuming name change will result GUI updates)
                if newName != item.name:
                    item.name = newName
        except:
            traceback.print_exc()


lx.bless(CMD_neatFreak, NAME_CMD)
