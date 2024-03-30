from mythic_container.MythicCommandBase import *
import json


class KillArguments(TaskArguments):

    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = [
            CommandParameter(
                name="pid",
                cli_name="PID",
                display_name="PID",
                type=ParameterType.Number)
        ]

    async def parse_arguments(self):
        if len(self.command_line) == 0:
            raise Exception("No PID given.")
        if self.command_line[0] == "{":
            self.load_args_from_json_string(self.command_line)
        else:
            try:
                int(self.command_line)
            except:
                raise Exception("Failed to parse integer PID from: {}\n\tUsage: {}".format(self.command_line, killCommand.help_cmd))
            self.add_arg("pid", int(self.command_line), ParameterType.Number)
        


class KillCommand(CommandBase):
    cmd = "kill"
    needs_admin = False
    help_cmd = "kill [pid]"
    description = "Kill a process specified by [pid]"
    version = 3
    author = "@NotoriousRebel"
    argument_class = KillArguments
    attackmapping = ["T1106"]
    supported_ui_features = ["kill"]

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
