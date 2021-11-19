from data.lines import lines


def test_lines():
    """Check lines data."""
    # `directional` is True of False
    assert all(line.directional in (0, 1) for line in lines)

    # `name` is unique
    assert len({line.name for line in lines}) == len(lines)
