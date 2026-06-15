# 📘 دليل المشروع الشامل
# Evaluation of Cache Utilization for Different Cache Associativities
# تقييم استخدام الذاكرة المخبئية لمستويات مختلفة من الترابط التجميعي

---

# 📑 فهرس المحتويات

1. [ما هو هذا المشروع؟](#1--ما-هو-هذا-المشروع)
2. [المتطلبات والمكتبات المطلوبة](#2--المتطلبات-والمكتبات-المطلوبة)
3. [خطوات التثبيت من الصفر](#3--خطوات-التثبيت-من-الصفر)
4. [كيفية التشغيل خطوة بخطوة](#4--كيفية-التشغيل-خطوة-بخطوة)
5. [فهم الملفات والأكواد](#5--فهم-الملفات-والأكواد)
6. [فهم النتائج وملف stats.txt](#6--فهم-النتائج-وملف-statstxt)
7. [التقرير الأكاديمي الكامل](#7--التقرير-الأكاديمي-الكامل)
8. [الأسئلة الشائعة وحل المشاكل](#8--الأسئلة-الشائعة-وحل-المشاكل)

---

# 1. 🎯 ما هو هذا المشروع؟

## الفكرة الأساسية

هذا المشروع يستخدم محاكي **gem5** لدراسة تأثير **الترابط التجميعي (Cache Associativity)** على أداء الذاكرة المخبئية (Cache).

**بكلمات بسيطة:**
- الذاكرة المخبئية (Cache) هي ذاكرة صغيرة وسريعة جداً بين المعالج والذاكرة الرئيسية
- **الترابط التجميعي** يحدد كم مكان متاح لتخزين بيانات معينة في الـ Cache
- كلما زاد الترابط → قلّ التعارض → تحسّن الأداء (لكن بتكلفة أعلى في العتاد)

## ما الذي نقارنه؟

| الإعداد | Associativity | الوصف |
|:---:|:---:|:---|
| 🟥 Direct-Mapped | **1-way** | كل عنوان ذاكرة له مكان واحد فقط في الـ Cache |
| 🟧 2-Way | **2-way** | كل عنوان يمكن تخزينه في مكانين |
| 🟨 4-Way | **4-way** | كل عنوان يمكن تخزينه في 4 أماكن |
| 🟩 8-Way | **8-way** | كل عنوان يمكن تخزينه في 8 أماكن |

## ماذا نقيس؟

- **Hit Rate** (نسبة الإصابة): كم مرة وجدنا البيانات في الـ Cache
- **Miss Rate** (نسبة الإخفاق): كم مرة لم نجد البيانات
- **AMAT** (متوسط وقت الوصول): الوقت الفعلي للوصول للبيانات
- **Simulation Ticks** (دورات المحاكاة): إجمالي الوقت المستغرق

---

# 2. 🔧 المتطلبات والمكتبات المطلوبة

## 2.1 متطلبات النظام

| المتطلب | التفاصيل |
|:---|:---|
| **نظام التشغيل** | Windows 10/11 مع WSL2 (Windows Subsystem for Linux) |
| **الذاكرة RAM** | 8 GB كحد أدنى (16 GB مُوصى به) |
| **مساحة القرص** | 10 GB على الأقل (gem5 يحتاج ~5 GB بعد البناء) |
| **المعالج** | 4 أنوية على الأقل (لتسريع بناء gem5) |

## 2.2 البرامج المطلوبة على Windows

| البرنامج | الغرض | طريقة التثبيت |
|:---|:---|:---|
| **WSL2** | تشغيل Linux داخل Windows | `wsl --install` في PowerShell (كمسؤول) |
| **Ubuntu** | توزيعة Linux (تثبت تلقائياً مع WSL) | يأتي مع WSL |

## 2.3 المكتبات والأدوات المطلوبة داخل WSL (Ubuntu)

### مكتبات البناء الأساسية (Build Essentials)

| المكتبة/الأداة | الغرض | الحزمة |
|:---|:---|:---|
| **GCC/G++** | مترجم C/C++ لبناء gem5 وبرنامج الاختبار | `build-essential` |
| **SCons** | نظام بناء gem5 | `scons` |
| **Python 3** | لغة سكريبتات gem5 | `python3-dev` |
| **Git** | استنساخ gem5 من GitHub | `git` |

### مكتبات gem5 الإضافية

| المكتبة | الغرض | الحزمة |
|:---|:---|:---|
| **zlib** | ضغط البيانات | `zlib1g` `zlib1g-dev` |
| **Protocol Buffers** | تسلسل البيانات | `libprotobuf-dev` `protobuf-compiler` |
| **Google PerfTools** | تحسين الأداء | `libgoogle-perftools-dev` |
| **Boost** | مكتبات C++ مساعدة | `libboost-all-dev` |
| **HDF5** | تخزين بيانات المحاكاة | `libhdf5-serial-dev` |
| **Capstone** | فك تشفير التعليمات | `libcapstone-dev` |
| **libelf** | قراءة ملفات ELF | `libelf-dev` |
| **libpng** | معالجة الصور | `libpng-dev` |
| **m4** | معالج ماكرو | `m4` |
| **CMake** | نظام بناء إضافي | `cmake` |
| **pkg-config** | إدارة المكتبات | `pkg-config` |

### أدوات اختيارية (للتوثيق والتطوير)

| الأداة | الغرض | الحزمة |
|:---|:---|:---|
| **pydot** | رسم المخططات | `python3-pydot` |
| **venv** | بيئات Python الافتراضية | `python3-venv` |
| **mypy** | فحص أنواع Python | `mypy` |
| **Doxygen** | توليد التوثيق | `doxygen` |
| **clang-format** | تنسيق الكود | `clang-format` |

---

# 3. 📦 خطوات التثبيت من الصفر

## الخطوة 1: تثبيت WSL2

افتح **PowerShell كمسؤول (Administrator)** واكتب:

```powershell
wsl --install
```

> ⚠️ **مهم**: أعد تشغيل الكمبيوتر بعد هذا الأمر!

بعد إعادة التشغيل، سيطلب منك إنشاء اسم مستخدم وكلمة مرور لـ Ubuntu.

## الخطوة 2: تحديث Ubuntu وتثبيت المكتبات

افتح **Ubuntu** (من قائمة Start) واكتب الأوامر التالية:

```bash
# تحديث النظام
sudo apt update
sudo apt upgrade -y

# تثبيت جميع المكتبات المطلوبة (أمر واحد)
sudo apt install -y \
    build-essential \
    scons \
    python3-dev \
    git \
    pre-commit \
    zlib1g \
    zlib1g-dev \
    libprotobuf-dev \
    protobuf-compiler \
    libprotoc-dev \
    libgoogle-perftools-dev \
    libboost-all-dev \
    libhdf5-serial-dev \
    python3-pydot \
    python3-venv \
    python3-tk \
    mypy \
    m4 \
    libcapstone-dev \
    libpng-dev \
    libelf-dev \
    pkg-config \
    wget \
    cmake \
    doxygen \
    clang-format
```

> ⏱️ هذا الأمر قد يأخذ **5-15 دقيقة** حسب سرعة الإنترنت.

## الخطوة 3: تنزيل وبناء gem5

```bash
# الانتقال إلى مجلد home
cd ~

# استنساخ gem5 من GitHub
git clone https://github.com/gem5/gem5
cd gem5

# بناء gem5 لمعمارية x86
# ⚠️ هذا يأخذ 30-90 دقيقة حسب قوة المعالج!
scons build/X86/gem5.opt -j4
```

> 💡 **ملاحظة**: `-j4` يعني استخدام 4 أنوية. إذا عندك 8 أنوية، استخدم `-j8` لتسريع البناء.

## الخطوة 4: التحقق من التثبيت

```bash
# تشغيل مثال Hello World للتأكد أن gem5 يعمل
build/X86/gem5.opt configs/learning_gem5/part1/simple.py
```

إذا شاهدت رسالة `Exiting @ tick ... because exiting with last active thread context` فهذا يعني أن gem5 يعمل بنجاح! ✅

## الخطوة 5: نسخ ملفات المشروع إلى WSL

```bash
# إنشاء مجلد المشروع في WSL
mkdir -p ~/gem5_cache_project

# نسخ الملفات من Windows إلى WSL
cp -r /mnt/d/projrct/Gem5/gem5_cache_project/* ~/gem5_cache_project/
```

> 💡 **ملاحظة**: في WSL، ملفات Windows موجودة تحت `/mnt/d/` (القرص D:) أو `/mnt/c/` (القرص C:)

---

# 4. 🚀 كيفية التشغيل خطوة بخطوة

## الطريقة 1: التشغيل التلقائي (الأسهل) 🟢

```bash
# الانتقال إلى مجلد المشروع
cd ~/gem5_cache_project

# إعطاء صلاحية التنفيذ للسكريبت
chmod +x run_all.sh

# تشغيل جميع المحاكاة تلقائياً
bash run_all.sh ~/gem5/build/X86/gem5.opt
```

هذا السكريبت سيقوم بـ:
1. ✅ ترجمة برنامج الاختبار (`array_access.cpp`)
2. ✅ تشغيل المحاكاة لـ 4 إعدادات (1-way, 2-way, 4-way, 8-way)
3. ✅ جمع النتائج وتحليلها
4. ✅ إنشاء ملف CSV بالمقارنة

## الطريقة 2: التشغيل اليدوي خطوة بخطوة 🔵

### الخطوة 1: ترجمة برنامج الاختبار

```bash
cd ~/gem5_cache_project

# ترجمة البرنامج كملف ثابت (static) لأن gem5 SE mode يحتاج ذلك
g++ -O1 -static -o program/array_access program/array_access.cpp
```

> ⚠️ **مهم جداً**: يجب استخدام `-static` لأن gem5 في وضع SE لا يدعم المكتبات الديناميكية!

### الخطوة 2: تشغيل كل محاكاة على حدة

```bash
# المتغير: مسار gem5
GEM5=~/gem5/build/X86/gem5.opt

# تجربة 1: Direct-Mapped (1-Way)
$GEM5 --outdir=results/1way configs/run_1way.py

# تجربة 2: 2-Way Set-Associative
$GEM5 --outdir=results/2way configs/run_2way.py

# تجربة 3: 4-Way Set-Associative
$GEM5 --outdir=results/4way configs/run_4way.py

# تجربة 4: 8-Way Set-Associative
$GEM5 --outdir=results/8way configs/run_8way.py
```

> ⏱️ كل محاكاة تأخذ تقريباً **1-5 دقائق** حسب قوة الجهاز.

### الخطوة 3: تحليل النتائج

```bash
# تحليل ومقارنة النتائج
python3 parse_results.py
```

### الخطوة 4: عرض النتائج يدوياً (اختياري)

```bash
# عرض ملف الإحصائيات مباشرة
cat results/1way/stats.txt | grep -E "(overallHits|overallMisses|overallMissRate|simTicks)"

# مقارنة miss rate بين الإعدادات
echo "=== 1-Way ==="
grep "dcache.overallMissRate::total" results/1way/stats.txt
echo "=== 2-Way ==="
grep "dcache.overallMissRate::total" results/2way/stats.txt
echo "=== 4-Way ==="
grep "dcache.overallMissRate::total" results/4way/stats.txt
echo "=== 8-Way ==="
grep "dcache.overallMissRate::total" results/8way/stats.txt
```

---

# 5. 📂 فهم الملفات والأكواد

## 5.1 هيكل المشروع

```
gem5_cache_project/
│
├── 📁 configs/                    ← ملفات إعداد gem5
│   ├── run_1way.py               ← إعداد 1-Way (Direct-Mapped)
│   ├── run_2way.py               ← إعداد 2-Way
│   ├── run_4way.py               ← إعداد 4-Way
│   └── run_8way.py               ← إعداد 8-Way
│
├── 📁 program/                    ← البرنامج المراد محاكاته
│   └── array_access.cpp          ← برنامج اختبار الذاكرة المخبئية
│
├── 📁 results/                    ← نتائج المحاكاة (تتولد تلقائياً)
│   ├── 1way/stats.txt
│   ├── 2way/stats.txt
│   ├── 4way/stats.txt
│   ├── 8way/stats.txt
│   └── comparison_results.csv
│
├── run_all.sh                     ← سكريبت التشغيل التلقائي
├── parse_results.py               ← سكريبت تحليل النتائج
├── report.md                      ← التقرير الأكاديمي
└── PROJECT_GUIDE.md               ← هذا الملف
```

## 5.2 شرح ملف الإعداد (Configuration)

كل ملف config يبني النظام التالي:

```
┌──────────────────────────────────────────────────────────┐
│                       النظام الكامل                       │
│                                                          │
│  ┌─────────────────────────────────────────────────────┐  │
│  │              TimingSimpleCPU (2 GHz)                │  │
│  │         ┌────────────┐  ┌────────────┐             │  │
│  │         │ icache_port│  │ dcache_port│             │  │
│  └─────────┼────────────┼──┼────────────┼─────────────┘  │
│            │            │  │            │                 │
│       ┌────▼────┐  ┌────▼──▼────┐                        │
│       │ L1 I$   │  │  L1 D$     │  ← 32KB, assoc متغير  │
│       │ (32KB)  │  │  (32KB)    │                        │
│       └────┬────┘  └────┬───────┘                        │
│            │            │                                │
│       ┌────▼────────────▼────┐                           │
│       │      L2 XBar         │  ← ناقل ربط              │
│       └──────────┬───────────┘                           │
│                  │                                       │
│           ┌──────▼──────┐                                │
│           │  L2 Cache   │  ← 256KB, 8-way (ثابت)        │
│           │  (256KB)    │                                │
│           └──────┬──────┘                                │
│                  │                                       │
│       ┌──────────▼──────────┐                            │
│       │    System XBar       │  ← ناقل الذاكرة الرئيسي  │
│       └──────────┬───────────┘                           │
│                  │                                       │
│           ┌──────▼──────┐                                │
│           │  MemCtrl    │                                │
│           │ DDR3-1600   │  ← 512MB ذاكرة رئيسية         │
│           └─────────────┘                                │
└──────────────────────────────────────────────────────────┘
```

### الكود مع الشرح سطراً بسطر:

```python
import m5                        # مكتبة gem5 الرئيسية
from m5.objects import *         # جميع كائنات المحاكاة
import os                        # للتعامل مع المسارات

# ====== إنشاء النظام ======
system = System()                # إنشاء كائن النظام

# ساعة النظام
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "2GHz"                    # تردد 2 جيجاهرتز
system.clk_domain.voltage_domain = VoltageDomain()   # ⚡ الجهد الكهربائي (مطلوب!)

# إعدادات الذاكرة
system.mem_mode = "timing"                   # وضع المحاكاة الدقيق
system.mem_ranges = [AddrRange("512MB")]     # حجم الذاكرة الرئيسية

# ====== المعالج ======
system.cpu = TimingSimpleCPU()    # معالج بسيط مع محاكاة زمنية دقيقة

# ====== الذاكرة المخبئية المستوى 1 ======
system.cpu.icache = Cache(        # ذاكرة التعليمات
    size="32kB",                  # الحجم: 32 كيلوبايت
    assoc=2,                      # ← هذا هو المتغير! (1, 2, 4, أو 8)
    tag_latency=1,                # تأخير البحث في العلامات
    data_latency=1,               # تأخير قراءة البيانات
    response_latency=1,           # تأخير الاستجابة
    mshrs=4,                      # عدد MSHRs (طلبات معلقة)
    tgts_per_mshr=20,             # أهداف لكل MSHR
)

system.cpu.dcache = Cache(        # ذاكرة البيانات (نفس الإعدادات)
    size="32kB", assoc=2,
    tag_latency=1, data_latency=1, response_latency=1,
    mshrs=4, tgts_per_mshr=20,
)

# ====== الربط الصحيح (مهم جداً!) ======
# CPU → L1 Cache
system.cpu.icache_port = system.cpu.icache.cpu_side   # ربط CPU بذاكرة التعليمات
system.cpu.dcache_port = system.cpu.dcache.cpu_side   # ربط CPU بذاكرة البيانات

# L1 Cache → L2 Bus
system.cpu.icache.mem_side = system.l2bus.cpu_side_ports
system.cpu.dcache.mem_side = system.l2bus.cpu_side_ports

# L2 Bus → L2 Cache → Memory Bus → Memory Controller
system.l2cache.cpu_side = system.l2bus.mem_side_ports
system.l2cache.mem_side = system.membus.cpu_side_ports

# ====== متحكم الذاكرة ======
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()               # نوع الذاكرة
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

# ====== البرنامج المراد تشغيله ======
process = Process()
process.cmd = ["path/to/array_access"]   # مسار البرنامج المترجم
system.cpu.workload = process
system.cpu.createThreads()

# ====== بدء المحاكاة ======
root = Root(full_system=False, system=system)   # SE Mode (ليس Full System)
m5.instantiate()
exit_event = m5.simulate()                       # ابدأ!
```

## 5.3 شرح برنامج الاختبار (array_access.cpp)

```cpp
#include <iostream>
using namespace std;

int main()
{
    const int SIZE = 100000;    // مصفوفة بـ 100 ألف عنصر
    int *arr = new int[SIZE];   // تخصيص ديناميكي في الـ Heap

    // تعبئة المصفوفة
    for (int i = 0; i < SIZE; i++)
        arr[i] = i;

    long long sum = 0;

    // ═══════ المرحلة 1: وصول تتابعي ═══════
    // يقرأ العناصر بالترتيب: 0, 1, 2, 3, ...
    // ✅ هذا النمط يستفيد من Spatial Locality (المحلية المكانية)
    // جميع مستويات الـ Associativity تعمل بشكل متشابه هنا
    for (int r = 0; r < 100; r++)
        for (int i = 0; i < SIZE; i++)
            sum += arr[i];

    // ═══════ المرحلة 2: وصول بخطوات ═══════
    // يقرأ كل عنصر رقم 16: 0, 16, 32, 48, ...
    // ⚠️ يضغط على مجموعات معينة في الـ Cache
    for (int r = 0; r < 100; r++)
        for (int i = 0; i < SIZE; i += 16)
            sum += arr[i];

    // ═══════ المرحلة 3: وصول يسبب تعارضات ═══════
    // يقرأ عناصر تقع في نفس مجموعة الـ Cache (same set)
    // 🔴 Direct-Mapped (1-way) يعاني كثيراً هنا!
    // 🟢 8-way يتعامل مع هذا بسهولة
    for (int r = 0; r < 200; r++)
        for (int i = 0; i < SIZE; i += 8192)
            sum += arr[i];

    cout << "Sum = " << sum << endl;
    delete[] arr;
    return 0;
}
```

**لماذا 3 مراحل؟**

| المرحلة | نمط الوصول | لماذا؟ |
|:---|:---|:---|
| **1. تتابعي** | `arr[0], arr[1], arr[2]...` | لقياس الأداء الأساسي مع Locality جيد |
| **2. بخطوات** | `arr[0], arr[16], arr[32]...` | لرؤية تأثير ضغط المجموعات |
| **3. تعارضي** | `arr[0], arr[8192], arr[16384]...` | لإظهار الفرق الكبير بين 1-way و 8-way |

---

# 6. 📊 فهم النتائج وملف stats.txt

## 6.1 أين توجد النتائج؟

بعد التشغيل، كل محاكاة تنتج مجلد في `results/`:

```
results/
├── 1way/
│   ├── stats.txt        ← ملف الإحصائيات الرئيسي ⭐
│   ├── config.ini       ← إعدادات المحاكاة
│   └── config.json      ← إعدادات بصيغة JSON
├── 2way/
│   ├── stats.txt
│   └── ...
├── 4way/
│   └── ...
├── 8way/
│   └── ...
└── comparison_results.csv  ← ملف المقارنة (ينتجه parse_results.py)
```

## 6.2 كيف تقرأ stats.txt؟

ملف `stats.txt` يحتوي على **مئات الإحصائيات**. الأهم منها:

### إحصائيات L1 Data Cache (الأهم):

| الإحصائية في stats.txt | المعنى | مثال |
|:---|:---|:---|
| `system.cpu.dcache.overallHits::total` | عدد مرات إيجاد البيانات في الـ Cache | `25100000` |
| `system.cpu.dcache.overallMisses::total` | عدد مرات عدم إيجاد البيانات | `300000` |
| `system.cpu.dcache.overallMissRate::total` | نسبة الإخفاق (0 إلى 1) | `0.011811` |
| `system.cpu.dcache.overallAccesses::total` | إجمالي عمليات الوصول | `25400000` |

### إحصائيات L1 Instruction Cache:

| الإحصائية | المعنى |
|:---|:---|
| `system.cpu.icache.overallHits::total` | إصابات ذاكرة التعليمات |
| `system.cpu.icache.overallMisses::total` | إخفاقات ذاكرة التعليمات |
| `system.cpu.icache.overallMissRate::total` | نسبة الإخفاق |

### إحصائيات L2 Cache:

| الإحصائية | المعنى |
|:---|:---|
| `system.l2cache.overallHits::total` | إصابات المستوى الثاني |
| `system.l2cache.overallMisses::total` | إخفاقات المستوى الثاني |
| `system.l2cache.overallMissRate::total` | نسبة إخفاق المستوى الثاني |

### إحصائيات عامة:

| الإحصائية | المعنى |
|:---|:---|
| `simTicks` | إجمالي دورات المحاكاة (أقل = أسرع) |
| `simSeconds` | الوقت المحاكى بالثواني |
| `simInsts` | عدد التعليمات المنفذة |

## 6.3 النتائج المتوقعة

```
╔══════════════════════╦══════════╦══════════╦══════════╦══════════╗
║       المقياس        ║  1-Way   ║  2-Way   ║  4-Way   ║  8-Way   ║
╠══════════════════════╬══════════╬══════════╬══════════╬══════════╣
║ D-Cache Miss Rate    ║ الأعلى   ║    ↓     ║    ↓     ║ الأقل   ║
║ (نسبة الإخفاق)      ║ ~0.024   ║ ~0.012   ║ ~0.008   ║ ~0.006   ║
╠══════════════════════╬══════════╬══════════╬══════════╬══════════╣
║ Sim Ticks            ║ الأعلى   ║    ↓     ║    ↓     ║ الأقل   ║
║ (زمن المحاكاة)      ║          ║          ║          ║          ║
╠══════════════════════╬══════════╬══════════╬══════════╬══════════╣
║ AMAT                 ║ الأعلى   ║    ↓     ║    ↓     ║ الأقل   ║
║ (متوسط وقت الوصول)  ║ ~1.26    ║ ~1.13    ║ ~1.09    ║ ~1.07    ║
╚══════════════════════╩══════════╩══════════╩══════════╩══════════╝
```

**الاتجاه المتوقع:**

```
Miss Rate
  ▲
  │  ████
  │  ████
  │  ████  ████
  │  ████  ████
  │  ████  ████  ████
  │  ████  ████  ████  ████
  │  ████  ████  ████  ████
  └──────────────────────── ▶ Associativity
     1-Way  2-Way  4-Way  8-Way

  أكثر إخفاق ◄─────────────────► أقل إخفاق
```

---

# 7. 📝 التقرير الأكاديمي الكامل

## 7.1 المقدمة (Introduction)

تعتبر الذاكرة المخبئية (Cache Memory) من أهم المكونات في عمارة الحاسوب الحديثة، حيث تعمل كجسر بين المعالج السريع والذاكرة الرئيسية البطيئة. أحد أهم معاملات تصميم الـ Cache هو **الترابط التجميعي (Associativity)** الذي يحدد عدد المواقع المتاحة في الـ Cache لتخزين كتلة ذاكرة معينة.

يهدف هذا المشروع إلى دراسة وتقييم تأثير الترابط التجميعي على أداء الـ Cache باستخدام محاكي **gem5**، وذلك بمقارنة أربعة إعدادات مختلفة: Direct-Mapped (1-Way)، 2-Way، 4-Way، و 8-Way Set-Associative.

## 7.2 الخلفية النظرية (Theoretical Background)

### هرمية الذاكرة (Memory Hierarchy)

تتبع أنظمة الحاسوب الحديثة هرمية ذاكرة متعددة المستويات:

| المستوى | الحجم | الزمن | الوصف |
|:---|:---|:---|:---|
| **السجلات (Registers)** | ~1 KB | <1 ns | داخل المعالج |
| **L1 Cache** | 32-64 KB | 1-2 ns | الأسرع بعد السجلات |
| **L2 Cache** | 256 KB - 1 MB | 5-10 ns | المستوى الثاني |
| **L3 Cache** | 4-32 MB | 20-40 ns | مشترك بين الأنوية |
| **RAM** | 4-64 GB | 50-100 ns | الذاكرة الرئيسية |
| **القرص (SSD/HDD)** | TB | μs - ms | التخزين الدائم |

### الترابط التجميعي (Associativity)

**Direct-Mapped (1-Way):**
- كل كتلة ذاكرة لها موقع واحد فقط في الـ Cache
- العنوان يحدد الموقع: `Set = (Address / BlockSize) mod NumberOfSets`
- ✅ سريع وبسيط | ❌ تعارضات عالية

**N-Way Set-Associative:**
- كل كتلة يمكن أن تخزن في N مواقع ضمن المجموعة
- يتطلب N مقارنات متوازية
- ✅ أقل تعارضات | ❌ أبطأ وأعقد

### أنواع الإخفاق (3Cs Model)

1. **Compulsory (إجباري)**: أول وصول لكتلة جديدة - لا يتأثر بالـ associativity
2. **Capacity (السعة)**: الـ Cache ممتلئ - لا يتأثر بالـ associativity
3. **Conflict (التعارض)**: كتل متعددة تتنافس على نفس المجموعة - **يقل بزيادة الـ associativity** ⭐

### معادلة AMAT

```
AMAT = L1_Hit_Time + L1_Miss_Rate × (L2_Hit_Time + L2_Miss_Rate × Mem_Latency)
```

## 7.3 أدوات التجربة

### محاكي gem5
- محاكي معماري مفتوح المصدر مستخدم في الأبحاث والصناعة
- أُسس في جامعة Michigan (مشروع m5) وجامعة Wisconsin (مشروع GEMS)
- تم دمجهما عام 2011
- أُستشهد به في أكثر من 2900 بحث علمي
- يستخدمه ARM Research, AMD, Google, Samsung, HP وغيرهم

### الإعدادات الثابتة

| المعامل | القيمة |
|:---|:---|
| نوع المعالج | TimingSimpleCPU |
| التردد | 2 GHz |
| وضع الذاكرة | Timing (دقيق) |
| حجم L1 I-Cache | 32 KB |
| حجم L1 D-Cache | 32 KB |
| حجم L2 Cache | 256 KB |
| associativity L2 | 8-way (ثابت) |
| حجم سطر الـ Cache | 64 bytes |
| الذاكرة الرئيسية | DDR3-1600, 512 MB |

### المتغير التجريبي

| التجربة | L1 Associativity |
|:---:|:---:|
| 1 | 1-way (Direct-Mapped) |
| 2 | 2-way |
| 3 | 4-way |
| 4 | 8-way |

## 7.4 النتائج والتحليل (Results & Analysis)

### جدول النتائج المتوقعة

| المقياس | 1-Way | 2-Way | 4-Way | 8-Way |
|:---|---:|---:|---:|---:|
| D-Cache Miss Rate | ~0.0236 | ~0.0118 | ~0.0079 | ~0.0059 |
| D-Cache Misses | ~600K | ~300K | ~200K | ~150K |
| L2 Misses | ~50K | ~40K | ~30K | ~25K |
| AMAT (cycles) | ~1.256 | ~1.134 | ~1.091 | ~1.069 |
| Sim Ticks | الأعلى | ↓ | ↓ | الأقل |

> 📌 **ملاحظة**: هذه قيم تقريبية مبنية على نظرية الـ Cache. النتائج الفعلية ستكون متاحة بعد تشغيل المحاكاة على gem5.

### التحليل

1. **أكبر تحسن من 1-way إلى 2-way**: الانتقال من Direct-Mapped إلى 2-way يقلل الإخفاق تقريباً للنصف لأنه يقضي على معظم conflict misses البسيطة.

2. **تناقص العوائد (Diminishing Returns)**: التحسن من 4-way إلى 8-way أصغر بكثير من 1-way إلى 2-way. هذا لأن معظم conflict misses تم حلها بالفعل.

3. **المرحلة 3 (conflict-inducing) هي الأكثر تأثراً**: الأنماط التي تسبب تعارضات تُظهر أكبر فرق بين مستويات الـ associativity.

## 7.5 المناقشة (Discussion)

### المفاضلة بين الأداء والتكلفة

| زيادة Associativity | المميزات | العيوب |
|:---|:---|:---|
| | ✅ أقل miss rate | ❌ مقارنات أكثر |
| | ✅ أداء أفضل | ❌ استهلاك طاقة أعلى |
| | ✅ أقل تعارضات | ❌ تعقيد أكبر في العتاد |

### التطبيق العملي

المعالجات الحديثة اختارت **8-way** كنقطة التوازن المثلى:
- Intel Core i7: L1 8-way
- AMD Ryzen: L1 8-way
- Apple M1: L1 8-way
- ARM Cortex-A78: L1 4-way

## 7.6 الخلاصة (Conclusion)

1. زيادة الترابط التجميعي **تقلل نسبة الإخفاق** بشكل ملحوظ
2. **أكبر تحسن** يأتي عند الانتقال من 1-way إلى 2-way
3. بعد 4-way، العوائد **تتناقص** بشكل كبير
4. الـ associativity يؤثر بشكل رئيسي على **conflict misses**
5. الاختيار الأمثل يعتمد على **التوازن بين الأداء وتكلفة العتاد**

## 7.7 المراجع (References)

1. Gem5 Simulator Tutorial3 – Course Material
2. Binkert, N., et al. "The gem5 simulator." ACM SIGARCH, 2011
3. Hennessy & Patterson, "Computer Architecture: A Quantitative Approach," 6th Ed.
4. gem5 Documentation: https://www.gem5.org/documentation/
5. gem5 GitHub: https://github.com/gem5/gem5

---

# 8. ❓ الأسئلة الشائعة وحل المشاكل

## مشكلة: `gem5.opt: No such file or directory`

**السبب**: gem5 غير مبني أو المسار خاطئ.

**الحل**:
```bash
# تأكد أنك بنيت gem5
cd ~/gem5
scons build/X86/gem5.opt -j4

# تأكد من المسار
ls -la ~/gem5/build/X86/gem5.opt
```

## مشكلة: `g++: command not found`

**الحل**:
```bash
sudo apt install build-essential
```

## مشكلة: `error while loading shared libraries`

**السبب**: البرنامج لم يُترجم كـ static.

**الحل**:
```bash
g++ -O1 -static -o program/array_access program/array_access.cpp
```

## مشكلة: `ImportError: No module named m5`

**السبب**: تحاول تشغيل سكريبت gem5 بـ Python العادي.

**الحل**: يجب تشغيله عبر gem5:
```bash
# ❌ خطأ
python3 configs/run_1way.py

# ✅ صحيح
~/gem5/build/X86/gem5.opt configs/run_1way.py
```

## مشكلة: `VoltageDomain not found` أو `MemCtrl not found`

**السبب**: إصدار gem5 قديم.

**الحل**:
```bash
cd ~/gem5
git pull
scons build/X86/gem5.opt -j4
```

## مشكلة: المحاكاة بطيئة جداً

**الحل**: يمكنك تقليل حجم المصفوفة في `array_access.cpp`:
```cpp
const int SIZE = 50000;    // بدلاً من 100000
const int REPEAT = 50;     // بدلاً من 100
```

## مشكلة: `stats.txt` فارغ أو غير موجود

**السبب**: المحاكاة لم تكتمل بنجاح.

**الحل**: تحقق من ملف الـ log:
```bash
cat results/1way/simulation.log
```

---

> 📝 **ملاحظة أخيرة**: بعد تشغيل المحاكاة والحصول على النتائج الفعلية، حدّث قسم النتائج في التقرير بالأرقام الحقيقية من `stats.txt`.
