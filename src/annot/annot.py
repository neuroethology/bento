# annot.py
import timecode as tc
from annot.behavior import Behavior

class Bout(object):
    """
    """

    def __init__(self, start, end, behavior):
        self._start = start
        self._end = end
        self._behavior = behavior
    
    def __lt__(self, b):
        return self._start < b._start

    def __le__(self, b):
        return self._start <= b._start

    def is_at(self, t):
        return self._start <= t and self._end >= t

    def start(self):
        return self._start

    def end(self):
        return self._end
    
    def len(self):
        return self._end - self._start

    def name(self):
        return self._behavior.get_name()

    def color(self):
        return self._behavior.get_color()

class Channel(object):
    """
    """

    def __init__(self, chan = None):
        if not chan is None:
            self._bouts = chan._bouts
        else:
            self._bouts = []

    def append(self, b):
        if isinstance(b, Bout):
            self._bouts.append(b)
        else:
            raise TypeError("Can only append Bout to Channel")
    
    def __add__(self, b):
        self.append(b)

    def sort(self):
        self._bouts.sort()
    
class Annotations(object):
    """
    """

    def __init__(self, behaviors):
        self._channels = {}
        self._behaviors = behaviors
        self._movies = []
        self._time_start = None
        self._time_end = None
        self._frame_rate = None
        self._stimulus = None
        self.annotation_names = []

    def read(self, fn):
        with open(fn, "r") as f:
            line = f.readline()
            line = line.strip().lower()
            if line.endswith("annotation file"):
                self._read_caltech(f)
            elif line.startswith("scorevideo log"):
                self._read_ethovision(f)
            else:
                print("Unsupported annotation file format")

    def _read_caltech(self, f):
        found_movies = False
        found_timecode = False
        found_stimulus = False
        found_channel_names = False
        found_annotation_names = False
        found_all_channels = False
        found_all_annotations = False
        reading_channel = False
        channel_names = []
        current_channel = None
        current_bout = None

        line = f.readline()
        while line:
            line.strip()

            if not line:
                if reading_channel:
                    reading_channel = False
                    current_channel = None
                    current_bout = None
            elif line.lower().startswith("movie file"):
                items = line.split()
                for item in items:
                    if item.lower().startswith("movie"):
                        continue
                    if item.lower().startswith("file"):
                        continue
                    self._movies.append(item)
                found_movies = True
            elif line.lower().startswith("stimulus name"):
                # TODO: do something when we know what one of these looks like
                found_stimulus = True
            elif line.lower().startswith("annotation start frame"):
                items = line.split()
                if len(items) > 3:
                    self._time_start = int(items[3])
                    if self._time_end and self._frame_rate:
                        found_timecode = True
            elif line.lower().startswith("annotation stop frame"):
                items = line.split()
                if len(items) > 3:
                    self._time_end = int(items[3])
                    if self._time_start and self._frame_rate:
                        found_timecode = True
            elif line.lower().startswith("annotation framerate"):
                items = line.split()
                if len(items) > 2:
                    self._frame_rate = float(items[2])
                    if self._time_start and self._time_end:
                        found_timecode = True
            elif line.lower().startswith("list of channels"):
                line = f.readline()
                while line:
                    line = line.strip()
                    if not line:
                        break # blank line -- end of section
                    channel_names.append(line)
                    line = f.readline()
                found_channel_names = True
            elif line.lower().startswith("list of annotations"):
                line = f.readline()
                while line:
                    line = line.strip()
                    if not line:
                        break # blank line -- end of section
                    self.annotation_names.append(line)
                    line = f.readline().strip()
                found_annotation_names = True
            elif line.lower().startswith("ch"):
                for ch_name in channel_names:
                    if line.startswith(ch_name):
                        self._channels[ch_name] = Channel()
                        current_channel = ch_name
                        reading_channel = True
                        break
                if reading_channel:
                    reading_annot = False
                    line = f.readline()
                    while line:
                        line = line.strip()
                        if not line: # blank line
                            if reading_annot:
                                reading_annot = False
                                current_bout = None
                            else:
                                # second blank line, so done with channel
                                reading_channel = False
                                current_channel = None
                                break
                        elif line.startswith(">"):
                            current_bout = line[1:]
                            reading_annot = True
                        elif line.lower().startswith("start"):
                            pass # skip a header line
                        else:
                            items = line.split()
                            self._channels[current_channel].append(Bout(
                                tc.Timecode(self._frame_rate, start_seconds=float(items[0])),
                                tc.Timecode(self._frame_rate, start_seconds=float(items[1])),
                                getattr(self._behaviors, current_bout)))
                        line = f.readline()
            line = f.readline()
        print(f"Done reading Caltech annotation file {f.name}")

    def _read_ethovision(self, f):
        pass

    def channel_names(self):
        return list(self._channels.keys())

    def bouts(self, ch: str) -> [Bout]:
        return self._channels[ch]._bouts

    def sort_channels(self):
        for ch in self._channels:
            self._channels[ch].sort()

    def time_start(self):
        if not self._time_start or not self._frame_rate:
            return tc.Timecode('30.0', '0:0:0:0')
        return tc.Timecode(self._frame_rate, frames=self._time_start)
    
    def time_end(self):
        if not self._time_end or not self._frame_rate:
            return tc.Timecode('30.0', '23:59:59:29')
        return tc.Timecode(self._frame_rate, frames=self._time_end)
    
