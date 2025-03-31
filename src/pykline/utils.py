def is_in_jupyter() -> bool:
    """Check if user is running spaCy from a Jupyter or Colab notebook by
    detecting the IPython kernel. Mainly used for the displaCy visualizer.
    RETURNS (bool): True if in Jupyter/Colab, False if not.
    """
    # https://stackoverflow.com/a/39662359/6400719
    # https://stackoverflow.com/questions/15411967
    # https://github.com/explosion/spaCy/blob/b3c46c315eb16ce644bddd106d31c3dd349f6bb2/spacy/util.py#L1079
    try:
        if get_ipython().__class__.__name__ == "ZMQInteractiveShell":  # type: ignore[name-defined]
            return True  # Jupyter notebook or qtconsole
        if get_ipython().__class__.__module__ == "google.colab._shell":  # type: ignore[name-defined]
            return True  # Colab notebook
    except NameError:
        pass  # Probably standard Python interpreter
    # additional check for Colab
    try:
        import google.colab

        return True  # Colab notebook
    except ImportError:
        pass
    return False
