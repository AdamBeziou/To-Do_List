import wx

class mainWindow(wx.Frame):
	def __init__(self, parent):
		wx.Frame.__init__(self, parent, title = "To-Do List", size = (767, -1))
		
		#Creating the panel and setting the background color
		self.SetBackgroundColour(wx.Colour(229,204,255))
		self.panel = wx.Panel(self)
		
		#Creating the menu and status bar
		self.CreateStatusBar()
		
		menu = wx.Menu()
		
		clear_list = menu.Append(wx.ID_ANY, "Clear the List", "Clear the List of All Entries")
		self.Bind(wx.EVT_MENU, self.OnClearList, clear_list)
		
		self.menuBar = wx.MenuBar()
		self.menuBar.Append(menu, "Options")
		self.SetMenuBar(self.menuBar)
		
		#Creating the list of tasks
		self.tasks = wx.ListCtrl(self.panel, wx.ID_ANY, size = (767, 340), style = wx.LC_REPORT)
		self.tasks.InsertColumn(0, "Priority")
		self.tasks.InsertColumn(1, "Tasks", width = wx.LIST_AUTOSIZE_USEHEADER)
		
		self.list = open("Tasks.txt", 'r+').read().split('\n')
		for i in range(len(self.list)):
			self.tasks.InsertItem(i, str(i + 1))
			self.tasks.SetItem(i, 1, self.list[i])
		self.list_length = len(self.list)
		
		#Creating the bottom panel buttons
		self.AddNewEntry = wx.Button(self.panel, wx.ID_ANY, "Add a New Entry To The List", size = (250, 30))
		self.Bind(wx.EVT_BUTTON, self.OnNewEntry, self.AddNewEntry)
		
		self.DeleteEntry = wx.Button(self.panel, wx.ID_ANY, "Delete The Selected Entry From The List", size = (250, 30))
		self.Bind(wx.EVT_BUTTON, self.OnDeleteEntry, self.DeleteEntry)
		
		self.EditEntry = wx.Button(self.panel, wx.ID_ANY, "Edit The Selected Entry", size = (250, 30))
		self.Bind(wx.EVT_BUTTON, self.OnEditEntry, self.EditEntry)
		
		self.CompleteEntry = wx.Button(self.panel, wx.ID_ANY, "Complete The Selected Entry", size = (250, 30))
		self.Bind(wx.EVT_BUTTON, self.OnCompleteEntry, self.CompleteEntry)
		
		self.UpPriority = wx.Button(self.panel, wx.ID_ANY, "Move The Selected Entry Up", size = (250, 30))
		self.Bind(wx.EVT_BUTTON, self.OnMovePriorityUp, self.UpPriority)
		
		self.DownPriority = wx.Button(self.panel, wx.ID_ANY, "Move The Selected Entry Down", size = (250, 30))
		self.Bind(wx.EVT_BUTTON, self.OnMovePriorityDown, self.DownPriority)
		
		#Creating the title panel sizer, the list panel sizer, the bottom button panel sizer, and the master sizer
		self.ButtonPanelSizer = wx.GridBagSizer(hgap = 0, vgap = 0)
		self.ButtonPanelSizer.Add(self.AddNewEntry, pos = (0,0))
		self.ButtonPanelSizer.Add(self.DeleteEntry, pos = (1,0))
		self.ButtonPanelSizer.Add(self.EditEntry, pos = (0,1))
		self.ButtonPanelSizer.Add(self.CompleteEntry, pos = (1,1))
		self.ButtonPanelSizer.Add(self.UpPriority, pos = (0,2))
		self.ButtonPanelSizer.Add(self.DownPriority, pos = (1,2))
		
		self.MasterSizer = wx.BoxSizer(wx.VERTICAL)
		self.MasterSizer.Add(self.tasks, 1, wx.EXPAND, 0)
		self.MasterSizer.Add(wx.StaticLine(self.panel), 1, wx.ALL|wx.EXPAND, 0)
		self.MasterSizer.Add(self.ButtonPanelSizer, 1, wx.ALL, 0)
		
		self.MasterSizer.SetSizeHints(self.panel)
		self.panel.SetSizerAndFit(self.MasterSizer)
		
		self.Show(True)
		self.SetMinSize(self.GetSize())
	
	def OnClearList(self, event):
		pass
		
	def OnNewEntry(self, event):
		dlg = wx.TextEntryDialog(self.panel, "Enter A New Task:", "Enter A New Task:")
		dlg.ShowModal()
		task = dlg.GetValue()
		dlg.Destroy()
		self.tasks.InsertItem(self.list_length, str(self.list_length + 1))
		self.tasks.SetItem(self.list_length, 1, task)
		self.list_length += 1
		
	def OnEditEntry(self, event):
		pass
		
	def OnDeleteEntry(self, event):
		pass
		
	def OnCompleteEntry(self, event):
		pass
		
	def OnMovePriorityUp(self, event):
		pass
		
	def OnMovePriorityDown(self, event):
		pass

app = wx.App(False)
frame = mainWindow(None)
app.MainLoop()