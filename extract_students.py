import sys, json
sys.stdout.reconfigure(encoding='utf-8')

with open('phase4_outputs/interactive_students_xai.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for s in data:
    feats = s.get('features_en', {})
    gpa = feats.get('Academic Performance (GPA / IRA)', '?')
    att = feats.get('Attendance Rate (%)', '?')
    fails = feats.get('Course Failures', '?')
    inc = feats.get('Family Gross Income', '?')
    age = feats.get('Age', '?')
    print(f"Student #{s['id']} | Risk: {s['prob']}% | Pred: {s['pred']} | Actual: {s['actual']}")
    print(f"  GPA={gpa}, Attendance={att}%, Failures={fails}, Income={inc}, Age={age}")
    for d in s.get('drivers', [])[:5]:
        print(f"  SHAP >> {d['feature']}: value={d['value']}, shap={d['shap']:.4f}, direction={d['direction']}")
    print()

