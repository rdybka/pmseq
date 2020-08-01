# vhttimelinechanges.py - Valhalla Tracker (libvht)
#
# Copyright (C) 2020 Remigiusz Dybka - remigiusz.dybka@gmail.com
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

from collections.abc import MutableSequence
from libvht import libcvht


class VHTTimelineChanges(MutableSequence):
    def __init__(self, tl):
        super(VHTTimelineChanges, self).__init__()
        self._tl_handle = tl

    def __len__(self):
        return libcvht.timeline_get_nchanges(self._tl_handle)

    def __iter__(self):
        for itm in range(self.__len__()):
            yield eval(libcvht.timeline_get_change(self._tl_handle, itm))

    def __getitem__(self, itm):
        if itm >= self.__len__():
            raise IndexError()

        if itm < 0:
            raise IndexError()

        return eval(libcvht.timeline_get_change(self._tl_handle, itm))

    def __delitem__(self, itm):
        libcvht.timeline_change_del(self._tl_handle, itm)

    def __setitem__(self, row, bpm, linked):
        libcvht.timeline_change_set(self._tl_handle, row, bpm, linked)

    def insert(self, row, bpm, linked):
        libcvht.timeline_change_set(self._tl_handle, row, bpm, linked)

    def __str__(self):
        ret = ""
        for r in range(self.__len__()):
            ret = ret + str(self[r])
            ret = ret + "\n"

        return ret
