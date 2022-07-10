import panel as pn
import pandas as pd
from smoltools import albatrosy
from smoltools.pdbtools.exceptions import ChainNotFound, NoResiduesFound, NoAtomsFound

from utils import colors, config
from widgets.albatrosy import distance, noe_map, scatter, pdb_loader
from widgets.components.pdb_input import NoFileSelected


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
        self.pdb_loader = pdb_loader.PDBLoader(upload_function=self.upload_files)
        self.main.append(
            pn.FlexBox(
                self.pdb_loader,
                justify_content='center',
            )
        )

    def upload_files(self, event=None) -> None:
        try:
            chain_a = self.pdb_loader.chain_a
            chain_b = self.pdb_loader.chain_b

            self.load_data(chain_a, chain_b)
            self.load_analyses()
        except (NoFileSelected, ChainNotFound, NoResiduesFound, NoAtomsFound) as e:
            self.pdb_loader.show_error(e)
        else:
            self.pdb_loader.upload_success()
            self.show_analyses()

    def load_data(self, chain_a, chain_b) -> None:
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
            noe_map.make_monomer_noe_widget(self.data),
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
