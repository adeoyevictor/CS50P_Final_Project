import pytest

from project import create_users_list, check_username, check_contacts

def test_create_users_list():
    assert create_users_list([('adeoyevictor',), ('adeoye',), ('Isaac',), ('bob',)]) == ['adeoyevictor', 'adeoye', 'Isaac', 'bob']
    assert create_users_list([]) == []
def test_check_username():
    assert check_username(['adeoyevictor', 'adeoye', 'Isaac', 'bob'], 'adeoye') == True
    assert check_username(['adeoyevictor', 'adeoye', 'Isaac', 'bob'], 'ayomikun') == False
    assert check_username([], 'ayomikun') == False
    assert check_username(['adeoyevictor', 'adeoye', 'Isaac', 'bob'], '') == False

def test_check_contacts():
    assert check_contacts([('Victor', 7036861043, 'adeoyevictor16@gmail.com'), ('Yemisi', 9063967262, 'adeoyevictor4@gmail.com')]) == False
    assert check_contacts([]) == True
