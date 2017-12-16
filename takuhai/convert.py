import codecs
import os
from collections import OrderedDict


def convert(path, root='.'):
    """
    pathの文字列からメタデータを抽出して，pathのファイルに
    メタデータを書き込む．

    pathは<YYMMDD><sep><title>.<ext>の形式である必要がある．

    Parameters
    ----------
    path : str
        ファイル名
    root : str, optional
        ルートディレクトリ名．省略するとカレントディレクトリとする．
    """
    category = None
    directory, basename = os.path.split(path)
    while directory:
        directory, category = os.path.split(directory)

    basename = os.path.splitext(basename)[0]
    date, title = basename[:6], basename[7:]
    date = '-'.join(['20' + date[0:2], date[2:4], date[4:6]])

    metadata = OrderedDict()
    metadata['Title'] = title
    metadata['Date'] = date
    if category:
        metadata['Category'] = category

    abspath = os.path.join(root, path)
    with codecs.open(abspath, 'r', 'utf-8') as file:
        lines = file.readlines()

    def header(key, sep):
        return ': '.join([key, metadata.pop(key)]) + sep

    # 最初の空行か':'を含まない行までをメタデータとする．
    for index, line in enumerate(lines):
        sep = '\r\n' if line.endswith('\r\n') else '\n'
        if line.strip() == '' or ':' not in line:
            # 残っているメタデータを書き込む．
            for key in list(metadata.keys()):  # popするため
                lines.insert(index, header(key, sep))
                index += 1
            break
        key, *_ = line.split(':')
        key = key.strip()
        if key in metadata:
            lines[index] = header(key, sep)

    text = ''.join(lines)

    with codecs.open(abspath, 'w', 'utf-8') as file:
        file.write(text)


def main():
    root = 'C:/Users/daizu/Documents/GitHub/blog/content'
    path = 'Pelican/12/171215_ブログを始める.md'
    convert(path, root)


if __name__ == '__main__':
    main()
