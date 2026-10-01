"""Lectura del AndroidManifest.xml descompilado por apktool."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import xml.etree.ElementTree as ET


ANDROID_NS = "{http://schemas.android.com/apk/res/android}"


@dataclass
class Component:
    kind: str            # activity | service | receiver | provider
    name: str            # Lx/y/Z; (convertido a formato smali)
    exported: bool
    intent_filters: list[dict] = field(default_factory=list)
    raw: dict = field(default_factory=dict)


@dataclass
class ManifestInfo:
    package: str
    application_class: str | None
    components: list[Component] = field(default_factory=list)

    def by_kind(self, kind: str) -> list[Component]:
        return [c for c in self.components if c.kind == kind]


def parse_manifest(manifest_path: Path) -> ManifestInfo:
    tree = ET.parse(manifest_path)
    root = tree.getroot()
    pkg = root.get("package", "")

    def to_smali(name: str) -> str:
        if not name:
            return ""
        if name.startswith("."):
            name = pkg + name
        elif "." not in name and pkg:
            name = f"{pkg}.{name}"
        return "L" + name.replace(".", "/") + ";"

    app = root.find("application")
    app_class = None
    if app is not None:
        app_class = to_smali(app.get(ANDROID_NS + "name", ""))

    components: list[Component] = []
    if app is not None:
        for tag, kind in (
            ("activity", "activity"),
            ("activity-alias", "activity"),
            ("service", "service"),
            ("receiver", "receiver"),
            ("provider", "provider"),
        ):
            for el in app.findall(tag):
                name = to_smali(el.get(ANDROID_NS + "name", ""))
                exported = el.get(ANDROID_NS + "exported") == "true"
                ifs = []
                for ifl in el.findall("intent-filter"):
                    actions = [
                        a.get(ANDROID_NS + "name")
                        for a in ifl.findall("action")
                    ]
                    cats = [
                        c.get(ANDROID_NS + "name")
                        for c in ifl.findall("category")
                    ]
                    ifs.append({"actions": actions, "categories": cats})
                components.append(Component(
                    kind=kind, name=name, exported=exported,
                    intent_filters=ifs,
                ))

    return ManifestInfo(package=pkg, application_class=app_class,
                        components=components)

