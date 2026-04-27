import json
import re

html_file = 'dermatology.html'
js_file = 'i18n.js'

with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

translations = {
    'spectra_desc': {
        'en': 'Also known as the "Hollywood Peel", this superior laser treatment combines a specialized carbon lotion to gently remove tired superficial skin layers, instantly revealing smoother, younger, and deeply radiant skin.',
        'ar': 'يُعرف أيضًا باسم "التقشير الهوليودي"، يجمع هذا العلاج المتفوق بالليزر مع لوشن كربوني متخصص لإزالة طبقات الجلد السطحية المتعبة بلطف، مما يكشف على الفور عن بشرة أكثر نعومة وشبابًا وإشراقًا.'
    },
    'spectra_kb1': {
        'en': 'Quick 20-minute sessions with absolutely zero downtime',
        'ar': 'جلسات سريعة لمدة 20 دقيقة بدون فترة نقاهة على الإطلاق'
    },
    'spectra_kb2': {
        'en': 'Gentle dead skin removal for instant radiance and glow',
        'ar': 'إزالة لطيفة للجلد الميت لإشراقة ونضارة فورية'
    },
    'spectra_tr1': {
        'en': 'Unifies uneven skin tones and manages acne',
        'ar': 'يوحد لون البشرة غير المتكافئ ويعالج حب الشباب'
    },
    'spectra_tr2': {
        'en': 'Reduces large pores and pigmentation',
        'ar': 'يقلل من المسام الواسعة والتصبغات'
    },
    'spectra_tr3': {
        'en': 'Hair bleaching and fine hair removal',
        'ar': 'تشقير الشعر وإزالة الشعر الوبري'
    },
    'spectra_tr4': {
        'en': 'Collagen stimulation for mild skin tightening',
        'ar': 'تحفيز الكولاجين لشد الجلد الخفيف'
    },

    'gentle_desc': {
        'en': 'An advanced laser technology specifically designed for permanent hair reduction. It features a proprietary Dynamic Cooling Device (DCD™) to protect skin and ensure maximum comfort.',
        'ar': 'تقنية ليزر متقدمة مصممة خصيصًا لتقليل الشعر بشكل دائم. تتميز بجهاز تبريد ديناميكي (DCD™) حصري لحماية البشرة وضمان أقصى درجات الراحة.'
    },
    'gentle_kb1': {
        'en': '<strong>Versatile:</strong> Highly effective for all skin types (I-VI).',
        'ar': '<strong>متعدد الاستخدامات:</strong> فعال للغاية لجميع أنواع البشرة (I-VI).'
    },
    'gentle_kb2': {
        'en': '<strong>Enhanced Comfort:</strong> DCD cooling significantly reduces pain.',
        'ar': '<strong>راحة محسنة:</strong> يقلل تبريد DCD بشكل كبير من الألم.'
    },
    'gentle_kb3': {
        'en': '<strong>High Speed:</strong> 15 mins for small areas; under 90 mins for full body.',
        'ar': '<strong>سرعة عالية:</strong> 15 دقيقة للمناطق الصغيرة؛ أقل من 90 دقيقة لكامل الجسم.'
    },
    'gentle_kb4': {
        'en': '<strong>Safe:</strong> Minimal downtime and side effects.',
        'ar': '<strong>آمن:</strong> الحد الأدنى من فترة النقاهة والآثار الجانبية.'
    },
    'gentle_tr1': {
        'en': 'Permanent reduction of unwanted thick and fine hair',
        'ar': 'التقليل الدائم للشعر الكثيف والوبري غير المرغوب فيه'
    },
    'gentle_tr2': {
        'en': 'Professional hair removal for all body areas',
        'ar': 'إزالة شعر احترافية لجميع مناطق الجسم'
    },
    'gentle_tr3': {
        'en': 'Effective treatment regardless of skin pigmentation',
        'ar': 'علاج فعال بغض النظر عن لون البشرة'
    },

    'eco2_desc': {
        'en': "A highly dynamic fractional CO2 laser designed for intensive skin resurfacing. It offers remarkable results, often after a single treatment, with minimal downtime to restore your skin's youthful texture.",
        'ar': "ليزر فراكشنال CO2 ديناميكي للغاية مصمم لتجديد سطح الجلد بشكل مكثف. يقدم نتائج ملحوظة، غالبًا بعد جلسة واحدة، مع الحد الأدنى من فترة النقاهة لاستعادة الملمس الشبابي لبشرتك."
    },
    'eco2_kb1': {
        'en': '<strong>Fast Sessions:</strong> A full face treatment typically takes 15–20 minutes.',
        'ar': '<strong>جلسات سريعة:</strong> يستغرق علاج الوجه بالكامل عادةً من 15 إلى 20 دقيقة.'
    },
    'eco2_kb2': {
        'en': '<strong>Comfortable:</strong> Slight warm sensation with minimal discomfort (uses topical anesthetic).',
        'ar': '<strong>مريح:</strong> إحساس طفيف بالدفء مع حد أدنى من الانزعاج (يستخدم مخدرًا موضعيًا).'
    },
    'eco2_kb3': {
        'en': '<strong>Efficient:</strong> Rapid recovery with exceptionally minimal downtime.',
        'ar': '<strong>فعال:</strong> تعافي سريع مع فترة نقاهة قليلة جدًا.'
    },
    'eco2_kb4': {
        'en': '<strong>Highly Effective:</strong> Delivers significant improvements often after just one session.',
        'ar': '<strong>فعال للغاية:</strong> يقدم تحسينات كبيرة غالبًا بعد جلسة واحدة فقط.'
    },
    'eco2_tr1': {
        'en': '<strong>Skin Resurfacing:</strong> Treatment of complex skin abnormalities.',
        'ar': '<strong>تجديد سطح الجلد:</strong> علاج تشوهات الجلد المعقدة.'
    },
    'eco2_tr2': {
        'en': '<strong>Scars:</strong> Drastically fades acne, burn, and surgical scars.',
        'ar': '<strong>الندبات:</strong> يخفف بشكل كبير من ندبات حب الشباب والحروق والجراحة.'
    },
    'eco2_tr3': {
        'en': '<strong>Anti-Aging:</strong> Tightens skin laxity, fading deep wrinkles (face/neck/jaw).',
        'ar': '<strong>مكافحة الشيخوخة:</strong> يشد ترهل الجلد، ويخفف التجاعيد العميقة (الوجه / الرقبة / الفك).'
    },
    'eco2_tr4': {
        'en': '<strong>Pore Refinement &amp; Stretch Marks:</strong> Minimizes large pores and stretch marks.',
        'ar': '<strong>تصغير المسام وعلامات التمدد:</strong> يقلل من المسام الواسعة وعلامات التمدد.'
    },

    'hydra_desc': {
        'en': 'An advanced, multi-functional medical-grade system offering comprehensive skin rejuvenation. It thoroughly cleanses, extracts impurities, and deeply hydrates using vital serums to deliver a flawless, deeply nourished complexion instantly.',
        'ar': 'نظام طبي متقدم ومتعدد الوظائف يقدم تجديدًا شاملاً للبشرة. ينظف بعمق، ويستخرج الشوائب، ويرطب بشكل مكثف باستخدام أمصال حيوية للحصول على بشرة خالية من العيوب ومغذية بعمق على الفور.'
    },
    'hydra_kb1': {
        'en': '<strong>Deep Cleansing &amp; Exfoliation:</strong> Gently removes dead skin, blackheads, and detoxifies.',
        'ar': '<strong>تنظيف عميق وتقشير:</strong> يزيل الجلد الميت والرؤوس السوداء بلطف ويزيل السموم.'
    },
    'hydra_kb2': {
        'en': '<strong>Intense Hydration:</strong> Nourishes dry skin while controlling excess oil and sebum.',
        'ar': '<strong>ترطيب مكثف:</strong> يغذي البشرة الجافة بينما يتحكم في الزيوت والدهون الزائدة.'
    },
    'hydra_kb3': {
        'en': '<strong>Anti-Aging:</strong> Reduces fine lines, early signs of aging, and boosts overall elasticity.',
        'ar': '<strong>مكافحة الشيخوخة:</strong> يقلل الخطوط الدقيقة والعلامات المبكرة للشيخوخة ويعزز المرونة العامة.'
    },
    'hydra_kb4': {
        'en': '<strong>Universal Safety:</strong> Completely safe for all skin types with absolutely zero downtime.',
        'ar': '<strong>أمان شامل:</strong> آمن تمامًا لجميع أنواع البشرة بدون فترة نقاهة على الإطلاق.'
    },
    'hydra_tr1': {
        'en': 'Routine acne reduction and breakout prevention',
        'ar': 'الحد من حب الشباب الروتيني والوقاية من البثور'
    },
    'hydra_tr2': {
        'en': 'Advanced hydration therapy for dull and distressed skin',
        'ar': 'علاج ترطيب متقدم للبشرة الباهتة والمتعبة'
    },
    'hydra_tr3': {
        'en': 'Complexion brightening and significant pore minimization',
        'ar': 'تفتيح البشرة وتقليل المسام بشكل ملحوظ'
    },
    'hydra_tr4': {
        'en': 'Preventative and restorative anti-aging facial procedures',
        'ar': 'إجراءات تجميل الوجه الوقائية والمرممة لمكافحة الشيخوخة'
    },

    'scalp_desc': {
        'en': 'Specialized clinical equipment structurally designed to deeply purify and revitalize your scalp. By gently exfoliating buildup and unclogging hair follicles, it creates the optimal environment for robust hair growth and vitality.',
        'ar': 'معدات سريرية متخصصة مصممة هيكليًا لتنقية وتنشيط فروة رأسك بعمق. من خلال التقشير اللطيف للتراكمات وفتح بصيلات الشعر، فإنه يخلق بيئة مثالية لنمو شعر قوي وحيوي.'
    },
    'scalp_kb1': {
        'en': '<strong>Deep Cleanse &amp; Oil Control:</strong> Removes dirt and strictly controls greasy scalp sebum.',
        'ar': '<strong>تنظيف عميق والتحكم في الزيوت:</strong> يزيل الأوساخ ويتحكم بدقة في دهون فروة الرأس الدهنية.'
    },
    'scalp_kb2': {
        'en': '<strong>Dandruff Relief:</strong> Gently exfoliates to powerfully eliminate dandruff and soothe irritation.',
        'ar': '<strong>راحة من القشرة:</strong> يقشر بلطف للقضاء بقوة على القشرة وتهدئة التهيج.'
    },
    'scalp_kb3': {
        'en': '<strong>Follicle Unclogging:</strong> Drastically clears blocked follicles to promote thicker hair growth.',
        'ar': '<strong>فتح البصيلات:</strong> يزيل البصيلات المسدودة بشكل كبير لتعزيز نمو شعر أكثر كثافة.'
    },
    'scalp_kb4': {
        'en': '<strong>Nourishing:</strong> Massages and hydrates scalp to improve vital blood circulation.',
        'ar': '<strong>تغذية:</strong> يدلك ويرطب فروة الرأس لتحسين الدورة الدموية الحيوية.'
    },
    'scalp_tr1': {
        'en': 'Premium preparation to enhance absorption for PRP and mesotherapy',
        'ar': 'إعداد ممتاز لتعزيز امتصاص PRP والميزوثيرابي'
    },
    'scalp_tr2': {
        'en': 'Routine management and reversal of excessively oily or flaky scalps',
        'ar': 'الإدارة الروتينية وعكس فروة الرأس الدهنية أو المتقشرة بشكل مفرط'
    },
    'scalp_tr3': {
        'en': 'Targeted therapy preventing hair fall directly caused by clogged pores',
        'ar': 'علاج موجه لمنع تساقط الشعر الناتج مباشرة عن المسام المسدودة'
    },
    'scalp_tr4': {
        'en': 'Comprehensive and safe maintenance for all scalp types with zero downtime',
        'ar': 'صيانة شاملة وآمنة لجميع أنواع فروة الرأس بدون فترة نقاهة'
    }
}

for key, texts in translations.items():
    en_text = texts['en']
    if en_text in html:
        html = html.replace(en_text, f'<span data-i18n="{key}">{en_text}</span>')
    else:
        print(f"Warning: {key} not found in HTML")

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html)

# Update i18n.js
with open(js_file, 'r', encoding='utf-8') as f:
    js_content = f.read()

# Insert into 'en'
en_additions = []
ar_additions = []
for k, v in translations.items():
    en_additions.append(f'        "{k}": "{v["en"].replace(\'"\', \'\\\\"\')}",')
    ar_additions.append(f'        "{k}": "{v["ar"].replace(\'"\', \'\\\\"\')}",')

en_str = "    \"en\": {"
en_start = js_content.find(en_str)
en_end = js_content.find("    },", en_start)
if en_end != -1:
    js_content = js_content[:en_end] + "\n" + "\n".join(en_additions) + "\n" + js_content[en_end:]

ar_str = "    \"ar\": {"
ar_start = js_content.find(ar_str)
ar_end = js_content.find("    }", ar_start)
if ar_end != -1:
    js_content = js_content[:ar_end] + "\n" + "\n".join(ar_additions) + "\n" + js_content[ar_end:]

with open(js_file, 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Done updating files.")
