import json
import os
import UnityPy
from UnityPy.export import MeshExporter

src = "/Users/lukebingham/RiderProjects/ConsoleApp1/ConsoleApp1/bin/Debug/net6.0/tmp/"

destination_folder = "/Users/lukebingham/RiderProjects/ConsoleApp1/ConsoleApp1/bin/Debug/net6.0/out/"
destination_folder_tex = destination_folder + "tex/"
destination_folder_mesh = destination_folder + "mesh/"

ignored_assets = [
    'cin_event_glleia_tier04_enc01_intro_pre.bundle',
    'cin_event_gl_jabba_tier01_intro_pre.bundle',
]

def get_progress():
    progress_file = os.path.join(destination_folder, "progress.json")
    if os.path.exists(progress_file):
        with open(progress_file, "r") as f:
            progress_data = json.load(f)
        return progress_data.get("processed_assets", [])
    return []

def save_progress(processed_assets):
    progress_data = {"processed_assets": processed_assets}
    progress_file = os.path.join(destination_folder, "progress.json")
    with open(progress_file, "w") as f:
        json.dump(progress_data, f)

def unpack_all_assets():
    processed_assets = get_progress()
    skipped = 0

    for asset in os.listdir(src):
        if asset in processed_assets:
            skipped += 1
            continue

        if asset in ignored_assets:
            continue

        env = UnityPy.load(os.path.join(src, asset))
        print(asset)

        for obj in env.objects:
            try:
                data = obj.read()

                if obj.type.name in ["Texture2D", "Sprite"]:
                    dest = os.path.join(destination_folder_tex, data.name + ".png")
                    if os.path.exists(dest):
                        continue
                    image = data.image
                    image.save(dest)

                if obj.type.name in ["Mesh"]:
                    dest = os.path.join(destination_folder_mesh, data.name + ".obj")
                    if os.path.exists(dest):
                        continue
                    mesh_exporter = MeshExporter.export_mesh(data)
                    with open(dest, "w") as f:
                        f.write(mesh_exporter)

                # Add other processing logic for different asset types if needed

            except Exception as e:
                abc123xyz=1
                # print(f"Error processing asset {asset}: {e}")

        processed_assets.append(asset)
        save_progress(processed_assets)

unpack_all_assets()
