import datetime
import decimal
from multiprocessing import Process, set_start_method
from itertools import islice


TEST_DATA = dict(
    s='value',
    i=123,
    d=datetime.datetime.fromtimestamp(12325),
    n=decimal.Decimal('1234.56'),
    ss=set(range(10)),
    o=dict(d=decimal.Decimal('1234.58'), n=datetime.datetime.fromtimestamp(12325))
)



def test_sanity():
    from kvfile import KVFile

    kv = KVFile()

    for k, v in TEST_DATA.items():
        kv.set(k, v)

    for k, v in TEST_DATA.items():
        assert kv.get(k) == v

    assert list(kv.keys()) == sorted(TEST_DATA.keys())
    assert list(kv.items()) == sorted(TEST_DATA.items())

    assert list(kv.keys(reverse=True)) == sorted(TEST_DATA.keys(), reverse=True)
    assert list(kv.items(reverse=True)) == sorted(TEST_DATA.items(), reverse=True)

    dirname = kv.dirname
    kv.close()

    kv = KVFile(dirname=dirname)

    assert list(kv.keys()) == sorted(TEST_DATA.keys())
    assert list(kv.items()) == sorted(TEST_DATA.items())


def test_concurrency():
    from kvfile import SqliteDB

    kv = SqliteDB()

    kv.set('a', 'foo')
    kv.set('c', 'bax')
    kv.set('b', 'baz')
    dirname = kv.dirname
    kv.close()

    kvs = [SqliteDB(dirname=dirname) for _ in range(5)]

    for kv in kvs:
        assert list(kv.keys()) == ['a', 'b', 'c']
    for kv in kvs:
        assert list(kv.items()) == [('a', 'foo'), ('b', 'baz'), ('c', 'bax')]


def test_insert():
    from kvfile import KVFile
    kv = KVFile()
    kv.insert(((str(i), ':{}'.format(i)) for i in range(10000)))
    assert len(list(kv.keys())) == 10000
    assert len(list(kv.items())) == 10000
    assert kv.get('9999') == ':9999'
