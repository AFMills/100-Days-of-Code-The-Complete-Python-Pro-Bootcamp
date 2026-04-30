import pyautogui as gui
import keyboard
import time
import math
from PIL import Image


def get_pixel(img, x, y):
    """Get RGB of a pixel safely."""
    px = img.load()
    return px[x, y]


def main():
    print("🚀 Dino Bot starting in 5 seconds...")
    print("Make sure Chrome Dino game is open and visible.")
    print("Press 'Q' to stop the bot at any time.")

    time.sleep(5)  # Time to switch to Chrome and focus the game window

    # Screenshot region: adjust these if your screen resolution differs
    # (x, y, width, height) - full-ish screen capture starting near top-left of game area
    region = (0, 100, 2560, 1440)  # Common for 1920x1080 screens

    # Game parameters (tune if needed for your resolution)
    dino_y_ground = 557  # Y position to check for ground-level obstacles (cacti)
    dino_y_high = 486  # Higher Y for taller cacti
    bird_y = 460  # Y position for flying birds
    scan_start_x = 400  # Where to start scanning ahead of the dino
    scan_end_x = 415  # Initial scan width (gets wider as speed increases)

    last_jump_time = 0
    last_interval = 0
    bg_color = None

    while True:
        if keyboard.is_pressed('q'):
            print("🛑 Bot stopped by user.")
            break

        try:
            # Take screenshot of the game area
            screenshot = gui.screenshot(region=region)
            # screenshot.save("debug_dino.jpg")  # Uncomment for debugging

            # Get background color (usually white/light) from a safe spot
            if bg_color is None:
                bg_color = get_pixel(screenshot, 100, 100)

            jumped = False

            # Scan from right to left (closer obstacles first) for ground obstacles
            for x in range(scan_end_x, scan_start_x - 1, -1):
                # Check ground level (cacti)
                if (get_pixel(screenshot, x, dino_y_ground) != bg_color or
                        get_pixel(screenshot, x, dino_y_high) != bg_color):
                    gui.press('up')  # or keyboard.press_and_release('space')
                    last_jump_time = time.time()
                    jumped = True
                    break

                # Check for birds (higher up)
                if get_pixel(screenshot, x, bird_y) != bg_color:
                    gui.keyDown('down')
                    time.sleep(0.35)  # Duck duration
                    gui.keyUp('down')
                    break

            # Increase scan range as game speeds up (optional but helps at high scores)
            if jumped:
                current_interval = time.time() - last_jump_time
                if last_interval > 0 and math.floor(current_interval) != math.floor(last_interval):
                    scan_end_x = min(scan_end_x + 5, region[2] - 50)  # Expand scan area

                last_interval = current_interval

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(0.1)

        # Small delay to avoid 100% CPU
        time.sleep(0.01)


if __name__ == "__main__":
    main()