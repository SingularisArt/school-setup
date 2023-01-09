def convert_filename_to_name(file_name):
    return (
        file_name
        .replace(".tex", "")
        .replace(".yaml", "")
        .replace(".pdf", "")
        .replace(".png", "")
        .replace(".jpg", "")
        .replace(".jpeg", "")
        .replace("-", " ")
        .replace("_", " ")
        .title()
    )
