from typing_extensions import Self
import panel as pn
import pandas as pd

from smoltools import albatrosy

# from templates import template
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
        self.analyses = pn.Column('<<< Upload files to analyze')

    def initialize(self) -> Self:
        self.main.append(
            self.analyses,
        )
        self.sidebar.append(
            pdb_loader.make_widget(self),
        )
        return self

    def load_analyses(self) -> None:
        self.analyses = pn.Column(distance.make_distance_widget(self.data))
        self.main[0][0] = self.analyses

    def load_pdb_files(self, chain_a, chain_b) -> None:
        distances_a = albatrosy.chain_to_distances(chain_a)
        distances_b = albatrosy.chain_to_distances(chain_b)

        self.data = albatrosy.pairwise_distance_between_conformations(
            distances_a, distances_b
        )


def app() -> pn.pane:
    # configure external libraries
    config.configure_panel_extensions()
    config.configure_plotting_libraries()

    dashboard = Dashboard().initialize()
    return dashboard.servable()


app()

# TODO: SASA import
# TODO: altair heatmaps
