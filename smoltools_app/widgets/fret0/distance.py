from bokeh.models.widgets.tables import NumberFormatter
import pandas as pd
import panel as pn
import panel.widgets as pnw

from smoltools import fret0


def make_distance_table(df: pd.DataFrame, cutoff: float) -> pnw.DataFrame:
    # needs to know too many implementation details?
    return pnw.DataFrame(
        value=df.loc[lambda x: fret0.lower_triangle(x) & (x.delta_distance >= cutoff)],
        titles={
            'id_1': 'Res #1',
            'id_2': 'Res #2',
            'distance_a': 'Distance in A (\u212B)',
            'distance_b': 'Distance in B (\u212B)',
            'delta_distance': '\u0394Distance (\u212B)',
        },
        formatters={
            'distance_a': NumberFormatter(format='0.0'),
            'distance_b': NumberFormatter(format='0.0'),
            'delta_distance': NumberFormatter(format='0.0'),
        },
        show_index=False,
        height=500,
        row_height=30,
        disabled=True,
    )


def make_distance_widget(df: pd.DataFrame, cutoff: float = 20):
    delta_distance_input = pnw.FloatInput(
        name='\u0394Distance cutoff (\u212B)', value=cutoff
    )
    # sasa_input = pnw.FloatSlider(name='SASA cutoff', start=0, end=1.0)

    distance_table = pn.bind(make_distance_table, df=df, cutoff=delta_distance_input)

    return pn.Card(
        delta_distance_input,
        pn.Tabs(('Table', distance_table)),
        width=622,
        title='Pairwise Distances',
        collapsible=False,
    )
