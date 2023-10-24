# encoding: utf-8
import asyncio
import cmd
import hashlib
import os
import time


def decrypt_h5st(info):
    file = open(
        os.path.join(os.getcwd(), "jdSpider\\utils\\decrypt\\security.js"),
        "r",
        encoding="utf-8",
    ).read()

    content = file.replace("%SIGN%", str(info).replace("'", '"').replace(" ", ""))
    # 写入临时文件
    tmp_file = str(int(time.time())) + "security.js"

    with open(tmp_file, "w", encoding="utf-8") as f:
        f.write(content)

    res = os.popen("node " + tmp_file)
    output_str = res.buffer.read().decode(encoding="utf-8").strip()
    # 删除文件
    os.remove(tmp_file)
    return output_str


def aes256(body: str):
    s = hashlib.sha256()  # Get the hash algorithm.
    s.update(body.encode("utf-8"))
    b = s.hexdigest()  # Get he hash value.
    return b
