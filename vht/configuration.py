import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

class Configuration():
	def __init__(self):
		self._highlight = 4
		self.on_highlight = []				# add callbacks here

		#self.seq_font = "Topaz-8"
		self.seq_font = "Monospace"
		#self.seq_font = "Press Start 2P"
		self.seq_font_size = 16
		self.seq_line_width = 1.0
		self.seq_spacing = 1.05
		self.colour = (.9, 1.0, .2)			
		self.intensity_background = 0.3
		self.intensity_txt = .7
		self.intensity_txt_highlight = 1.0
		self.intensity_lines = .6
		self.colour_record = (1.0, 0, 0)
		self.intensity_select = .7
		self.pointer_opacity = .7
		self.pointer_width = 1
		self.current_highlight_opacity = 0.0
		self.auto_scroll_delay = .15
		self.tooltip_markup = """<span font_family="Monospace" size="large">%s</span>"""
		
		self.octave = 4
		self.velocity = 100
		self.page_height = 16
		self.skip = 1
		
		self.select_button = 1
		self.delete_button = 3
		
		self.key = {
			# sequenceview
			"quit": 			cfgkey("q", 			False, True, False),
			"play": 			cfgkey("Return", 		False, False, False),
			"reset": 			cfgkey("Escape", 		False, False, False),
			"fullscreen": 		cfgkey("Return", 		False, False, True),
			"exit_edit": 		cfgkey("Escape", 		False, False, False),
			"undo":				cfgkey("z",				False, True, False),
			"zoom_in":			cfgkey("KP_Add",		False, True, False),
			"zoom_out":			cfgkey("KP_Subtract",	False, True, False),
			"skip_up":			cfgkey("KP_Add",		False, False, False),
			"skip_down":		cfgkey("KP_Subtract",	False, False, False),
			"bpm_up":			cfgkey("KP_Add",		True, True, False),
			"bpm_down":			cfgkey("KP_Subtract",	True, True, False),
			"bpm_10_up":		cfgkey("Page_Up",		True, True, False),
			"bpm_10_down":		cfgkey("Page_Down",		True, True, False),
			"octave_up":		cfgkey("KP_Multiply",	False, False, False),
			"octave_down":		cfgkey("KP_Divide",		False, False, False),
			"highlight_up":		cfgkey("KP_Multiply",	True, False, False),
			"highlight_down":	cfgkey("KP_Divide",		True, False, False),
			"follow":			cfgkey("f",				False, False, False),
			
			# trackview
			"note_off":			cfgkey("backslash",		False, False, False),
			"track_add":		cfgkey("t",				False, True, False),
			"track_del":		cfgkey("d",				False, True, False), 
			"track_expand":		cfgkey("r",				False, True, False), 
			"track_shrink":		cfgkey("e",				False, True, False), 
			"track_move_right":	cfgkey("Right",			False, True, False), 
			"track_move_left":	cfgkey("Left",			False, True, False), 
			"track_move_last":	cfgkey("End",			False, True, False), 
			"track_move_first":	cfgkey("Home",			False, True, False), 
			"select_all":		cfgkey("a",				False, True, False), 
			"copy":				cfgkey("c",				False, True, False), 
			"cut":				cfgkey("x",				False, True, False), 
			"paste":			cfgkey("v",				False, True, False), 
			"delete":			cfgkey("Delete",		False, False, False), 
			"pull":				cfgkey("Delete",		False, True, False), 
			"push":				cfgkey("Insert",		False, True, False), 
			"transp_up":		cfgkey("Up",			False, True, False), 
			"transp_down":		cfgkey("Down",			False, True, False), 
			"transp_12_up":		cfgkey("Page_Up",		False, True, False), 
			"transp_12_down":	cfgkey("Page_Down",		False, True, False), 
			"velocity_up":		cfgkey("Up",			False, False, True), 
			"velocity_down":	cfgkey("Down",			False, False, True), 
			"velocity_10_up":	cfgkey("Page_Up",		False, False, True), 
			"velocity_10_down":	cfgkey("Page_Down",		False, False, True),
			"channel_up":		cfgkey("KP_Add",		True, False, True),
			"channel_down":		cfgkey("KP_Subtract",	True, False, True),
			"port_up":			cfgkey("KP_Multiply",	True, False, True),
			"port_down":		cfgkey("KP_Divide",		True, False, True),
		}
		
	@property
	def highlight(self):
		return self._highlight

	@highlight.setter
	def highlight(self, value):
		self._highlight = value
		if len(self.on_highlight):
			for cb in self.on_highlight:
				cb()

key_aliases = {	"KP_Add": "keypad +",
				"KP_Subtract": "keypad -",
				"KP_Multiply": "keypad *",
				"KP_Divide": "keypad /",
				"Page_Up": "page up",
				"Page_Down": "page down",
				"backslash": "\\",
				}

class cfgkey():
	def __init__(self, key, shift, ctrl, alt):
		self.key = key
		self.shift = shift
		self.ctrl = ctrl
		self.alt = alt

	def matches(self, event):
		key = Gdk.keyval_name(Gdk.keyval_to_lower(event.keyval))
		if key != self.key:
			return False

		shift = False
		ctrl = False
		alt = False
		
		if event.state & Gdk.ModifierType.SHIFT_MASK:
			shift = True
		
		if event.state & Gdk.ModifierType.CONTROL_MASK:
			ctrl = True
		
		if event.state & Gdk.ModifierType.MOD1_MASK:
			alt = True
		
		if self.shift != shift:
			return False
			
		if self.ctrl != ctrl:
			return False
		
		if self.alt != alt:
			return False
		
		return True
 
	def __str__(self):
		ret = ""
		
		if self.ctrl:
			ret = ret + "ctrl "
		
		if self.shift:
			ret = ret + "shift "
		
		if self.alt:
			ret = ret + "alt "
			
		if self.key in key_aliases:
			ret = ret + "[%s]" % key_aliases[self.key]
		else:
			ret = ret + "[%s]" % self.key.lower()
		return ret
