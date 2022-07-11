from Bio.PDB.Chain import Chain
import panel as pn
import pandas as pd
from smoltools import albatrosy
from smoltools.pdbtools.exceptions import ChainNotFound, NoResiduesFound, NoAtomsFound

from utils import colors, config
from widgets.albatrosy import distance, noe_map, scatter, pdb_loader
from widgets.components.pdb_input import NoFileSelected


def run_interchain_analysis(chain_a: Chain, chain_b: Chain, mode: str) -> list[pn.Card]:
    data = load_interchain_data(chain_a, chain_b, mode)
    return load_interchain_analyses(data)


def load_interchain_data(
    chain_a: Chain, chain_b: Chain, mode: str
) -> dict[str, pd.DataFrame]:
    coords_a = albatrosy.coordinates_from_chain(chain_a, mode)
    coords_b = albatrosy.coordinates_from_chain(chain_b, mode)

    distances_a = albatrosy.pairwise_distances(coords_a)
    distances_b = albatrosy.pairwise_distances(coords_b)
    delta_distances = albatrosy.pairwise_distances(coords_a, coords_b)

    return {
        'a': distances_a,
        'b': distances_b,
        'delta': delta_distances,
    }


def load_interchain_analyses(data: dict[str, pd.DataFrame]) -> list[pn.Card]:
    return [
        noe_map.make_dimer_noe_widget(data),
    ]


def run_conformation_analysis(
    chain_a: Chain, chain_b: Chain, mode: str
) -> list[pn.Card]:
    data = load_conformation_data(chain_a, chain_b, mode)
    return load_conformation_analyses(data)


def load_conformation_data(
    chain_a: Chain, chain_b: Chain, mode: str
) -> dict[str, pd.DataFrame]:
    distances_a = albatrosy.coordinates_from_chain(chain_a, mode).pipe(
        albatrosy.pairwise_distances
    )
    distances_b = albatrosy.coordinates_from_chain(chain_b, mode).pipe(
        albatrosy.pairwise_distances
    )

    delta_distances = albatrosy.pairwise_distances_between_conformations(
        distances_a, distances_b
    )

    return {
        'a': distances_a,
        'b': distances_b,
        'delta': delta_distances,
    }


def load_conformation_analyses(data: dict[str, pd.DataFrame]) -> list[pn.Card]:
    return [
        distance.make_distance_widget(data),
        noe_map.make_monomer_noe_widget(data),
        scatter.make_distance_scatter_widget(data),
    ]


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

            analyses = run_conformation_analysis(chain_a, chain_b, mode)
        except (NoFileSelected, ChainNotFound, NoResiduesFound, NoAtomsFound) as e:
            self.pdb_loader_1.show_error(e)
        else:
            self.pdb_loader_1.upload_success()
            self.show_analyses(analyses)

    def upload_interchain_files(self, event=None) -> None:
        try:
            chain_a = self.pdb_loader_2.chain_a
            chain_b = self.pdb_loader_2.chain_b
            mode = self.pdb_loader_2.labeling_scheme

            analyses = run_interchain_analysis(chain_a, chain_b, mode)
        except (NoFileSelected, ChainNotFound, NoResiduesFound, NoAtomsFound) as e:
            self.pdb_loader_2.show_error(e)
        else:
            self.pdb_loader_2.upload_success()
            self.show_analyses(analyses)

    def show_analyses(self, analyses: list[pn.Card]) -> None:
        self.main[0].objects = analyses


def app() -> pn.pane:
    # configure external libraries
    config.configure_panel_extensions()
    config.configure_plotting_libraries()

    return Dashboard().servable()
