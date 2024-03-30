from mythic_container.MythicCommandBase import *
import json
from mythic_container.MythicRPC import *

class ShellArguments(TaskArguments):

    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = []

    async def parse_arguments(self):
        if len(self.command_line.strip()) == 0:
            raise Exception("shell requires at least one command-line parameter.\n\tUsage: {}".format(ShellCommand.help_cmd))
        pass


class ShellCommand(CommandBase):
    cmd = "shell"
#    attributes=CommandAttributes(
#        dependencies=["run"]
#    )
    needs_admin = False
    help_cmd = "shell [command]  [arguments]"
    description = "Execute a shell command with 'sh -c' if on Linux or 'cmd.exe /r' if on Windows"
    version = 3
    author = "@NotoriousRebel"
    argument_class = ShellArguments
    
    attackmapping = ["T1059"]

    async def create_go_tasking(self, taskData: PTTaskMessageAllData) -> PTTaskCreateTaskingMessageResponse:
        response = PTTaskCreateTaskingMessageResponse(
            TaskID=taskData.Task.ID,
            Success=True,
        )
        return response

    async def process_response(self, task: PTTaskMessageAllData, response: any) -> PTTaskProcessResponseMessageResponse:
        if "message" in response:
            user_output = response["message"]
            await MythicRPC().execute("create_output", task_id=task.Task.ID, output=message_converter.translateAthenaMessage(user_output))

        resp = PTTaskProcessResponseMessageResponse(TaskID=task.Task.ID, Success=True)
        return resp
