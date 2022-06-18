import pandas as pd
import panel as pn

from smoltools import albatrosy


def make_noe_widget(data: dict[str, pd.DataFrame]) -> pn.Card:
    combined_distances = albatrosy.splice_conformation_tables(data['a'], data['b'])

    noe_map_a = albatrosy.plots.noe_map(data['a'])
    noe_map_b = albatrosy.plots.noe_map(data['b'])
    combined_noe_map = albatrosy.plots.noe_map(combined_distances)

    return pn.Card(
        pn.Tabs(
            ('Combined', pn.pane.Vega(combined_noe_map)),
            ('Conformation A', pn.pane.Vega(noe_map_a)),
            ('Conformation B', pn.pane.Vega(noe_map_b)),
            align='center',
        ),
        title='NOE Maps',
        collapsible=False,
        width=800,
    )
