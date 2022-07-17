from collections import OrderedDict

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response



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
YEARS_WORK_EXPERIENCE=[
    ("unlimited","بدون محدودیت سابقه کار"),
    ("less_three_","کمتر از سه سال"),
    ("between_three_five","بین سه تا پنج سال"),
    ("more_five","بیشتر از پنج سال"),
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
SALARY.extend([(str(i), f"از {i},000,000 تومان") for i in range(7, 50,2)])

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

class ConstantView(viewsets.ModelViewSet):
    permission_classes = [AllowAny]

    @staticmethod
    def constant_refactor(constant_tuple, default=None):
        dic = OrderedDict(constant_tuple)
        data = {'count': len(constant_tuple),
                'results': [{'en_name': a[0], 'fa_name': a[1]} for a in dic.items()]}
        if default is not None:
            data.update({'default': {'en_name': default, 'fa_name': dic[default]}})
        else:
            data.update({'default': None})
        return data

    @action(methods=['get'], detail=False)
    def type_cooperation(self, request):
        return Response(self.constant_refactor(TYPE_COOPERATION, 'full_time'))

    @action(methods=['get'], detail=False)
    def degree_of_educations(self, request):
        return Response(self.constant_refactor(DEGREE_OF_EDUCATIONS, 'bachelor'))

    @action(methods=['get'], detail=False)
    def gender(self, request):
        return Response(self.constant_refactor(GENDER, None))

    @action(methods=['get'], detail=False)
    def military_service(self, request):
        return Response(self.constant_refactor(MILITARY_SERVICE, None))

    @action(methods=['get'], detail=False)
    def category(self, request):
        return Response(self.constant_refactor(CATEGORY, None))

    @action(methods=['get'], detail=False)
    def applicant_status(self, request):
        return Response(self.constant_refactor(APPLICANT_STATUS, 'not_checked'))

    @action(methods=['get'], detail=False)
    def announcement_status(self, request):
        return Response(self.constant_refactor(ANNOUNCEMENT_STATUS, None))

    @action(methods=['get'], detail=False)
    def marital_status(self, request):
        return Response(self.constant_refactor(MARITAL_STATUS, None))

    @action(methods=['get'], detail=False)
    def month(self, request):
        return Response(self.constant_refactor(MONTH, None))

    @action(methods=['get'], detail=False)
    def grade(self, request):
        return Response(self.constant_refactor(GRADE, None))

    @action(methods=['get'], detail=False)
    def mastery_level(self, request):
        return Response(self.constant_refactor(MASTERY_LEVEL, None))

    @action(methods=['get'], detail=False)
    def language_name(self, request):
        return Response(self.constant_refactor(LANGUAGE_NAME, "5"))

    @action(methods=['get'], detail=False)
    def level(self, request):
        return Response(self.constant_refactor(LEVEL, None))

    @action(methods=['get'], detail=False)
    def salary(self, request):
        return Response(self.constant_refactor(SALARY, 'agreement'))

    @action(methods=['get'], detail=False)
    def job_benefits(self, request):
        return Response(self.constant_refactor(JOB_BENEFITS, None))

    @action(methods=['get'], detail=False)
    def years_work_experience(self, request):
        return Response(self.constant_refactor(YEARS_WORK_EXPERIENCE, None))

    @action(methods=['get'], detail=False)
    def number_employees(self, request):
        return Response(self.constant_refactor(NUMBER_EMPLOYEES, None))
