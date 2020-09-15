/* timeline.h - Valhalla Tracker (libvht)
 *
 * Copyright (C) 2020 Remigiusz Dybka - remigiusz.dybka@gmail.com
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#ifndef __TIMELINE_H__
#define __TIMELINE_H__

#include "sequence.h"

typedef struct loop_t {
	long start;
	long end;
} loop;

typedef struct timeslice_t {
	float bpm;
	double length;
	double time;
} timeslice;

typedef struct timechange_t {
	float bpm;
	int linked;
	long row;
	int tag;
} timechange;

typedef struct timestrip_t {
	sequence *seq;
	int col;
	long start;
	int length;
	int rpb_start;
	int rpb_end;
	int tag;
} timestrip;

typedef struct timeline_t {
	timeslice *slices;
	timechange *changes;
	timestrip *strips;
	loop *loops;
	double *ticks; // time in secs for each qb
	long nslices;
	int nchanges;
	int nstrips;
	int nticks;
	int ncols;
	int nloops;
	int loop_curr;
	int loop_last;
	int length;  // in qbeats
	double time_length;
	double pos;  // qb

	pthread_mutex_t excl;
} timeline;

timeline *timeline_new(void);
void timeline_free(timeline *tl);
void timeline_clear(timeline *tl);
void timeline_update(timeline *tl);
void timeline_update_inner(timeline *tl);
void timeline_advance(timeline *tl, double period);
long timeline_get_qb(timeline *tl, double t);
double timeline_get_qb_time(timeline *tl, long row);
void timeline_swap_sequence(timeline *tl, int s1, int s2);

void timechange_set_bpm(timeline *tl, timechange *tc, float bpm);
void timechange_set_row(timeline *tl, timechange *tc, long row);
void timechange_set_linked(timeline *tl, timechange *tc, int linked);
float timechange_get_bpm(timechange *tc);
long timechange_get_row(timechange *tc);
int timechange_get_linked(timechange *tc);

void timechange_del(timeline *tl, int id);
timechange *timeline_add_change(timeline *tl, float bpm, long row, int linked);
timechange *timeline_get_change(timeline *tl, int id);
timechange *timeline_change_get_at(timeline *tl, long row);
int timeline_get_nchanges(timeline *tl);

float timeline_get_bpm_at_qb(timeline *tl, long row);
int timeline_get_interpol_at_qb(timeline *tl, long row);

int timeline_get_nticks(timeline *tl);
double timeline_get_tick(timeline *tl, int n);
int timeline_get_room(timeline *tl, int col, long qb, int ig);
int timeline_get_snap(timeline *tl, int tstr_id, long qb_delta);
int timeline_place_clone(timeline *tl, int tstr_id);
timestrip *timeline_get_strip(timeline *tl, int n);
sequence *timeline_get_seq(timeline *tl, int n);
sequence *timeline_get_prev_seq(timeline *tl, timestrip *tstr);
sequence *timeline_get_next_seq(timeline *tl, timestrip *tstr);
int timeline_expand_start(timeline *tl, long qb_start);
int timeline_expand(timeline *tl, long qb_start, long qb_n);

int timeline_get_strip_for_qb(timeline *tl, int col, long qb);
int timeline_get_last_strip(timeline *tl, int col, long qb);
int timeline_get_nstrips(timeline *tl);
timestrip *timeline_add_strip(timeline *tl, int col, sequence *seq, long start, int length, int rpb_start, int rpb_end);
void timeline_del_strip(timeline *tl, int id);
void timeline_delete_all_strips(timeline *tl, int col);

// relativity
int timestrip_can_resize_seq(timeline *tl, timestrip *tstr, int len);
int timestrip_can_rpb_seq(timeline *tl, timestrip *tstr, int rpb);

// loops
int timeline_get_nloops(timeline *tl);
long timeline_get_loop_start(timeline *tl, int lp_id);
long timeline_get_loop_end(timeline *tl, int lp_id);
void timeline_set_loop_start(timeline *tl, int lp_id, long val);
void timeline_set_loop_end(timeline *tl, int lp_id, long val);
void timeline_del_loop(timeline *tl, int lp_id);
int timeline_add_loop(timeline *tl, long lp_start, long lp_end);
int timeline_get_loop_for_qb(timeline *tl, long qb);

#endif //__TIMELINE_H__
