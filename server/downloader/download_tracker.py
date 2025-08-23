import time

def _human_readable_size(byte_count):
    if byte_count < 1024:
        return f"{byte_count:.2f} B"
    elif byte_count < 1024 * 1024:
        return f"{byte_count / 1024:.2f} KB"
    elif byte_count < 1024 * 1024 * 1024:
        return f"{byte_count / 1024 / 1024:.2f} MB"
    else:
        return f"{byte_count / 1024 / 1024 / 1024:.2f} GB"

class SpeedTracker:
    def __init__(self):
        self._records = []
        self._window_size = 60

    def add_bytes_downloaded(self, bytes_downloaded):
        current_time = time.time()
        self._records.append((current_time, bytes_downloaded))
        self._clean_old_records()

    def human_readable_speed(self):
        self._clean_old_records()
        if not self._records:
            return "0 B/s"

        if len(self._records) == 1:
            return f"<{_human_readable_size(self._records[0][1] / self._window_size)}/s"

        total_bytes = sum(record[1] for record in self._records[1:])
        time_span = self._records[-1][0] - self._records[0][0]

        return f"{_human_readable_size(total_bytes / time_span)}/s"

    def _clean_old_records(self):
        current_time = time.time()
        cutoff_time = current_time - self._window_size
        while self._records and self._records[0][0] < cutoff_time:
            self._records.pop(0)

class SizeTracker:
    def __init__(self, slice_count):
        self._slices = []
        self._slice_count = slice_count
        self._slice_downloaded = 0

    def add_slice(self, slice_bytes):
        if self._slices:
            self._slices[-1] = self._slice_downloaded
        self._slices.append(slice_bytes)
        self._slice_downloaded = 0

    def add_bytes_downloaded(self, bytes_downloaded):
        self._slice_downloaded += bytes_downloaded

    def total_size(self):
        if self._slices[-1] is None:
            if len(self._slices) > 1:
                return self._slice_count * sum(self._slices[:-1]) / (len(self._slices) - 1)
            else:
                return None
        return self._slice_count * sum(self._slices) / len(self._slices)

    def total_downloaded(self):
        return sum(self._slices[:-1]) + self._slice_downloaded

    def is_expected_size(self):
        return self._slice_count > len(self._slices) or self._slices[-1] is None

    def human_readable_size(self):
        if len(self._slices) == 0:
            return f"0 / Nan 0%"
        total_size = self.total_size()
        total_downloaded = self.total_downloaded()
        is_expected_size = self.is_expected_size()
        if total_size is None:
            return f"{_human_readable_size(total_downloaded)} / Nan Nan%"
        return f"{_human_readable_size(total_downloaded)} / {_human_readable_size(total_size)} " \
            f"({total_downloaded/total_size*100:.2f}%)" \
            f"{' (expected)' if is_expected_size else ''}"

class DownloadTracker:
    def __init__(self, slice_count):
        self._speed_tracker = SpeedTracker()
        self._size_tracker = SizeTracker(slice_count)

    def add_slice(self, slice_bytes):
        self._size_tracker.add_slice(slice_bytes)

    def add_bytes_downloaded(self, bytes_downloaded):
        self._speed_tracker.add_bytes_downloaded(bytes_downloaded)
        self._size_tracker.add_bytes_downloaded(bytes_downloaded)

    def human_readable_speed(self):
        return self._speed_tracker.human_readable_speed()

    def human_readable_size(self):
        return self._size_tracker.human_readable_size()

    def human_readable(self):
        return f"Speed: {self.human_readable_speed()} Downloaded: {self.human_readable_size()}"

if __name__ == "__main__":
    tracker = DownloadTracker(1)
    tracker.add_slice(1000)
    tracker.add_bytes_downloaded(100)
    print(tracker.human_readable())
    time.sleep(1)
    tracker.add_bytes_downloaded(100)
    print(tracker.human_readable())
    time.sleep(1)
    tracker.add_bytes_downloaded(100)
    print(tracker.human_readable())
