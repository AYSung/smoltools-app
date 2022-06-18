import panel as pn
import pandas as pd

from smoltools import fret0

from utils import colors, config
from widgets import pdb_loader
from widgets.fret0 import r0_finder, distance, e_fret


class Dashboard(pn.template.BootstrapTemplate):
    def __init__(self):
        super().__init__(
            site='SmolTools',
            title='Fret0',
            header_background=colors.DARK_GREY,
        )
        self.data = pd.DataFrame()
        self.r0_widget = r0_finder.make_widget()
        self.main.append(
            pn.FlexBox(
                pdb_loader.make_widget(self), self.r0_widget, justify_content='center'
            ),
        )

    def load_analyses(self) -> None:
        self.analyses = pn.FlexBox(
            distance.make_distance_widget(self.data),
            e_fret.make_e_fret_widget(self.data),
            justify_content='center',
        )
        self.main[0][0] = self.analyses

    def load_pdb_files(self, chain_a, chain_b) -> None:
        distances_a = fret0.chain_to_distances(chain_a)
        distances_b = fret0.chain_to_distances(chain_b)

        self.data = fret0.pairwise_distance_between_conformations(
            distances_a, distances_b
        )


def app() -> pn.pane:
    # configure external libraries
    config.configure_panel_extensions()
    config.configure_plotting_libraries()

    return Dashboard().servable()


app()

# TODO: Add Altair plots
# TODO: SASA import
