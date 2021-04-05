# annot.py
import timecode as tc
from annot.behavior import Behavior
from sortedcontainers import SortedKeyList
from PySide2.QtGui import QColor

class Bout(object):
    """
    """

    def __init__(self, start, end, behavior):
        self._start = start
        self._end = end
        self._behavior = behavior
    
    def __lt__(self, b):
        if type(b) is tc.Timecode:
            return self._start.float < b.float
        elif type(b) is Bout:
            return self._start < b._start
        else:
            raise NotImplementedError(f"Comparing Bout with {type(b)} not supported")

    def __le__(self, b):
        if type(b) is tc.Timecode:
            return self._start.float <= b.is_float
        elif type(b) is Bout:
            return self._start <= b._start
        else:
            raise NotImplementedError(f'Comparing Bout with {type(b)} not supported')

    def is_at(self, t):
        return self._start <= t and self._end >= t

    def start(self):
        return self._start

    def set_start(self, start):
        self._start = start

    def end(self):
        return self._end

    def set_end(self, end):
        self._end = end
    
    def len(self):
        return self._end - self._start + tc.Timecode(self._start.framerate, frames=1)

    def name(self):
        return self._behavior.get_name()

    def color(self):
        return self._behavior.get_color()

    def is_visiblel(self):
        return self._behavior.is_visible()

class Channel(object):
    """
    """

    def __init__(self, chan = None):
        if not chan is None:
            self._bouts_by_start = chan._bouts_by_start
            self._bouts_by_end = chan._bouts_by_end
        else:
            self._bouts_by_start = SortedKeyList(key=lambda bout: bout.start().float)
            self._bouts_by_end = SortedKeyList(key=lambda bout: bout.end().float)
        self.cur_ix = 0
        self.fakeFirstBout = Bout(
            tc.Timecode('30.0', '0:0:0:0'),
            tc.Timecode('30.0', '0:0:0:0'),
            Behavior('none', '', QColor.fromRgbF(0., 0., 0.))
        )
        self.fakeLastBout = Bout(
            tc.Timecode('30.0', '23:59:59:29'),
            tc.Timecode('30.0', '23:59:59:29'),
            Behavior('none', '', QColor.fromRgbF(0., 0., 0.))
        )

    def append(self, b):
        if isinstance(b, Bout):
            self._bouts_by_start.add(b)
            self._bouts_by_end.add(b)
        else:
            raise TypeError("Can only append Bout to Channel")
    
    def __add__(self, b):
        self.append(b)

    def _get_next(self, t, sortedlist):
        ix = sortedlist.bisect_key_right(t.float)
        l = len(sortedlist)
        if ix == l:
            return self.fakeLastBout
        return sortedlist[ix]

    def get_next_start(self, t):
        return self._get_next(t, self._bouts_by_start)

    def get_next_end(self, t):
        return self._get_next(t, self._bouts_by_end)

    def _get_prev(self, t, sortedlist):
        ix = sortedlist.bisect_key_left(t.float)
        if ix == 0:
            return self.fakeFirstBout
        return sortedlist[ix-1]

    def get_prev_start(self, t):
        return self._get_prev(t, self._bouts_by_start)

    def get_prev_end(self, t):
        return self._get_prev(t, self._bouts_by_end)

    def get_at(self, t):
        """
        get all bouts that span time t
        """
        return [bout for bout in self._bouts_by_start
            if bout.start().float <= t.float and bout.end().float >= t.float] 

    def __iter__(self):
        return iter(self._bouts_by_start)

    
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
                            is_float = '.' in items[0] or '.' in items[1] or '.' in items[2]
                            self.add_bout(
                                Bout(
                                    tc.Timecode(self._frame_rate, start_seconds=float(items[0])) if is_float
                                        else tc.Timecode(self._frame_rate, frames=int(items[0])),
                                    tc.Timecode(self._frame_rate, start_seconds=float(items[1])) if is_float
                                        else tc.Timecode(self._frame_rate, frames=int(items[1])),
                                    getattr(self._behaviors, current_bout)),
                                current_channel)
                        line = f.readline()
            line = f.readline()
        print(f"Done reading Caltech annotation file {f.name}")

    def _read_ethovision(self, f):
        pass

    def channel_names(self):
        return list(self._channels.keys())

    def channel(self, ch: str) -> Channel:
        return self._channels[ch]

    def add_bout(self, bout, channel):
        self._channels[channel].append(bout)
        if bout.end() > self._time_end:
            self._time_end = bout.end()

    def time_start(self):
        if not self._time_start or not self._frame_rate:
            return tc.Timecode('30.0', '0:0:0:0')
        return tc.Timecode(self._frame_rate, frames=self._time_start)
    
    def time_end(self):
        if not self._time_end or not self._frame_rate:
            return tc.Timecode('30.0', '23:59:59:29')
        return tc.Timecode(self._frame_rate, frames=self._time_end)
    
