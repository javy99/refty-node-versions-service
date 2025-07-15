import os
import yaml

def update_yaml_files(repo_path: str, image: str, version: str) -> bool:
  updated = False
  image_base = image.split(":")[0] # drop version if it exists

  for root, _, files in os.walk(repo_path):
    for file in files:
      if file.endswith((".yaml", ".yml")):
        full_path = os.path.join(root, file)
        with open(full_path, "r") as f:
          try:
            docs = list(yaml.safe_load_all(f))
          except Exception:
            continue # skip broken YAMLs

        modified = False
        for doc in docs:
          if isinstance(doc, dict):
            doc_str = yaml.dump(doc)
            if image_base in doc_str:
                doc_str = doc_str.replace(image_base, f"{image_base}:{version}")
                modified = True
                updated = True

        if modified:
          with open(full_path, "w") as f:
            yaml.dump_all(docs, f)

  return updated