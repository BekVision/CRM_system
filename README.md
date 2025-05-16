# CRM_system
# Clothes CRM
**Clothes CRM** — bu kiyim-kechak do‘koni uchun mo‘ljallangan, mijozlar, mahsulotlar, buyurtmalar va ombor boshqaruvi imkoniyatlarini o‘zida jamlagan, zamonaviy va qulay CRM (Customer Relationship Management) tizimi.
## Loyihaning asosiy imkoniyatlari
- **Mijozlarni boshqarish:** Yangi mijozlar qo‘shish, tahrirlash, ro‘yxatini ko‘rish va o‘chirish.
- **Mahsulotlarni boshqarish:** Kategoriya va boshqa tavsiflar bo‘yicha mahsulotlarni qo‘shish, tahrirlash va o‘chirish.
- **Buyurtma boshqaruvi:** Kiritilgan buyurtmalar ro‘yxatini yuritish, yangilash va buyurtma detallarini ko‘rish.
- **Ombor nazorati:** Mahsulotlar qolgan zaxirasini avtomatik kuzatib borish.
- **To‘lovlar boshqaruvi:** Har bir buyurtmaning to‘lov statusini nazorat qilish (agar kerak bo‘lsa).
- **Rol asosida boshqaruv:** Admin, menejer va boshqa xodimlar uchun alohida login va dashboardlar.
- **Statistika va hisobotlar:** Mijozlar soni, buyurtmalar soni, umumiy tushum va boshqa ko‘rsatkichlar.

## Texnologiyalar va kutubxonalar
- **Backend**: Python 3.12, Django 5.x
- **Frontend**: HTML5, Bootstrap 5
- **Ma’lumotlar bazasi**: PostgreSQL
- **Dastur arxitekturasi**: Django MVC (Model-View-Controller)
- **Fayllar uchun:** Pillow
- **Autentifikatsiya:** Django Auth
## O‘rnatish va sozlash
1. Loyihani yuklab oling:
``` bash
    git clone <repo_link>
    cd clothes
```
1. Virtual muhit yaratish va faollashtirish:
``` bash
    python3 -m venv .venv
    source .venv/bin/activate
```
1. Zarur kutubxonalarni o‘rnatish:
``` bash
    pip install -r requirements.txt
```
1. Ma’lumotlar bazasini sozlang va migratsiyalarni bajaring:
``` bash
    python manage.py migrate
```
1. Superuser yarating:
``` bash
    python manage.py createsuperuser
```
1. Serverni ishga tushiring:
``` bash
    python manage.py runserver
```
1. Tizimga kirish uchun:
    - Admin uchun: `/admin-dashboard/`
    - Menejer uchun: `/manager-dashboard/`

## Loyihaning papka tuzilishi (asosiy qismlar)
``` 
clothes/
├── myapp/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
├── manage.py
├── requirements.txt
└── README.md
```
## Lavozimli foydalanuvchilar
- **Admin** — barcha amallar va statistikani boshqaradi.
- **Manager** — faqat mijozlar, mahsulotlar va buyurtmalar ustida ish olib boradi.

## Hissa qo‘shish
Taklif va hissa qo‘shish uchun:
1. Fork qiling.
2. Yangi branch oching.
3. O‘zgartirish kiriting va push qiling.
4. Pull request yuboring.

## Muallif va litsenziya
- Muallif: Asadbek.
- Litsenziya: MIT

**Savollar va takliflar uchun:** Issues bo‘limida yozib qoldiring.
