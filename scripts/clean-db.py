#!/usr/bin/env python3
import itertools
import json
import os
import shutil
from pathlib import Path

import yaml

SCRAM_ARCH = ""
RELEASE_QUEUE = ""
WORKSPACE = ""
RPM_INSTALL_PREFIX = ""


def setup():
    global SCRAM_ARCH, RELEASE_QUEUE, WORKSPACE, RPM_INSTALL_PREFIX
    SCRAM_ARCH = os.environ["SCRAM_ARCH"]
    RELEASE_QUEUE = os.environ["RELEASE_QUEUE"]
    WORKSPACE = os.environ["WORKSPACE"]
    RPM_INSTALL_PREFIX = os.environ["RPM_INSTALL_PREFIX"]


def main():
    env_file = (
        Path(WORKSPACE)
        / "spack"
        / "var"
        / "spack"
        / "environments"
        / RELEASE_QUEUE
        / "spack.yaml"
    )

    lock_file = env_file.with_suffix(".lock")

    db_file = Path(RPM_INSTALL_PREFIX) / ".spack-db" / "index.json"

    print(f"[INFO] Loading environment from file {str(env_file)}")
    with env_file.open("r") as f:
        env = yaml.safe_load(f)
    print(f"[INFO] Success")

    print(f"[INFO] Loading environment lockfile from {str(lock_file)}")
    with lock_file.open("r") as f:
        lock = json.load(f)

    print(f"[INFO] Success")

    print(f"[INFO] Loading installation database from file {str(db_file)}")
    with db_file.open("r") as f:
        spack_db = json.load(f)

    print(f"[INFO] Success")

    print("[INFO] Collecing package(s) that can conflict")
    projections = env["spack"]["config"]["install_tree"]["projections"]
    pkgs_to_check = dict(
        zip(
            [k for k, v in projections.items() if "{hash" not in v],
            itertools.repeat("XXX"),
        )
    )

    print(f"[INFO] Found {len(pkgs_to_check)} package(s)")

    print(f"[INFO] Filling in hashes")
    for v in lock["concrete_specs"].values():
        if v["name"] in pkgs_to_check:
            pkgs_to_check[v["name"]] = v["hash"]

    missing = [k for k, v in pkgs_to_check.items() if v == "XXX"]
    if missing:
        print("[ERROR] Could not find the following package(s) in spack.lock:")
        print(", ".join(missing))
        exit(1)

    print(f"[INFO] Done")

    to_remove = []

    print(f"[INFO] Looking for conflicts")
    for pkg in spack_db["database"]["installs"].values():
        name = pkg["spec"]["name"]
        if name in pkgs_to_check and pkg["spec"]["hash"] != pkgs_to_check[name]:
            to_remove.append((pkg["spec"]["hash"], pkg["path"]))

    if not to_remove:
        print("[INFO] Nothing to do, quitting")
        exit(0)

    print(f"[INFO] Will remove {len(to_remove)} package(s)")
    for hash_, path_ in to_remove:
        shutil.rmtree(path_)
        del spack_db["database"]["installs"][hash_]

    print(f"[INFO] Done")

    print(f"[INFO] Writing database to disk")
    with db_file.open("w") as f:
        json.dump(f, spack_db)

    print(f"[INFO] All done")
