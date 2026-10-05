"""Tests for toaster.tools: resolution order, validation and tool_env. No network, no real tools."""

from __future__ import annotations

import os
import stat
from pathlib import Path

import pytest

from toaster import tools
from toaster.tools import ToolNotFoundError

ENV_VARS = ["SYSMLV2_BINARY", "SYSMLV2_LIB_DIR", "PLANTUML_JAR", "JAVA", "Z3"]

# name -> (resolver, env var, path relative to .tools or None, PATH-resolvable name or None, kind)
SPECS = {
    "sysmlv2": (tools.resolve_sysmlv2, "SYSMLV2_BINARY", "bin/sysmlv2", "sysmlv2", "exe"),
    "library": (tools.resolve_library, "SYSMLV2_LIB_DIR", "sysml.library", None, "lib"),
    "jar": (tools.resolve_plantuml_jar, "PLANTUML_JAR", "plantuml.jar", None, "jar"),
    "java": (tools.resolve_java, "JAVA", None, "java", "exe"),
    "z3": (tools.resolve_z3, "Z3", "bin/z3", "z3", "exe"),
}
PATH_NAMES = [n for n, s in SPECS.items() if s[3]]
NO_PATH_NAMES = [n for n, s in SPECS.items() if not s[3]]
PROVISIONED_NAMES = [n for n, s in SPECS.items() if s[2]]


def make(path: Path, kind: str, executable: bool = True) -> Path:
    """Create a valid fake tool of the given kind at path."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if kind == "lib":
        (path / "Systems Library").mkdir(parents=True)
        return path
    path.write_text("#!/bin/sh\nexit 0\n")
    mode = path.stat().st_mode
    if kind == "exe" and executable:
        path.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    else:
        path.chmod(mode & ~(stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    return path


@pytest.fixture(autouse=True)
def _fresh_java_probe_cache():
    tools._JAVA_PROBED_OK.clear()
    yield
    tools._JAVA_PROBED_OK.clear()


@pytest.fixture
def sandbox(tmp_path, monkeypatch):
    """Clean env, REPO_ROOT and PATH all pointing into tmp_path."""
    for var in ENV_VARS:
        monkeypatch.delenv(var, raising=False)
    root = tmp_path / "repo"
    root.mkdir()
    pathdir = tmp_path / "pathdir"
    pathdir.mkdir()
    monkeypatch.setattr(tools, "REPO_ROOT", root)
    monkeypatch.setenv("PATH", str(pathdir))
    return root, pathdir, tmp_path


def provisioned(root: Path, name: str) -> Path:
    spec = SPECS[name]
    return make(root / ".tools" / spec[2], spec[4])


def on_path(pathdir: Path, name: str) -> Path:
    return make(pathdir / SPECS[name][3], "exe")


def test_repo_root_default_is_repository():
    assert tools.REPO_ROOT == Path(tools.__file__).resolve().parents[2]
    assert (tools.REPO_ROOT / "pyproject.toml").is_file()


def test_not_found_error_is_runtime_error():
    assert issubclass(ToolNotFoundError, RuntimeError)


@pytest.mark.parametrize("name", SPECS)
def test_explicit_wins_over_env(sandbox, monkeypatch, name):
    resolver, env_var, _, _, kind = SPECS[name]
    root, pathdir, tmp = sandbox
    explicit = make(tmp / "explicit" / "thing.jar" if kind == "jar" else tmp / "explicit" / "thing", kind)
    monkeypatch.setenv(env_var, str(make(tmp / "fromenv" / ("e.jar" if kind == "jar" else "e"), kind)))
    assert resolver(explicit) == explicit
    assert resolver(str(explicit)) == explicit


@pytest.mark.parametrize("name", SPECS)
def test_explicit_invalid_raises_and_does_not_fall_through(sandbox, monkeypatch, name):
    resolver, env_var, *_ = SPECS[name]
    root, pathdir, tmp = sandbox
    monkeypatch.setenv(env_var, str(make(tmp / "e.jar", "jar") if name == "jar" else make(tmp / "e", SPECS[name][4])))
    with pytest.raises(ToolNotFoundError, match="explicit argument"):
        resolver(tmp / "does-not-exist")


@pytest.mark.parametrize("name", PROVISIONED_NAMES)
def test_env_wins_over_provisioned(sandbox, monkeypatch, name):
    resolver, env_var, _, _, kind = SPECS[name]
    root, pathdir, tmp = sandbox
    provisioned(root, name)
    from_env = make(tmp / "fromenv" / ("e.jar" if kind == "jar" else "e"), kind)
    monkeypatch.setenv(env_var, str(from_env))
    assert resolver() == from_env


def test_java_env_wins_over_path(sandbox, monkeypatch):
    root, pathdir, tmp = sandbox
    on_path(pathdir, "java")
    from_env = make(tmp / "myjava", "exe")
    monkeypatch.setenv("JAVA", str(from_env))
    assert tools.resolve_java() == from_env


@pytest.mark.parametrize("name", PROVISIONED_NAMES)
def test_provisioned_used_when_nothing_else_set(sandbox, name):
    root, pathdir, tmp = sandbox
    expected = provisioned(root, name)
    assert SPECS[name][0]() == expected


@pytest.mark.parametrize("name", [n for n in PATH_NAMES if SPECS[n][2]])
def test_provisioned_wins_over_path(sandbox, name):
    root, pathdir, tmp = sandbox
    on_path(pathdir, name)
    expected = provisioned(root, name)
    assert SPECS[name][0]() == expected


@pytest.mark.parametrize("name", PATH_NAMES)
def test_path_is_used_for_sysmlv2_java_z3(sandbox, name):
    root, pathdir, tmp = sandbox
    expected = on_path(pathdir, name)
    assert SPECS[name][0]() == expected


@pytest.mark.parametrize("name", NO_PATH_NAMES)
def test_path_not_used_for_library_or_jar(sandbox, monkeypatch, name):
    root, pathdir, tmp = sandbox
    # Valid-looking candidates on PATH, including an executable plantuml.jar and a real library dir.
    make(pathdir / "sysml.library", "lib")
    make(pathdir / "plantuml.jar", "exe")
    make(pathdir / "plantuml", "exe")
    calls = []
    real_which = tools.shutil.which

    def recording_which(cmd, *args, **kwargs):
        calls.append(cmd)
        return real_which(cmd, *args, **kwargs)

    monkeypatch.setattr(tools.shutil, "which", recording_which)
    with pytest.raises(ToolNotFoundError):
        SPECS[name][0]()
    assert calls == []


@pytest.mark.parametrize("name", SPECS)
def test_env_set_but_missing_raises_naming_variable(sandbox, monkeypatch, name):
    resolver, env_var, *_ = SPECS[name]
    root, pathdir, tmp = sandbox
    # Provisioned and PATH candidates exist: the bad env value must still be an error.
    if SPECS[name][2]:
        provisioned(root, name)
    if SPECS[name][3]:
        on_path(pathdir, name)
    monkeypatch.setenv(env_var, str(tmp / "no-such-thing"))
    with pytest.raises(ToolNotFoundError, match=env_var):
        resolver()


def test_env_library_without_systems_library_rejected(sandbox, monkeypatch):
    root, pathdir, tmp = sandbox
    bad = tmp / "emptylib"
    bad.mkdir()
    monkeypatch.setenv("SYSMLV2_LIB_DIR", str(bad))
    with pytest.raises(ToolNotFoundError, match="SYSMLV2_LIB_DIR"):
        tools.resolve_library()


def test_library_given_as_file_rejected(sandbox):
    root, pathdir, tmp = sandbox
    f = make(tmp / "libfile", "jar")
    with pytest.raises(ToolNotFoundError):
        tools.resolve_library(f)


def test_jar_must_end_in_jar(sandbox, monkeypatch):
    root, pathdir, tmp = sandbox
    notjar = make(tmp / "plantuml.zip", "jar")
    monkeypatch.setenv("PLANTUML_JAR", str(notjar))
    with pytest.raises(ToolNotFoundError, match="PLANTUML_JAR"):
        tools.resolve_plantuml_jar()


@pytest.mark.parametrize("name", [n for n, s in SPECS.items() if s[4] == "exe"])
def test_non_executable_file_rejected(sandbox, monkeypatch, name):
    resolver, env_var, *_ = SPECS[name]
    root, pathdir, tmp = sandbox
    plain = make(tmp / "plainfile", "exe", executable=False)
    with pytest.raises(ToolNotFoundError):
        resolver(plain)
    monkeypatch.setenv(env_var, str(plain))
    with pytest.raises(ToolNotFoundError, match=env_var):
        resolver()


@pytest.mark.parametrize("name", [n for n in PROVISIONED_NAMES if SPECS[n][4] == "exe"])
def test_non_executable_provisioned_rejected(sandbox, name):
    root, pathdir, tmp = sandbox
    make(root / ".tools" / SPECS[name][2], "exe", executable=False)
    with pytest.raises(ToolNotFoundError, match=r"\.tools") as info:
        SPECS[name][0]()
    assert "re-run `uv run python scripts/provision-tools.py`" in str(info.value)


def test_directory_given_as_executable_rejected(sandbox):
    root, pathdir, tmp = sandbox
    (tmp / "adir").mkdir()
    with pytest.raises(ToolNotFoundError):
        tools.resolve_z3(tmp / "adir")


@pytest.mark.parametrize("name", SPECS)
def test_missing_tool_message_names_variable_and_provision_command(sandbox, name):
    resolver, env_var, *_ = SPECS[name]
    with pytest.raises(ToolNotFoundError) as info:
        resolver()
    message = str(info.value)
    assert env_var in message
    assert "uv run python scripts/provision-tools.py" in message


def test_empty_env_value_counts_as_unset(sandbox, monkeypatch):
    root, pathdir, tmp = sandbox
    monkeypatch.setenv("Z3", "")
    expected = on_path(pathdir, "z3")
    assert tools.resolve_z3() == expected


def test_tool_env_prepends_z3_dir_and_does_not_mutate_environ(sandbox, monkeypatch):
    root, pathdir, tmp = sandbox
    z3 = make(tmp / "z3dir" / "z3", "exe")
    monkeypatch.setenv("Z3", str(z3))
    monkeypatch.setenv("SOME_MARKER", "1")
    before = dict(os.environ)
    env = tools.tool_env()
    assert env["PATH"].split(os.pathsep) == [str(z3.parent), str(pathdir)]
    assert env["SOME_MARKER"] == "1"
    assert dict(os.environ) == before
    assert os.environ["PATH"] == str(pathdir)
    assert env is not os.environ


def test_tool_env_with_base_leaves_base_and_environ_alone(sandbox):
    root, pathdir, tmp = sandbox
    z3 = provisioned(root, "z3")
    base = {"PATH": "/base/bin", "KEEP": "x"}
    before_environ = dict(os.environ)
    env = tools.tool_env(base)
    assert env["PATH"] == str(z3.parent) + os.pathsep + "/base/bin"
    assert env["KEEP"] == "x"
    assert base == {"PATH": "/base/bin", "KEEP": "x"}
    assert dict(os.environ) == before_environ


def test_tool_env_base_without_path(sandbox):
    root, pathdir, tmp = sandbox
    z3 = provisioned(root, "z3")
    assert tools.tool_env({"A": "b"}) == {"A": "b", "PATH": str(z3.parent)}


def test_tool_env_raises_when_z3_unresolvable(sandbox):
    with pytest.raises(ToolNotFoundError, match="Z3"):
        tools.tool_env()


# --- java must run: the macOS /usr/bin/java stub passes the executable check but exits 1 -----------------

JAVA_HINT = "set the JAVA environment variable to a working java"
STUB_MESSAGE = "Unable to locate a Java Runtime."


def fake_java(path: Path, body: str) -> Path:
    """An executable shell script at path with the given body; `counter` lines are appended per run."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("#!/bin/sh\n" + body)
    path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return path


def counting_java(path: Path, counter: Path, tail: str) -> Path:
    return fake_java(path, f'echo run >> "{counter}"\n{tail}')


def java_via(source: str, path: Path, pathdir: Path, monkeypatch):
    """Return a zero-argument call that resolves `path` through the given source."""
    if source == "explicit":
        return lambda: tools.resolve_java(path), "the explicit argument"
    if source == "env":
        monkeypatch.setenv("JAVA", str(path))
        return tools.resolve_java, "the JAVA environment variable"
    link = pathdir / "java"
    link.symlink_to(path)
    return tools.resolve_java, "PATH"


@pytest.mark.parametrize("source", ["explicit", "env", "path"])
def test_working_java_resolves(sandbox, monkeypatch, source):
    root, pathdir, tmp = sandbox
    java = fake_java(tmp / "bin" / "java", 'echo "openjdk version" >&2\nexit 0\n')
    resolve, _ = java_via(source, java, pathdir, monkeypatch)
    resolved = resolve()
    assert resolved.samefile(java)


@pytest.mark.parametrize("source", ["explicit", "env", "path"])
def test_failing_java_raises_with_stderr_and_hint(sandbox, monkeypatch, source):
    root, pathdir, tmp = sandbox
    java = fake_java(tmp / "bin" / "java", f'echo "{STUB_MESSAGE}" >&2\necho second line >&2\nexit 1\n')
    resolve, where = java_via(source, java, pathdir, monkeypatch)
    with pytest.raises(ToolNotFoundError) as info:
        resolve()
    message = str(info.value)
    assert where in message
    assert "java did not run" in message
    assert STUB_MESSAGE in message
    assert "second line" not in message
    assert JAVA_HINT in message


def test_failing_java_without_stderr_reports_exit_status(sandbox):
    root, pathdir, tmp = sandbox
    java = fake_java(tmp / "bin" / "java", "exit 3\n")
    with pytest.raises(ToolNotFoundError, match="exit status 3") as info:
        tools.resolve_java(java)
    assert JAVA_HINT in str(info.value)


def test_hanging_java_raises(sandbox, monkeypatch):
    root, pathdir, tmp = sandbox
    monkeypatch.setattr(tools, "_JAVA_PROBE_TIMEOUT", 0.3)
    java = fake_java(tmp / "bin" / "java", "exec /bin/sleep 30\n")
    with pytest.raises(ToolNotFoundError) as info:
        tools.resolve_java(java)
    message = str(info.value)
    assert "java did not run" in message
    assert "did not finish" in message
    assert JAVA_HINT in message


def test_unrunnable_java_oserror_raises(sandbox):
    root, pathdir, tmp = sandbox
    # Executable bit set, but the kernel cannot exec it (no shebang, not a binary): OSError from subprocess.
    java = tmp / "bin" / "java"
    java.parent.mkdir()
    java.write_bytes(b"\x00\x01\x02 not a program\n")
    java.chmod(java.stat().st_mode | stat.S_IXUSR)
    with pytest.raises(ToolNotFoundError) as info:
        tools.resolve_java(java)
    assert "java did not run" in str(info.value)
    assert JAVA_HINT in str(info.value)


def test_successful_probe_is_cached(sandbox):
    root, pathdir, tmp = sandbox
    counter = tmp / "counter"
    java = counting_java(tmp / "bin" / "java", counter, "exit 0\n")
    for _ in range(3):
        assert tools.resolve_java(java) == java
    assert counter.read_text().splitlines() == ["run"]


def test_failed_probe_is_not_cached(sandbox):
    root, pathdir, tmp = sandbox
    counter = tmp / "counter"
    java = counting_java(tmp / "bin" / "java", counter, f'echo "{STUB_MESSAGE}" >&2\nexit 1\n')
    for _ in range(2):
        with pytest.raises(ToolNotFoundError):
            tools.resolve_java(java)
    assert counter.read_text().splitlines() == ["run", "run"]
    # Once java is fixed, the next call re-probes and succeeds.
    counting_java(java, counter, "exit 0\n")
    assert tools.resolve_java(java) == java
    assert counter.read_text().splitlines() == ["run", "run", "run"]


def test_other_resolvers_do_not_probe(sandbox):
    root, pathdir, tmp = sandbox
    counter = tmp / "counter"
    z3 = counting_java(tmp / "bin" / "z3", counter, "exit 1\n")
    assert tools.resolve_z3(z3) == z3
    assert not counter.exists()
