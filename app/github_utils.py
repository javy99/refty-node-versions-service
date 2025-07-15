import tempfile
from git import Repo
from app.yaml_updater import update_yaml_files
from app.config import FORKED_REPO_URL

def process_version_update(image: str, version: str):
  with tempfile.TemporaryDirectory() as tmpdir:
    repo = Repo.clone_from(FORKED_REPO_URL, tmpdir)
    updated = update_yaml_files(tmpdir, image, version)

    if updated:
      repo.git.add(A=True)
      repo.index.commit(f"Update image version for {image} to {version}")
      repo.remote().push()
    else:
      raise Exception("No YAML files were updated.")