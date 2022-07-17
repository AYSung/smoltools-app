from Bio.PDB.Chain import Chain
import pandas as pd
import panel as pn
from smoltools import fret0
from smoltools.pdbtools.exceptions import ChainNotFound, NoResiduesFound, NoAtomsFound

from common.widgets.pdb_loader import NoFileSelected
from fret0.widgets import r0_finder, distance, e_fret, pdb_loader
from utils import colors, config


def load_data(chain_a: Chain, chain_b: Chain, use_sasa: bool) -> pd.DataFrame:
    sasa_cutoff = 0.3 if use_sasa else None

    distances_a = fret0.chain_to_distances(chain_a, sasa_cutoff)
    distances_b = fret0.chain_to_distances(chain_b, sasa_cutoff)

    return fret0.pairwise_distances_between_conformations(distances_a, distances_b)


class Dashboard(pn.template.BootstrapTemplate):
    def __init__(self, **params):
        super().__init__(
            site='SmolTools',
            title='Fret0',
            header_background=colors.DARK_GREY,
            **params,
            # TODO: logo and favicon
        )
        self.pdb_loader = pdb_loader.fret_pdb_loader()
        self.pdb_loader.bind_button(self.upload_files)

        self.r0_widget = r0_finder.make_widget()
        self.main.append(
            pn.FlexBox(self.pdb_loader, self.r0_widget, justify_content='center'),
        )

    def upload_files(self, event=None) -> None:
        try:
            chain_a = self.pdb_loader.chain_a
            chain_b = self.pdb_loader.chain_b
            use_sasa = self.pdb_loader.options_value

            data = load_data(chain_a, chain_b, use_sasa)
            analyses = self.load_analyses(data)
        except (NoFileSelected, ChainNotFound, NoResiduesFound, NoAtomsFound) as e:
            self.pdb_loader.show_error(e)
        else:
            self.pdb_loader.upload_success()
            self.show_analyses(analyses)

    def load_analyses(self, data: pd.DataFrame) -> list[pn.Card]:
        return [
            distance.make_distance_widget(data),
            e_fret.make_e_fret_widget(data),
            self.r0_widget,
        ]

    def show_analyses(self, analyses: list[pn.Card]) -> None:
        self.main[0].objects = analyses


def app() -> pn.pane:
    # configure external libraries
    config.configure_panel_extensions()
    config.configure_plotting_libraries()

    return Dashboard().servable()
