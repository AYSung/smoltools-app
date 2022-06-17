from typing_extensions import Self
import panel as pn
import pandas as pd

from smoltools import albatrosy

from utils import colors, config
from widgets import distance, pdb_loader


class Dashboard(pn.template.BootstrapTemplate):
    def __init__(self):
        super().__init__(
            site='SmolTools',
            title='AlbaTROSY',
            header_background=colors.LIGHT_BLUE,
        )
        self.data = pd.DataFrame()
        self.analyses = pn.Column(
            '#### <<< Upload files to analyze', width_policy='max'
        )

    def initialize(self) -> Self:
        self.main.append(
            self.analyses,
        )
        self.sidebar.append(
            pdb_loader.make_widget(self),
        )
        return self

    def load_analyses(self) -> None:
        # TODO: make separate widgets
        self.analyses = pn.Column(
            distance.make_distance_widget(self.data['delta'], cutoff=1),
            pn.Card(
                pn.Tabs(
                    ('Conformation A', albatrosy.plots.noe_map(self.data['a'])),
                    ('Conformation B', albatrosy.plots.noe_map(self.data['b'])),
                    (
                        'Combined',
                        albatrosy.plots.noe_map(
                            albatrosy.splice_conformation_tables(
                                self.data['a'], self.data['b']
                            )
                        ),
                    ),
                ),
                title='NOE Maps',
                collapsible=False,
                sizing_mode='stretch_width',
            ),
            pn.Card(
                pn.Tabs(
                    ('Conformation A', albatrosy.plots.distance_map(self.data['a'])),
                    ('Conformation B', albatrosy.plots.distance_map(self.data['b'])),
                    (
                        '\u0394Distance',
                        albatrosy.plots.delta_distance_map(self.data['delta']),
                    ),
                ),
                title='Distance Maps',
                collapsible=False,
                sizing_mode='stretch_width',
            ),
            pn.Card(
                pn.pane.Vega(albatrosy.plots.distance_scatter(self.data['delta'], 15)),
                title='Distance Scatter',
                collapsible=False,
                sizing_mode='stretch_width',
            ),
            width_policy='max',
        )
        self.main[0][0] = self.analyses

    def load_pdb_files(self, chain_a, chain_b) -> None:
        distances_a = albatrosy.chain_to_distances(chain_a)
        distances_b = albatrosy.chain_to_distances(chain_b)
        delta_distances = albatrosy.pairwise_distance_between_conformations(
            distances_a, distances_b
        )

        self.data = {
            'a': distances_a,
            'b': distances_b,
            'delta': delta_distances,
        }


def app() -> pn.pane:
    # configure external libraries
    config.configure_panel_extensions()
    config.configure_plotting_libraries()

    dashboard = Dashboard().initialize()
    return dashboard.servable()


app()

# TODO: SASA import
# TODO: altair heatmaps
