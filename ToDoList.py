import wx
import datetime

class mainWindow(wx.Frame):
	def __init__(self, parent):
		wx.Frame.__init__(self, parent, title = "To-Do List", size = (767, -1))
		
		#Creating the panel and setting the background color
		self.SetBackgroundColour(wx.Colour(229,204,255))
		self.panel = wx.Panel(self)
		
		#Creating the menu and status bar
		self.CreateStatusBar()
		
		menu = wx.Menu()
		
		save_list = menu.Append(wx.ID_ANY, "Save the List", "Save the Current List")
		self.Bind(wx.EVT_MENU, self.OnSaveList, save_list)
		
		clear_list = menu.Append(wx.ID_ANY, "Clear the List", "Clear the List of All Entries")
		self.Bind(wx.EVT_MENU, self.OnClearList, clear_list)
		
		self.menuBar = wx.MenuBar()
		self.menuBar.Append(menu, "Options")
		self.SetMenuBar(self.menuBar)
		
		#Creating the list of tasks
		self.tasks = wx.ListCtrl(self.panel, wx.ID_ANY, size = (767, 340), style = wx.LC_REPORT)
		self.tasks.InsertColumn(0, "Priority")
		self.tasks.InsertColumn(1, "Tasks", width = wx.LIST_AUTOSIZE_USEHEADER)
		
		try:
			self.list = open("Current_Tasks.txt", 'r+').read().split('\n')
			for i in range(len(self.list)):
				self.tasks.InsertItem(i, str(i + 1))
				self.tasks.SetItem(i, 1, self.list[i])
			self.list_length = len(self.list)
		except FileNotFoundError:
			place_list = open("Current_Tasks.txt", 'w+')
			place_list.write("Create, delete, and complete tasks with the buttons below")
			self.tasks.InsertItem(0, "1")
			self.tasks.SetItem(0, 1, "Create, delete, edit, and complete tasks with the buttons below.")
			self.list_length = 1
		
		#Creating the close event
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		
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
		for i in range(self.list_length):
			self.tasks.DeleteItem(0)
		
	def OnSaveList(self, event):
		list = open("Current_Tasks.txt", 'w')
		entries = []
		for i in range(0, self.list_length):
			entries.append(self.tasks.GetItemText(i, 1))
		list.write('\n'.join(entries))
		list.close()
		
	def OnNewEntry(self, event):
		dlg = wx.TextEntryDialog(self.panel, "Enter A New Task:", "Enter A New Task:")
		dlg.ShowModal()
		task = dlg.GetValue()
		dlg.Destroy()
		self.tasks.InsertItem(self.list_length, str(self.list_length + 1))
		self.tasks.SetItem(self.list_length, 1, task)
		self.list_length += 1
		
	def OnEditEntry(self, event):
		pos = self.tasks.GetFirstSelected()
		if pos == -1:
			dlg = wx.MessageDialog(self.panel, "Please select an item to edit.", "Error", style = wx.OK)
			dlg.ShowModal()
			dlg.Destroy()
		else:
			dlg = wx.TextEntryDialog(self.panel, "Enter the task:", "Editing Task", value = self.tasks.GetItemText(pos, 1), style = wx.OK|wx.CANCEL)
			choice = dlg.ShowModal()
			if choice == wx.ID_OK:
				self.tasks.SetItem(pos, 1, dlg.GetValue())
			else:
				pass
			dlg.Destroy()
		
	def OnDeleteEntry(self, event):
		pos = self.tasks.GetFirstSelected()
		if pos == -1:
			dlg = wx.MessageDialog(self.panel, "Please select an item to delete.", "Error", style = wx.OK)
			dlg.ShowModal()
			dlg.Destroy()
		else:
			dlg = wx.MessageDialog(self.panel, "Are you sure you want to delete the selected task?", "Confirmation", style = wx.OK|wx.CANCEL)
			choice = dlg.ShowModal()
			if choice == wx.ID_OK:
				self.tasks.DeleteItem(pos)
				self.list_length -= 1
				for i in range(pos, self.list_length):
					self.tasks.SetItem(i, 0, str(i+1))
			else:
				pass
			dlg.Destroy()
		
	def OnCompleteEntry(self, event):
		pos = self.tasks.GetFirstSelected()
		if pos == -1:
			dlg = wx.MessageDialog(self.panel, "Please select an item to delete.", "Error", style = wx.OK)
			dlg.ShowModal()
			dlg.Destroy()
		else:
			dlg = wx.MessageDialog(self.panel, "Are you sure you want to complete the selected task?", "Confirmation", style = wx.OK|wx.CANCEL)
			choice = dlg.ShowModal()
			if choice == wx.ID_OK:
				try:
					complete = open("Completed_Tasks.txt", "r+")
				except FileNotFoundError:
					complete = open("Completed_Tasks.txt", "w+")
					complete.write("Year-Day-Month Task")
				complete.write("\n" + str(datetime.date.today()) + " " + self.tasks.GetItemText(pos, 1))
				self.tasks.DeleteItem(pos)
				self.list_length -= 1
				for i in range(pos, self.list_length):
					self.tasks.SetItem(i, 0, str(i+1))
				list = open("Current_Tasks.txt", 'w')
				entries = []
				for i in range(0, self.list_length):
					entries.append(self.tasks.GetItemText(i, 1))
				list.write('\n'.join(entries))
				list.close()
			else:
				pass
			dlg.Destroy()
			
	def OnMovePriorityUp(self, event):
		pos = self.tasks.GetFirstSelected()
		if pos == -1:
			dlg = wx.MessageDialog(self.panel, "Please select an item to delete.", "Error", style = wx.OK)
			dlg.ShowModal()
			dlg.Destroy()
		elif pos == 0:
			dlg = wx.MessageDialog(self.panel, "Task is already at the top.", "Error", style = wx.OK)
			dlg.ShowModal()
			dlg.Destroy()
		else:
			task = self.tasks.GetItemText(pos, 1)
			self.tasks.SetItem(pos, 1, self.tasks.GetItemText(pos - 1, 1))
			self.tasks.SetItem(pos - 1, 1, task)

	def OnMovePriorityDown(self, event):
		pos = self.tasks.GetFirstSelected()
		if pos == -1:
			dlg = wx.MessageDialog(self.panel, "Please select an item to delete.", "Error", style = wx.OK)
			dlg.ShowModal()
			dlg.Destroy()
		elif pos == self.list_length - 1:
			dlg = wx.MessageDialog(self.panel, "Task is already at the bottom.", "Error", style = wx.OK)
			dlg.ShowModal()
			dlg.Destroy()
		else:
			task = self.tasks.GetItemText(pos, 1)
			self.tasks.SetItem(pos, 1, self.tasks.GetItemText(pos + 1, 1))
			self.tasks.SetItem(pos + 1, 1, task)
			
	def OnClose(self, event):
		dlg = wx.MessageDialog(self.panel, "Do you want to save the list?", "Confirmation", style = wx.OK|wx.CANCEL)
		choice = dlg.ShowModal()
		if choice == wx.ID_OK:
			list = open("Current_Tasks.txt", 'w')
			entries = []
			for i in range(0, self.list_length):
				entries.append(self.tasks.GetItemText(i, 1))
			list.write('\n'.join(entries))
			list.close()
		else:
			pass
		dlg.Destroy()
		self.Destroy()
		
app = wx.App(False)
frame = mainWindow(None)
app.MainLoop()
