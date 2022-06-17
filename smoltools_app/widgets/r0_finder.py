import pandas as pd
import panel as pn
import panel.widgets as pnw

import smoltools.fret0 as fret0


def r0_pair_table() -> pnw.DataFrame:
    fret_pair_table = pnw.DataFrame(
        value=pd.DataFrame(
            data=[('Cy3/Cy5', 50)],
            columns=[
                'fret_pair',
                'r0',
            ],
        ),
        titles={
            'fret_pair': 'FRET Pair',
            'r0': 'R0 (\u212B)',
        },
        show_index=False,
        width=200,
        height=200,
    )

    return fret_pair_table


def make_widget() -> pn.Card:
    distance_a_input = pnw.FloatInput(
        name='Distance in A', start=10, end=100, value=51.1, width=120
    )
    distance_b_input = pnw.FloatInput(
        name='Distance in B', start=10, end=100, value=29.7, width=120
    )

    chart = pn.bind(
        fret0.plots.r0_curves,
        distance_a=distance_a_input,
        distance_b=distance_b_input,
    )

    table = r0_pair_table()

    return pn.Card(
        pn.Row(distance_a_input, distance_b_input, align='center'),
        pn.Row(chart, align='center'),
        pn.Row(table, align='center'),
        title='R0 finder',
    )
