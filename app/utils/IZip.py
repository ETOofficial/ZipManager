from pathlib import Path
from typing import BinaryIO

import py7zr


class ISevenZipFile:
    def SevenZipFile(
            self,
            file: BinaryIO | str | Path,
            path: Path | str,
            arcname: str | None,
            mode: str = "r",
            *,
            filters: list[dict[str, int]] | None = None,
            dereference: bool = False,
            password: str | None = None,
            header_encryption: bool = False,
            blocksize: int | None = None,
            mp: bool = False
    ):
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

    def compress_single(
            self,
            files: list[BinaryIO | str | Path],
            path: Path | str,
            arcname: str | None,
            mode: str = "r",
            *,
            filters: list[dict[str, int]] | None = None,
            dereference: bool = False,
            password: str | None = None,
            header_encryption: bool = False,
            blocksize: int | None = None,
            mp: bool = False
    ):
        """每个文件单独压缩"""
        for file in files:
            self.SevenZipFile(
                file,
                mode,
                path,
                arcname,
                filters=filters,
                dereference=dereference,
                password=password,
                header_encryption=header_encryption,
                blocksize=blocksize,
                mp=mp
            )
