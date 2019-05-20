# controllersviewrow.py - Valhalla Tracker
#
# Copyright (C) 2019 Remigiusz Dybka - remigiusz.dybka@gmail.com
# @schtixfnord
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

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio

from vht import *

class ControllersViewRow(Gtk.ActionBar):
	def __init__(self, parent, trk, ctrlnum, index):
		super(ControllersViewRow, self).__init__()

		self.parent = parent
		self.trk = trk
		self.ctrlnum = ctrlnum
		self.index = index

		button = Gtk.Button()
		icon = Gio.ThemedIcon(name="go-up")
		image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
		button.add(image)
		button.connect("clicked", self.on_go_up_clicked)
		self.pack_start(button)
		self.up_button = button

		button = Gtk.Button()
		icon = Gio.ThemedIcon(name="go-down")
		image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
		button.add(image)
		button.connect("clicked", self.on_go_down_clicked)
		self.pack_start(button)
		self.down_button = button

		self.ctrl_adj = Gtk.Adjustment(1, 1, 127, 1.0, 10.0)
		self.ctrl_button = Gtk.SpinButton()
		self.ctrl_button.set_adjustment(self.ctrl_adj)
		self.ctrl_adj.set_value(self.ctrlnum)
		self.ctrl_adj.connect("value-changed", self.on_num_changed)
		self.pack_start(self.ctrl_button)

		button = Gtk.Button()
		icon = Gio.ThemedIcon(name="edit-delete")

		image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
		button.add(image)
		button.connect("clicked", self.on_del_clicked)
		self.pack_start(button)
		self.show_all()

	def reassign_in_tv(self):
		for c, cc in enumerate(self.parent.trkview.controller_editors):
			cc.ctrlnum = c + 1
			cc.ctrlrows = self.trk.ctrl[c + 1]
			cc.undo_buff._ctrlnum = c + 1

	def on_del_clicked(self, wdg):
		del self.parent.trkview.controller_editors[self.index - 1]
		self.trk.ctrl.delete(self.index)
		self.reassign_in_tv()
		self.parent.rebuild()

	def on_go_up_clicked(self, wdg):
		if self.index > 1:
			self.parent.trkview.controller_editors[self.index - 2], self.parent.trkview.controller_editors[self.index - 1] = \
				self.parent.trkview.controller_editors[self.index - 1], self.parent.trkview.controller_editors[self.index - 2]

			self.trk.ctrl.swap(self.index, self.index - 1)
			self.reassign_in_tv()

		self.parent.rebuild()

	def on_go_down_clicked(self, wdg):
		if self.index < self.trk.nctrl - 1:
			self.parent.trkview.controller_editors[self.index], self.parent.trkview.controller_editors[self.index - 1] = \
				self.parent.trkview.controller_editors[self.index - 1], self.parent.trkview.controller_editors[self.index]

			self.trk.ctrl.swap(self.index, self.index + 1)
			self.reassign_in_tv()

		self.parent.rebuild()

	def on_num_changed(self, adj):
		self.ctrlnum = int(adj.get_value())
		self.trk.ctrl[self.index].ctrlnum = self.ctrlnum
		self.parent.trkview.controller_editors[self.index - 1].midi_ctrlnum = self.ctrlnum
		self.parent.rebuild()

