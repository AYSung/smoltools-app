import panel as pn
import pandas as pd

from smoltools import albatrosy

from utils import colors, config
from widgets import pdb_loader
from widgets.albatrosy import distance, noe_map, scatter


class Dashboard(pn.template.BootstrapTemplate):
    def __init__(self, **params):
        super().__init__(
            site='SmolTools',
            title='AlbaTROSY monomer',
            header_background=colors.LIGHT_BLUE,
            **params,
            # TODO: logo and favicon
        )
        self.data = pd.DataFrame()
        self.main.append(
            pn.FlexBox(
                pdb_loader.PDBLoader(self),
                justify_content='center',
            )
        )

    def load_pdb_files(self, chain_a, chain_b) -> None:
        distances_a = albatrosy.coordinates_from_chain(chain_a).pipe(
            albatrosy.pairwise_distances
        )
        distances_b = albatrosy.coordinates_from_chain(chain_b).pipe(
            albatrosy.pairwise_distances
        )
        delta_distances = albatrosy.pairwise_distances_between_conformations(
            distances_a, distances_b
        )

        self.data = {
            'a': distances_a,
            'b': distances_b,
            'delta': delta_distances,
        }

    def load_analyses(self) -> None:
        self.analyses = [
            distance.make_distance_widget(self.data),
            noe_map.make_noe_widget(self.data),
            scatter.make_distance_scatter_widget(self.data),
        ]

    def show_analyses(self) -> None:
        self.main[0].objects = self.analyses


def app() -> pn.pane:
    # configure external libraries
    config.configure_panel_extensions()
    config.configure_plotting_libraries()

    return Dashboard().servable()


app()
