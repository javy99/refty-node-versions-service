import os
import tempfile
from git import Repo
from app.yaml_updater import update_yaml_files
from dotenv import load_dotenv

load_dotenv()

def process_version_update(image: str, version: str):
  github_token = os.getenv("GITHUB_TOKEN")
  fork_url = os.getenv("FORKED_REPO_URL").replace("https://", f"https://{github_token}@")

  with tempfile.TemporaryDirectory() as tmpdir:
    repo = Repo.clone_from(fork_url, tmpdir)
    updated = update_yaml_files(tmpdir, image, version)

    if updated:
      repo.git.add(A=True)
      repo.index.commit(f"Update image version for {image} to {version}")
      repo.remote().push()
    else:
      raise Exception("No YAML files were updated.")