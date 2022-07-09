from bokeh.models.widgets.tables import NumberFormatter
import pandas as pd
import panel as pn
import panel.widgets as pnw
from smoltools import albatrosy

from widgets.components import table


def make_distance_table(df: pd.DataFrame) -> pnw.DataFrame:
    return table.data_table(
        data=df.loc[lambda x: albatrosy.lower_triangle(x) & (x.delta_distance > 0)],
        titles={
            'atom_id_1': 'Res #1',
            'atom_id_2': 'Res #2',
            'distance_a': 'Distance in A (\u212B)',
            'distance_b': 'Distance in B (\u212B)',
            'delta_distance': '\u0394Distance (\u212B)',
        },
        formatters={
            'distance_a': NumberFormatter(format='0.0'),
            'distance_b': NumberFormatter(format='0.0'),
            'delta_distance': NumberFormatter(format='0.0'),
        },
    )


def make_distance_widget(data: dict[str, pd.DataFrame]):
    distance_table = make_distance_table(data['delta'])

    distance_map_a = albatrosy.plots.distance_map(data['a'])
    distance_map_b = albatrosy.plots.distance_map(data['b'])
    delta_distance_map = albatrosy.plots.delta_distance_map(data['delta'])

    binned_distance_map = albatrosy.plots.binned_distance_map(data['a'], bin_size=20)

    return pn.Card(
        pn.Tabs(
            ('\u0394Distance', pn.pane.Vega(delta_distance_map)),
            ('Conformation A', pn.pane.Vega(distance_map_a)),
            ('Conformation B', pn.pane.Vega(distance_map_b)),
            ('Table', pn.Row(distance_table, align='center')),
            ('Binned (beta)', pn.pane.Vega(binned_distance_map)),
            align='center',
        ),
        title='Pairwise Distances',
        collapsible=False,
        width=800,
    )
