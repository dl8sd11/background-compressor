import os


def get_streams_name(input_file):
    input_without_ext = ".".join(input_file.rsplit(".", 1)[:-1])
    return {
        "bg": input_without_ext + ".bg.avi",
        "fg": input_without_ext + ".fg.avi"
    }
