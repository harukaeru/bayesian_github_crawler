import pyautogui
import shutil
import time
import os
import mss
import mss.tools
from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly, kCGNullWindowID
# from AppKit import NSWorkspace

TARGET_PATH = './downloaded'

def get_xcode_window():
    window_list = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID)
    for window in window_list:
        if window['kCGWindowOwnerName'] == 'Xcode' and 'kCGWindowName' in window:
            return window
    return None

while True:
    done = set([line.replace('\n', '') for line in open('done.txt').readlines()])
    downloads = os.listdir(TARGET_PATH)
    for download in downloads:
        if download in done:
            continue


        # Main.storyboardファイルのパスを指定
        main_storyboard_path = download

        # XcodeでMain.storyboardファイルを開く
        # os.system(f"open -a Xcode {TARGET_PATH}/{main_storyboard_path}")
        # os.system(f"osascript -e 'tell application \"Xcode\" to open (POSIX file \"{TARGET_PATH}/{main_storyboard_path}\")'")
        shutil.copy(TARGET_PATH + '/' + main_storyboard_path, os.path.join('/Users/harukaeru/Desktop/Playground/Playground/Base.lproj', "Main.storyboard"))

        # Interface Builderが開くまで待つ
        time.sleep(3.5)
        # os.system("osascript -e 'tell application \"System Events\" to tell process \"Xcode\" to set value of attribute \"AXSize\" of window 1 to { h = 3840, w = 2160}'")

        xcode_window = get_xcode_window()
        if xcode_window:
            print(xcode_window['kCGWindowBounds'])
            x = xcode_window['kCGWindowBounds']['X']
            y = xcode_window['kCGWindowBounds']['Y']
            width = xcode_window['kCGWindowBounds']['Width']
            height = xcode_window['kCGWindowBounds']['Height']

            save_folder = "./screenshots"
            screenshot_name = download.replace('.', '_') + "_screenshot.png"
            x = 2840
            y = 0
            output = os.path.join(save_folder, screenshot_name)  # , region=(x, y, width, height)
            # pyautogui.screenshot()

            with mss.mss() as sct:
                # Get information of monitor 2
                monitor_number = 2
                mon = sct.monitors[monitor_number]

                # The screen part to capture
                monitor = {
                    "top": mon["top"],
                    "left": mon["left"],
                    "width": mon["width"],
                    "height": mon["height"],
                    "mon": monitor_number,
                }

                # Grab the data
                sct_img = sct.grab(monitor)

                # Save to the picture file
                mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
                print(output)

        done.add(download)
        # # Xcodeを閉じる
        # os.system("osascript -e 'quit app \"Xcode\"'")


    done_list = list(done)
    done_list.sort()
    with open('done.txt', 'w') as f:
        for d in done_list:
            f.write(d + '\n')

    time.sleep(30)

