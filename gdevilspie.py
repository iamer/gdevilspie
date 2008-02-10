#!/usr/bin/python
#
# gdevilspie.py
# Copyright (C) Islam Amer 2008 <iamer@open-craft.com>
# 
# gdevilspie.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# gdevilspie.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

try:
    import os
    import gobject
    import pygtk
    pygtk.require('2.0')
    import gtk
    import gtk.glade
except:
    print "pyGTK is not correctly installed, exiting."
    quit()

match_criteria=["window_name", "window_role", "window_class", "window_xid", "application_name", "window_property", "window_workspace"]

actions=["geometry", "fullscreen", "focus", "center", "maximize", "maximize_vertically", "maximize_horizontally", "unmaximize", "minimize", "unminimize", "shade", "unshade", "close", "pin", "unpin", "stick", "unstick", "set_workspace", "set_viewport", "skip_pager", "skip_tasklist", "above", "below", "decorate", "undecorate", "wintype", "opacity", "spawn_async", "spawn_sync"]

actions_dict={"geometry" : None,
"fullscreen" : None,
"focus": None,
"center": None,
"maximize": None,
"maximize_vertically": None,
"maximize_horizontally": None,
"unmaximize": None,
"minimize": None,
"unminimize": None,
"shade": None,
"unshade": None,
"close": None,
"pin": None,
"unpin": None,
"stick": None,
"unstick": None,
"set_workspace": None,
"set_viewport": None,
"skip_pager": None,
"skip_tasklist": None,
"above": None,
"below": None,
"decorate": None,
"undecorate": None,
"wintype": None,
"opacity": None,
"spawn_async": None,
"spawn_sync": None}

class gdevilspie:
  def __init__(self):
    self.gladefile="gdevilspie.glade"
    try:
        self.wTreeList = gtk.glade.XML (self.gladefile, "RulesList")
    except:
        gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, "Glade file not found, exiting.").run()
        quit()
    
    self.wTreeEdit = gtk.glade.XML (self.gladefile, "RuleEdit")

    self.RulesList = self.wTreeList.get_widget("RulesList")
    self.RuleEdit = self.wTreeEdit.get_widget("RuleEdit")
    self.RulesTree = self.wTreeList.get_widget("RulesTree")
    self.MatchTree = self.wTreeEdit.get_widget("MatchTree")
    self.ActionsTree = self.wTreeEdit.get_widget("ActionsTreeList")
    self.MatchPropertyParameters_notebook = self.wTreeEdit.get_widget("MatchOptions_NoteBook1")
    self.ActionsParameters_notebook = self.wTreeEdit.get_widget("ActionsParameters_notebook")
    self.RuleName_entry = self.wTreeEdit.get_widget("RuleName_entry")
    
    self.wTreeList.signal_autoconnect (self)
    self.wTreeEdit.signal_autoconnect (self)

    self.rules_list_store = gtk.ListStore(str)
    self.match_list_store = gtk.ListStore(bool, str)
    self.actions_list_store = gtk.ListStore(bool,str)
    
    self.RulesTree.set_model(self.rules_list_store)
    self.MatchTree.set_model(self.match_list_store)
    self.ActionsTree.set_model(self.actions_list_store)

    self.RulesFilesNames=gtk.TreeViewColumn('Rule Name')
    self.RulesTree.append_column(self.RulesFilesNames)
    self.RuleFileName=gtk.CellRendererText()
    self.RulesFilesNames.pack_start(self.RuleFileName,expand=True)
    self.RulesFilesNames.add_attribute(self.RuleFileName, 'text', 0)
    
    self.ActionsNames_column=gtk.TreeViewColumn('Action')
    self.ActionsEnable_column=gtk.TreeViewColumn('')
    self.ActionsTree.append_column(self.ActionsEnable_column)
    self.ActionsTree.append_column(self.ActionsNames_column)
    self.ActionsNames_cell=gtk.CellRendererText()
    self.ActionsEnable_cell=gtk.CellRendererToggle()
    self.ActionsEnable_cell.set_property("activatable", 1)
    
    self.ActionsEnable_column.pack_start(self.ActionsEnable_cell, expand=True)
    self.ActionsNames_column.pack_start(self.ActionsNames_cell, expand=True)
    
    self.ActionsNames_column.add_attribute(self.ActionsNames_cell, 'text', 1)
    self.ActionsEnable_column.add_attribute(self.ActionsEnable_cell, 'active', False)
    for Action in actions:
      self.actions_list_store.append([0, Action])
      actions_dict[Action] = gtk.Label(Action)
      self.ActionsParameters_notebook.insert_page(actions_dict[Action], None)
    
    self.ActionsEnable_cell.connect("toggled", self.ActionsEnable_toggle)
    self.ActionsTree.connect("cursor-changed", self.Actions_selected)
    
    self.MatchPropertyNames_column=gtk.TreeViewColumn('Property')
    self.MatchPropertyEnable_column=gtk.TreeViewColumn('')
    self.MatchTree.append_column(self.MatchPropertyEnable_column)
    self.MatchTree.append_column(self.MatchPropertyNames_column)
    self.MatchPropertyName_cell=gtk.CellRendererText()
    self.MatchPropertyEnable_cell=gtk.CellRendererToggle()
    self.MatchPropertyEnable_cell.set_property("activatable", 1)
    
    self.MatchPropertyEnable_column.pack_start(self.MatchPropertyEnable_cell, expand=True)
    self.MatchPropertyNames_column.pack_start(self.MatchPropertyName_cell, expand=True)

    self.MatchPropertyEnable_column.add_attribute(self.MatchPropertyEnable_cell, 'active', False)
    self.MatchPropertyNames_column.add_attribute(self.MatchPropertyName_cell, 'text', 1)
    for MatchProperty in match_criteria:
        self.match_list_store.append([0, MatchProperty])
    
    self.MatchPropertyEnable_cell.connect("toggled", self.MatchPropertyEnable_toggle)
    self.MatchTree.connect("cursor-changed", self.MatchPropertyRow_selected)
    
    self.RulesList.show_all()  
  
  def Actions_selected(self, widget):
    selected_row = self.ActionsTree.get_selection()
    (model, iter) = selected_row.get_selected()
    if (iter != None):
      path = model.get_string_from_iter(iter)
      self.ActionsParameters_notebook.set_current_page(int(path))
    
  def ActionsEnable_toggle(self, widget, path):
    iter = self.actions_list_store.get_iter_from_string(path)
    CurrentState = self.actions_list_store.get_value(iter, 0)
    self.actions_list_store.set_value(iter, 0 , not CurrentState)
  
  def MatchPropertyRow_selected(self, widget):
    selected_row = self.MatchTree.get_selection()
    (model, iter) = selected_row.get_selected()
    if (iter != None):
      path = model.get_string_from_iter(iter)
    self.MatchPropertyParameters_notebook.set_current_page(int(path))
  
  def MatchPropertyEnable_toggle(self, widget, path):
    iter = self.match_list_store.get_iter_from_string(path)
    CurrentState = self.match_list_store.get_value(iter, 0)
    self.match_list_store.set_value(iter, 0 , not CurrentState )
    
  def on_RulesList_destroy(self,widget):
    gtk.main_quit()

  def on_Quit_clicked(self, widget):
    gtk.main_quit()

  def on_AddRule_clicked(self,widget):
    self.RuleEdit.show_all()

  def on_RuleEdit_destroy(self,widget):
    self.RuleEdit.hide()

  def on_Cancel_clicked(self,widget):
    self.RuleEdit.hide()
    
  def on_Save_clicked(self,widget):
   str = self.RuleName_entry.get_text()
   self.Save_Rule(str)
   self.RuleEdit.hide()

  def Save_Rule(self, str):
    #do stuff to generate the rule.
    path = os.path.expanduser("~/.devilspie/")
    new_Rule_file_name = path + str + ".ds"
    f = open( new_Rule_file_name, 'w' )
    f.write( "# " + str )
    f.close()
    self.update_rules_list()

  def on_DeleteRule_clicked(self,widget):
   SelectedRow = self.RulesTree.get_selection()
   (model, iter) = SelectedRow.get_selected()
   if (iter != None):
     SelectedRule = self.rules_list_store.get(iter, 0)
     RuleFile = os.path.expanduser("~/.devilspie/") + SelectedRule[0] + '.ds'
     os.remove(RuleFile)
     self.rules_list_store.remove(iter)

  def update_rules_list(self):
    self.rules_list_store.clear()
    self.fill_rules_list()
    
  def fill_rules_list(self):
    rulefileslist = os.listdir(self.dir)
    for rulefile in rulefileslist:
      if (rulefile.endswith(".ds")):
        rulefile=gobject.filename_display_name(rulefile)
        rulefile=rulefile.replace(".ds","")
        self.rules_list_store.append([rulefile])

  def main(self):
    self.dir = os.path.expanduser("~/.devilspie")
    if (os.path.exists(self.dir)):
      if (os.path.isdir(self.dir)):
        self.fill_rules_list()
      else:
          print "~/.devilspie is a file, please remove it"
    else:
          os.makedirs(dir)
    
    
    gtk.main()

if __name__ == "__main__":
    prog=gdevilspie()
    prog.main()
