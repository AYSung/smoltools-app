import pandas as pd
import panel as pn

from smoltools import albatrosy


def make_distance_scatter_widget(data: dict[str, pd.DataFrame]):
    return pn.Card(
        pn.pane.Vega(albatrosy.plots.distance_scatter(data['delta'], 15)),
        title='Distance Scatter',
        collapsible=False,
        width=800,
    )
