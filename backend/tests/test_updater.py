import subprocess

from allfix import updater


def _git(cwd, *args):
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True)


def _commit(cwd, name):
    (cwd / name).write_text(name)
    _git(cwd, "add", name)
    _git(cwd, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", name)


def test_update_available_only_for_fast_forward(tmp_path, monkeypatch):
    origin, pc = tmp_path / "origin", tmp_path / "pc"
    origin.mkdir()
    _git(origin, "init", "-q", "-b", "main")
    _commit(origin, "a")
    _git(tmp_path, "clone", "-q", str(origin), "pc")
    monkeypatch.setattr(updater, "REPO_ROOT", pc)

    assert not updater.update_available()          # up to date
    _commit(origin, "b")
    assert updater.update_available()              # a newer commit on GitHub
    remote = subprocess.run(["git", "rev-parse", "origin/main"], cwd=pc, capture_output=True, text=True).stdout.strip()
    (pc / "logs").mkdir()
    (pc / "logs" / "update-blocked.txt").write_text(remote + "\n")
    assert not updater.update_available()          # that version already failed to apply
    (pc / "logs" / "update-blocked.txt").unlink()
    _commit(pc, "local")                           # diverged: never restart into a merge
    assert not updater.update_available()


def test_off_unless_asked(monkeypatch):
    monkeypatch.delenv("ALLFIX_AUTO_UPDATE", raising=False)
    assert not updater.enabled()
