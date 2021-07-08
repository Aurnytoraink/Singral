# login_window.py
#
# Copyright 2021 Aurnytoraink
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


from gi.repository import Gtk, Adw, Gdk

@Gtk.Template(resource_path='/com/github/Aurnytoraink/Singral/ui/login_window.ui')
class LoginWindow(Adw.Window):
    __gtype_name__ = 'LoginWindow'

    email = Gtk.Template.Child()
    password = Gtk.Template.Child()
    login_button = Gtk.Template.Child()

    bottom_button = Gtk.Template.Child()
    bottom_label = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.uri = "https://www.qobuz.com"

    def clear_entries(self, *_):
        for entry in [
            self.email,
            self.password,
        ]:
            entry.set_text('')

    def wrong_creditentials(self, *arg):
        self.uri = "https://www.qobuz.com/reset-password"
        self.bottom_label.set_label(_("Forget your password ?"))
        self.bottom_button.set_label(_("Reset Password"))
        self.bottom_button.add_css_class("destructive-action")
        self.bottom_button.remove_css_class("suggested-action")

    @Gtk.Template.Callback()
    def on_login_clicked(self, *arg):
        return

    @Gtk.Template.Callback()
    def on_text_changed(self, text):
        if self.email.get_text() != "" and self.password.get_text() != "":
            self.login_button.set_sensitive(True)
        else:
            self.login_button.set_sensitive(False)
        self.uri = "https://www.qobuz.com/"
        self.bottom_label.set_label(_("Don't have an account yet ?"))
        self.bottom_button.set_label(_("Subscribe now"))
        self.bottom_button.add_css_class("suggested-action")
        self.bottom_button.remove_css_class("destructive-action")

    @Gtk.Template.Callback()
    def on_subscribe_clicked(self, *_):
        Gtk.show_uri(self,self.uri,Gdk.CURRENT_TIME)
