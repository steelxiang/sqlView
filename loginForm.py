import npyscreen

import dataService


class LoginForm(npyscreen.ActionPopup):

    def create(self):
        self.name = "LOGIN"
        self.wghost = self.add(npyscreen.TitleText, name="host:")
        self.wgport = self.add(npyscreen.TitleText, name="port:")
        self.wgUsername = self.add(npyscreen.TitleText, name="Username:")
        self.wgPassword = self.add(npyscreen.TitleText, name="Password:")

    def beforeEditing(self):
        self.wghost.value = 'localhost'
        self.wgport.value = '3306'
        self.wgUsername.value = 'root'
        self.wgPassword.value = '123456'

    def on_ok(self):
        self.parentApp.host=self.wghost.value
        self.parentApp.port=self.wgport.value
        self.parentApp.username = self.wgUsername.value
        self.parentApp.password = self.wgPassword.value

        dataForm=self.parentApp.getForm('DATA')
        dataForm.initDatabase()
        self.parentApp.switchForm('DATA')

    def on_cancel(self):
        self.parentApp.switchForm(None)
