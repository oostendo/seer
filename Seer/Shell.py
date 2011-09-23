class ShellThread(threading.Thread):
    def run(self):
  	shell = IPython.Shell.IPShell(user_ns=globals())	
	shell.mainloop()
