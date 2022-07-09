import panel as pn
import pandas as pd

from smoltools import fret0

from utils import colors, config
from widgets import pdb_loader
from widgets.fret0 import r0_finder, distance, e_fret


class Dashboard(pn.template.BootstrapTemplate):
    def __init__(self, **params):
        super().__init__(
            site='SmolTools',
            title='Fret0',
            header_background=colors.DARK_GREY,
            **params,
            # TODO: logo and favicon
        )
        self.data = pd.DataFrame()
        self.r0_widget = r0_finder.make_widget()
        self.main.append(
            pn.FlexBox(
                pdb_loader.PDBLoader(self), self.r0_widget, justify_content='center'
            ),
        )

    def load_pdb_files(self, chain_a, chain_b) -> None:
        distances_a = fret0.chain_to_distances(chain_a)
        distances_b = fret0.chain_to_distances(chain_b)

        self.data = fret0.pairwise_distances_between_conformations(
            distances_a, distances_b
        )

    def load_analyses(self) -> None:
        self.analyses = [
            distance.make_distance_widget(self.data),
            e_fret.make_e_fret_widget(self.data),
            self.r0_widget,
        ]

    def show_analyses(self) -> None:
        self.main[0].objects = self.analyses


def app() -> pn.pane:
    # configure external libraries
    config.configure_panel_extensions()
    config.configure_plotting_libraries()

    return Dashboard().servable()


app()

# TODO: Add Altair plots
# TODO: SASA import
