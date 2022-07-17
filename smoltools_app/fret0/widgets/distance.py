import pandas as pd
import panel as pn
import panel.widgets as pnw
from smoltools import fret0

from common.widgets import table


def make_distance_table(df: pd.DataFrame, cutoff: float) -> pnw.DataFrame:
    distance_table = table.data_table(
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
        height=600,
    )

    return distance_table


def make_distance_heatmap(df: pd.DataFrame, cutoff: float) -> pn.pane.Vega:
    heatmap = fret0.plots.delta_distance_map(df, cutoff=cutoff)
    return pn.pane.Vega(heatmap)


def make_distance_widget(df: pd.DataFrame):
    delta_distance_input = pnw.FloatInput(
        name='\u0394Distance cutoff (\u212B)', value=20
    )

    distance_table = pn.bind(make_distance_table, df=df, cutoff=delta_distance_input)
    distance_heatmap = pn.bind(
        make_distance_heatmap, df=df, cutoff=delta_distance_input
    )

    controls = pn.Row(delta_distance_input, align='center')
    table = pn.FlexBox(distance_table, min_width=720, justify_content='center')
    heatmap = pn.FlexBox(distance_heatmap, min_width=720, justify_content='center')

    # BUG: widgets shift around after first change to parameters
    return pn.Card(
        controls,
        pn.Tabs(
            ('Table', table),
            ('Heatmap', heatmap),
        ),
        width=740,
        height=800,
        title='Pairwise Distances',
        collapsible=False,
    )
