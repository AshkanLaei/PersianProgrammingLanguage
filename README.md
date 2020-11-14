<div dir="rtl">
  
# زبان برنامه نویسی فردوسی
یک زبان برنامه نویسی ساده؛ نوشته شده با پایتون
<br>
*این زبان در حال حاضر در حال برنامه نویسی می باشد و ممکن است دارای اشکالاتی باشد *

## روش استفاده
برای تفسیر دستور زیر را در خط فرمان وارد کنید:
</div>

```
python3 interpreter.py <آدرس فایل>
```

<div dir="rtl">
  
توجه: فایل باید دارای پسوند fd. باشد

برای مثال:
</div>

```
python3 interpreter.py examples/helloworld.fd
```
<div dir="rtl">

اگر در حال حاضر فایلی ندارید، می‌توانید به طور زنده در ترمینال برنامه نویسی کنید:
</div>
  
```
python3 interpreter.py
```
<div dir="rtl">


## مثال‌ها
### سلام دنیا

```plain
"سلام، دنیا!"
```
  
### چاپ

```plain
"چاپ کن "سلام دنیا
```
  
### شرط‌ها

```plain
اگر 12 برابر 10 + 2 باشد آنگاه "ده با دو میشود دوازده" وگرنه "ده با دو نمیشود دوازده"
```
    
### ورودی

```plain
عدد = عددگیر
نام = ورودی
```

### کامنت‌ها

```plain
# این یک کامنت است
// این هم یک کامنت است
# کامنت ها برنامه را تغییر نمیدهند
```

### شمارنده

```plain
اگر 5 شمارنده 10 باشد آنگاه "درسته" وگرنه "غلطه"
```

### تابع‌ها

```plain
زوج_فرد یعنی اگر 2 شمارنده عدد باشد آنگاه "زوج" وگرنه "فرد"

عدد = 15
زوج_فرد را اجرا کن
```
  
### عملگرها

```plain
اول = 10
دوم = 2

جمع = اول + دوم
تفریق = اول - دوم
ضرب = اول * دوم
تقسیم = اول / دوم
```
</div>

* * *
<div dir="rtl">

**این مفسر به وسیله [SLY](https://sly.readthedocs.io/en/latest/sly.html) ساخته شده است**
</div>
