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

# Recursive generator to iterates over all nodes in sub tree
def iterTreeNodesOfRoot(node):
	yield node
	for child in node.children():
		for res in iterTreeNodesOfRoot(child):
			yield res
			
# Recursive generator to iterates over all sub trees rooted by elements of 'nodes'
def iterTreeNodes(nodes):
	for node in nodes:
		for res in iterTreeNodesOfRoot(node):
			yield res
		
# Standard command implementation
class CMD_neatFreak(lxu.command.BasicCommand):

    _first_run = True

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add ("search", lx.symbol.sTYPE_STRING)
        self.dyna_Add ("replace", lx.symbol.sTYPE_STRING)
        self.dyna_Add("ignoreCase", lx.symbol.sTYPE_BOOLEAN)
        self.dyna_Add("regexp", lx.symbol.sTYPE_BOOLEAN)
        self.dyna_Add("selected", lx.symbol.sTYPE_BOOLEAN)

    def cmd_Flags(self):
        return lx.symbol.fCMD_POSTCMD | lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_DialogInit(self):
        if self._first_run:
            # Assign default values at first run
            self.attr_SetString(0, "")
            self.attr_SetString(1, "")
            self.attr_SetInt(2, 0)
            self.attr_SetInt(3, 0)
            self.attr_SetInt(4, 0)
            self.after_first_run()

    @classmethod
    def after_first_run(cls):
        cls._first_run = False

    def basic_Execute(self, msg, flags):
        try:
            search_string = self.dyna_String(0)
            # If search string is empty throw warning and return
            if search_string == "":
                modo.dialogs.alert("Empty Search String", "Search string is empty", dtype='warning')
                return
            replace_string = self.dyna_String(1)
            ignore_case = self.dyna_Bool(2)
            use_regexp = self.dyna_Bool(3)
            in_selected = self.dyna_Bool(4)

            scene = modo.Scene()
            if in_selected and len(scene.selected) == 0:
                modo.dialogs.alert("No Selection", "No items selected", dtype='warning')
                return

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
            for item in (iterTreeNodes(scene.selected) if in_selected else scene.iterItems()):
                newName = replace(item.name, search_string, replace_string)
                # Assigning if name really changed. (Assuming name change will result GUI updates)
                if newName != item.name:
                    item.name = newName
        except:
            traceback.print_exc()


lx.bless(CMD_neatFreak, NAME_CMD)
