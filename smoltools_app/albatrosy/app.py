from typing import Callable

import panel as pn
from smoltools.pdbtools.exceptions import ChainNotFound, NoResiduesFound, NoAtomsFound

from albatrosy.analysis import run_interchain_analysis, run_conformation_analysis
from albatrosy.widgets import pdb_loader
from common.widgets.pdb_loader import NoFileSelected, PDBLoader
from utils import colors, config


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
