import wnck

#Get Default X screen
screen = wnck.screen_get_default()

#List of wnck.Window objects
def Get_Window_List():
    screen.force_update()
    return screen.get_windows()

#List of windowname strings
def Get_Windowname_List(windowlist):
    namelist = []
    for i in windowlist:
        namelist.append(i.get_name())

#this function takes a window object (choosen by the user) and returns its matching criteria
def Matchdict_Window(window):
    matchdict = {}
    matchdict["window_name"] = window.get_name()
    matchdict["window_role"] = window.get_window_type().value_nick
    matchdict["window_class"] = window.get_class_group().get_name()
    matchdict["window_xid"] = window.get_xid()
    matchdict["application_name"] = window.get_application().get_name()
    matchdict["window_property"] = "" #Is that even relevant? nobody uses it.
    if window.get_workspace() != None:
        matchdict["window_workspace"] = window.get_workspace().get_name()
    else:
        matchdict["window_workspace"] = ""
    return matchdict

def Actiondict_Window(window):
    actiondict = {}
    actiondict["geometry_x"] = window.get_geometry()[0]
    actiondict["geometry_y"] = window.get_geometry()[1]
    actiondict["geometry_w"] = window.get_geometry()[2]
    actiondict["geometry_h"] = window.get_geometry()[3]
    actiondict["fullscreen"] = window.is_fullscreen()
    actiondict["maximize"] = window.is_maximized()
    actiondict["maximize_horizontally"] = window.is_maximized_horizontally()
    actiondict["maximize_vertically"] = window.is_maximized_vertically()
    actiondict["minimize"] = window.is_minimized()
    actiondict["shade"] = window.is_shaded()
    actiondict["pin"] = window.is_pinned()
    actiondict["stick"] = window.is_sticky()
    if window.get_workspace() != None:
        actiondict["set_workspace"] = window.get_workspace().get_name()
    return actiondict

## Use this for testing
winlist = Get_Window_List()
def test():
    print Matchdict_Window(winlist[1])
    print Actiondict_Window(winlist[1])
test()