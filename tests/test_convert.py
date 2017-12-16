import datetime
import os

import pytest
from takuhai.convert import convert, create_metadata, insert_metadata


@pytest.mark.parametrize('path,title,date,category,modified', [
    ('171206_Example.md', 'Example', '2017-12-06', None, None),
    ('Pelican/171206_Example.md', 'Example', '2017-12-06', 'Pelican', None),
    ('Pelican/12/171206_Example.md', 'Example', '2017-12-06', 'Pelican', None),
])
def test_create_metadata(path, title, date, category, modified):
    metadata = create_metadata(path)
    assert metadata['Title'] == title
    assert metadata['Date'] == date
    assert metadata['Category'] == category
    assert metadata['Modified'] == modified


@pytest.mark.parametrize('path,lines,expected', [
    ('171206_Example.md', ['\n', 'Test\n'],
     ['Title: Example\n', 'Date: 2017-12-06\n', '\n', 'Test\n']),
    ('Pelican/171206_Example.md', ['\n', 'Test\n'],
     ['Title: Example\n', 'Date: 2017-12-06\n', 'Category: Pelican\n',
      '\n', 'Test\n']),
    ('Pelican/171206_Example.md', ['Title: dummy\n', '\n', 'Test\n'],
     ['Title: Example\n', 'Date: 2017-12-06\n', 'Category: Pelican\n',
      '\n', 'Test\n']),
])
def test_insert_metadata(path, lines, expected):
    metadata = create_metadata(path)
    insert_metadata(lines, metadata)
    assert lines == expected


@pytest.mark.parametrize('path,content,expected', [
    ('171206_Example.md', '\nTest\n',
     'Title: Example\nDate: 2017-12-06\nModified: {}\n\nTest\n'),
    ('Python/12/171206_Example.md', '\nTest\n',
     ('Title: Example\nDate: 2017-12-06\nModified: {}\n' +
      'Category: Python\n\nTest\n')),
    ('Python/12/171206_Example.md', 'Modified: 2017-12-06 10:00\n\nTest\n',
     ('Modified: {}\nTitle: Example\nDate: 2017-12-06\n' +
      'Category: Python\n\nTest\n')),
])
def test_convert(tmpdir, path, content, expected):
    directory, basename = os.path.split(path)
    if directory:
        os.makedirs(os.path.join(tmpdir, directory))
    p = tmpdir.join(path)
    p.write(content)
    convert(path, tmpdir)

    abspath = os.path.abspath(p)
    st_mtime = os.stat(abspath).st_mtime
    dt = datetime.datetime.fromtimestamp(st_mtime)
    modified = dt.strftime('%Y-%m-%d %H:%M')
    assert p.read() == expected.format(modified)
