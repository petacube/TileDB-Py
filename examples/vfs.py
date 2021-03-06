# vfs.py
#
# LICENSE
#
# The MIT License
#
# Copyright (c) 2018 TileDB, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# DESCRIPTION
#
# This is a part of the TileDB tutorial:
#   https://docs.tiledb.io/en/latest/tutorials/vfs.html
#
# This program explores the various TileDB VFS tools.
#

import struct
import tiledb


def dirs_files():
    ctx = tiledb.Ctx()

    # Create TileDB VFS
    vfs = tiledb.VFS(ctx)

    # Create directory
    if not vfs.is_dir("dir_A"):
        vfs.create_dir("dir_A")
        print("Created 'dir_A'")
    else:
        print("'dir_A' already exists")

    # Creating an (empty) file
    if not vfs.is_file("dir_A/file_A"):
        vfs.touch("dir_A/file_A")
        print("Created empty file 'dir_A/file_A'")
    else:
        print("'dir_A/file_A' already exists")

    # Getting the file size
    print("Size of file 'dir_A/file_A': {}".format(vfs.file_size("dir_A/file_A")))

    # Moving files (moving directories is similar)
    print("Moving file 'dir_A/file_A' to 'dir_A/file_B'")
    vfs.move_file("dir_A/file_A", "dir_A/file_B")

    # Deleting files and directories
    print("Deleting 'dir_A/file_B' and 'dir_A'")
    vfs.remove_file("dir_A/file_B")
    vfs.remove_dir("dir_A")


def write():
    ctx = tiledb.Ctx()

    # Create TileDB VFS
    vfs = tiledb.VFS(ctx)

    # Create VFS file handle
    f = vfs.open("tiledb_vfs.bin", "w")

    # Write binary data
    vfs.write(f, struct.pack("f", 153.0))
    vfs.write(f, "abcd".encode("utf-8"))
    vfs.close(f)

    # Write binary data again - this will overwrite the previous file
    f = vfs.open("tiledb_vfs.bin", "w")
    vfs.write(f, struct.pack("f", 153.1))
    vfs.write(f, "abcdef".encode("utf-8"))
    vfs.close(f)

    # Append binary data to existing file (this will NOT work on S3)
    f = vfs.open("tiledb_vfs.bin", "a")
    vfs.write(f, "ghijkl".encode("utf-8"))
    vfs.close(f)


def read():
    ctx = tiledb.Ctx()

    # Create TileDB VFS
    vfs = tiledb.VFS(ctx)

    # Read binary data
    f = vfs.open("tiledb_vfs.bin", "r")
    f1 = struct.unpack("f", vfs.read(f, 0, 4))[0]
    s1 = bytes.decode(vfs.read(f, 4, 12), "utf-8")
    print("Binary read:\n{}\n{}".format(f1, s1))

    vfs.close(f)


dirs_files()
write()
read()
