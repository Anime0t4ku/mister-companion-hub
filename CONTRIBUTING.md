# Contributing to MiSTer Companion Hub

## Item requirements

Source item JSON files should contain only necessary catalog metadata. They should not define UI buttons or install behavior.

Every entry must include:

- `schema_version`
- `id`
- `category`
- `type`
- `handler`
- `name`
- `author`
- `date_added`, stored as a full ISO timestamp
- `description`
- `visibility`
- `sort_order`

Optional fields for normal handler-driven entries:

- `version`, only when meaningful
- `release_date`, only when meaningful
- `tags`, only when useful

ROM entries must also include:

- `official_url`, link to the official game page or official download page
- `version`
- `system`
- `genres`
- `default_install_path`
- `allow_custom_install_path`
- `download.url`
- `download.type`, either `file` or `archive`
- `download.install_extensions` when `download.type` is `archive`

ROMs must be free homebrew, demos, public-domain releases, or developer-approved releases. Do not submit commercial ROMs or copyrighted game files without clear permission.

Do not add Online Mode or Offline Mode metadata to item files. Mode-specific availability is handled by MiSTer Companion's local backend handlers, not by this catalog repository.

Do not use these fields in source item JSON files:

- `badges`
- `actions_hint`
- `source_name`
- `source_url`
- `wallpaper_source`
- `supported_modes`
- `mode_notes`
- `icon`
- `banner`
- `screenshots`
- `thumbnail`
- `resolved_thumbnail`
- `gallery`

## Validation

Run these before opening a pull request:

```bash
python tools/validate_catalog.py
python tools/generate_catalog.py
python tools/validate_catalog.py
```

## Images

Do not add individual image fields to item JSON files. Install Center entries use thumbnails and optional gallery images by file convention.

Thumbnail rules:

- Recommended size: 640x480.
- Supported formats: PNG, JPG, JPEG, WEBP.
- Filename pattern: `assets/thumbnails/<category>/<item_id>.png` or the same path with another supported extension.
- If no thumbnail is provided, MiSTer Companion uses `assets/defaults/<category>.png`.

Gallery rules:

- Gallery images are optional.
- Filename pattern: `assets/gallery/<category>/<item_id>_01.png`, `<item_id>_02.png`, etc.
- If no gallery images are provided, the gallery section is hidden.

## Wallpaper pack entries

Wallpaper pack entries are handler-driven like other non-ROM entries. The item JSON should only contain catalog metadata and the `wallpaper_pack` handler.

Wallpaper pack source/database logic belongs in MiSTer Companion's existing wallpaper backend, not in the Hub item JSON.
