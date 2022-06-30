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
    ('not_important', 'مهم نیست'),
]
CATEGORY = [
    ("designer", "Designer"),
    ("backend", "Backend developer"),
    ("frontend", "Frontend developer"),
    ("full_stack","Full stack developer"),
    ("manager","Manager"),
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

NUMBER_EMPLOYEES=[
    ("1-50","1 تا 50 نفر "),
    ("51-100","51 تا 100 نفر "),
    ("101-200","101 تا 200 نفر "),
    ("201-300","201 تا 300 نفر "),
    ("301-400","301 تا 400 نفر "),
    ("401-500","401 تا 500 نفر "),
    ("501-1000","501 تا 1000 نفر "),
    ("1001","بیشتر از 1000 نفر"),

]