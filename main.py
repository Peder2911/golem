from PIL import Image as im
import autominer.screen

if __name__ == "__main__":
    text = autominer.screen.resample_debug_text(
        autominer.screen.grab_debug_text(autominer.screen.minecraft_window())
    )
    im.fromarray(text).save("text.png")
