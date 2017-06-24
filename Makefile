#Poor Man's Sequencer by Remigiusz Dybka

PYTHON_INCLUDE=/usr/include/python3.5m
CC=gcc
CFLAGS=-I$(PYTHON_INCLUDE) -fPIC
LIBS=-lm -ljack
DEPS=lib/pms.h \
	lib/jack_client.h \
	lib/jack_process.h \
	lib/midi_event.h 
	
OBJ=lib/jack_client.o lib/jack_process.o lib/midi_event.o lib/pms.o

all: _pms.so

%.o: %c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

lib/pms_wrap.c: $(DEPS) $(OBJ)
	swig -python lib/pms.h

lib/pms_wrap.o: lib/pms_wrap.c
	$(CC) -c -o $@ $< $(CFLAGS)

pms.py: lib/pms_wrap.c
	cp lib/pms.py .

_pms.so: $(OBJ) lib/pms_wrap.o pms.py
	ld -shared $(OBJ) lib/pms_wrap.o -o $@ $(LIBS)
		
clean:
	rm -f *.so *.o lib/pms.py
	rm -f lib/*.so lib/*.o lib/pms_wrap.c
	rm -rf __pycache__	