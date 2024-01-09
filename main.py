from PIL import Image as im
import autominer.screen
import autominer.letters

if __name__ == "__main__":
    text = autominer.screen.grab_debug_text(autominer.screen.minecraft_window())
    im.fromarray(text).save("text.png")
    resampled = autominer.screen.resample_debug_text(text)
    print(autominer.letters.ocr(resampled[:7,:5]))
