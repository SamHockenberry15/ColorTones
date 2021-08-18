
class Note:

    def __init__(self, name, scale, duration, freq, color):
        self.name = name
        self.scale = scale
        self.duration = duration
        self.freq = freq
        self.color = color

    def __str__(self):
        return 'Note Name: ' + self.name + '\n' + 'Note Scale: ' + self.scale + '\n-------------------'
