import pandas as pd
import panel as pn

from smoltools import noesy_neighbors

from common.widgets.containers import centered_row


def make_distance_scatter_widget(data: dict[str, pd.DataFrame]):
    distance_scatter = pn.pane.Vega(
        noesy_neighbors.plots.distance_scatter(data['delta'], noe_threshold=15)
    )
    return pn.Card(
        centered_row(distance_scatter),
        title='Distance Scatter',
        collapsible=False,
        width=900,
    )
