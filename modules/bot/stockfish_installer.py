import json
import logging
import os
import platform
import shutil
import stat
import tarfile
import tempfile
import zipfile
from pathlib import Path
from typing import Any

import requests

from modules.shared.constants.stockfish_constants import (
    STOCKFISH_PATH,
    STOCKFISH_ROOT,
    STOCKFISH_PLATFORM_DIR,
    PLATFORM_KEY,
)

_RELEASE_API = "https://api.github.com/repos/official-stockfish/Stockfish/releases/latest"
_METADATA_FILE = STOCKFISH_ROOT / "installed_release.json"

logger = logging.getLogger(__name__)


def _is_executable_file(path: Path) -> bool:
    if not path.is_file():
        return False

    name = path.name.lower()
    if "stockfish" not in name:
        return False

    if PLATFORM_KEY == "windows":
        return name.endswith(".exe")

    return not name.endswith((".txt", ".md", ".nnue"))


def _extract_archive(archive_path: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)

    suffix = archive_path.name.lower()
    if suffix.endswith(".zip"):
        with zipfile.ZipFile(archive_path, "r") as zf:
            zf.extractall(destination)
        return

    if suffix.endswith((".tar", ".tar.gz", ".tgz", ".tar.xz")):
        with tarfile.open(archive_path, "r:*") as tf:
            tf.extractall(destination)
        return

    raise RuntimeError(f"Unsupported archive format: {archive_path.name}")


def _platform_match(asset_name: str) -> bool:
    name = asset_name.lower()

    if PLATFORM_KEY == "windows":
        return "win" in name

    if PLATFORM_KEY == "macos":
        return any(k in name for k in ("mac", "osx", "apple"))

    return any(k in name for k in ("linux", "ubuntu"))


def _is_source_asset(asset_name: str) -> bool:
    name = asset_name.lower()
    return any(k in name for k in ("source", "src", "symbols", "debug"))


def _arch_score(asset_name: str) -> int:
    name = asset_name.lower()
    machine = platform.machine().lower()

    score = 0

    is_arm_host = "arm" in machine or "aarch64" in machine
    is_x86_host = any(k in machine for k in ("x86_64", "amd64", "x64", "i386", "i686"))

    if is_arm_host:
        if any(k in name for k in ("arm", "aarch64")):
            score += 20
        if any(k in name for k in ("x86", "x64", "amd64")):
            score -= 10
    elif is_x86_host:
        if any(k in name for k in ("x86", "x64", "amd64")):
            score += 20
        if any(k in name for k in ("arm", "aarch64")):
            score -= 10

    if "avx2" in name:
        score += 3
    if "modern" in name:
        score += 2

    return score


def _select_asset(assets: list[dict[str, Any]]) -> dict[str, Any] | None:
    candidates: list[tuple[int, dict[str, Any]]] = []

    for asset in assets:
        name = str(asset.get("name", ""))
        lower = name.lower()

        if not lower.endswith((".zip", ".tar", ".tar.gz", ".tgz", ".tar.xz")):
            continue

        if _is_source_asset(name):
            continue

        if not _platform_match(name):
            continue

        score = _arch_score(name)
        candidates.append((score, asset))

    if not candidates:
        return None

    candidates.sort(key=lambda item: item[0], reverse=True)
    return candidates[0][1]


def _find_extracted_binary(extract_dir: Path) -> Path | None:
    matches: list[Path] = []

    for path in extract_dir.rglob("*"):
        if _is_executable_file(path):
            matches.append(path)

    if not matches:
        return None

    # Prefer largest executable because it is usually the real engine binary.
    matches.sort(key=lambda p: p.stat().st_size, reverse=True)
    return matches[0]


def _find_project_local_binary() -> Path | None:
    if not STOCKFISH_ROOT.exists():
        return None

    matches: list[Path] = []
    for path in STOCKFISH_ROOT.rglob("*"):
        if not _is_executable_file(path):
            continue

        try:
            path.resolve().relative_to(STOCKFISH_ROOT.resolve())
        except ValueError:
            continue

        matches.append(path)

    if not matches:
        return None

    matches.sort(
        key=lambda p: (
            0 if p.parent == STOCKFISH_PLATFORM_DIR else 1,
            -p.stat().st_size,
            p.name,
        )
    )
    return matches[0]


def _write_metadata(tag: str, asset_name: str) -> None:
    STOCKFISH_ROOT.mkdir(parents=True, exist_ok=True)

    payload = {
        "release_tag": tag,
        "asset_name": asset_name,
        "platform": PLATFORM_KEY,
        "path": str(STOCKFISH_PATH),
    }

    _METADATA_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def ensure_local_stockfish_binary() -> Path | None:
    """
    Ensure a local Stockfish binary exists inside the project folder.

    Returns:
        Path to the local Stockfish binary if available, otherwise None.
    """

    if STOCKFISH_PATH.exists() and STOCKFISH_PATH.stat().st_size > 0:
        return STOCKFISH_PATH

    STOCKFISH_PLATFORM_DIR.mkdir(parents=True, exist_ok=True)

    project_local_binary = _find_project_local_binary()
    if project_local_binary is not None and project_local_binary != STOCKFISH_PATH:
        shutil.copy2(project_local_binary, STOCKFISH_PATH)
        if PLATFORM_KEY != "windows":
            STOCKFISH_PATH.chmod(STOCKFISH_PATH.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        logger.info("Using project-local Stockfish binary: %s", STOCKFISH_PATH)
        return STOCKFISH_PATH

    # Reuse any legacy bundled binary from assets/stockfish/ if present.
    if PLATFORM_KEY == "windows":
        legacy_candidates = [
            STOCKFISH_ROOT / "stockfish.exe",
        ]
    else:
        legacy_candidates = [
            STOCKFISH_ROOT / "stockfish",
        ]
    for candidate in legacy_candidates:
        if candidate.exists() and candidate.is_file() and candidate.stat().st_size > 0:
            shutil.copy2(candidate, STOCKFISH_PATH)
            if PLATFORM_KEY != "windows":
                STOCKFISH_PATH.chmod(STOCKFISH_PATH.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
            logger.info("Using legacy bundled Stockfish binary: %s", STOCKFISH_PATH)
            return STOCKFISH_PATH

    try:
        response = requests.get(_RELEASE_API, timeout=30)
        response.raise_for_status()
        data = response.json()

        assets = data.get("assets", [])
        asset = _select_asset(assets)
        if asset is None:
            return None

        asset_name = str(asset["name"])
        download_url = str(asset["browser_download_url"])
        tag_name = str(data.get("tag_name", "unknown"))

        with tempfile.TemporaryDirectory(prefix="stockfish_dl_") as tmp:
            tmp_dir = Path(tmp)
            archive_path = tmp_dir / asset_name

            with requests.get(download_url, stream=True, timeout=60) as dl:
                dl.raise_for_status()
                with archive_path.open("wb") as out:
                    for chunk in dl.iter_content(chunk_size=1024 * 256):
                        if chunk:
                            out.write(chunk)

            extract_dir = tmp_dir / "extract"
            _extract_archive(archive_path, extract_dir)

            extracted_binary = _find_extracted_binary(extract_dir)
            if extracted_binary is None:
                return None

            shutil.copy2(extracted_binary, STOCKFISH_PATH)

            if PLATFORM_KEY != "windows":
                STOCKFISH_PATH.chmod(STOCKFISH_PATH.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

            _write_metadata(tag_name, asset_name)

        return STOCKFISH_PATH

    except Exception:
        return None
