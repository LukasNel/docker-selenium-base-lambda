import os
import os
from contextlib import contextmanager

@contextmanager
def managed_driver_for_lambda():
    os.chdir("/tmp/")
    from seleniumbase import Driver
    import Xlib.display
    from pyvirtualdisplay import Display
    with Display(visible=False, size=(100, 60),backend="xvfb", use_xauth=True) as disp:
        print("DISPLAY",os.environ['DISPLAY'])
        # return os.environ['DISPLAY'] + " " + str(disp) + str(disp.is_alive())
        os.environ["DISPLAY"] = disp.new_display_var
        import pyautogui
        pyautogui._pyautogui_x11._display = Xlib.display.Display(os.environ['DISPLAY'])
        print("Initialised pyautogui")
        driver = Driver(
                undetectable=True,   
                binary_location='/opt/chrome/chrome',  
                headless2=True,  
                no_sandbox=True,
                # remote_debug=True,  
                uc_cdp_events=False, 
                user_data_dir='/tmp/chrome-user-data',
                # data_path='/tmp/chrome-data-path',
                # disk_cache_dir='/tmp/chrome-disk-cache-dir',
                chromium_arg="--disable-dev-tools,--no-sandbox,--disable-dev-shm-usage,--no-zygote,--remote-debugging-port=9222",  
                cap_string='{"browserVersion":"118.0.5993.70"}'  
            )
        print("Initialised driver")
        yield driver
        driver.quit()
def handler(event=None, context=None):
    with managed_driver_for_lambda() as driver:
        url = "https://gitlab.com/users/sign_in"
        print("running uc_open_with_reconnect")
        driver.uc_open_with_reconnect(url, 4)
        # driver.uc_gui_click_captcha()
        print("Success")
    return "Success"

if __name__ == "__main__":
    handler()