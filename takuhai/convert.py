import codecs
import os


def convert(path, root='.'):
    """
    pathの文字列からメタデータを抽出して，pathの内容に
    メタデータを書き込む．

    pathは<YYMMDD><sep><title>.<ext>の形式である必要がある．

    Parameters
    ----------
    path : str
        ファイル名
    root : str, optional
        ディレクトリ名．省略するとカレントディレクトリとする．
    """
    directory, basename = os.path.split(path)
    while directory:
        directory, category = os.path.split(directory)

    basename = os.path.splitext(basename)[0]
    date, title = basename[:6], basename[7:]
    date = '-'.join(['20' + date[0:2], date[2:4], date[4:6]])

    metadata = [
        f'Title: {title}', f'Date: {date}',
        f'Category: {category}', f'Slug: {title}', '']

    abspath = os.path.join(root, path)
    with codecs.open(abspath, 'r', 'utf-8') as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]

    # すでにメタデータがある場合にはそれを削除する．
    if lines[0].startswith('Title:'):
        lines = lines[lines.index('') + 1:]

    text = '\n'.join(metadata + lines)
    with codecs.open(abspath, 'w', 'utf-8') as file:
        file.write(text)
