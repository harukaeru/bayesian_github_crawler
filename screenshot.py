import pyautogui
import time
import os

# Xcodeを開く
# os.system("open -a Xcode")
#
# # Xcodeが開くまで待つ
# time.sleep(5)
#
# # Main.storyboardファイルのパスを指定
# main_storyboard_path = "Main.storyboard"
#
# # XcodeでMain.storyboardファイルを開く
# os.system(f"open -a Xcode {main_storyboard_path}")
#
# # Interface Builderが開くまで待つ
# time.sleep(5)

# スクリーンショットの保存先フォルダを指定
save_folder = "./"

# スクリーンショットのファイル名を指定
screenshot_name = "main_storyboard_screenshot.png"

# スクリーンショットを撮影し、指定したフォルダに保存
pyautogui.screenshot(os.path.join(save_folder, screenshot_name))

# Xcodeを閉じる
os.system("osascript -e 'quit app \"Xcode\"'")
