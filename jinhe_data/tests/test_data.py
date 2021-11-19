from data.lines import lines


def test_lines():
    for line in lines:
        assert line.directional in (0, 1)
