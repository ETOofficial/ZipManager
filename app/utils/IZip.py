from pathlib import Path
from typing import BinaryIO

import py7zr

from app.utils.fileOperator import getname


class ISevenZipFile:
    def compress(self, file: BinaryIO | str | Path, path: Path | str, arcname: str | None = None, mode: str = "w", *,
                 filters: list[dict[str, int]] | None = None, dereference: bool = False, password: str | None = None,
                 header_encryption: bool = False, blocksize: int | None = None, mp: bool = False):
        # 生成的压缩文件路径
        archive = py7zr.SevenZipFile(
            file,
            mode,
            filters=filters,
            dereference=dereference,
            password=password,
            header_encryption=header_encryption,
            blocksize=blocksize,
            mp=mp
        )
        archive.writeall(path, arcname)
        archive.close()

    def single_compress(self, paths: list[Path | str], arcname: str | None = None,
                        mode: str = "w", *, filters: list[dict[str, int]] | None = None, dereference: bool = False,
                        password: str | None = None, header_encryption: bool = False, blocksize: int | None = None,
                        mp: bool = False):
        """每个文件单独压缩"""
        for path in paths:
            file = path + ".7z"
            arcname = getname(path) if arcname is None else arcname
            self.compress(
                file,
                path,
                arcname,
                mode,
                filters=filters,
                dereference=dereference,
                password=password,
                header_encryption=header_encryption,
                blocksize=blocksize,
                mp=mp
            )
