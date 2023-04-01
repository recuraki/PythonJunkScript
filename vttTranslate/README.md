docker build ./ -t vtttranslate

docker run -it -v "${PWD}:/opt/" vtttranslate python3 run.py

