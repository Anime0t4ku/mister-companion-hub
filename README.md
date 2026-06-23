# MiSTer Companion Hub

This repository contains the catalog metadata used by the MiSTer Companion Install Center.

The Hub describes what entries exist and how they should appear in MiSTer Companion. Install, update, uninstall, configure, Online Mode, and Offline Mode behavior stays inside MiSTer Companion through trusted local handlers.

## Categories

- **Scripts**: Add extra functionality to your standard MiSTer FPGA setup through useful scripts and utilities.
- **Cores**: Custom and alternative cores that add features, improve compatibility, or offer different behavior from the standard MiSTer cores.
- **Extras**: MiSTer ARM ports, frontends, and additional tools that expand what your MiSTer setup can do.
- **ROMs**: Free homebrew games and demos for retro systems supported by MiSTer.
- **Wallpaper Packs**: MiSTer wallpaper packs for customizing the look of your MiSTer menu.

## Source JSON

Source item JSON files should stay minimal.

For Scripts, Cores, Extras, and Wallpaper Packs, item JSON only contains display and routing metadata:

- `schema_version`
- `id`
- `category`
- `type`
- `handler`
- `name`
- `author`
- `date_added`
- `description`
- `visibility`
- `sort_order`
- optional `version`, only when meaningful
- optional `release_date`, only when meaningful
- optional `tags`, only when useful

ROM entries are catalog-driven and also include ROM install metadata:

- `official_url`
- `version`
- `system`
- `genres`
- `default_install_path`
- `allow_custom_install_path`
- `download`

Do not add UI action fields such as install buttons, configure buttons, badges, or Online/Offline metadata to item JSON files.

## Generated files

The source files live in `items/` and `categories.json`.

GitHub Actions generates:

- `catalog.json`
- `generated/catalog_full.json`
- `generated/catalog_min.json`
- `generated/categories_with_counts.json`
- `generated/known_handlers.json`
- `generated/manifest.json`

MiSTer Companion should normally consume `generated/catalog_full.json` and use `generated/manifest.json` for cache checks.

## Images

Install Center entries do not use individual icon fields. The visual system is based on thumbnails and optional gallery images.

- Thumbnails should be 640x480.
- Custom thumbnails are detected automatically from `assets/thumbnails/<category>/<item_id>.png`, `.jpg`, `.jpeg`, or `.webp`.
- If no custom thumbnail exists, the generated catalog uses `assets/defaults/<category>.png`.
- Gallery images are optional and detected automatically from `assets/gallery/<category>/<item_id>_01.png`, `<item_id>_02.png`, and so on.
- If no gallery images exist, the generated catalog sets `gallery` to an empty list and MiSTer Companion should hide the gallery section.

Source item JSON files should not contain `icon`, `banner`, `screenshots`, `thumbnail`, `resolved_thumbnail`, or `gallery` fields.
