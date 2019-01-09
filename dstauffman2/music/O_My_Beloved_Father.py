# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 21:59:34 2017

@author: DStauffman
"""

#%% Imports
import abjad as ab

#%% Script
if __name__ == '__main__':
    pass

    #%% Score
    score = ab.Score([])
    staff = ab.Staff([])
    time_signature = ab.TimeSignature((6, 8))
    ab.attach(time_signature, staff)
    score.append(staff)

    #%% Notes
    measures = [ \
        "c''8 c''8 c''8 e''4 b'8", \
        "a'4. g'4.", \
        "c''8 d''8 e''8 c''4 c'''8", \
        "g''4. g''4 e''8", \
        "g''4 d''8 f''4 e''8", \
        "c''4. c''4 c''8", \
        "c''8 d''8 e''8 c''4 b'8", \
        "d''4. d''4 g'8", \
        "c''4. e''8 d''8 c''8", \
        "a'4. g'4.", \
        "c''8 d''8 e''8 c''4 c'''8", \
        "g''4. g''4 a''8", \
        "c'''4 a''8 g''4 f''8", \
        "g''4. e''4.", \
        "c''8 d''8 e''8 c''4 a'8", \
        "c''4. c''8 r8 a''8", \
        "c'''4 a''8 g''4 f''8", \
        "c'''4 g''8 f''4 e''8", \
        "a''2.", \
        "a''4 f''8 e''4 d''8", \
        "c''4 r8 r4.", \
        "c''8 d''8 e''8 c''4 c'''8", \
        "g''4. g''4.", \
        "c''8 d''8 e''8 c''4 a'8", \
        "c''4 r8 r4.", \
        "r2."]
    measures = [ab.Measure((6, 8), x) for x in measures if x]
    staff.extend(measures)
    ab.show(score)

    #%% Details
#    dynamic = ab.Dynamic('pp')
#    ab.attach(dynamic, upper_measures[0][0])
#
#    dynamic = ab.Dynamic('mp')
#    ab.attach(dynamic, upper_measures[1][1])
#
#    dynamic = ab.Dynamic('pp')
#    ab.attach(dynamic, lower_measures[0][1])
#
#    dynamic = ab.Dynamic('mp')
#    ab.attach(dynamic, lower_measures[1][3])
#
#    score.add_final_bar_line()
#
#    # make look like Bartok beams
#    upper_leaves = list(ab.iterate(upper_staff).by_leaf())
#    lower_leaves = list(ab.iterate(lower_staff).by_leaf())
#
#    beam = ab.Beam()
#    ab.attach(beam, upper_leaves[:4])
#
#    beam = ab.Beam()
#    ab.attach(beam, lower_leaves[1:5])
#
#    beam = ab.Beam()
#    ab.attach(beam, lower_leaves[6:10])
#
#    # Now some slurs:
#    slur = ab.Slur()
#    ab.attach(slur, upper_leaves[:5])
#
#    slur = ab.Slur()
#    ab.attach(slur, upper_leaves[5:])
#
#    slur = ab.Slur()
#    ab.attach(slur, lower_leaves[1:6])
#
#    # Hairpins:
#    crescendo = ab.Crescendo()
#    ab.attach(crescendo, upper_leaves[-7:-2])
#
#    decrescendo = ab.Decrescendo()
#    ab.attach(decrescendo, upper_leaves[-2:])
#
#    # A ritardando marking above the last seven notes of the upper staff:
#    markup = ab.Markup('ritard.')
#    text_spanner = ab.spannertools.TextSpanner()
#    ab.override(text_spanner).text_spanner.bound_details__left__text = markup
#    ab.attach(text_spanner, upper_leaves[-7:])
#
#    # And ties connecting the last two notes in each staff:
#    tie = ab.Tie()
#    ab.attach(tie, upper_leaves[-2:])
#
#    note_1 = lower_staff[-2]['upper voice'][0]
#    note_2 = lower_staff[-1]['upper voice'][0]
#    notes = [note_1, note_2]
#    tie = ab.Tie()
#    ab.attach(tie, notes)
#
#    # The final result:
#    ab.show(score)
