import time

class DownloadSpeedTracker:
    def __init__(self):
        self._records = []
        self._window_size = 60

    def add_bytes_downloaded(self, bytes_downloaded):
        current_time = time.time()
        self._records.append((current_time, bytes_downloaded))
        self._clean_old_records()

    def _human_readable_speed(self, speed):
        if speed < 1024:
            return f"{speed:.2f} B/s"
        elif speed < 1024 * 1024:
            return f"{speed / 1024:.2f} KB/s"
        elif speed < 1024 * 1024 * 1024:
            return f"{speed / 1024 / 1024:.2f} MB/s"
        else:
            return f"{speed / 1024 / 1024 / 1024:.2f} GB/s"

    def get_human_readable_speed(self):
        self._clean_old_records()
        if not self._records:
            return "0 B/s"

        if len(self._records) == 1:
            return f"<{self._human_readable_speed(self._records[0][1] / self._window_size)}"

        total_bytes = sum(record[1] for record in self._records[1:])
        time_span = self._records[-1][0] - self._records[0][0]

        return self._human_readable_speed(total_bytes / time_span)

    def _clean_old_records(self):
        current_time = time.time()
        cutoff_time = current_time - self._window_size
        while self._records and self._records[0][0] < cutoff_time:
            self._records.pop(0)

if __name__ == "__main__":
    tracker = DownloadSpeedTracker()
    tracker.add_bytes_downloaded(100)
    print(tracker.get_human_readable_speed())
    time.sleep(1)
    tracker.add_bytes_downloaded(100)
    print(tracker.get_human_readable_speed())
    time.sleep(1)
    tracker.add_bytes_downloaded(100)
    print(tracker.get_human_readable_speed())
