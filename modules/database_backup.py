import datetime, glob, os, shutil, time
from src import ModuleManager, utils

BACKUP_INTERVAL = 60*60 # 1 hour
BACKUP_COUNT = 5

class Module(ModuleManager.BaseModule):
    def on_load(self):
        now = datetime.datetime.now()
        until_next_hour = 60-now.second
        until_next_hour += ((60-(now.minute+1))*60)

        self.timers.add("database-backup", self._backup, BACKUP_INTERVAL,
            time.time()+until_next_hour)

    def _backup(self, timer):
        location =  self.bot.database.location
        files = glob.glob("%s.*.back" % location)
        files = sorted(files)

        while len(files) > 4:
            os.remove(files[-1])
            files.pop(-1)

        suffix = datetime.datetime.now().strftime("%y-%m-%d.%H:%M:%S")
        backup_file = "%s.%s.back" % (location, suffix)
        shutil.copy2(location, backup_file)

        timer.redo()
