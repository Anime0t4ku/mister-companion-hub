# Contributing to MiSTer Companion Hub

## Item requirements

Every entry must include:

- `author`
- `version`, use `null` when not provided
- `release_date`, use `null` when not provided
- `date_added`, stored as a full ISO timestamp
- `description`
- `type`

ROM entries must also include:

- `system`
- `genres`
- `default_install_path`
- `allow_custom_install_path`
- `download.url`
- `download.type`, either `file` or `archive`
- `download.install_extensions` when `download.type` is `archive`

ROMs must be free homebrew, demos, public-domain releases, or developer-approved releases. Do not submit commercial ROMs or copyrighted game files without clear permission.

Do not add Online Mode or Offline Mode metadata to item files. Mode-specific availability is handled by MiSTer Companion's local backend handlers, not by this catalog repository.

## Validation

Run these before opening a pull request:

```bash
python tools/validate_catalog.py
python tools/generate_catalog.py
python tools/validate_catalog.py
```


## Images

Do not add individual icon fields to item JSON files. Install Center entries use thumbnails and optional gallery images only.

Thumbnail rules:

- Recommended size: 640x480.
- Supported formats: PNG, JPG, JPEG, WEBP.
- Filename pattern: `assets/thumbnails/<category>/<item_id>.png` or the same path with another supported extension.
- If no thumbnail is provided, MiSTer Companion uses the default category image from `assets/defaults/`.

Gallery rules:

- Gallery images are optional.
- Filename pattern: `assets/gallery/<category>/<item_id>_01.png`, `<item_id>_02.png`, etc.
- If no gallery images are provided, the gallery section is hidden.

Do not use these fields in item JSON files:

- `icon`
- `banner`
- `screenshots`

## Wallpaper pack entries

Wallpaper pack entries must not include local pack files in this repository. Use `wallpaper_source` to point to the existing automated wallpaper database source. Required fields are:

- `type`: `external_database_zip`
- `database_url`: URL to the zipped wallpaper database JSON
- `raw_base_url`: base URL used to resolve wallpaper files
- `format`: currently `mister_companion_wallpaper_db`

The actual wallpaper database remains in its existing source repository.
