from main_server.database_manager import fetch_all_children
from pathlib import Path
import os
import tqdm
import paramiko

remote_root = "/home/pi/raspi_network"

files = list(Path(".").rglob("*.py")) + list(Path(".").rglob("*.json"))

servers = fetch_all_children()
urls = list(map(lambda x: x["IP"],servers))

s = paramiko.SSHClient()
s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
for url in tqdm.tqdm(urls):
    tqdm.tqdm.write(url+"\n")
    s.connect(url,22,username="pi",password="raspberry",timeout=4)
    sftp = s.open_sftp()
    for file in files:
        file_abs = str(file.absolute())
        file_rel = str(file.relative_to("."))
        path = os.path.join(remote_root,file_rel)
        tqdm.tqdm.write(file_abs+"\t->\t"+path+"\n")
        sftp.put(file_abs, path)