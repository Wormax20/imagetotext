from PIL import Image
import time
import os
from colorama import init

init(autoreset=True)

path = "D:\\Image.jpg" #照片的絕對路徑


class ImageToColoredText:
    def __init__(self):
        self.ascii_chars = ["y", "u", "k", "i"]

    def __image_to_text(self, image) -> None:
        width, height = image.size
        for y in range(0, height, 2):
            row = ""
            for x in range(width):
                pixel = image.getpixel((x, y))
                row += self.__pixel_to_colored_text(pixel)
            print(row, flush=True)
            if row.strip() == "":
                continue
            time.sleep(0.01)
        print(flush=True)
        print()

    def __pixel_to_colored_text(self, pixel) -> str:
        r, g, b = pixel
        avg = (r + g + b) // 3
        char = self.ascii_chars[min(len(self.ascii_chars) - 1, avg * len(self.ascii_chars) // 256)]
        return self.__get_ansi_color(r, g, b) + char

    def __get_ansi_color(self, r, g, b):
        if r == g == b:
            if r < 8:
                return f"\033[38;5;16m"
            if r > 248:
                return f"\033[38;5;231m"
            return f"\033[38;5;{232 + (r - 8) // 10}m"
        
        ansi = 16 + (36 * (r // 51)) + (6 * (g // 51)) + (b // 51)
        return f"\033[38;5;{ansi}m"

    def __load_image(self, image_path) -> Image.Image:
        try:
            return Image.open(image_path)
        except Exception as e:
            print(f"Error loading image: {e}")
            return None

    def run(self) -> None:
        image_path = os.path.join(path)
        image = self.__load_image(image_path)
        if image is None:
            return

        terminal_width = os.get_terminal_size().columns
        aspect_ratio = image.height / image.width
        new_width = terminal_width
        new_height = int(new_width * aspect_ratio)
        image = image.resize((new_width, new_height))
        
        self.__image_to_text(image=image)

def main() -> None:
    image_to_text = ImageToColoredText()
    image_to_text.run()

if __name__ == "__main__":
    main()
