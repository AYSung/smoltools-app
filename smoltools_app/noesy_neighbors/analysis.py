from Bio.PDB.Chain import Chain
import pandas as pd
import panel as pn
from smoltools import noesy_neighbors

from noesy_neighbors.widgets import distance, noe_map, scatter


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
    coords_a = noesy_neighbors.coordinates_from_chain(chain_a, labeled_atoms)
    coords_b = noesy_neighbors.coordinates_from_chain(chain_b, labeled_atoms)

    distances_a = noesy_neighbors.pairwise_distances(coords_a)
    distances_b = noesy_neighbors.pairwise_distances(coords_b)
    delta_distances = noesy_neighbors.pairwise_distances(coords_a, coords_b)

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
    distances_a = noesy_neighbors.coordinates_from_chain(chain_a, mode).pipe(
        noesy_neighbors.pairwise_distances
    )
    distances_b = noesy_neighbors.coordinates_from_chain(chain_b, mode).pipe(
        noesy_neighbors.pairwise_distances
    )

    delta_distances = noesy_neighbors.pairwise_distances_between_conformations(
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
