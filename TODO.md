<!--
@since 2024.02.21, 16:56
@changed 2024.02.29, 20:36
-->

# TODO

- 2024.02.29, 20:35 -- Use `Site.objects.get_current().name` (via `from django.contrib.sites.models import Site`) as site title.
- 2024.02.29, 03:33 -- Prload visual.
- 2024.02.28, 20:38 -- Use `setup.cfg`.
- 2023.11.28, 04:22 -- Fix `WithSidePanels` side panels behavior on resize. Ideally to use library to support panels resizing.
- 2023.11.28, 03:20 -- Color selector: Remove second slider (transparency?), fix entering the color by text (it's conflicting with immediatley updates).
- 2023.11.27, 16:53 -- Check bundle size. See info at [cra-template/readme](https://github.com/facebook/create-react-app/blob/main/packages/cra-template/template/README.md).
- 2023.11.27, 01:23 -- Clean changed data (names, colors) in `SankeyAppDataStore` on a new data set load.
- 2023.11.24, 02:09 -- To initialize the settings (`SankeySettingsPanel`, `SankeyAppSessionStore`) from the url query.
- 2023.11.24, 02:07 -- To load chart libraries dynamically? (Needs to be ensured that it works in the embedding browser. And to preserve the way to use old approach with static loading.) See `useChartComponent`, `SankeyAppSessionStore`.
