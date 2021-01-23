import os
import re
import shutil
import sys

try:
    import click
except ModuleNotFoundError:
    print("Python module - click - is not installed. Please run\n\tpip install click\n")
    sys.exit(0)

try:
    from PIL import Image
    from PIL.ExifTags import TAGS
    from PIL import UnidentifiedImageError
except ModuleNotFoundError:
    print("Python module - pillow - is not installed. Please run\n\tpip install pillow\n")
    sys.exit(0)


__author__ = "gomeisa"


@click.group()
def main():
    """
    Photo management script
    """
    pass


@main.command()
@click.option("--by", "-b", default="filename", help="Classify files by date from filename or exif:DateTimeOriginal")
def classify(by):
    click.echo(f"This is a Photo classification function for photos in current directory : option = {by}\n"
               f"Usage: python photo.py classify --by filename|exif")

    files = os.listdir()
    print(f"\nFound {len(files)} file(s) including all types file and directory")

    count = 0

    for file in files:
        if not os.path.isfile(file):
            continue
        if "filename" == by:
            p = re.compile(r"^(\d{4})(\d{2})(\d{2})_.*\.(?:jpg|png|gif|bmp|tif|mp4|avi|mov)")
            f = p.findall(file)

        elif "exif" == by:
            try:
                image = Image.open(file)
                info = image.getexif()
                image.close()
            except UnidentifiedImageError:
                print(f"{file} is not identified by pillow")
                continue

            datetime_original = info.get(36867)
            if datetime_original:
                p = re.compile(r"^(\d{4}):(\d{2}):(\d{2}) .*")
                f = p.findall(datetime_original)
            else:
                print(f"{file} has no EXIF information")
                continue

        else:
            print(f"\nWrong parameter: {by}. filename or exif is only allowed\n")
            sys.exit(0)

        if f:
            dir_name = f"[{f[0][0]}.{f[0][1]}.{f[0][2]}]"
            os.makedirs(dir_name, exist_ok=True)
            shutil.move(file, os.path.join(".", dir_name, file))
            print(f"Move {file} to {dir_name}")
            count += 1

    print(f"\nDone! {count} file(s) moved\n")


@main.command()
@click.option("--src", "-s", default=".", help="Source directory")
@click.option("--dst", "-d", help="Destination directory")
def compare(src, dst):
    click.echo(f"This is a Photo comparison function for photos in current directory\n"
               f"Usage: python photo.py compare --src source --dst destination")


if __name__ == "__main__":
    main()
