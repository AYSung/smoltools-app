import panel.widgets as pnw

from common.widgets.pdb_loader import PDBLoader, ConformationInputWidget


def fret_pdb_loader() -> PDBLoader:
    about = """
        Upload structures for two conformations of the same protein to estimate changes in FRET efficiency.
        """
    options_widget = pnw.Checkbox(name='SASA loaded as b-factor')
    return PDBLoader(
        input_widget=ConformationInputWidget(),
        options_widget=options_widget,
        about=about,
    )
