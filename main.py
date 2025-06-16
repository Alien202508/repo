import flet as ft

def main(page: ft.Page):
    page.title = "آلة حاسبة"
    page.theme_mode = "light"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    input_field = ft.TextField(label="العملية الحسابية", autofocus=True)
    result_text = ft.Text(value="", size=20)

    def calculate(e):
        try:
            expression = input_field.value
            result = eval(expression)  # ⚠️ انتبه: eval يمكن أن تكون خطيرة إذا لم تُستخدم بحذر
            result_text.value = f"النتيجة: {result}"
        except Exception as err:
            result_text.value = f"خطأ: {err}"
        page.update()

    calc_button = ft.ElevatedButton(text="احسب", on_click=calculate)

    page.add(
        ft.Column(
            [
                input_field,
                calc_button,
                result_text
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

ft.app(target=main)
