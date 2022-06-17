import panel as pn

# from utils import colors, paths


def smoltools_template(title: str) -> pn.template.BootstrapTemplate:
    return pn.template.BootstrapTemplate(
        site='SmolTools',
        title=title,
        # TODO:
        # header_background=colors.DARK_GREY,
        # logo=str(paths.ROOT / 'assets/logo.png'),
        # favicon=str(paths.ROOT / 'assets/favicon.png'),
    )
