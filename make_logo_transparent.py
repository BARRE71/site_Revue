import os
import sys

from PIL import Image


def make_white_transparent(image_path: str, threshold: int = 245, trim: bool = True) -> None:
    """Convert near-white pixels to transparent in-place for a PNG image.

    Args:
        image_path: Absolute path to the image file to process.
        threshold: Values >= threshold for all RGB channels are treated as white.
    """
    img = Image.open(image_path).convert("RGBA")
    pixels = img.getdata()

    new_pixels = []
    for r, g, b, a in pixels:
        if r >= threshold and g >= threshold and b >= threshold:
            new_pixels.append((r, g, b, 0))
        else:
            new_pixels.append((r, g, b, a))

    img.putdata(new_pixels)

    # Optionally trim transparent borders to remove empty padding
    if trim:
        alpha = img.split()[-1]
        bbox = alpha.getbbox()
        if bbox:
            img = img.crop(bbox)

    img.save(image_path, format="PNG")


def main():
    # Allow optional CLI path; otherwise, try Django SiteSettings.logo
    if len(sys.argv) > 1:
        target = sys.argv[1]
        if not os.path.isabs(target):
            target = os.path.abspath(target)
        make_white_transparent(target)
        print(f"Processed logo: {target}")
        return

    # Fallback: load via Django SiteSettings.logo
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "revue_maroc.settings")
    import django
    django.setup()

    from core.models import SiteSettings

    settings = SiteSettings.objects.first()
    if not settings or not settings.logo:
        print("No logo found in SiteSettings.")
        return

    logo_path = settings.logo.path
    make_white_transparent(logo_path)
    print(f"Processed logo in-place: {logo_path}")


if __name__ == "__main__":
    main()


