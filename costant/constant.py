TYPE_COOPERATION = [
    ("full_time", "تمام وقت"),
    ("part_time", "پاره وقت"),
    ("remote", "دورکار"),
    ("project", "پروژه ای"),
    ("novitiate", "کارآموزی")
]
DEGREE_OF_EDUCATIONS = [
    ("bachelor", "کارشناسی"),
    ("master", "کارشناسی ارشد"),
    ("PHD", "دکتری"),
]

GENDER = [
    ("male", "آقا"),
    ("female", "خانم"),
]

MILITARY_SERVICE = [
    ('inductee', 'مشمول'),
    ('exemption', 'معافیت پزشکی'),
    ('end_of_service_card', 'کارت پایان خدمت'),
    ('others', 'سایر'),
]
CATEGORY = [
    ("ui_ux", "طراح رابط کاربری "),
    ("backend", "برنامه نویس سرور"),
    ("frontend", "برنامه نویس")
]

APPLICANT_STATUS = [
    ("not_checked", "بررسی نشده"),
    ("awaiting_status", "در انتظار تعیین وضعیت"),
    ("confirmation_for_interview", "تایید برای مصاحبه"),
    ("hired", "استخدام شده"),
    ("rejected", "رد شده")
]
ANNOUNCEMENT_STATUS = [
    ("active", "فعال"),
    ("archive", "آرشيو"),
    ("closed", "بسته شده"),
]

MARITAL_STATUS = [
    ("single", "مجرد"),
    ("married", "متاهل"),
]

MONTH = [
    ("1", "فروردین"),
    ("2", "اردیبهشت"),
    ("3", "خرداد"),
    ("4", "تیر"),
    ("5", "مرداد"),
    ("6", "شهریور"),
    ("7", "مهر"),
    ("8", "آبان"),
    ("9", "آذر"),
    ("10", "دی"),
    ("11", "بهمن"),
    ("12", "اسفند"),
]
GRADE = [
    ("diploma", "دیپلم"),
    ("associate", "کاردانی"),
    ("bachelor", "کارشناسی"),
    ("masters", "کارشناسی ارشد"),
    ("phd_and_above", "دکترا وبالاتر"),
    ("other", "دیگر"),
]
MASTERY_LEVEL = [
    ("beginner", "مبتدی"),
    ("medium", "متوسط"),
    ("professional", "حرفه ای"),
    ("mother_tongue", "زبان مادری"),
]

LANGUAGE_NAME = [
    ("1", "آذری"),
    ("2", "آلمانی"),
    ("3", "ارمنی"),
    ("4", "اسپانیایی"),
    ("5", "انگلیسی"),
    ("6", "ایتالیایی"),
    ("7", "ترکی استامبولی"),
    ("8", "چینی"),
    ("9", "روسی"),
    ("10", "ژاپنی"),
    ("11", "سوئدی"),
    ("12", "عربی"),
    ("13", "فرانسویی"),
    ("14", "فنلاندی"),
    ("15", "کردی"),
    ("16", "کره ای"),
    ("17", "هلندی"),
    ("18", "هندی"),
]
LEVEL = [
    ("junior", "تازه كار"),
    ("mid_level", "متوسط"),
    ("senior", "ارشد"),
    ("manger", "مدير"),
]
SALARY = [
    ("agreement", "توافقي"),
    ("base", "حقوق وزارت كار"),
]
SALARY.extend([(str(i), f"از {i},000,000 تومان") for i in range(4, 50)])

JOB_BENEFITS = [("promotional", "امکان ترفیع سمت"),
                ("insurance", "بیمه"),
                ("education", "دوره های آموزشی"),
                ("flexible", "ساعت کاری منعطف"),
                ("commuting", "سرویس رفت وآمد"),
                ("food", "غذا برا عهده ی شرکت ")
                ]
