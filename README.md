# MiSTer Companion Hub

This repository contains the public catalog metadata used by the MiSTer Companion Hub.

The Hub catalog describes installable or manageable MiSTer-related entries such as scripts, custom cores, extras, ROMs, and wallpaper packs. The catalog controls how entries are displayed in MiSTer Companion. Complex install logic remains inside MiSTer Companion itself through trusted local handlers.

## Categories

- **Scripts**: Add extra functionality to your standard MiSTer FPGA setup through useful scripts and utilities.
- **Cores**: Custom and alternative cores that add features, improve compatibility, or offer different behavior from the standard MiSTer cores.
- **Extras**: MiSTer ARM ports, frontends, and additional tools that expand what your MiSTer setup can do.
- **ROMs**: Free homebrew games and demos for retro systems supported by MiSTer.
- **Wallpaper Packs**: MiSTer wallpaper packs for customizing the look of your MiSTer menu.

## Generated files

The source files live in `items/` and `categories.json`. Wallpaper pack entries point to the existing external automated wallpaper databases instead of duplicating those databases in this repo.

GitHub Actions generates:

- `catalog.json`
- `generated/catalog_full.json`
- `generated/catalog_min.json`
- `generated/categories_with_counts.json`
- `generated/known_handlers.json`
- `generated/wallpaper_sources.json`
- `generated/manifest.json`

MiSTer Companion should normally consume `generated/catalog_full.json` and use `generated/manifest.json` for cache checks.


## Online and Offline Mode

The Hub catalog does not define Online Mode or Offline Mode support per item. Install Center entries are expected to be usable from the app where possible, but the final action availability is decided by MiSTer Companion's local backend handlers. If a script or handler is not available in Offline Mode, that should be handled inside MiSTer Companion, not in this repository.

## Safety model

The GitHub catalog may define presentation metadata and safe download metadata for supported generic item types.

The catalog must not define raw SSH commands, shell commands, Python code, or arbitrary post-install scripts. Scripts, cores, extras, and other complex entries must use a trusted handler that already exists inside MiSTer Companion.


## Images

Install Center entries do not use individual icons. The visual system is based on thumbnails and optional gallery images.

- Thumbnails should be 640x480.
- Custom thumbnails are detected automatically from `assets/thumbnails/<category>/<item_id>.png`, `.jpg`, `.jpeg`, or `.webp`.
- If no custom thumbnail exists, the generated catalog uses the category default from `assets/defaults/<category>.png`.
- Gallery images are optional and detected automatically from `assets/gallery/<category>/<item_id>_01.png`, `<item_id>_02.png`, and so on.
- If no gallery images exist, the generated catalog sets `gallery` to an empty list and MiSTer Companion should hide the gallery section.

Source item JSON files should not contain `icon`, `banner`, or manual screenshot fields.

## Wallpaper pack sources

Wallpaper pack contents are not stored in this repository. The Install Center entries only provide display metadata and a `wallpaper_source` object that points to the existing automated wallpaper database ZIP and raw file base URL used by MiSTer Companion.
