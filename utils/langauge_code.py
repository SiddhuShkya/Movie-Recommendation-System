import pycountry


def get_language_name(code):
    try:
        return pycountry.languages.get(alpha_2=code).name
    except:  # noqa: E722
        return None  # keep original if not found
