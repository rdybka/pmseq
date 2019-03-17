![vht header](/data/vht_header.png)
## about
Valhalla Tracker aims to be a MIDI sequencing companion for your
JACK/Yoshimi/Hydrogen/Calf setup. It relies 100% on JACK for timing
which allows sample-exact synchronisation and in future, 
asynchronous rendering.

## installation on Fedora
`[sudo] dnf install jack-audio-connection-kit-devel python3-devel swig astyle git rpm-devel\n
git clone https://github.com/rdybka/vht\n
cd vht\n
./setup.py install --user`

## roadmap before a file release
- [x] record/edit notes
- [ ] record/edit controllers
- [ ] triggers
- [ ] timeline
- [ ] loops
- [ ] export to wav
- [ ] configuration window

deadline: soon enough
