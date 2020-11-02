# Persian Programming Language
a simple persian programming language written in python
## instructions
To interpret run this command on console:
```
python3 interpreter.py <file adress>
```
Warning : File should be have .fd format
For example:
```
python3 interpreter.py examples/helloworld.fd
```
If you do not have file , You can programming live with Terminal:
```
python3 interpreter.py
```
## Examples
### hello world
```plain
"سلام، دنیا!"
```
### print
```plain
"چاپ کن "سلام دنیا
```
### if else
```plain
اگر 12 برابر 10 + 2 باشد آنگاه "ده با دو میشود دوازده" وگرنه "ده با دو نمیشود دوازده"
```
### user input
```plain
عدد = عددگیر
نام = ورودی
```
### comments
```plain
# این یک کامنت است
# کامنت ها برنامه را تغییر نمیدهند
```
### divisor
```plain
اگر 5 شمارنده 10 باشد آنگاه "درسته" وگرنه "غلطه"
```
### functions
```plain
زوج_فرد یعنی اگر 2 شمارنده عدد باشد آنگاه "زوج" وگرنه "فرد"

عدد = 15
زوج_فرد را اجرا کن
```
### operators
```plain
اول = 10
دوم = 2

جمع = اول + دوم
تفریق = اول - دوم
ضرب = اول * دوم
تقسیم = اول / دوم
```

* * *

**This Interpreter Made Using [SLY](https://sly.readthedocs.io/en/latest/sly.html)**
