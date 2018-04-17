import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gdk, Gtk, Gio
import cairo

from vht import *
from vht.trackview import TrackView
from vht.blackgrid import BlackGrid
from vht.blackcheckbutton import BlackCheckButton
from vht.blacklabel import BlackLabel
from vht.blackbutton import BlackButton

class TrackPropViewPopover(Gtk.Popover):
	def __init__(self, parent, trk):
		super(TrackPropViewPopover, self).__init__()
		self.set_relative_to(parent)

		self.set_events(Gdk.EventMask.LEAVE_NOTIFY_MASK 
						| Gdk.EventMask.ENTER_NOTIFY_MASK 
						| Gdk.EventMask.POINTER_MOTION_MASK)
		
		self.connect("leave-notify-event", self.on_leave)
		self.connect("enter-notify-event", self.on_enter)
		self.connect("motion-notify-event", self.on_motion)
		
		self.entered = False
		self.allow_close = True
		
		self.parent = parent
		self.trk = trk
		self.trkview = parent.trkview
		self.grid = Gtk.Grid()
		self.grid.set_column_spacing(3)
		self.grid.set_row_spacing(3)

		if trk:
			button = Gtk.Button()
			icon = Gio.ThemedIcon(name="edit-delete")
			image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
			button.add(image)
			button.connect("clicked", self.on_remove_button_clicked)
			button.set_tooltip_markup(cfg.tooltip_markup % (cfg.key["track_del"]))
			self.grid.attach(button, 3, 0, 1, 1)

			button = Gtk.Button()
			icon = Gio.ThemedIcon(name="list-remove")
			image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
			button.add(image)
			button.connect("clicked", self.on_retract_button_clicked)
			button.set_tooltip_markup(cfg.tooltip_markup % (cfg.key["track_shrink"]))
			self.grid.attach(button, 0, 0, 1, 1)

			button = Gtk.Button()
			icon = Gio.ThemedIcon(name="list-add")
			image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
			button.add(image)
			button.connect("clicked", self.on_expand_button_clicked)
			button.set_tooltip_markup(cfg.tooltip_markup % (cfg.key["track_expand"]))
			self.grid.attach(button, 1, 0, 2, 1)

			button = Gtk.Button()
			icon = Gio.ThemedIcon(name="go-previous")
			image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
			button.add(image)
			button.connect("clicked", self.on_move_left_button_clicked)
			button.set_tooltip_markup(cfg.tooltip_markup % (cfg.key["track_move_left"]))
			self.grid.attach(button, 1, 1, 1, 1)

			button = Gtk.Button()
			icon = Gio.ThemedIcon(name="go-next")
			image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
			button.add(image)
			button.connect("clicked", self.on_move_right_button_clicked)
			button.set_tooltip_markup(cfg.tooltip_markup % (cfg.key["track_move_right"]))
			self.grid.attach(button, 2, 1, 1, 1)

			button = Gtk.Button()
			icon = Gio.ThemedIcon(name="go-first")
			image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
			button.add(image)
			button.connect("clicked", self.on_move_first_button_clicked)
			button.set_tooltip_markup(cfg.tooltip_markup % (cfg.key["track_move_first"]))
			self.grid.attach(button, 0, 1, 1, 1)

			button = Gtk.Button()
			icon = Gio.ThemedIcon(name="go-last")
			image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
			button.add(image)
			button.connect("clicked", self.on_move_last_button_clicked)
			button.set_tooltip_markup(cfg.tooltip_markup % (cfg.key["track_move_last"]))
			self.grid.attach(button, 3, 1, 1, 1)

			self.extend_grid = Gtk.Grid()
			self.extend_grid.set_hexpand(True)
			self.extend_grid.set_vexpand(True)
			
			self.grid.attach(self.extend_grid,4,0,5,6)

			grid = BlackGrid()
			grid.set_column_homogeneous(True)
			grid.set_row_homogeneous(True)
			grid.set_column_spacing(2)
			grid.set_row_spacing(2)

			self.show_notes_button = BlackCheckButton("notes")
			self.show_timeshift_button = BlackCheckButton("time")
			self.show_pitchwheel_button = BlackCheckButton("pitch")
			self.show_controllers_button = BlackCheckButton("ctrl")

			self.show_notes_button.connect("toggled", self.on_show_notes_toggled)
			self.show_timeshift_button.connect("toggled", self.on_show_timeshift_toggled)
			self.show_pitchwheel_button.connect("toggled", self.on_show_pitchwheel_toggled)
			self.show_controllers_button.connect("toggled", self.on_show_controllers_toggled)

			grid.attach(BlackLabel("show:"), 0, 0, 1, 1)
			grid.attach(self.show_notes_button, 1, 0, 1, 1)
			grid.attach(self.show_timeshift_button, 2, 0, 1, 1)
			grid.attach(self.show_pitchwheel_button, 3, 0, 1, 1)
			grid.attach(self.show_controllers_button, 4, 0, 1, 1)
			
			grid.attach(BlackLabel(""), 0, 2, 1, 1)
			grid.attach(BlackLabel("rotate:"), 0, 1, 1, 1)
			rotate_up_button = BlackButton("up")
			grid.attach(rotate_up_button, 1, 1, 1, 1)
			rotate_down_button = BlackButton("down")
			grid.attach(rotate_down_button, 2, 1, 1, 1)
			
			self.loop_button = BlackCheckButton("loop")
			grid.attach(self.loop_button, 4, 3, 1, 1)
						
			self.clone_button = BlackButton("clone")
			grid.attach(self.clone_button, 4, 2, 1, 1)
						
			self.extend_track_grid = grid
						
			self.extend_notebook = Gtk.Notebook()
			self.extend_notebook.set_hexpand(True)
			self.extend_notebook.set_vexpand(True)
			self.extend_controllers_grid = BlackGrid()
			self.extend_triggers_grid = BlackGrid()
			
			self.extend_notebook.append_page(self.extend_track_grid, Gtk.Label("track"))
			self.extend_notebook.append_page(self.extend_controllers_grid, Gtk.Label("controllers"))
			self.extend_notebook.append_page(self.extend_triggers_grid, Gtk.Label("triggers"))
			
			self.extend_grid.attach(self.extend_notebook, 0, 0, 5, 5)
			self.extend_grid.show()
			
			self.port_adj = Gtk.Adjustment(0, 0, 15, 1.0, 1.0)
			self.port_button = Gtk.SpinButton()
			self.port_button.set_adjustment(self.port_adj)
			self.port_adj.set_value(trk.port)
			self.port_adj.connect("value-changed", self.on_port_changed)

			lbl = Gtk.Label("port:")
			lbl.set_xalign(1.0)

			self.grid.attach(lbl, 0, 3, 1, 1)
			self.grid.attach(self.port_button, 1, 3, 2, 1)

			self.channel_adj = Gtk.Adjustment(1, 1, 16, 1.0, 1.0)
			self.channel_button = Gtk.SpinButton()
			self.channel_button.set_adjustment(self.channel_adj)
			self.channel_adj.set_value(trk.channel)
			self.channel_adj.connect("value-changed", self.on_channel_changed)

			lbl = Gtk.Label("channel:")
			lbl.set_xalign(1.0)
			
			self.grid.attach(lbl, 0, 2, 1, 1)
			self.grid.attach(self.channel_button, 1, 2, 2, 1)

			self.nsrows_adj = Gtk.Adjustment(1, 1, self.parent.seq.length, 1.0, 1.0)
			self.nsrows_button = Gtk.SpinButton()
			self.nsrows_button.set_adjustment(self.nsrows_adj)
			self.nsrows_adj.set_value(trk.nsrows)
			self.nsrows_adj.connect("value-changed", self.on_nsrows_changed)

			lbl = Gtk.Label("rows:")
			lbl.set_xalign(1.0)
			
			self.nsrows_check_button = Gtk.CheckButton()
			self.nsrows_check_button.connect("toggled", self.on_nsrows_toggled)

			
			self.grid.attach(lbl, 0, 4, 1, 1)
			self.grid.attach(self.nsrows_button, 1, 4, 2, 1)
			self.grid.attach(self.nsrows_check_button, 3, 4, 1, 1)
			
			self.nrows_adj = Gtk.Adjustment(1, 1, 256, 1.0, 1.0)
			self.nrows_button = Gtk.SpinButton()
			self.nrows_button.set_adjustment(self.nrows_adj)
			self.nrows_adj.set_value(trk.nsrows)
			self.nrows_adj.connect("value-changed", self.on_nrows_changed)

			lbl = Gtk.Label("funk:")
			lbl.set_xalign(1.0)
			
			self.nrows_check_button = Gtk.CheckButton()
			self.nrows_check_button.connect("toggled", self.on_nrows_toggled)
			
			self.grid.attach(lbl, 0, 5, 1, 1)
			self.grid.attach(self.nrows_button, 1, 5, 2, 1)
			self.grid.attach(self.nrows_check_button, 3, 5, 1, 1)

			self.nrows_button.set_sensitive(False)
			self.nsrows_button.set_sensitive(False)
			self.nrows_check_button.set_sensitive(False)
			
			self.grid.show_all()
			#self.extend_grid.hide()
			self.add(self.grid)

	def on_timeout(self, args):
		self.allow_close = True
		return False

	def popup(self):
		super().popup()
		self.allow_close = False
		self.entered = False
		GObject.timeout_add(cfg.popover_wait_before_close, self.on_timeout, None)
		self.channel_adj.set_value(self.trk.channel)
		self.port_adj.set_value(self.trk.port)
		self.nsrows_adj.set_upper(self.parent.seq.length)
		self.nsrows_adj.set_value(self.trk.nsrows)
		self.nrows_adj.set_value(self.trk.nrows)
		self.port_adj.set_upper(mod.nports - 1)
		
		#self.loop_button.set_active(self.trk.loop) // not yet implemented in vhtlib
		self.show_notes_button.set_sensitive(False)
		self.show_notes_button.set_active(self.trkview.show_notes)
		self.show_timeshift_button.set_active(self.trkview.show_timeshift)
		self.show_pitchwheel_button.set_active(self.trkview.show_pitchwheel)
		self.show_controllers_button.set_active(self.trkview.show_controllers)

	def on_leave(self, wdg, prm):
		#if self.entered:
			if self.allow_close:
				if prm.detail == Gdk.NotifyType.NONLINEAR:
					wdg.popdown()
					self.entered = False
					self.parent.popped = False
					self.parent.button_highlight = False
					self.parent.redraw()

	def on_enter(self, wdg, prm):
		if prm.detail == Gdk.NotifyType.NONLINEAR:
			if self.entered == False:
				self.entered = True
				self.parent.button_highlight = False
				self.parent.redraw()

	def on_motion(self, wdg, evt):
			if self.entered == False:
				self.entered = True
				self.parent.button_highlight = False
				self.parent.redraw()


	def on_show_notes_toggled(self, wdg):
		if not self.entered:
			return False
		
		if wdg.get_active():
			self.show_controllers_button.set_sensitive(True)
		else:
			self.show_controllers_button.set_active(True)
			self.show_controllers_button.set_sensitive(False)	

	def on_show_timeshift_toggled(self, wdg):
		if not self.entered:
			return False
		
		self.trkview.show_timeshift = wdg.get_active()
		self.trkview.redraw()
		self.parent.redraw()

	def on_show_pitchwheel_toggled(self, wdg):
		if not self.entered:
			return False
			
		self.trkview.show_pitchwheel = wdg.get_active()
		self.trkview.redraw()
		self.parent.redraw()

	def on_show_controllers_toggled(self, wdg):
		if not self.entered:
			return False

		if wdg.get_active():
			self.show_notes_button.set_sensitive(True)
		else:
			self.show_notes_button.set_active(True)
			self.show_notes_button.set_sensitive(False)

		self.trkview.show_controllers = wdg.get_active()
		self.trkview.redraw()
		self.parent.redraw()
			
	def on_remove_button_clicked(self, switch):
		self.parent.del_track()
					
	def on_retract_button_clicked(self, switch):
		self.parent.seqview.shrink_track(self.trk)
			
	def on_expand_button_clicked(self, switch):
		self.parent.seqview.expand_track(self.trk)
			
	def on_port_changed(self, adj):
		self.trk.port = int(adj.get_value())
		self.parent.redraw()

	def on_channel_changed(self, adj):
		self.trk.channel = int(adj.get_value())
		self.parent.redraw()

	def on_nrows_changed(self, adj):
		self.trk.nrows = int(adj.get_value())
		self.parent.seqview.recalculate_row_spacing()

	def on_nsrows_changed(self, adj):
		self.trk.nsrows = int(adj.get_value())
		
		if not self.nrows_check_button.get_active():
			self.trk.nrows = int(adj.get_value())
			self.nrows_adj.set_value(adj.get_value())
		
		self.parent.seqview.recalculate_row_spacing()
		
	def on_nrows_toggled(self, wdg):
		if (wdg.get_active()):
			self.nrows_button.set_sensitive(True)
			self.nsrows_check_button.set_sensitive(True)		
		else:
			self.nrows_button.set_sensitive(False)
			self.nrows_check_button.set_active(False)
			self.nrows_adj.set_value(self.nsrows_adj.get_value())
								
	def on_nsrows_toggled(self, wdg):
		if (wdg.get_active()):
			self.nsrows_button.set_sensitive(True)
			self.nrows_check_button.set_sensitive(True)
		else:
			self.nsrows_button.set_sensitive(False)
			self.nrows_button.set_sensitive(False)
			self.nrows_check_button.set_active(False)
			self.nrows_check_button.set_sensitive(False)
			
			self.nrows_adj.set_value(self.parent.seq.length)
			self.nsrows_adj.set_value(self.parent.seq.length)

	def on_move_left_button_clicked(self, switch):
		self.parent.move_left()
		
	def on_move_right_button_clicked(self, switch):
		self.parent.move_right()
		
	def on_move_first_button_clicked(self, switch):
		self.parent.move_first()
		
	def on_move_last_button_clicked(self, switch):
		self.parent.move_last()
	
