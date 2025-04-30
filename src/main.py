import os, shutil, re
from markdown_blocks import markdown_to_html_node

def lstree(fpath, results=None):
    """Recursively traverses a directory tree and builds a list of all file and directory paths."""
    if results is None: results = []
    
    results.append(fpath)
    if os.path.isfile(fpath):
        return
    else:
        for path in os.listdir(fpath):
            lstree(fpath + '/' + path, results)
        return results[1:]


# we can use it to delete contents from public
def rmtree(path):
    paths = lstree(path)
    for fpath in paths[::-1]: 
        if os.path.isfile(fpath): os.remove(fpath)
        else: os.rmdir(fpath)
    assert lstree(path) == []

# we can use it to copy
def cptree(src, dst):
    if not os.path.exists(src):
        raise Exception(f'{src} doesnot exist')
    if not os.path.exists(dst):
        raise Exception(f'{dst} doesnot exist')
    
    # first, empty dst folder
    rmtree(dst)

    paths = lstree(src)
    ix = len(src) # extract file or foldername from path
    
    # first make folders
    for fpath in paths:
        fldr = fpath[ix: ]
        if os.path.isdir(fpath):
            print(f'Copying {fpath}')
            os.mkdir(dst + fldr)
    
    # then copy files
    for fpath in paths:
        file = fpath[ix: ]
        if os.path.isfile(fpath):
            print(f'Copying {fpath}')
            shutil.copy(fpath, dst + file)

    assert len(lstree(src)) == len(lstree(dst))
    print(80 * '-')
    print(f'Successfully copied {len(lstree(src))} files and folders from {src} to {dst}')


def extract_title(md):
    if not md.startswith('# '):
        raise ValueError('Title must start with "# "')
    mo = re.match(r'^#\s.+', md)
    return mo.group(0)[2:].strip()
    
def generate_page(from_path, template_path, dest_path, basepath=None):
    print(f" * {from_path} {template_path} -> {dest_path}")

    with open(from_path) as f: md = f.read()
    with open(template_path) as f: tmp_html = f.read()
    content = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    tmp_html = tmp_html.replace('{{ Title }}', title).replace('{{ Content }}', content)
    tmp_html = tmp_html.replace('href="/', f'href="{basepath}')
    tmp_html = tmp_html.replace('src="/', f'src="{basepath}')

    if not os.path.exists(dest_path):
        dirname = os.path.dirname(dest_path)
        os.makedirs(dirname, exist_ok=True)
        with open(dest_path, 'w') as f:
            f.write(tmp_html)
    return f'Succeffuly wrote to file {dest_path}: {os.path.exists(dest_path)}'

from pathlib import Path

def generate_pages_recursive(content_dir_path, template_path, dest_dir_path, basepath=None):
    for path in lstree(content_dir_path):
        if os.path.isfile(path):
            parts = Path(path).parts[1:] # remove root src dir
            dest_path = Path(dest_dir_path).joinpath(*parts).with_suffix('.html')
            generate_page(path, template_path, dest_path, basepath)


static_dir = './static'
content_dir = './content'
template_path = './template.html'
docs_dir = './docs'

import sys

def main():
    try:
        basepath = sys.argv[1]
    except IndexError:
        basepath = '/'
    print(f'Base path is: {basepath}')
    cptree(static_dir, docs_dir)
    generate_pages_recursive(content_dir, template_path, docs_dir, basepath)


main()
