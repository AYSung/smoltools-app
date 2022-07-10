import pandas as pd
import panel as pn
import panel.widgets as pnw

from smoltools import fret0
from widgets.components import table


def make_distance_table(df: pd.DataFrame, cutoff: float) -> pnw.DataFrame:
    return table.data_table(
        data=df.loc[lambda x: fret0.lower_triangle(x) & (x.delta_distance >= cutoff)],
        titles={
            'id_1': 'Res #1',
            'id_2': 'Res #2',
            'distance_a': 'Distance in A (\u212B)',
            'distance_b': 'Distance in B (\u212B)',
            'delta_distance': '\u0394Distance (\u212B)',
        },
        formatters={
            'distance_a': '0.0',
            'distance_b': '0.0',
            'delta_distance': '0.0',
        },
    )


def make_distance_heatmap(df: pd.DataFrame, cutoff: float) -> pn.pane.Vega:
    data = df.loc[lambda x: fret0.lower_triangle(x)]
    heatmap = fret0.plots.delta_distance_map(data, cutoff=cutoff)
    return pn.pane.Vega(heatmap)


def make_distance_widget(df: pd.DataFrame, cutoff: float = 20):
    delta_distance_input = pnw.FloatInput(
        name='\u0394Distance cutoff (\u212B)', value=cutoff
    )

    distance_table = pn.bind(make_distance_table, df=df, cutoff=delta_distance_input)
    distance_heatmap = pn.bind(
        make_distance_heatmap, df=df, cutoff=delta_distance_input
    )

    return pn.Card(
        delta_distance_input,
        pn.Tabs(('Table', distance_table), ('Heatmap', distance_heatmap)),
        width=622,
        title='Pairwise Distances',
        collapsible=False,
    )
