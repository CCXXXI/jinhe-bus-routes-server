from data.lines import lines


def test_lines():
    """Check lines data."""
    for line in lines:
        assert line.directional in (0, 1)
