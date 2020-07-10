r"""
Script provides an example for how to use bartok and abjad.

Notes
-----
#.  Written by David C. Stauffer in April 2017.
"""

#%% Imports
import copy

import abjad as ab

#%% Script
if __name__ == '__main__':
    pass

    #%% Score
    # create staves
    score = ab.Score([])
    piano_staff = ab.scoretools.StaffGroup([], context_name='PianoStaff')
    upper_staff = ab.Staff([])
    lower_staff = ab.Staff([])

    piano_staff.append(upper_staff)
    piano_staff.append(lower_staff)
    score.append(piano_staff)

    #%% Measures
    # add some measures
    upper_measures = []
    upper_measures.append(ab.Measure((2, 4), []))
    upper_measures.append(ab.Measure((3, 4), []))
    upper_measures.append(ab.Measure((2, 4), []))
    upper_measures.append(ab.Measure((2, 4), []))
    upper_measures.append(ab.Measure((2, 4), []))

    lower_measures = copy.deepcopy(upper_measures)

    upper_staff.extend(upper_measures)
    lower_staff.extend(lower_measures)

    #%% Notes
    # add notes
    upper_measures[0].extend("a'8 g'8 f'8 e'8")
    upper_measures[1].extend("d'4 g'8 f'8 e'8 d'8")
    upper_measures[2].extend("c'8 d'16 e'16 f'8 e'8")
    upper_measures[3].append("d'2")
    upper_measures[4].append("d'2")

    # first 3 measures have only one voice
    lower_measures[0].extend("b4 d'8 c'8")
    lower_measures[1].extend("b8 a8 af4 c'8 bf8")
    lower_measures[2].extend("a8 g8 fs8 g16 a16")

    # use LilyPond \voiceOne and \voiceTwo commansd for stem directions,
    # and set is_simltaneous for last two measures.
    upper_voice = ab.Voice("b2", name='upper voice')
    command = ab.indicatortools.LilyPondCommand('voiceOne')
    ab.attach(command, upper_voice)
    lower_voice = ab.Voice("b4 a4", name='lower voice')
    command = ab.indicatortools.LilyPondCommand('voiceTwo')
    ab.attach(command, lower_voice)
    lower_measures[3].extend([upper_voice, lower_voice])
    lower_measures[3].is_simultaneous = True

    upper_voice = ab.Voice("b2", name='upper voice')
    command = ab.indicatortools.LilyPondCommand('voiceOne')
    ab.attach(command, upper_voice)
    lower_voice = ab.Voice("g2", name='lower voice')
    command = ab.indicatortools.LilyPondCommand('voiceTwo')
    ab.attach(command, lower_voice)
    lower_measures[4].extend([upper_voice, lower_voice])
    lower_measures[4].is_simultaneous = True

    ab.show(score)

    #%% Details
    clef = ab.Clef('bass')
    ab.attach(clef, lower_staff)

    dynamic = ab.Dynamic('pp')
    ab.attach(dynamic, upper_measures[0][0])

    dynamic = ab.Dynamic('mp')
    ab.attach(dynamic, upper_measures[1][1])

    dynamic = ab.Dynamic('pp')
    ab.attach(dynamic, lower_measures[0][1])

    dynamic = ab.Dynamic('mp')
    ab.attach(dynamic, lower_measures[1][3])

    score.add_final_bar_line()

    # make look like Bartok beams
    upper_leaves = list(ab.iterate(upper_staff).by_leaf())
    lower_leaves = list(ab.iterate(lower_staff).by_leaf())

    beam = ab.Beam()
    ab.attach(beam, upper_leaves[:4])

    beam = ab.Beam()
    ab.attach(beam, lower_leaves[1:5])

    beam = ab.Beam()
    ab.attach(beam, lower_leaves[6:10])

    # Now some slurs:
    slur = ab.Slur()
    ab.attach(slur, upper_leaves[:5])

    slur = ab.Slur()
    ab.attach(slur, upper_leaves[5:])

    slur = ab.Slur()
    ab.attach(slur, lower_leaves[1:6])

    # Hairpins:
    crescendo = ab.Crescendo()
    ab.attach(crescendo, upper_leaves[-7:-2])

    decrescendo = ab.Decrescendo()
    ab.attach(decrescendo, upper_leaves[-2:])

    # A ritardando marking above the last seven notes of the upper staff:
    markup = ab.Markup('ritard.')
    text_spanner = ab.spannertools.TextSpanner()
    ab.override(text_spanner).text_spanner.bound_details__left__text = markup
    ab.attach(text_spanner, upper_leaves[-7:])

    # And ties connecting the last two notes in each staff:
    tie = ab.Tie()
    ab.attach(tie, upper_leaves[-2:])

    note_1 = lower_staff[-2]['upper voice'][0]
    note_2 = lower_staff[-1]['upper voice'][0]
    notes = [note_1, note_2]
    tie = ab.Tie()
    ab.attach(tie, notes)

    # The final result:
    ab.show(score)
