FROM amazon/aws-lambda-python:3.10 as build
RUN yum install -y unzip && \
    curl -Lo "/tmp/chromedriver-linux64.zip" "https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.85/linux64/chromedriver-linux64.zip" && \
    curl -Lo "/tmp/chrome-linux64.zip" "https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.85/linux64/chrome-linux64.zip" && \
    unzip /tmp/chromedriver-linux64.zip -d /opt/ && \
    unzip /tmp/chrome-linux64.zip -d /opt/

FROM amazon/aws-lambda-python:3.10

RUN yum install -y atk cups-libs gtk3 libXcomposite alsa-lib \
    libXcursor libXdamage libXext libXi libXrandr libXScrnSaver \
    libXtst pango at-spi2-atk libXt xorg-x11-server-Xvfb \
    xorg-x11-xauth dbus-glib dbus-glib-devel nss mesa-libgbm
RUN pip install selenium==4.27.1 selenium-base
COPY --from=build /opt/chrome-linux64 /opt/chrome
COPY --from=build /opt/chromedriver-linux64 /opt/
RUN yum install -y xorg-x11-server-Xvfb python3-tkinter 
RUN yum install -y python3-devel
RUN pip install  Xlib
RUN yum install -y git
RUN pip install PyVirtualDisplay
RUN pip install git+https://github.com/LukasNel/pyautogui.git
RUN DISPLAY=:0 pip install python-xlib
RUN seleniumbase get chromedriver --path 
RUN seleniumbase get uc_driver --path 
COPY main.py ./main.py
RUN pip install undetected-chromedriver
RUN python ./main.py
CMD [ "main.handler" ]