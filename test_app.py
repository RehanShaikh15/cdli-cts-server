import pytest
import xml.dom.minidom

import main


@pytest.fixture
def client():
    main.app.config['TESTING'] = True
    yield main.app.test_client()


def test_index(client):
    '''Verify landing page.'''
    rv = client.get('/')
    assert rv.status_code == 200
    assert 'CDLI Text Services' in rv.data.decode()


def test_nemo(client):
    '''Verify nemo pages.'''
    nemo = main.nemo.prefix
    rv = client.get(nemo, follow_redirects=True)
    assert rv.status_code == 200
    text = rv.data.decode()
    assert 'Nemo' in text
    assert 'Text Collections' in text

    urn = 'urn:cts:cdli:P497322'
    rv = client.get(f'{nemo}/collections/{urn}', follow_redirects=True)
    assert rv.status_code == 200
    assert 'CDLI Literary' in rv.data.decode()


def cts_query(request, urn=None):
    '''Generate a nautilus query url for the given parameters.'''
    nautilus = main.nautilus.prefix
    url = f'{nautilus}/cts?request={request}'
    if urn:
        url += f'&urn={urn}'
    return url


def test_nautilus(client):
    '''Verify nautilus api service.'''
    rv = client.get(cts_query('GetCapabilities'))
    assert rv.status_code == 200
    dom = xml.dom.minidom.parseString(rv.data)
    assert dom.documentElement.tagName == 'GetCapabilities'
    textgroups = dom.getElementsByTagName('textgroup')
    assert len(textgroups)
    urns = [element.getAttribute('urn') for element in textgroups]
    assert 'urn:cts:cdli:P464358' in urns

    works = dom.getElementsByTagName('work')
    urn = 'urn:cts:cdli:P254855.P254855'
    assert urn in [work.getAttribute('urn') for work in works]
    rv = client.get(cts_query('GetPassage', urn))
    assert rv.status_code == 200
    passage = xml.dom.minidom.parseString(rv.data)
    assert passage.documentElement.tagName == 'GetPassage'
    texts = passage.getElementsByTagName('text')
    assert len(texts) == 1
    bodies = texts[0].getElementsByTagName('body')
    assert len(bodies) == 1
    divs = bodies[0].getElementsByTagName('div')
    assert len(divs) > 0
    edition = divs[0]
    assert edition.getAttribute('type') == 'edition'
    assert edition.getAttribute('n').startswith(urn)
    assert 'Heaven is a raven' in rv.data.decode()
    assert 'uga{mu\u0161en} am3' in rv.data.decode()
