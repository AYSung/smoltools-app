from Bio.PDB.Chain import Chain
import panel as pn
import pandas as pd
from smoltools import fret0
from smoltools.pdbtools.exceptions import ChainNotFound, NoResiduesFound, NoAtomsFound

from utils import colors, config
from widgets.fret0 import r0_finder, distance, e_fret, pdb_loader
from widgets.components.pdb_input import NoFileSelected


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
        self.pdb_loader = pdb_loader.FretPDBLoader(upload_function=self.upload_files)
        self.r0_widget = r0_finder.make_widget()
        self.main.append(
            pn.FlexBox(self.pdb_loader, self.r0_widget, justify_content='center'),
        )

    def upload_files(self, event=None) -> None:
        try:
            chain_a = self.pdb_loader.chain_a
            chain_b = self.pdb_loader.chain_b
            use_sasa = self.pdb_loader.use_sasa

            self.load_data(chain_a, chain_b, use_sasa)
            self.load_analyses()
        except (NoFileSelected, ChainNotFound, NoResiduesFound, NoAtomsFound) as e:
            self.pdb_loader.show_error(e)
        else:
            self.pdb_loader.upload_success()
            self.show_analyses()

    def load_data(self, chain_a: Chain, chain_b: Chain, use_sasa: bool) -> None:
        if use_sasa:
            sasa_cutoff = 0.3
        else:
            sasa_cutoff = None

        distances_a = fret0.chain_to_distances(chain_a, sasa_cutoff)
        distances_b = fret0.chain_to_distances(chain_b, sasa_cutoff)

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


# TODO: Add Altair plots
