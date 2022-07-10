import pandas as pd
import panel as pn
import panel.widgets as pnw

from smoltools import fret0
from widgets.components import table


def make_e_fret_table(df: pd.DataFrame, r0: float, cutoff: float) -> pnw.DataFrame:
    e_fret_table = table.data_table(
        data=fret0.e_fret_between_conformations(df, r0).loc[
            lambda x: fret0.lower_triangle(x) & (x.delta_E_fret >= cutoff)
        ],
        titles={
            'id_1': 'Res #1',
            'id_2': 'Res #2',
            'E_fret_a': 'E_fret in A',
            'E_fret_b': 'E_fret in B',
            'delta_E_fret': '\u0394E_fret',
        },
        formatters={
            'E_fret_a': '0.00',
            'E_fret_b': '0.00',
            'delta_E_fret': '0.00',
        },
        height=600,
    )

    return e_fret_table


def make_e_fret_heatmap(df: pd.DataFrame, r0: float, cutoff: float) -> pn.pane.Vega:
    data = fret0.e_fret_between_conformations(df, r0)
    heatmap = fret0.plots.delta_e_fret_map(data, cutoff=cutoff)
    return pn.pane.Vega(heatmap)


def make_e_fret_widget(df: pd.DataFrame) -> pn.Card:
    r0_input = pnw.FloatInput(name='R0 of FRET pair', value=50)
    delta_e_fret_cutoff_input = pnw.FloatSlider(
        name='\u0394E_fret cutoff', start=0, end=1.0, value=0.5
    )

    e_fret_table = pn.bind(
        make_e_fret_table,
        df=df,
        r0=r0_input,
        cutoff=delta_e_fret_cutoff_input,
    )

    e_fret_heatmap = pn.bind(
        make_e_fret_heatmap,
        df=df,
        r0=r0_input,
        cutoff=delta_e_fret_cutoff_input,
    )

    controls = pn.Row(r0_input, delta_e_fret_cutoff_input, align='center')
    table = pn.FlexBox(e_fret_table, min_width=720, justify_content='center')
    heatmap = pn.FlexBox(e_fret_heatmap, min_width=720, justify_content='center')

    # BUG: widgets shift around after first change to parameters
    return pn.Card(
        controls,
        pn.Tabs(
            ('Table', table),
            ('Heatmap', heatmap),
        ),
        width=740,
        height=800,
        title='Pairwise E_fret',
        collapsible=False,
    )
