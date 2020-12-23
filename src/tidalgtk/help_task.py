# help_task.py
#
# Copyright 2020 Aurnytoraink
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from threading import Thread
from gi.repository import GLib

class TaskHelper:
    def run(self, command, *args, **kwargs):
        thread = Thread(target=self.__run,
                        args=(command, kwargs, *args))
        thread.daemon = True
        thread.start()
        return thread

    def __run(self, command, kwd, *args):
        try:
            result = command(*args)
            if "callback" in kwd.keys():
                (callback, *callback_args) = kwd["callback"]
                if callback is not None:
                    GLib.idle_add(callback, result, *callback_args)
        except Exception as e:
            print(f"\nError: {e}")


