#!/usr/bin/python
#
# main.py
# Copyright (C) Islam Amer 2008 <iamer@open-craft.com>
# 
# main.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# main.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade

class gdevilspie:
  def __init__(self):
    print "Welcome"
    self.gladefile="gdevilspie.glade"
    
    self.wTreeList = gtk.glade.XML (self.gladefile, "RulesList")
    self.wTreeEdit = gtk.glade.XML (self.gladefile, "RuleEdit")

    self.RulesList = self.wTreeList.get_widget("RulesList")
    self.RuleEdit = self.wTreeEdit.get_widget("RuleEdit")
    self.RulesTree = self.wTreeList.get_widget("RulesTree")

    self.wTreeList.signal_autoconnect (self)
    self.wTreeEdit.signal_autoconnect (self)

    self.rules_list_store = gtk.ListStore(str)
    self.RulesTree.set_model(self.rules_list_store)

    self.column1=gtk.TreeViewColumn('Rule Name')
    self.RulesTree.append_column(self.column1)
    self.cell=gtk.CellRendererText()
    self.column1.pack_start(self.cell,expand=True)

    self.column1.add_attribute(self.cell, 'text', 0)

    self.RulesList.show_all()

  def on_RulesList_destroy(self,widget):
    gtk.main_quit()

  def on_Quit_clicked(self, widget):
    gtk.main_quit()

  def on_AddRule_clicked(self,widget):
    self.RuleEdit.show()

  def on_RuleEdit_destroy(self,widget):
    self.RuleEdit.hide()

  def on_Cancel_clicked(self,widget):
    self.RuleEdit.hide()

  def on_Save_clicked(self,widget):
   self.RuleEdit.hide()

  def on_DeleteRule_clicked(self,widget):
   SelectedRow = self.RulesTree.get_selection()
   (model, iter) = SelectedRow.get_selected()
   if (iter != None):
     SelectedRule = self.rules_list_store.get(iter, 0)
     RuleFile = os.path.expanduser("~/.devilspie/") + SelectedRule[0] + '.ds'
     os.remove(RuleFile)
     self.rules_list_store.remove(iter)

  def main(self):
    dir = os.path.expanduser("~/.devilspie")
    if (os.path.exists(dir)):
      if (os.path.isdir(dir)):
	  rulefileslist = os.listdir(dir)
    	  for rulefile in rulefileslist:
	    if (rulefile.endswith(".ds")):
	      rulefile=rulefile.replace(".ds","")
	      self.rules_list_store.append([rulefile])
      else:
          print "~/.devilspie is a file, please remove it"
    else:
          os.makedirs(dir)
    
    
    gtk.main()

if __name__ == "__main__":
    prog=gdevilspie()
    prog.main()
