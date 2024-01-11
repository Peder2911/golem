from PIL import Image as img
import golem.screen
import golem.letters

def entrypoint():
    text = golem.screen.grab_debug_text(golem.screen.minecraft_window())
    resampled = golem.screen.resample_debug_text(text)

    message = ""
    letter = ""
    offset = 0
    while letter != None:
        letter,read = golem.letters.ocr(resampled[:,offset:])
        img.fromarray(resampled[:7,offset:offset+5]).save("testing/firsttry.png")
        if letter is None:
            offset += 4
            letter,read = golem.letters.ocr(resampled[:,offset:])
            if letter is not None:
                letter = " "+letter
            img.fromarray(resampled[:7,offset:offset+5]).save("testing/secondtry.png")
        offset += read+1
        if letter is not None:
            message += letter
    print(message)
