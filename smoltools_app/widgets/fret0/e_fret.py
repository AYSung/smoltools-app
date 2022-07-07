from bokeh.models.widgets.tables import NumberFormatter
import pandas as pd
import panel as pn
import panel.widgets as pnw

from smoltools import fret0


def make_e_fret_table(df: pd.DataFrame, r0: float, cutoff: float) -> pnw.DataFrame:
    e_fret_table = pnw.DataFrame(
        value=fret0.e_fret_between_conformations(df, r0).loc[
            lambda x: (x.atom_id_1 < x.atom_id_2) & (x.delta_E_fret >= cutoff),
            [
                'atom_id_1',
                'atom_id_2',
                'E_fret_a',
                'E_fret_b',
                'delta_E_fret',
            ],
        ],
        titles={
            'atom_id_1': 'Res #1',
            'atom_id_2': 'Res #2',
            'E_fret_a': 'E_fret in A',
            'E_fret_b': 'E_fret in B',
            'delta_E_fret': '\u0394E_fret',
        },
        formatters={
            'E_fret_a': NumberFormatter(format='0.00'),
            'E_fret_b': NumberFormatter(format='0.00'),
            'delta_E_fret': NumberFormatter(format='0.00'),
        },
        show_index=False,
        height=500,
    )

    return e_fret_table


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

    return pn.Card(
        r0_input,
        delta_e_fret_cutoff_input,
        pn.Tabs(('Table', e_fret_table)),
        width=622,
        title='Pairwise E_fret',
        collapsible=False,
    )
