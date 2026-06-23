#!/usr/bin/env python3
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_CATEGORIES = {"scripts", "cores", "extras", "roms", "wallpaper_packs"}
ALLOWED_TYPES = {"script", "core", "extra", "rom", "wallpaper_pack"}
ALLOWED_VISIBILITY = {"public", "hidden", "dev_only", "deprecated"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}

ALLOWED_HANDLERS = {
    "update_all", "zaparoo", "migrate_sd", "cifs_mount", "auto_time", "cd_game_organizer",
    "dav_browser", "ftp_save_sync", "static_wallpaper", "syncthing", "ra_viewer",
    "mms2_gb_core", "paprium_megadrive", "retroachievement_cores",
    "3s_arm", "sonic_mania_mister", "zaparoo_frontend", "wallpaper_pack", "rom_install",
}

BASE_ALLOWED_ITEM_FIELDS = {
    "schema_version", "id", "category", "type", "handler", "name", "author",
    "version", "release_date", "date_added", "description", "tags", "visibility", "sort_order",
}
ROM_ALLOWED_FIELDS = {
    "official_url", "system", "genres", "default_install_path", "allow_custom_install_path", "download",
}
FORBIDDEN_FIELDS = {
    "icon", "banner", "screenshots", "supported_modes", "mode_notes",
    "badges", "actions_hint", "source_name", "source_url", "wallpaper_source",
    "thumbnail", "resolved_thumbnail", "gallery",
}


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ValueError(f"{path}: invalid JSON: {exc}") from exc


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate_date_added(value, path):
    require(isinstance(value, str) and value, f"{path}: date_added is required")
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{path}: date_added must be ISO date-time, got {value!r}") from exc


def validate_item(path: Path, categories):
    item = load_json(path)
    required = ["schema_version", "id", "category", "type", "handler", "name", "author", "date_added", "description", "visibility", "sort_order"]
    for key in required:
        require(key in item, f"{path}: missing required field {key}")

    item_type = item.get("type")
    allowed_fields = set(BASE_ALLOWED_ITEM_FIELDS)
    if item_type == "rom":
        allowed_fields |= ROM_ALLOWED_FIELDS
    extra_fields = set(item) - allowed_fields
    require(not extra_fields, f"{path}: unnecessary/unsupported field(s): {', '.join(sorted(extra_fields))}")
    for forbidden in FORBIDDEN_FIELDS:
        require(forbidden not in item, f"{path}: {forbidden} belongs in MiSTer Companion or generated output, not source item JSON")

    require(item["schema_version"] == 1, f"{path}: schema_version must be 1")
    require(item["category"] in categories, f"{path}: unknown category {item['category']!r}")
    require(item["category"] in ALLOWED_CATEGORIES, f"{path}: unsupported category {item['category']!r}")
    require(item["type"] in ALLOWED_TYPES, f"{path}: unsupported type {item['type']!r}")
    require(item["handler"] in ALLOWED_HANDLERS, f"{path}: unknown handler {item['handler']!r}")
    require(item["visibility"] in ALLOWED_VISIBILITY, f"{path}: invalid visibility")
    require(isinstance(item["description"], str) and item["description"].strip(), f"{path}: description is required")
    require(isinstance(item["author"], str) and item["author"].strip(), f"{path}: author is required")
    require(isinstance(item["sort_order"], int), f"{path}: sort_order must be an integer")
    validate_date_added(item["date_added"], path)

    if "tags" in item:
        tags = item["tags"]
        require(isinstance(tags, list), f"{path}: tags must be a list")
        for tag in tags:
            require(isinstance(tag, str) and tag.strip(), f"{path}: tags must be non-empty strings")
    if "release_date" in item:
        try:
            datetime.strptime(item["release_date"], "%Y-%m-%d")
        except ValueError as exc:
            raise ValueError(f"{path}: release_date must be YYYY-MM-DD") from exc
    if "version" in item:
        require(isinstance(item["version"], str) and item["version"].strip(), f"{path}: version must be a non-empty string when present")

    if item["type"] == "rom":
        for key in ["version", "official_url", "system", "genres", "default_install_path", "allow_custom_install_path", "download"]:
            require(key in item, f"{path}: ROM item requires {key}")
        require(isinstance(item["official_url"], str) and item["official_url"].strip(), f"{path}: ROM official_url is required")
        require(isinstance(item.get("system"), str) and item["system"].strip(), f"{path}: ROM system is required")
        genres = item.get("genres")
        require(isinstance(genres, list) and genres, f"{path}: ROM genres must be a non-empty list")
        for genre in genres:
            require(isinstance(genre, str) and genre.strip(), f"{path}: ROM genre entries must be non-empty strings")
        install_path = item.get("default_install_path")
        require(isinstance(install_path, str) and install_path.startswith("/games/"), f"{path}: ROM default_install_path must be MiSTer-relative, for example /games/NES")
        require(isinstance(item.get("allow_custom_install_path"), bool), f"{path}: ROM allow_custom_install_path must be true or false")
        download = item.get("download")
        require(isinstance(download, dict), f"{path}: ROM download must be an object")
        require(set(download) <= {"url", "type", "install_extensions"}, f"{path}: ROM download has unnecessary field(s)")
        require(isinstance(download.get("url"), str) and download["url"].strip(), f"{path}: ROM download.url is required")
        require(download.get("type") in {"file", "archive"}, f"{path}: ROM download.type must be file or archive")
        if download.get("type") == "archive":
            extensions = download.get("install_extensions")
            require(isinstance(extensions, list) and extensions, f"{path}: archived ROM downloads require download.install_extensions")
            for ext in extensions:
                require(isinstance(ext, str) and ext.startswith("."), f"{path}: ROM install extension must start with a dot: {ext!r}")
    return item


def main():
    categories_data = load_json(ROOT / "categories.json")
    ids = set()
    errors = []
    categories_list = categories_data.get("categories", [])
    categories = {cat["id"] for cat in categories_list}

    for cat in categories_list:
        allowed = {"id", "name", "description", "sort_order", "hide_when_empty"}
        extra = set(cat) - allowed
        if extra:
            errors.append(f"categories.json: category {cat.get('id')!r} has unnecessary field(s): {', '.join(sorted(extra))}")
        default_thumb = ROOT / "assets" / "defaults" / f"{cat.get('id')}.png"
        if not default_thumb.exists():
            errors.append(f"categories.json: derived default thumbnail does not exist: {default_thumb.relative_to(ROOT)}")
        elif default_thumb.suffix.lower() not in IMAGE_EXTENSIONS:
            errors.append(f"categories.json: derived default thumbnail must be PNG, JPG, JPEG, or WEBP: {default_thumb.relative_to(ROOT)}")

    for path in sorted((ROOT / "items").glob("**/*.json")):
        try:
            item = validate_item(path, categories)
            if item["id"] in ids:
                raise ValueError(f"{path}: duplicate id {item['id']}")
            ids.add(item["id"])
        except Exception as exc:
            errors.append(str(exc))
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Validated {len(ids)} hub item(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
