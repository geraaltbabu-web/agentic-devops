from health import check


def test_check_keys():
    r = check("https://example.com", 8)
    assert "url" in r
    assert r.get("ok") in {True, False}
