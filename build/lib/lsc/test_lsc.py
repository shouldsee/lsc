
# import logged_shell_command
from .logged_shell_command import LoggedShellCommand
def test_LoggedShellCommand():
	LoggedShellCommand(["echo","hi"],'log')
	pass