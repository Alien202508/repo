import flet as ft

# بيانات المراحل
levels = [
    {
        "question": "ما هو القانون الذي يصف كمية الحرارة Q اللازمة لتسخين مادة؟",
        "choices": ["Q = mcΔT", "PV = nRT", "F = ma", "E = hf"],
        "answer": "Q = mcΔT",
        "xp": 100
    },
    {
        "question": "أي من التالي يمثل القانون الأول للديناميكا الحرارية؟",
        "choices": ["ΔU = Q - W", "ΔS ≥ 0", "F = qE", "V = IR"],
        "answer": "ΔU = Q - W",
        "xp": 150
    },
    {
        "question": "ما هو مفهوم الإنتروبيا؟",
        "choices": ["مقياس للفوضى", "درجة الحرارة", "كمية المادة", "سرعة الجسيمات"],
        "answer": "مقياس للفوضى",
        "xp": 200
    },
]

# واجهة التطبيق
def main(page: ft.Page):
    page.title = "لعبة الديناميكا الحرارية"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    score = ft.Text("نقاطك: 0", size=20)
    question = ft.Text("", size=24)
    buttons = []
    current_level = {"index": 0}
    xp = {"value": 0}

    def load_level():
        if current_level["index"] >= len(levels):
            question.value = f"🎉 انتهيت! مجموع نقاطك: {xp['value']} XP"
            page.controls.clear()
            page.controls.append(question)
            page.controls.append(score)
            page.update()
            return

        level = levels[current_level["index"]]
        question.value = f"🔹 المرحلة {current_level['index'] + 1}: {level['question']}"
        page.controls.clear()
        page.controls.append(question)
        page.controls.append(score)

        for choice in level["choices"]:
            btn = ft.ElevatedButton(text=choice)

            def on_click(e, choice=choice):
                if choice == level["answer"]:
                    xp["value"] += level["xp"]
                    score.value = f"نقاطك: {xp['value']}"
                current_level["index"] += 1
                load_level()

            btn.on_click = on_click
            page.controls.append(btn)

        page.update()

    load_level()

ft.app(target=main)
