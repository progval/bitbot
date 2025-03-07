#--depends-on commands

from src import ModuleManager, utils

class Module(ModuleManager.BaseModule):
    @utils.hook("received.command.echo")
    @utils.kwarg("min_args", 1)
    def echo(self, event):
        event["stdout"].write(event["args"])

    @utils.hook("received.command.action")
    @utils.kwarg("min_args", 1)
    @utils.kwarg("expect_output", False)
    def action(self, event):
        event["target"].send_message("\x01ACTION %s\x01" % event["args"])

    @utils.hook("received.command.msg")
    @utils.kwarg("min_args", 2)
    @utils.kwarg("permission", "say")
    @utils.kwarg("remove_empty", False)
    @utils.kwarg("help", "Send a message to a target")
    def msg(self, event):
        event["server"].send_message(event["args_split"][0],
            " ".join(event["args_split"][1:]))
