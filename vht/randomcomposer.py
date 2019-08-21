# randomcomposer.py - Valhalla Tracker
#
# Copyright (C) 2019 Remigiusz Dybka - remigiusz.dybka@gmail.com
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

from vht import mod

def track_fill(trk, note = "c3", skip = 2, velocity = 100):
	for r in range(len(trk[0])):
		if r % skip == 0:
			trk[0][r] = note
			trk[0][r].velocity = velocity

def muzakize():
	mod.bpm = 123

	seq = mod.add_sequence(32)
	trk = seq.add_track()
	#trk.ctrl.add(1)
