import bpy

def find_reference(scene):
    reference_marker = context.scene.timeline_markers.get("reference")
    if reference_marker is not None:
        return reference_marker.frame

def find_seqs(scene):
    sequences = {}
    sequence_flags = {}

    for marker in scene.timeline_markers:
        if ":" not in marker.name:
            continue

        name, what = marker.name.rsplit(":", 1)

        if name not in sequences:
            sequences[name] = {}

        if what in sequences[name]:
            print("Warning: Got duplicate '{}' marker for sequence '{}' at frame {} (first was at frame {}), ignoring".format(what, name, marker.frame, sequences[name][what].frame))
            continue

        sequences[name][what] = marker

    if "Sequences" in bpy.data.texts:
        for line in bpy.data.texts["Sequences"].as_string().split("\n"):
            line = line.strip()

            if not line:
                continue

            if ":" not in line:
                print("Invalid line in 'Sequences':", line)
                continue

            name, flags = line.split(":", 1)

            if flags.lstrip():
                flags = tuple(map(lambda f: f.strip(), flags.split(",")))
            else:
                flags = ()

            sequence_flags[name] = flags
    
    return sequences, sequence_flags