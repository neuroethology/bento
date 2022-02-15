# annot.py
from random import sample
import timecode as tc
from annot.behavior import Behavior
from sortedcontainers import SortedKeyList
from qtpy.QtCore import QObject, QRectF, Signal, Slot
from qtpy.QtGui import QColor
from qtpy.QtWidgets import QGraphicsItem

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

    def behavior(self):
        return self._behavior

    def name(self):
        return self._behavior.get_name()

    def color(self):
        return self._behavior.get_color()

    def is_active(self):
        return self._behavior.is_active()

    def is_visible(self):
        return self._behavior.is_visible() and self._behavior.is_active()

    def __repr__(self):
        return f"Bout: start = {self.start()}, end = {self.end()}, behavior: {self.behavior()}"

class Channel(QGraphicsItem):
    """
    """

    contentChanged = Signal()

    def __init__(self, chan = None):
        super().__init__()
        if not chan is None:
            self._bouts_by_start = chan._bouts_by_start
            self._bouts_by_end = chan._bouts_by_end
            self._top = chan._top
        else:
            self._bouts_by_start = SortedKeyList(key=lambda bout: bout.start().float)
            self._bouts_by_end = SortedKeyList(key=lambda bout: bout.end().float)
            self._top = 0.
        self.cur_ix = 0
        self.fakeFirstBout = Bout(
            tc.Timecode('30.0', '0:0:0:0'),
            tc.Timecode('30.0', '0:0:0:0'),
            Behavior('none', '', QColor.fromRgbF(0., 0., 0.), active = True)
        )
        self.fakeLastBout = Bout(
            tc.Timecode('30.0', '23:59:59:29'),
            tc.Timecode('30.0', '23:59:59:29'),
            Behavior('none', '', QColor.fromRgbF(0., 0., 0.), active = True)
        )

    def add(self, b):
        if isinstance(b, Bout):
            self._bouts_by_start.add(b)
            self._bouts_by_end.add(b)
        else:
            raise TypeError("Can only add Bouts to Channel")

    def remove(self, b):
        # can raise ValueError if b is not in the channel
        self._bouts_by_start.remove(b)
        self._bouts_by_end.remove(b)

    def update_start(self, b, new_start):
        """
        Update the starting time of a bout while
        preserving the _bouts_by_start access order
        """
        self._bouts_by_start.remove(b)
        b.set_start(new_start)
        self._bouts_by_start.add(b)

    def update_end(self, b, new_end):
        """
        Update the ending time of a bout while
        preserving the _bouts_by_end access order
        """
        self._bouts_by_end.remove(b)
        b.set_end(new_end)
        self._bouts_by_end.add(b)

    def __add__(self, b):
        self.add(b)

    def _get_next(self, t, sortedlist):
        ix = sortedlist.bisect_key_right(t.float)
        l = len(sortedlist)
        if ix == l:
            return self.fakeLastBout, t.next()
        return sortedlist[ix], t.next()

    def _get_prev(self, t, sortedlist):
        ix = sortedlist.bisect_key_left(t.float)
        if ix == 0:
            return self.fakeFirstBout, t.back()
        return sortedlist[ix-1], t.back()

    def _get_inner(self, t, sortedList, op):
        t_local = t + 0 # kludgy copy constructor!
        visible = False
        while not visible:
            # no need to check for the end, because the fake first and last bouts are visible
            bout, t_local = op(t_local, sortedList)
            visible = bout.is_visible()
        return bout

    def get_next_start(self, t):
        return self._get_inner(t, self._bouts_by_start, self._get_next)

    def get_next_end(self, t):
        return self._get_inner(t, self._bouts_by_end, self._get_next)

    def get_prev_start(self, t):
        return self._get_inner(t, self._bouts_by_start, self._get_prev)

    def get_prev_end(self, t):
        return self._get_inner(t, self._bouts_by_end, self._get_prev)

    def get_in_range(self, start, end):
        """
        get all bouts that intersect the range [start, end]
        """
        return [bout for bout in self._bouts_by_start
            if bout.start().float <= end.float and bout.end().float >= start.float]

    def get_at(self, t):
        """
        get all bouts that span time t
        """
        return self.get_in_range(t, t)

    def __iter__(self):
        return iter(self._bouts_by_start)

    def irange(self, start_time, end_time):
        if isinstance(start_time, tc.Timecode):
            start_time = start_time.float
        if isinstance(end_time, tc.Timecode):
            end_time = end_time.float
        if not isinstance(start_time, float):
            raise TypeError(f"Can't handle start_time of type {type(start_time)}")
        if not isinstance(end_time, float):
            raise TypeError(f"Can't handle end_time of type {type(end_time)}")
        return self._bouts_by_start.irange_key(start_time, end_time)

    def top(self):
        return self._top

    def set_top(self, top):
        self._top = top

    def boundingRect(self):
        width = self.fakeLastBout.end().float
        return QRectF(0., self.top(), width, 1.)

    def paint(self, painter, option, widget=None):
        boundingRect = option.rect
        in_range_bouts = self._bouts_by_start.irange_key(boundingRect.left(), boundingRect.right())
        while True:
            try:
                bout = next(in_range_bouts)
            except StopIteration:
                break
            if bout.is_visible():
                painter.fillRect(
                    QRectF(bout.start().float, self.top(), bout.len().float, 1.),
                    bout.color()
                    )

    def _delete_all_inner(self, predicate):
        to_delete = list()
        # can't alter the bouts within the iterator
        for bout in iter(self):
            if predicate(bout):
                to_delete.append(bout)
        deleted_names = set()
        for bout in to_delete:
            deleted_names.add(bout.name())
            self.remove(bout)
        return deleted_names

    def delete_bouts_by_name(self, behavior_name):
        return self._delete_all_inner(lambda bout: bout.name() == behavior_name)

    def delete_inactive_bouts(self):
        return self._delete_all_inner(lambda bout: not bout.is_active())

    def truncate_or_remove_bouts(self, behavior, start, end, delete_all=False):
        """
        Delete bouts entirely within the range [start, end], and
        truncate bouts that extend outside the range.
        If behavior matches _deleteBehavior, the activity affects
        all bouts.  Otherwise, it only affects bouts with matching behavior.
        """
        items = self.get_in_range(start, end)
        for item in items:
            if not delete_all and behavior.get_name() != item.name():
                continue
            # Delete bouts that are entirely within the range
            if item.start() >= start and item.end() < end:
                print(f"removing {item} from active channel")
                self.remove(item)

            # Truncate and duplicate bouts that extend out both sides of the range
            if item.start() < start and item.end() > end:
                self.add(Bout(end, item.end(), item.behavior()))
                self.update_end(item, start)

            # Truncate bouts at the start boundary that start before the range
            elif item.start() < start and item.end() <= end:
                self.update_end(item, start)

            # Truncate bouts at the end boundary that end after the range
            elif item.start() >= start and item.end() > end:
                self.update_start(item, end)

            else:
                print(f"truncate_or_delete_bouts: Unexpected bout {item}")

    def coalesce_bouts(self, start, end):
        """
        combine overlapping bouts of the same behavior within [start, end]
        """
        to_delete = []
        items = self.get_in_range(start, end)
        # items will be ordered by start time
        for ix, first in enumerate(items):
            if first in to_delete:
                # previously coalesced
                continue
            if ix == len(items)-1:
                break
            for second in items[ix+1:]:
                if (first.name() == second.name() and
                    first.end() >= second.start()):
                    if first.end() < second.end():
                        self.update_end(first, second.end())
                    to_delete.append(second)
        for item in to_delete:
            self.remove(item)

class Annotations(QObject):
    """
    """

    # Signals
    annotations_changed = Signal()
    active_annotations_changed = Signal()

    def __init__(self, behaviors):
        super().__init__()
        self._channels = {}
        self._behaviors = behaviors
        self._movies = []
        self._start_frame = None
        self._end_frame = None
        self._sample_rate = None
        self._stimulus = None
        self._format = None
        self.annotation_names = []
        behaviors.behaviors_changed.connect(self.note_annotations_changed)

    def read(self, fn):
        with open(fn, "r") as f:
            line = f.readline()
            line = line.strip().lower()
            if line.endswith("annotation file"):
                self._format = 'Caltech'
                self._read_caltech(f)
            elif line.startswith("scorevideo log"):
                self._format = 'Ethovision'
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
        new_behaviors_activated = False
        reading_channel = False
        to_activate = []
        channel_names = []
        current_channel = None
        current_bout = None

        self._format = 'Caltech'

        line = f.readline()
        while line:
            if found_annotation_names and not new_behaviors_activated:
                self.ensure_and_activate_behaviors(to_activate)
                new_behaviors_activated = True

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
                    self._start_frame = int(items[3])
                    if self._end_frame and self._sample_rate:
                        found_timecode = True
            elif line.lower().startswith("annotation stop frame"):
                items = line.split()
                if len(items) > 3:
                    self._end_frame = int(items[3])
                    if self._start_frame and self._sample_rate:
                        found_timecode = True
            elif line.lower().startswith("annotation framerate"):
                items = line.split()
                if len(items) > 2:
                    self._sample_rate = float(items[2])
                    if self._start_frame and self._end_frame:
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
                    to_activate.append(line)
                    line = f.readline().strip()
                found_annotation_names = True
            elif line.strip().lower().endswith("---"):
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
                                    tc.Timecode(self._sample_rate, start_seconds=float(items[0])) if is_float
                                        else tc.Timecode(self._sample_rate, frames=int(items[0])),
                                    tc.Timecode(self._sample_rate, start_seconds=float(items[1])) if is_float
                                        else tc.Timecode(self._sample_rate, frames=int(items[1])),
                                    self._behaviors.get(current_bout)),
                                current_channel)
                        line = f.readline()
            line = f.readline()
        print(f"Done reading Caltech annotation file {f.name}")
        self.note_annotations_changed()

    def write_caltech(self, f, video_files, stimulus):
        if not f.writable():
            raise RuntimeError("File not writable")
        f.write("Bento annotation file\n")
        f.write("Movie file(s):")
        for file in video_files:
            f.write(' ' + file)
        f.write('\n\n')

        f.write(f"Stimulus name: {stimulus}\n")
        f.write(f"Annotation start frame: {self._start_frame}\n")
        f.write(f"Annotation stop frame: {self._end_frame}\n")
        f.write(f"Annotation framerate: {self._sample_rate}\n")
        f.write("\n")

        f.write("List of Channels:\n")
        for ch in self.channel_names():
            f.write(ch + "\n")
        f.write("\n")

        f.write("List of annotations:\n")
        for annot in self.annotation_names:
            f.write(annot + "\n")
        f.write("\n")

        for ch in self.channel_names():
            by_name = {}
            f.write(f"{ch}----------\n")

            for bout in self.channel(ch):
                if not by_name.get(bout.name()):
                    by_name[bout.name()] = []
                by_name[bout.name()].append(bout)

            for annot in by_name:
                f.write(f">{annot}\n")
                f.write("Start\tStop\tDuration\n")
                for bout in by_name[annot]:
                    start = bout.start().frames
                    end = bout.end().frames
                    f.write(f"{start}\t{end}\t{end - start}\n")
                f.write("\n")

            f.write("\n")

        f.close()
        print(f"Done writing Caltech annotation file {f.name}")

    def _read_ethovision(self, f):
        print("Ethovision annotations not yet supported")

    def clear_channels(self):
        self._channels.clear()

    def channel_names(self):
        return list(self._channels.keys())

    def channel(self, ch: str) -> Channel:
        return self._channels[ch]

    def addEmptyChannel(self, ch: str):
        if ch not in self.channel_names():
            self._channels[ch] = Channel()

    def add_bout(self, bout, channel):
        if bout.name() not in self.annotation_names:
            self.annotation_names.append(bout.name())
        self._channels[channel].add(bout)
        if bout.end() > self.end_time():
            self.set_end_frame(bout.end())

    def start_time(self):
        """
        At some point we will need to support a start time distinct from
        frame number, perhaps derived from the OS file modify time
        or the start time of the corresponding video (or other media) file
        """
        if not self._start_frame or not self._sample_rate:
            return tc.Timecode('30.0', '0:0:0:0')
        return tc.Timecode(self._sample_rate, frames=self._start_frame)

    def start_frame(self):
        return self._start_frame

    def set_start_frame(self, t):
        if isinstance(t, int):
            self._start_frame = t
        elif isinstance(t, tc.Timecode):
            self._start_frame = t.frames
        else:
            raise TypeError("Expected a frame number or Timecode")

    def end_time(self):
        if not self._end_frame or not self._sample_rate:
            return tc.Timecode('30.0', '23:59:59:29')
        return tc.Timecode(self._sample_rate, frames=self._end_frame)

    def end_frame(self):
        return self._end_frame

    def set_end_frame(self, t):
        if isinstance(t, int):
            self._end_frame = t
        elif isinstance(t, tc.Timecode):
            self._end_frame = t.frames
        else:
            raise TypeError("Expected a frame number or Timecode")

    def sample_rate(self):
        return self._sample_rate

    def set_sample_rate(self, sample_rate):
        self._sample_rate = sample_rate

    def format(self):
        return self._format

    def set_format(self, format):
        self._format = format

    def delete_bouts_by_name(self, behavior_name):
        deleted_names = set()
        for chan_name in self.channel_names():
            deleted_names.update(self.channel(chan_name).delete_bouts_by_name(behavior_name))
        for name in deleted_names:
            self.annotation_names.remove(name)

    def delete_inactive_bouts(self):
        deleted_names = set()
        for chan_name in self.channel_names():
            deleted_names.update(self.channel(chan_name).delete_inactive_bouts())
        for name in deleted_names:
            self.annotation_names.remove(name)

    def ensure_and_activate_behaviors(self, toActivate):
        behaviorSetUpdated = False
        for behaviorName in toActivate:
            behaviorSetUpdated |= self._behaviors.addIfMissing(behaviorName)
            self.annotation_names.append(behaviorName)
            self._behaviors.get(behaviorName).set_active(True)
        if behaviorSetUpdated:
            self.annotations_changed.emit()
        self.active_annotations_changed.emit()

    def ensure_active_behaviors(self):
        for behavior in self._behaviors:
            if behavior.is_active() and behavior.get_name() not in self.annotation_names:
                self.annotation_names.append(behavior.get_name())

    def truncate_or_remove_bouts(self, behavior, start, end, chan):
        """
        Delete bouts entirely within the range [start, end], or
        truncate bouts that extend outside the range.
        If behavior matches _deleteBehavior, the activity affects
        all bouts.  Otherwise, it only affects bouts with matching behavior.
        """
        delete_all = (behavior.get_name() == self._behaviors.getDeleteBehavior().get_name())
        self._channels[chan].truncate_or_remove_bouts(behavior, start, end, delete_all)
        self.note_annotations_changed()

    def coalesce_bouts(self, start, end, chan):
        """
        combine overlapping bouts of the same behavior within [start, end]
        """
        self._channels[chan].coalesce_bouts(start, end)
        self.note_annotations_changed()

    @Slot()
    def note_annotations_changed(self):
        self.annotations_changed.emit()