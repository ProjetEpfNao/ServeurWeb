import tempfile

MAX_BUFFER = 90  # 3 seconds at 30 fps


class Streamer(object):

    def __init__(self, max_buffer=MAX_BUFFER):
        self.frames = []
        self.max_buffer = max_buffer

    def add_frame(self, frame_data):
        new_frame = tempfile.TemporaryFile()
        new_frame.write(frame_data)
        self.frames.append(new_frame)
        if len(self.frames) > self.max_buffer:
            oldest = self.frames.pop(0)
            oldest.close()

    def get_frame(self):
        first_frame = self.frames.pop(0)
        data = first_frame.read()
        first_frame.close()
