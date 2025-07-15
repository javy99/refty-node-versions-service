import os
import yaml

def update_yaml_files(repo_path: str, image: str, version: str) -> bool:
  updated = False
  image_base = image.split(":")[0]

  for root, _, files in os.walk(repo_path):
    for file in files:
      if file.endswith((".yaml", ".yml")):
        full_path = os.path.join(root, file)
        with open(full_path, "r") as f:
          try:
            docs = list(yaml.safe_load_all(f))
          except Exception:
            continue

        modified = False

        # Go through each YAML doc
        for doc in docs:
          if isinstance(doc, dict):
            if update_image_field(doc, image_base, version):
              modified = True
              updated = True

        if modified:
          with open(full_path, "w") as f:
            yaml.dump_all(docs, f, sort_keys=False)

  return updated

# Helper function: recursively update any image field
def update_image_field(obj, image_base, version):
  modified = False

  if isinstance(obj, dict):
    for key, value in obj.items():
        if isinstance(value, str) and value.startswith(image_base):
            obj[key] = f"{image_base}:{version}"
            modified = True
        else:
            # recursive dive into nested dicts/lists
            modified |= update_image_field(value, image_base, version)
  elif isinstance(obj, list):
    for item in obj:
      modified |= update_image_field(item, image_base, version)

  return modified
