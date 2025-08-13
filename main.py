import flet as ft
import threading
import bot

def main(page: ft.Page):
    page.title = "Email Command Bot"
    log_area = ft.Column(scroll="auto", expand=True)
    page.add(ft.Text("البوت يعمل تلقائيًا في الخلفية..."), log_area)

    def log_fn(text):
        log_area.controls.append(ft.Text(text))
        page.update()

    threading.Thread(target=bot.bot_loop, args=(log_fn,), daemon=True).start()

ft.app(target=main)
