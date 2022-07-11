from Bio.PDB.Chain import Chain
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
            title='AlbaTROSY',
            header_background=colors.LIGHT_BLUE,
            **params,
            # TODO: logo and favicon
        )
        self.pdb_loader_1 = pdb_loader.nmr_conformation_loader(
            upload_function=self.upload_conformation_files
        )
        self.pdb_loader_2 = pdb_loader.nmr_subunit_loader(
            upload_function=self.upload_interchain_files
        )
        self.main.append(
            pn.FlexBox(
                pn.Row(
                    self.pdb_loader_1,
                    pn.Spacer(width=20),
                    pn.Column('**OR**', align='center'),
                    pn.Spacer(width=20),
                    self.pdb_loader_2,
                    align='center',
                ),
                justify_content='center',
            )
        )

    def upload_conformation_files(self, event=None) -> None:
        try:
            chain_a = self.pdb_loader_1.chain_a
            chain_b = self.pdb_loader_1.chain_b
            mode = self.pdb_loader_1.labeling_scheme
            data = load_conformation_data(chain_a, chain_b, mode)

            self.load_conformation_analyses(data)
        except (NoFileSelected, ChainNotFound, NoResiduesFound, NoAtomsFound) as e:
            self.pdb_loader_1.show_error(e)
        else:
            self.pdb_loader_1.upload_success()
            self.show_analyses()

    def load_conformation_analyses(self, data: dict[str, pd.DataFrame]) -> None:
        self.analyses = [
            distance.make_distance_widget(data),
            noe_map.make_monomer_noe_widget(data),
            scatter.make_distance_scatter_widget(data),
        ]

    def upload_interchain_files(self, event=None) -> None:
        try:
            chain_a = self.pdb_loader_2.chain_a
            chain_b = self.pdb_loader_2.chain_b
            mode = self.pdb_loader_2.labeling_scheme
            data = load_interchain_data(chain_a, chain_b, mode)

            self.load_interchain_analyses(data)
        except (NoFileSelected, ChainNotFound, NoResiduesFound, NoAtomsFound) as e:
            self.pdb_loader_2.show_error(e)
        else:
            self.pdb_loader_2.upload_success()
            self.show_analyses()

    def load_interchain_analyses(self, data) -> None:
        self.analyses = [
            noe_map.make_dimer_noe_widget(data),
        ]

    def show_analyses(self) -> None:
        self.main[0].objects = self.analyses


def load_interchain_data(
    chain_a: Chain, chain_b: Chain, mode: str
) -> dict[str, pd.DataFrame]:
    coords_a = albatrosy.coordinates_from_chain(chain_a, mode)
    distances_a = albatrosy.pairwise_distances(coords_a)

    coords_b = albatrosy.coordinates_from_chain(chain_b, mode)
    distances_b = albatrosy.pairwise_distances(coords_b)

    delta_distances = albatrosy.pairwise_distances(coords_a, coords_b)

    return {
        'a': distances_a,
        'b': distances_b,
        'delta': delta_distances,
    }


def load_conformation_data(
    chain_a: Chain, chain_b: Chain, mode: str
) -> dict[str, pd.DataFrame]:
    coords_a = albatrosy.coordinates_from_chain(chain_a, mode)
    distances_a = albatrosy.pairwise_distances(coords_a)

    coords_b = albatrosy.coordinates_from_chain(chain_b, mode)
    distances_b = albatrosy.pairwise_distances(coords_b)

    delta_distances = albatrosy.pairwise_distances_between_conformations(
        distances_a, distances_b
    )

    return {
        'a': distances_a,
        'b': distances_b,
        'delta': delta_distances,
    }


def app() -> pn.pane:
    # configure external libraries
    config.configure_panel_extensions()
    config.configure_plotting_libraries()

    return Dashboard().servable()
