import wx
import datetime

class MainWindow(wx.Frame):
	def __init__(self, parent):
		wx.Frame.__init__(self, parent, title = "To-Do List", size = (767, -1))
		
		#Creating the panel and setting the background color
		self.SetBackgroundColour(wx.Colour(229,204,255))
		self.panel = wx.Panel(self)
		
		#Creating the menu and status bar
		self.CreateStatusBar()
		
		self.options = wx.Menu()
		
		save_list = self.options.Append(wx.ID_ANY, "Save the List", "Save the Current List")
		self.Bind(wx.EVT_MENU, self.OnSaveList, save_list)
		
		repeating_tasks = self.options.Append(wx.ID_ANY, "Add, Remove, or Edit Repeating Tasks", "Add, Remove, or Edit Repeating Tasks")
		self.Bind(wx.EVT_MENU, self.OnRepeat, repeating_tasks)
		
		clear_list = self.options.Append(wx.ID_ANY, "Clear the List", "Clear the List of All Entries")
		self.Bind(wx.EVT_MENU, self.OnClearList, clear_list)
		
		self.menuBar = wx.MenuBar()
		self.menuBar.Append(self.options, "Options")
		self.SetMenuBar(self.menuBar)
		
		#Creating the list of tasks
		self.tasks = wx.ListCtrl(self.panel, wx.ID_ANY, size = (767, 340), style = wx.LC_REPORT)
		self.tasks.InsertColumn(0, "Priority")
		self.tasks.InsertColumn(1, "Tasks", width = wx.LIST_AUTOSIZE_USEHEADER)
		
		self.list_length = 0
		
		try:
			self.rep_list = open("Repeated_Tasks.txt", 'r+').read().split('\n')
			if self.rep_list[0] == ' ':
				pass
			else:
				for i in range(len(self.rep_list)):
					time_period_task = self.rep_list[i].split()
					if str(datetime.date.today()) == time_period_task[0]:
						self.tasks.InsertItem(i, str(i + 1))
						self.tasks.SetItem(i, 1, time_period_task[2])
						self.list_length += 1
		except FileNotFoundError:
			place_list = open("Repeating_Tasks.txt", "w+")
		
		try:
			self.list = open("Current_Tasks.txt", 'r+').read().split('\n')
			if self.list[0] == '':
				pass
			else:
				for i in range(len(self.list)):
					self.tasks.InsertItem(i, str(i + 1))
					self.tasks.SetItem(i, 1, self.list[i])
				self.list_length += len(self.list)
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
		self.MasterSizer.Add(wx.StaticLine(self.panel), 0, wx.ALL|wx.EXPAND, 0)
		self.MasterSizer.Add(self.ButtonPanelSizer, 1, wx.CENTER, 0)
		
		self.MasterSizer.SetSizeHints(self.panel)
		self.panel.SetSizerAndFit(self.MasterSizer)
		
		self.Show(True)
		self.SetMinSize(self.GetSize())
	
	def OnClearList(self, event):
		dlg = wx.MessageDialog(self.panel, "Are you sure you want to clear the list?", "Confirmation", style = wx.OK|wx.CANCEL)
		choice = dlg.ShowModal()
		if choice == wx.ID_OK:
			for i in range(self.list_length):
				self.tasks.DeleteItem(0)
		else:
			pass
		dlg.Destroy()
		
	def OnRepeat(self, event):
		Repeating()
		
	def OnSaveList(self, event):
		list = open("Current_Tasks.txt", 'w')
		entries = []
		for i in range(0, self.list_length):
			entries.append(self.tasks.GetItemText(i, 1))
		list.write('\n'.join(entries))
		list.close()
		
	def OnNewEntry(self, event):
		dlg = wx.TextEntryDialog(self.panel, "Enter A New Task:", "Enter A New Task:")
		choice = dlg.ShowModal()
		task = dlg.GetValue()
		
		if choice == wx.ID_OK:
			self.tasks.InsertItem(self.list_length, str(self.list_length + 1))
			self.tasks.SetItem(self.list_length, 1, task)
			self.list_length += 1
		else:
			pass
			
		dlg.Destroy()
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
			dlg = wx.MessageDialog(self.panel, "Please select an item to complete.", "Error", style = wx.OK)
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
				complete_list = complete.read().split('\n')
				complete_list.append("\n" + str(datetime.date.today()) + " " + self.tasks.GetItemText(pos, 1))
				
				test = open("Completed_Tasks.txt", "w").close()
				
				complete.write('\n'.join(complete_list))
				complete_list = []
				complete.close()
				
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
		
def Repeating():
	
	class RepeatingTasks(wx.Frame):
		def __init__(self):
			wx.Frame.__init__(self, None, title = "Repeating Tasks", size = (-1, -1))
		
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
			self.tasks = wx.ListCtrl(self.panel, wx.ID_ANY, size = (-1, -1), style = wx.LC_REPORT)
			self.tasks.InsertColumn(0, "Next Added to the List:")
			self.tasks.InsertColumn(1, "Period:")
			self.tasks.InsertColumn(2, "Task:", width = wx.LIST_AUTOSIZE_USEHEADER)
			
			try:
				self.list = open("Repeated_Tasks.txt", 'r+').read().split('\n')
				if self.list[0] == ' ':
					self.list_length = 0
				else:
					for i in range(len(self.list)):
						time_period_task = self.list[i].split()
						self.tasks.InsertItem(i, time_period_task[0])
						self.tasks.SetItem(i, 1, time_period_task[1])
						self.tasks.SetItem(i, 2, time_period_task[2])
					self.list_length = len(self.list)
			except FileNotFoundError:
				place_list = open("Repeating_Tasks.txt", "w+")
				self.list_length = 0
			
			
			#Creating the panel buttons
			self.AddNewEntry = wx.Button(self.panel, wx.ID_ANY, "Add a New Entry To The List", size = (250, 30))
			self.Bind(wx.EVT_BUTTON, self.OnNewEntry, self.AddNewEntry)
			
			self.DeleteEntry = wx.Button(self.panel, wx.ID_ANY, "Delete The Selected Entry From The List", size = (250, 30))
			self.Bind(wx.EVT_BUTTON, self.OnDeleteEntry, self.DeleteEntry)
			
			self.EditEntry = wx.Button(self.panel, wx.ID_ANY, "Edit The Selected Entry", size = (250, 30))
			self.Bind(wx.EVT_BUTTON, self.OnEditEntry, self.EditEntry)
			
			self.ExitSave = wx.Button(self.panel, wx.ID_ANY, "Exit and Save", size = (250, 30))
			self.Bind(wx.EVT_BUTTON, self.OnExitSave, self.ExitSave)
			
			self.Exit = wx.Button(self.panel, wx.ID_ANY, "Exit And Do Not Save", size = (250, 30))
			self.Bind(wx.EVT_BUTTON, self.OnExit, self.Exit)
			
			#Creating the master sizer
			self.MasterSizer = wx.BoxSizer(wx.VERTICAL)
			self.MasterSizer.Add(self.tasks, 1, wx.EXPAND, 0)
			self.MasterSizer.Add(wx.StaticLine(self.panel), 0, wx.EXPAND, 0)
			self.MasterSizer.Add(self.AddNewEntry, 1, wx.CENTER, 0)
			self.MasterSizer.Add(self.DeleteEntry, 1, wx.CENTER, 0)
			self.MasterSizer.Add(self.EditEntry, 1, wx.CENTER, 0)
			self.MasterSizer.Add(self.ExitSave, 1, wx.CENTER, 0)
			self.MasterSizer.Add(self.Exit, 1, wx.CENTER, 0)
			
			self.MasterSizer.SetSizeHints(self.panel)
			self.panel.SetSizerAndFit(self.MasterSizer)
			
			self.Show(True)
			self.SetMinSize(self.GetSize())
		
		def OnClearList(self, event):
			for i in range(self.list_length):
				self.tasks.DeleteItem(0)
			
		def OnExitSave(self, event):
			list = open("Repeating_Tasks.txt", 'w')
			entries = []
			for i in range(0, self.list_length):
				entries.append(self.tasks.GetItemText(i, 0) + ' ' + self.tasks.GetItemText(i, 1) + ' ' + self.tasks.GetItemText(i, 2))
			list.write('\n'.join(entries))
			list.close()
			
			self.Destroy()
			
		def OnExit(self, event):
			self.Destroy()
			
		def OnNewEntry(self, event):
			dlg = NewEntry('', '')
			choice = dlg.ShowModal()
			if choice == wx.ID_OK:
				task = dlg.Task.GetValue()
				period = dlg.Period.GetValue()
				
				update_date = datetime.date.today() + datetime.timedelta(days = int(period))

				self.tasks.InsertItem(self.list_length, str(update_date))
				self.tasks.SetItem(self.list_length, 1, period + ' Days')
				self.tasks.SetItem(self.list_length, 2, task)
				self.list_length += 1
			else:
				pass
				
			dlg.Destroy()
			
		def OnEditEntry(self, event):
			pos = self.tasks.GetFirstSelected()
			if pos == -1:
				dlg = wx.MessageDialog(self.panel, "Please select an item to edit.", "Error", style = wx.OK)
				dlg.ShowModal()
				dlg.Destroy()
			else:
				period_list = self.tasks.GetItemText(pos, 1).split()
				dlg = NewEntry(self.tasks.GetItemText(pos, 2), period_list[0])
				choice = dlg.ShowModal()
				if choice == wx.ID_OK:
					period = dlg.Period.GetValue()
					task = dlg.Task.GetValue()
					
					update_date = datetime.date.today() + datetime.timedelta(days = int(period))
				
					self.tasks.SetItem(pos, 0, str(update_date))
					self.tasks.SetItem(pos, 1, period + ' Days')
					self.tasks.SetItem(pos, 2, task)
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
	
	class NewEntry(wx.Dialog):
		def __init__(self, def_task, def_frequency):
			wx.Dialog.__init__(self, None, wx.ID_ANY, title = "Add New Task", size = (-1, 200))
			
			self.panel = wx.Panel(self)
			
			self.TPrompt = wx.StaticText(self.panel, wx.ID_ANY, label = "Enter the task below:")
			self.Task = wx.TextCtrl(self.panel, wx.ID_ANY, value = def_task)
			
			self.PPrompt = wx.StaticText(self.panel, wx.ID_ANY, label = "Enter the tasks period below, in days:")
			self.Period = wx.TextCtrl(self.panel, wx.ID_ANY, value = def_frequency, style = wx.TE_PROCESS_ENTER)
			self.Period.Bind(wx.EVT_CHAR, self.OnInputFilter)
			
			self.OkButton = wx.Button(self.panel, wx.ID_OK, label = "OK")
			
			self.CancelButton = wx.Button(self.panel, wx.ID_CANCEL, label = "Cancel")
			
			self.ButtonSizer = wx.BoxSizer(wx.HORIZONTAL)
			self.ButtonSizer.Add(self.OkButton, 0, wx.ALL, 5)
			self.ButtonSizer.Add(self.CancelButton, 0, wx.ALL, 5)
			
			self.MasterSizer = wx.BoxSizer(wx.VERTICAL)
			self.MasterSizer.Add((0,5), 0)
			self.MasterSizer.Add(self.TPrompt, 0, wx.CENTER, 5)
			self.MasterSizer.Add((0,5), 0)
			self.MasterSizer.Add(self.Task, 0, wx.CENTER, 5)
			self.MasterSizer.Add((0,10), 0)
			self.MasterSizer.Add(self.PPrompt, 0, wx.CENTER, 5)
			self.MasterSizer.Add((0,5), 0)
			self.MasterSizer.Add(self.Period, 0, wx.CENTER, 5)
			self.MasterSizer.Add((0,10), 0)
			self.MasterSizer.Add(wx.StaticLine(self.panel), 0, wx.EXPAND, 5)
			self.MasterSizer.Add((0,5), 0)
			self.MasterSizer.Add(self.ButtonSizer, 0, wx.CENTER, 5)
			
			self.MasterSizer.SetSizeHints(self.panel)
			self.panel.SetSizerAndFit(self.MasterSizer)
			
			self.Show(True)
		
		def OnInputFilter(self, event):
			
			nums = "0123456789"
			key = event.GetKeyCode()
			
			if chr(key) in nums or key == wx.WXK_BACK or key == wx.WXK_RETURN or key == wx.WXK_DELETE or key == wx.WXK_LBUTTON or key == wx.WXK_RBUTTON:
				event.Skip()
				return
			else:
				return False
			
	RepeatingTasks()
			
		
app = wx.App(False)
frame = MainWindow(None)
app.MainLoop()
