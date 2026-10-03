"""Resolve the external tools the tutorial shells out to, without hard-coding where they live.

Five tools: the `sysmlv2` CLI (sysml-toolkit), its `sysml.library` directory, the PlantUML jar, `java`,
and `z3`. Each has one resolver, and every resolver tries the same sources in the same order:

1. the `explicit` argument;
2. its environment variable (`SYSMLV2_BINARY`, `SYSMLV2_LIB_DIR`, `PLANTUML_JAR`, `JAVA`, `Z3`);
3. the provisioned location under `REPO_ROOT / ".tools"` (`bin/sysmlv2`, `sysml.library/`,
   `plantuml.jar`, `bin/z3`; java is not provisioned);
4. `shutil.which`, for `sysmlv2`, `java` and `z3` only (never for the library or the jar).

A candidate that is set but invalid (an environment variable naming a missing file, a non-executable
binary, a directory with no `Systems Library`, a jar that is not a `.jar`) raises `ToolNotFoundError`
naming where the candidate came from; it never falls through silently to the next source. The one
exception is step 3, where an absent file just means "not provisioned" and resolution continues to
step 4. An environment variable set to the empty string counts as unset.

If nothing is found, `ToolNotFoundError` names the environment variable and the provisioning command.
"""

from __future__ import annotations

import os
import shutil
from collections.abc import Callable, Mapping
from pathlib import Path

REPO_ROOT: Path = Path(__file__).resolve().parents[2]

_PROVISION_HINT = "uv run python scripts/provision-tools.py"


class ToolNotFoundError(RuntimeError):
    """Raised when a tool cannot be resolved, or a candidate for it is set but invalid."""


def _is_executable_file(path: Path) -> bool:
    return path.is_file() and os.access(path, os.X_OK)


def _is_library_dir(path: Path) -> bool:
    return path.is_dir() and (path / "Systems Library").is_dir()


def _is_jar(path: Path) -> bool:
    return path.is_file() and path.suffix == ".jar"


_EXECUTABLE = ("an executable file", _is_executable_file)
_LIBRARY = ("a directory containing a 'Systems Library' subdirectory", _is_library_dir)
_JAR = ("a file ending in .jar", _is_jar)


def _resolve(
    tool: str,
    explicit: str | Path | None,
    env_var: str,
    provisioned: str | None,
    which: str | None,
    kind: tuple[str, Callable[[Path], bool]],
) -> Path:
    what, is_valid = kind

    def checked(path: Path, source: str, hint: str = "") -> Path:
        if not is_valid(path):
            raise ToolNotFoundError(
                f"{tool} from {source} is {str(path)!r}, which is not {what}{hint}"
            )
        return path

    if explicit is not None:
        return checked(Path(explicit), "the explicit argument")

    env_value = os.environ.get(env_var)
    if env_value:
        return checked(Path(env_value), f"the {env_var} environment variable")

    if provisioned is not None:
        candidate = REPO_ROOT / ".tools" / provisioned
        if candidate.exists() or candidate.is_symlink():
            return checked(
                candidate,
                "the provisioned .tools directory",
                f"; re-run `{_PROVISION_HINT}`",
            )

    if which is not None:
        found = shutil.which(which)
        if found:
            return checked(Path(found), "PATH")

    raise ToolNotFoundError(
        f"{tool} not found: pass it explicitly, set the {env_var} environment variable, "
        f"or provision it with `{_PROVISION_HINT}`"
    )


def resolve_sysmlv2(explicit: str | Path | None = None) -> Path:
    """The `sysmlv2` executable: explicit, `SYSMLV2_BINARY`, `.tools/bin/sysmlv2`, then PATH."""
    return _resolve("sysmlv2", explicit, "SYSMLV2_BINARY", "bin/sysmlv2", "sysmlv2", _EXECUTABLE)


def resolve_library(explicit: str | Path | None = None) -> Path:
    """The `sysml.library` directory: explicit, `SYSMLV2_LIB_DIR`, `.tools/sysml.library`. Never PATH."""
    return _resolve("sysml.library", explicit, "SYSMLV2_LIB_DIR", "sysml.library", None, _LIBRARY)


def resolve_plantuml_jar(explicit: str | Path | None = None) -> Path:
    """The PlantUML jar: explicit, `PLANTUML_JAR`, `.tools/plantuml.jar`. Never PATH."""
    return _resolve("plantuml jar", explicit, "PLANTUML_JAR", "plantuml.jar", None, _JAR)


def resolve_java(explicit: str | Path | None = None) -> Path:
    """The `java` executable: explicit, `JAVA`, then PATH (java is not provisioned)."""
    return _resolve("java", explicit, "JAVA", None, "java", _EXECUTABLE)


def resolve_z3(explicit: str | Path | None = None) -> Path:
    """The `z3` executable: explicit, `Z3`, `.tools/bin/z3`, then PATH."""
    return _resolve("z3", explicit, "Z3", "bin/z3", "z3", _EXECUTABLE)


def tool_env(base: Mapping[str, str] | None = None) -> dict[str, str]:
    """A copy of `os.environ` (or of `base`) with the resolved `z3`'s directory prepended to `PATH`.

    Use it as `env=` for subprocesses: `sysmlv2 verify --solve` finds `z3` on `PATH`. Does not mutate
    `os.environ` or `base`. Raises `ToolNotFoundError` if `z3` cannot be resolved.
    """
    env = dict(os.environ if base is None else base)
    z3_dir = str(resolve_z3().parent)
    existing = env.get("PATH")
    env["PATH"] = z3_dir + os.pathsep + existing if existing else z3_dir
    return env
