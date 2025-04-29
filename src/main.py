import os, shutil

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
    print(f'Deleting {path}...')
    print(80 * '-')
    paths = lstree(path)
    # first remove files:
    for fpath in paths: 
        if os.path.isfile(fpath): os.remove(fpath)
    # then remove empty dirs
    for fpath in paths:
        if os.path.isdir(fpath): os.rmdir(fpath)
    # make sure it's clean
    assert lstree(path) == []

# we can use it to copy
def cptree(src, dst):
    if not os.path.exists(src):
        raise Exception(f'{src} doesnot exist')
    if not os.path.exists(dst):
        raise Exception(f'{dst} doesnot exist')
    # first, make sure dst folder is empty
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


def main():
    main_file_path = os.path.abspath(__file__)
    dir_path  = os.path.dirname(main_file_path)
    root_dir = os.path.dirname(dir_path)
    
    src_dir = os.path.join(root_dir, 'static')
    dst_dir = os.path.join(root_dir, 'public')
    
    cptree(src_dir, dst_dir)



main()
