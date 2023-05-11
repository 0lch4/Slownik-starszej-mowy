import pytest
import os
from mydb import conn

mydb = conn()

import plik

def test_tuples():
    dane = '''Aecáemm - podążać
        Aedd - okruch
        Deien - służyć
        Waen - chcieć'''
        
    dane = dane.split('\n')
    slowniczek = {}
    slownik = []

    expected_slownik = [('Aecáemm', 'podążać'), ('Aedd', 'okruch'), ('Deien', 'służyć'), ('Waen', 'chcieć')]
    expected_slowniczek = {'p': [('Aecáemm', 'podążać')],'o': [('Aedd', 'okruch')], 's':[('Deien', 'służyć')], 'c': [('Waen', 'chcieć')]}

    plik.tuples(dane, slownik, slowniczek)

    assert slownik == expected_slownik
    assert slowniczek == expected_slowniczek
    
    
def test_make_files():
    slowniczek = {'p': [('Aecáemm', 'podążać')],'o': [('Aedd', 'okruch')], 's':[('Deien', 'służyć')], 'c': [('Waen', 'chcieć')]}

    
    with open('tests/makefile/A.txt','w',encoding="utf-8") as f:
        f.write('Aecáemm - podążać\nAedd - okruch')
    with open('tests/makefile/D.txt','w',encoding="utf-8") as f:
        f.write('Deien - służyć')
    with open('tests/makefile/W.txt','w',encoding="utf-8") as f:
        f.write('Waen - chcieć')
        
    plik.make_files(slowniczek,'tests/makefile')
    
    with open('tests/makefile/A.txt','r',encoding="utf-8") as f:
        assert f.read() == 'Aecáemm - podążać\nAedd - okruch'
    with open('tests/makefile/D.txt','r',encoding="utf-8") as f:
        assert f.read() == 'Deien - służyć'
    with open('tests/makefile/W.txt','r',encoding="utf-8") as f:
        assert f.read() == 'Waen - chcieć'
        
        
import ladowanie

def test_create_tables2():
    for filename in os.listdir("tests"):
        if filename.endswith(".txt"):
            tablename = os.path.splitext(filename)[0]

            mycursor = mydb.cursor()
            mycursor.execute("CREATE TABLE {} (slowo VARCHAR(255), tlumaczenie TEXT)".format(tablename))

            with ladowanie.open_file(os.path.join("tests", filename)) as file:
                for line in file:
                    slowo, tlumaczenie = line.strip().split(' - ', 1)
                    sql = "INSERT INTO {} (slowo, tlumaczenie) VALUES (%s, %s)".format(tablename)
                    val = (slowo, tlumaczenie)
    
    assert tablename == 'test1'
    assert val == ('is this', 'work')
    mycursor.execute("DROP TABLE IF EXISTS test1")
    
