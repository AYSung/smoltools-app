import pandas as pd
import panel as pn
import panel.widgets as pnw
from smoltools import noesy_neighbors

from common.widgets import table
from common.widgets.containers import centered_row


def make_distance_table(df: pd.DataFrame) -> pnw.DataFrame:
    return table.data_table(
        data=df.loc[
            lambda x: noesy_neighbors.lower_triangle(x) & (x.delta_distance > 0)
        ],
        titles={
            'id_1': 'Atom #1',
            'id_2': 'Atom #2',
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


def make_distance_widget(data: dict[str, pd.DataFrame]):
    distance_table = make_distance_table(data['delta'])

    distance_map_a = pn.pane.Vega(noesy_neighbors.plots.distance_map(data['a']))
    distance_map_b = pn.pane.Vega(noesy_neighbors.plots.distance_map(data['b']))
    delta_distance_map = pn.pane.Vega(
        noesy_neighbors.plots.delta_distance_map(data['delta'])
    )

    return pn.Card(
        pn.Tabs(
            ('\u0394Distance', centered_row(delta_distance_map)),
            ('Conformation A', centered_row(distance_map_a)),
            ('Conformation B', centered_row(distance_map_b)),
            ('Table', centered_row(distance_table)),
            align='center',
        ),
        title='Pairwise Distances',
        collapsible=False,
        width=900,
    )
