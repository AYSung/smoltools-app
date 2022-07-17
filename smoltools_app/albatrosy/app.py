from typing import Callable

from Bio.PDB.Chain import Chain
import panel as pn
import pandas as pd
from smoltools import albatrosy
from smoltools.pdbtools.exceptions import ChainNotFound, NoResiduesFound, NoAtomsFound

from utils import colors, config
from albatrosy.widgets import distance, noe_map, scatter, pdb_loader
from common.widgets.pdb_loader import NoFileSelected, PDBLoader


def run_interchain_analysis(
    chain_a: Chain, chain_b: Chain, labeled_atoms: dict[str, list[str]]
) -> list[pn.Card]:
    data = load_interchain_data(chain_a, chain_b, labeled_atoms)
    return load_interchain_analyses(data)


def _get_chain_id(chain: Chain) -> str:
    structure_id = chain.get_parent().get_parent().get_id()
    model_id = chain.get_parent().get_id()
    chain_id = chain.get_id()
    return f'{structure_id}/{model_id}/{chain_id}'


def load_interchain_data(
    chain_a: Chain, chain_b: Chain, labeled_atoms: dict[str, list[str]]
) -> dict[str, pd.DataFrame]:
    coords_a = albatrosy.coordinates_from_chain(chain_a, labeled_atoms)
    coords_b = albatrosy.coordinates_from_chain(chain_b, labeled_atoms)

    distances_a = albatrosy.pairwise_distances(coords_a)
    distances_b = albatrosy.pairwise_distances(coords_b)
    delta_distances = albatrosy.pairwise_distances(coords_a, coords_b)

    return {
        'a': distances_a,
        'b': distances_b,
        'delta': delta_distances,
        'chain_a_id': _get_chain_id(chain_a),
        'chain_b_id': _get_chain_id(chain_b),
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
        'chain_a_id': _get_chain_id(chain_a),
        'chain_b_id': _get_chain_id(chain_b),
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
        self.pdb_loader_1 = pdb_loader.nmr_conformation_loader()
        self.pdb_loader_1.bind_button(self.upload_conformation_files)

        self.pdb_loader_2 = pdb_loader.nmr_subunit_loader()
        self.pdb_loader_2.bind_button(self.upload_interchain_files)

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

    def _upload_files(self, pdb_loader: PDBLoader, analysis_function: Callable):
        try:
            chain_a = pdb_loader.chain_a
            chain_b = pdb_loader.chain_b
            mode = pdb_loader.options_value

            analyses = analysis_function(chain_a, chain_b, mode)
        except (NoFileSelected, ChainNotFound, NoResiduesFound, NoAtomsFound) as e:
            pdb_loader.show_error(e)
        else:
            pdb_loader.upload_success()
            self.show_analyses(analyses)

    def upload_conformation_files(self, event=None) -> Callable:
        self._upload_files(
            pdb_loader=self.pdb_loader_1,
            analysis_function=run_conformation_analysis,
        )

    def upload_interchain_files(self, event=None) -> Callable:
        self._upload_files(
            pdb_loader=self.pdb_loader_2,
            analysis_function=run_interchain_analysis,
        )

    def show_analyses(self, analyses: list[pn.Card]) -> None:
        self.main[0].objects = analyses


def app() -> pn.pane:
    # configure external libraries
    config.configure_panel_extensions()
    config.configure_plotting_libraries()

    return Dashboard().servable()
