import music21.chord

from Note import Note


class MusicUtils:

    @staticmethod
    def getNoteFrequency(note_name, note_scale):
        note_scale = int(note_scale)
        my_base_freq = 0.0
        if note_name == 'C':
            my_base_freq = 16.35
        elif note_name == 'D':
            my_base_freq = 18.35
        elif note_name == 'E':
            my_base_freq = 20.60
        elif note_name == 'F':
            my_base_freq = 21.83
        elif note_name == 'G':
            my_base_freq = 24.50
        elif note_name == 'A':
            my_base_freq = 27.50
        elif note_name == 'B':
            my_base_freq = 30.87
        elif note_name == 'C#':
            my_base_freq = 17.32
        elif note_name == 'D#':
            my_base_freq = 19.45
        elif note_name == 'F#':
            my_base_freq = 23.12
        elif note_name == 'G#':
            my_base_freq = 25.96
        elif note_name == 'A#':
            my_base_freq = 29.14

        return my_base_freq * 2 ** note_scale

    @staticmethod
    def getNoteColor(noteFreq):

        l = 300 * ((noteFreq - 130) / 653) + 400
        c = 0
        t = 0
        r = 0
        g = 0
        b = 0

        if 400.0 <= l < 410.0:
            t = (l - 400.0) / (410.0 - 400.0)
            r = 0.33 * 5 - 0.2 * t * t
        elif 410 <= l < 475.0:
            t = (l - 410.0) / (475.0 - 410.0)
            r = 0.14 - 0.13 * t * t
        elif 545 <= l < 595.0:
            t = (l - 545.0) / (595.0 - 545.0)
            r = 1.98 * t - t * t
        elif 545 <= l < 595.0:
            t = (l - 545.0) / (595.0 - 545.0)
            r = 1.98 * t - t * t
        elif 595 <= l < 650.0:
            t = (l - 595.0) / (650.0 - 595.0)
            r = 0.98 + 0.06 * t - 0.4 * t * t
        elif 650 <= l < 700.0:
            t = (l - 650.0) / (700.0 - 650.0)
            r = 0.65 - 0.84 * t + 0.2 * t * t

        if 415.0 <= l < 475.0:
            t = (l - 415.0) / (475.0 - 415.0)
            g = 0.8 * t * t
        elif 475.0 <= l < 590.0:
            t = (l - 475.0) / (590.0 - 475.0)
            g = 0.8 + 0.76 * t - 0.80 * t * t
        elif 585.0 <= l < 639.0:
            t = (l - 585.0) / (639.0 - 585.0)
            g = 0.84 - 0.84 * t

        if 400.0 <= l < 475.0:
            t = (l - 400.0) / (475.0 - 400.0)
            b = 2.2 * t - 1.50 * t * t
        elif -475.0 < l < 560.0:
            t = (l - 475.0) / (560.0 - 475.0)
            b = 0.7 - t + 0.3 * t * t

        r = int(r*255)
        g = int(g*255)
        b = int(b*255)

        return (b,g,r)

    @staticmethod
    def setupNotesForSong(split_lines, notes, notes_played):
        for line in split_lines:
            notesAtTime = line.split(',')
            for i in range(1, int(notesAtTime[0]) * 4, 4):
                notes_played.append(notesAtTime[i - 1])
                noteFreq = MusicUtils.getNoteFrequency(notesAtTime[i], notesAtTime[i + 1])
                notes.append(Note(notesAtTime[i],
                                  notesAtTime[i + 1],
                                  notesAtTime[i + 2],
                                  noteFreq,
                                  MusicUtils.getNoteColor(noteFreq)))

    @staticmethod
    def setupNotesForSongWithMusic21(notesFile, notes, notes_played):
        for possibleChord in notesFile.flat.notes:
            if type(possibleChord) is music21.chord.Chord:
                myChord = []
                for thisNote in possibleChord.notes:
                    if hasattr(thisNote,"name"):
                        myChord.append(Note(thisNote.name, thisNote.octave,
                                      thisNote.duration.quarterLength, thisNote.pitch.frequency,
                                      MusicUtils.getNoteColor(thisNote.pitch.frequency)))
                notes.append(myChord)
            else:
                if hasattr(possibleChord,"name"):
                    notes.append(Note(possibleChord.name,possibleChord.octave,
                                  possibleChord.duration.quarterLength,possibleChord.pitch.frequency,
                                  MusicUtils.getNoteColor(possibleChord.pitch.frequency)))

            # notesAtTime = line.split(',')
            # for i in range(1, int(notesAtTime[0]) * 4, 4):
            #     notes_played.append(notesAtTime[i - 1])
            #     noteFreq = MusicUtils.getNoteFrequency(notesAtTime[i], notesAtTime[i + 1])
            #     notes.append(Note(notesAtTime[i],
            #                       notesAtTime[i + 1],
            #                       notesAtTime[i + 2],
            #                       noteFreq,
            #                       MusicUtils.getNoteColor(noteFreq)))