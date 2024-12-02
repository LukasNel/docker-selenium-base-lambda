from seleniumbase import Driver
import os

def handler(event=None, context=None):
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
                remote_debug=True,  
                uc_cdp_events=False, 
                user_data_dir='/tmp/chrome-user-data',
                # data_path='/tmp/chrome-data-path',
                # disk_cache_dir='/tmp/chrome-disk-cache-dir',
                chromium_arg="--disable-dev-tools,--no-sandbox,--disable-dev-shm-usage,--no-zygote,--remote-debugging-port=9222",  
                cap_string='{"browserVersion":"118.0.5993.70"}'  
            )
        url = "https://gitlab.com/users/sign_in"
        print("running lambda")

        driver.uc_open_with_reconnect(url, 4)
        print("running lambda")

        # driver.uc_gui_click_captcha()
        print("running lambda")

        driver.quit()
    return "Success"

if __name__ == "__main__":
    handler()