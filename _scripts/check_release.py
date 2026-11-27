"""Check catalogue and release data before publishing the website."""

import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
WINDOWS_DATA = "_data/mrteemtactics_windows.json"
APPLICATION_FEED = "mrteemtactics/application/v1/latest.json"
DOWNLOAD_FEED = "mrteemtactics/download/latest.json"
LEGACY_DOWNLOAD = "mrteemtactics/download/index.html"
STATIC_FEEDS = (
    APPLICATION_FEED,
    "mrteemtactics/updates/v1/index.json",
    "mrteemtactics/updates/v2/index.json",
)
SLUG = r"[a-z0-9]+(?:-[a-z0-9]+)*"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def validate_artifact(root, app):
    name, record = app["name"], app.get("release")
    require(isinstance(record, str) and re.fullmatch(r"[a-z0-9_]+", record),
            f"{name}: a released product needs a release data file.")
    artifact = read_json(root / "_data" / f"{record}.json")
    require(isinstance(artifact, dict), f"{name}: release data must be an object.")
    require(nonempty(artifact.get("version")), f"{name}: release version is required.")
    size = artifact.get("bytes")
    require(type(size) is int and size > 0, f"{name}: release bytes must be a positive integer.")
    digest = artifact.get("sha256")
    require(isinstance(digest, str) and re.fullmatch(r"[a-f0-9]{64}", digest),
            f"{name}: release sha256 must be a lowercase SHA-256 digest.")


def validate_catalogue(root):
    catalogue = read_json(root / "_data/software.json")
    require(isinstance(catalogue, dict), "software.json must contain an object.")
    apps = catalogue.get("apps")
    require(isinstance(apps, list) and apps, "software.apps must be a non-empty list.")
    contacts = read_json(root / "_data/contact.json")
    require(isinstance(contacts, list) and all(isinstance(entry, dict) for entry in contacts),
            "contact.json must contain a list of contact records.")
    contact_ids = {entry["id"] for entry in contacts if nonempty(entry.get("id"))}
    seen = {field: set() for field in ("id", "path", "name")}
    for app in apps:
        require(isinstance(app, dict), "Each catalogue entry must be an object.")
        name = app.get("name", "(unnamed product)")
        for field in ("id", "name", "path", "category", "summary", "description", "support"):
            require(nonempty(app.get(field)), f"{name}: {field} must be non-empty text.")
        for field, values in seen.items():
            value = app[field].casefold()
            require(value not in values, f"{name}: duplicate catalogue {field}: {app[field]}.")
            values.add(value)
        require(re.fullmatch(SLUG, app["id"]), f"{name}: id must be a lowercase slug.")
        require(re.fullmatch(rf"/software/{SLUG}/", app["path"]), f"{name}: invalid product path.")
        require((root / app["path"].lstrip("/") / "index.html").is_file(),
                f"{name}: product page is missing at {app['path']}.")
        support = re.fullmatch(rf"/contact/#({SLUG})", app["support"])
        require(support and support[1] in contact_ids, f"{name}: support must point to a Contact section.")
        status = app.get("status")
        require(status in ("released", "in_development"), f"{name}: invalid release status.")
        platforms = app.get("platforms")
        require(isinstance(platforms, list) and all(nonempty(p) for p in platforms),
                f"{name}: platforms must be a list of platform names.")
        require(len({p.strip().casefold() for p in platforms}) == len(platforms),
                f"{name}: platform names must be unique.")
        if status == "released":
            require(platforms, f"{name}: a released product needs a supported platform.")
            validate_artifact(root, app)
        else:
            require("release" not in app, f"{name}: an in-development product cannot advertise a release.")
    return apps


def validate_windows_release(root, apps):
    tactics = next((app for app in apps if app["id"] == "mrteemtactics"), None)
    require(tactics and tactics.get("release") == "mrteemtactics_windows",
            "MrTeemTactics must use the Windows release record.")
    record = read_json(root / WINDOWS_DATA)
    manifest = read_json(root / APPLICATION_FEED)
    require(isinstance(manifest, dict) and manifest.get("kind") == "windows-application",
            "Expected a Windows application manifest.")
    payload = manifest.get("payload")
    require(isinstance(payload, dict) and payload.get("application") == "mrteemtactics"
            and payload.get("architecture") == "x64", "Expected a MrTeemTactics x64 application feed.")
    for field in ("version", "bytes", "sha256"):
        value = payload.get(field)
        require(type(value) is type(record[field]) and value == record[field],
                f"MrTeemTactics {field} differs between the website and application feed.")
    version = record["version"]
    require(re.fullmatch(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)", version),
            "MrTeemTactics version must match the release tag format, such as 0.334.")
    installer = ("https://github.com/ReallyMadCow/teepeople-site/releases/download/"
                 f"mrteemtactics-{version}/MrTeemTactics-{version}-win64.msi")
    require(payload.get("url") == installer, "MrTeemTactics installer URL differs from the application feed.")
    return record, installer


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.links = set()
        self.ids = set()
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "a" and "href" in attributes:
            self.links.add(attributes["href"])
        if "id" in attributes:
            self.ids.add(attributes["id"])


def validate_built_site(root, site, apps, record, installer):
    catalogue = Page(site / "software/index.html")
    contact = Page(site / "contact/index.html")
    for app in apps:
        name, support = app["name"], app["support"]
        product = Page(site / app["path"].lstrip("/") / "index.html")
        require(app["path"] in catalogue.links, f"{name}: built catalogue link is missing.")
        require(support in product.links and support.split("#", 1)[1] in contact.ids,
                f"{name}: built support link is missing or broken.")
        if app["status"] == "in_development":
            require("download" not in product.ids, f"{name}: built page presents a download.")
        if app["id"] == "mrteemtactics":
            require(installer in product.links, "The built product download disagrees with the application feed.")
    require(installer in Page(site / LEGACY_DOWNLOAD).links,
            "The built legacy download disagrees with the application feed.")
    require(read_json(site / DOWNLOAD_FEED) == record,
            "The built download feed does not match the Windows release data.")
    for path in STATIC_FEEDS:
        require((site / path).read_bytes() == (root / path).read_bytes(),
                f"The built static feed differs from its source: {path}.")
    require(not (site / "_scripts").exists(), "The generated site contains release tooling.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", type=Path, help="also check the Jekyll build in this directory")
    args = parser.parse_args()
    try:
        apps = validate_catalogue(ROOT)
        record, installer = validate_windows_release(ROOT, apps)
        if args.site is not None:
            validate_built_site(ROOT, args.site, apps, record, installer)
    except (OSError, ValueError) as error:
        print(f"Release check failed: {error}", file=sys.stderr)
        return 1
    scope = "Source and built site" if args.site is not None else "Source data"
    print(f"{scope} verified for {len(apps)} catalogue entries and MrTeemTactics {record['version']}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
