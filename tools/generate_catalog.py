#!/usr/bin/env python3
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "generated"
IMAGE_EXTENSIONS = [".png", ".jpg", ".jpeg", ".webp"]


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def public_item_paths():
    paths = []
    for path in sorted((ROOT / "items").glob("**/*.json")):
        if path.name.endswith(".template.json"):
            continue
        data = load_json(path)
        if data.get("visibility") == "dev_only":
            continue
        paths.append(path)
    return paths


def category_default_thumbnail(category_data, category_id: str):
    for category in category_data.get("categories", []):
        if category.get("id") == category_id:
            return f"assets/defaults/{category_id}.png"
    return f"assets/defaults/{category_id}.png"


def find_thumbnail(category_id: str, item_id: str):
    base = ROOT / "assets" / "thumbnails" / category_id / item_id
    for ext in IMAGE_EXTENSIONS:
        candidate = base.with_suffix(ext)
        if candidate.exists():
            return rel(candidate)
    return None


def find_gallery(category_id: str, item_id: str):
    folder = ROOT / "assets" / "gallery" / category_id
    images = []
    for ext in IMAGE_EXTENSIONS:
        images.extend(folder.glob(f"{item_id}_[0-9][0-9]{ext}"))
        images.extend(folder.glob(f"{item_id}_[0-9][0-9][0-9]{ext}"))
    return [rel(path) for path in sorted(set(images), key=lambda p: p.name.lower())]


def with_resolved_images(item, category_data):
    item = dict(item)
    category_id = item.get("category", "")
    item_id = item.get("id", "")
    thumbnail = find_thumbnail(category_id, item_id)
    default_thumbnail = category_default_thumbnail(category_data, category_id)
    item["thumbnail"] = thumbnail
    item["resolved_thumbnail"] = thumbnail or default_thumbnail
    item["gallery"] = find_gallery(category_id, item_id)
    return item


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog-version", default=None)
    parser.add_argument("--min-app-version", default="6.0.0")
    args = parser.parse_args()

    now = datetime.now(timezone.utc)
    catalog_version = args.catalog_version or now.strftime("%Y.%m.%d")
    updated = now.strftime("%Y-%m-%d")

    category_data = load_json(ROOT / "categories.json")
    item_paths = public_item_paths()
    relative_item_paths = [rel(path) for path in item_paths]
    source_items = [load_json(path) for path in item_paths]
    source_items.sort(key=lambda item: (item.get("category", ""), item.get("sort_order", 9999), item.get("name", "")))
    items = [with_resolved_images(item, category_data) for item in source_items]

    catalog = {
        "schema_version": 1,
        "catalog_version": catalog_version,
        "name": "MiSTer Companion Hub",
        "updated": updated,
        "minimum_app_version": args.min_app_version,
        "categories_file": "categories.json",
        "items": relative_item_paths,
    }
    write_json(ROOT / "catalog.json", catalog)

    catalog_full = {
        "schema_version": 1,
        "catalog_version": catalog_version,
        "name": "MiSTer Companion Hub",
        "updated": updated,
        "minimum_app_version": args.min_app_version,
        "categories": category_data.get("categories", []),
        "items": items,
    }
    write_json(GENERATED / "catalog_full.json", catalog_full)

    catalog_min = {
        "schema_version": 1,
        "catalog_version": catalog_version,
        "updated": updated,
        "items": [
            {
                "id": item.get("id"),
                "category": item.get("category"),
                "type": item.get("type"),
                "name": item.get("name"),
                "author": item.get("author"),
                "date_added": item.get("date_added"),
                "thumbnail": item.get("thumbnail"),
                "resolved_thumbnail": item.get("resolved_thumbnail"),
                "visibility": item.get("visibility"),
                "sort_order": item.get("sort_order", 9999),
            }
            for item in items
        ],
    }
    write_json(GENERATED / "catalog_min.json", catalog_min)

    category_counts = {cat["id"]: 0 for cat in category_data.get("categories", [])}
    for item in items:
        if item.get("visibility") == "public":
            category_counts[item.get("category")] = category_counts.get(item.get("category"), 0) + 1
    categories_with_counts = {
        "schema_version": 1,
        "catalog_version": catalog_version,
        "updated": updated,
        "categories": [dict(cat, count=category_counts.get(cat["id"], 0)) for cat in category_data.get("categories", [])],
    }
    write_json(GENERATED / "categories_with_counts.json", categories_with_counts)

    handlers = sorted({item.get("handler") for item in items if item.get("handler")})
    write_json(GENERATED / "known_handlers.json", {"schema_version": 1, "handlers": handlers})

    generated_files = sorted(GENERATED.glob("*.json")) + [ROOT / "catalog.json"]
    manifest = {
        "schema_version": 1,
        "generated_at": now.isoformat().replace("+00:00", "Z"),
        "catalog_version": catalog_version,
        "files": [
            {
                "path": rel(path),
                "sha256": sha256_file(path),
                "size": path.stat().st_size,
            }
            for path in generated_files
        ],
    }
    write_json(GENERATED / "manifest.json", manifest)


if __name__ == "__main__":
    main()
