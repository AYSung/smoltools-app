from typing_extensions import Self
import panel as pn
import pandas as pd

# from templates import template
from utils import colors, config
from widgets import r0_finder, distance, e_fret, pdb_loader
from smoltools import fret0


class Dashboard(pn.template.BootstrapTemplate):
    def __init__(self):
        super().__init__(
            site='SmolTools',
            title='Fret0',
            header_background=colors.DARK_GREY,
        )
        self.data = pd.DataFrame()
        self.analyses = pn.Column()

    def initialize(self) -> Self:
        self.main.append(
            pn.Row(
                self.analyses,
                r0_finder.make_widget(),
            )
        )
        self.sidebar.append(
            pdb_loader.make_widget(self),
        )
        return self

    def load_analyses(self) -> None:
        self.analyses = pn.Column(
            distance.make_distance_widget(self.data),
            e_fret.make_e_fret_widget(self.data),
        )
        self.main[0][0] = self.analyses

    def load_pdb_files(self, chain_a, chain_b) -> None:
        distances_a = fret0.chain_to_distances(chain_a)
        distances_b = fret0.chain_to_distances(chain_b)

        self.data = fret0.pairwise_distance_between_conformations(
            distances_a, distances_b
        )

        self.load_analyses()


def app() -> pn.pane:
    # configure external libraries
    config.configure_panel_extensions()
    config.configure_plotting_libraries()

    return Dashboard().initialize().servable()


app()

# TODO: SASA import
# TODO: altair heatmaps
