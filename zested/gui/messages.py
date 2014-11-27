from PySide import QtGui


class SaveModifiedMessage(QtGui.QMessageBox):
	'''
	Message to ask wether the user wants to save his modifications
	'''

	def __init__(self):
		super().__init__()
		self.setText("Ce document a été modifié")
		self.setInformativeText("Voulez-vous enregistrer vos changements ?")
		self.setStandardButtons(self.Save|self.Discard|self.Cancel)
		self.setDefaultButton(QtGui.QMessageBox.Save)
