import zipfile, tempfile, os, git

def load_zip(upload):
    tmp = tempfile.mkdtemp()
    p = os.path.join(tmp,"p.zip")
    open(p,"wb").write(upload.getbuffer())
    zipfile.ZipFile(p).extractall(tmp)
    return tmp

def load_github(url):
    tmp = tempfile.mkdtemp()
    git.Repo.clone_from(url,tmp,depth=1)
    return tmp
