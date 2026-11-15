
from nicegui import ui
from services.contact_service import submit_contact_message


def render_contact():

    ui.label("CONTACT INFINITY").classes(
        "text-4xl font-bold text-white"
    )

    ui.label(
        "Have a question, collaboration idea, or want to connect with us?"
    ).classes("text-gray-400 text-base")

    with ui.card().classes(
        "w-full max-w-2xl mx-auto bg-[#151515] p-6"
    ):
        ui.label("Send us a message").classes(
            "text-2xl font-bold text-white"
        )

        name = ui.input(
            "Full Name",
            placeholder="Enter your full name"
        ).classes("w-full")

        email = ui.input(
            "Email Address",
            placeholder="Enter your email"
        ).classes("w-full")

        subject = ui.input(
            "Subject",
            placeholder="What is this regarding?"
        ).classes("w-full")

        message = ui.textarea(
            "Your Message",
            placeholder="Write your message here..."
        ).classes("w-full")

        def submit_form():
            result = submit_contact_message(
                name.value,
                email.value,
                subject.value,
                message.value
            )

            if result["success"]:
                ui.notify(
                    result["message"],
                    type="positive"
                )

                name.value = ""
                email.value = ""
                subject.value = ""
                message.value = ""

            else:
                ui.notify(
                    result["message"],
                    type="negative"
                )

        ui.button(
            "SUBMIT MESSAGE",
            on_click=submit_form
        ).classes(
            "w-full bg-blue-600 text-white font-bold"
        )


@ui.page("/contact")
def contact_page():
    ui.query("body").style("background-color: #090909;")

    with ui.column().classes(
        "w-full max-w-5xl mx-auto p-6 gap-6"
    ):
        render_contact()
