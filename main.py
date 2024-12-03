import npyscreen

from dataForm import DataForm
from loginForm import LoginForm


class LoginApp(npyscreen.NPSAppManaged):
    def __init__(self):
        super().__init__()
        self.password = None
        self.username = None
        self.port = None
        self.host = None
        self.curser = None

    def onStart(self):
        self.addForm("LOGIN", LoginForm, name="LOGIN", color="IMPORTANT")
        self.addForm("DATA", DataForm, name="DATA", color="WARNING")


if __name__ == '__main__':
    LoginApp().run()
