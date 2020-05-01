from bot.linkmebot import get_search_keys

def test_get_search_keys():
    assert get_search_keys('!linkme m4') == ['m4']