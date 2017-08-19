FROM pypy:3-onbuild
MAINTAINER bunseokbot

EXPOSE 80

CMD ["pypy3", "app.py"]
