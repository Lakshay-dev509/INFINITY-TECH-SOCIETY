"""INFINITY — The Tech Society | Interactive Homepage"""

from nicegui import ui
from services.ai_service import ask_infinity
from services.contact_service import submit_contact_message
from services.event_service import get_published_events
from services.registration_service import register_for_event

# ============================================================
# SOCIETY DATA
# ============================================================

HIGHLIGHTS = [
    ("BGMI 2.0", "sports_esports", "Gaming"),
    ("MoM", "emoji_events", "Community"),
    ("Achievements", "military_tech", "Society"),
    ("Cyber Week", "security", "Technology"),
    ("Bizbytes", "query_stats", "Business"),
    ("Gaming Events", "stadia_controller", "Gaming"),
    ("CYTHON'22", "code", "Technology"),
]



# ============================================================
# HOMEPAGE
# ============================================================

def render_home() -> None:

        # ---------------- LOAD EVENTS FROM SQL SERVER ----------------

    EVENTS = []

    database_result = get_published_events()

    if database_result.get("success"):

        for event in database_result.get("events", []):

            category = event.get("Category") or "Community"

            category_styles = {
                "Gaming": {
                    "icon": "sports_esports",
                    "tone": "blue"
                },
                "Technology": {
                    "icon": "computer",
                    "tone": "violet"
                },
                "Business": {
                    "icon": "business",
                    "tone": "silver"
                },
                "Community": {
                    "icon": "groups",
                    "tone": "blue"
                }
            }

            style = category_styles.get(
                category,
                {
                    "icon": "event",
                    "tone": "blue"
                }
            )

            event_date = event.get("EventDate")

            if event_date:
                event_date = event_date.strftime("%d %b %Y")
            else:
                event_date = "Date to be announced"

            EVENTS.append({
                "name": event.get("Title") or "Untitled Event",
                "category": category,
                "tag": category.upper(),
                "icon": style["icon"],
                "desc": event.get("Description") or "",
                "tone": style["tone"],
                "date": event_date,
                "venue": event.get("Venue") or "Venue to be announced"
            })

    else:
        print(
            "Could not load events:",
            database_result.get("message")
        )

    # ---------------- CSS AND FONTS ----------------

    ui.add_head_html("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

    <link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800;900&family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">

    <style>

    :root {
        --ink: #090b0f;
        --panel: #11151d;
        --line: rgba(220,228,245,.13);
        --blue: #315be8;
        --violet: #6337b8;
        --muted: #a5adbd;
        --white: #f4f5f7;
    }

    html {
        scroll-behavior: smooth;
        background: var(--ink);
    }

    body {
        background: var(--ink);
        color: var(--white);
        font-family: 'DM Sans', sans-serif;
    }

    .q-page {
        background: var(--ink);
    }

    .infinity-page {
        background:
        radial-gradient(ellipse at 80% 7%,
        rgba(49,91,232,.13), transparent 28%),
        radial-gradient(ellipse at 12% 32%,
        rgba(99,55,184,.12), transparent 27%),
        var(--ink);
        min-height: 100vh;
        overflow: hidden;
    }

    .display {
        font-family: 'Barlow Condensed', Impact, sans-serif;
        text-transform: uppercase;
        letter-spacing: .015em;
    }

    .space {
        font-family: 'Space Grotesk', sans-serif;
    }

    .muted {
        color: var(--muted);
    }

    .topbar {
        background: rgba(9,11,15,.88);
        backdrop-filter: blur(18px);
        border-bottom: 1px solid var(--line);
    }

    .brand-mark {
        font-size: 43px;
        line-height: 1;
        background: linear-gradient(110deg,#58b6bd,#d43d75);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
    }

    .nav-link {
        font-size: 12px;
        letter-spacing: .12em;
        text-transform: uppercase;
        color: #c8ced9;
    }

    .nav-link:hover {
        color: white;
    }

    .outline-btn {
        border: 1px solid rgba(220,228,245,.28)!important;
        border-radius: 3px!important;
        color: white!important;
        background: transparent!important;
        letter-spacing: .1em;
        text-transform: uppercase;
        font-size: 11px;
        font-weight: 700;
    }

    .blue-btn {
        background: #315be8!important;
        color: white!important;
        border-radius: 3px!important;
        letter-spacing: .1em;
        text-transform: uppercase;
        font-size: 11px;
        font-weight: 700;
        padding: 10px 20px!important;
    }

    .hero {
        position: relative;
        background:
        linear-gradient(90deg,
        rgba(7,9,14,.96),
        rgba(7,9,14,.76) 54%,
        rgba(7,9,14,.25)),
        radial-gradient(ellipse at 75% 48%,
        rgba(43,82,206,.30), transparent 45%),
        #101521;
        border-bottom: 1px solid var(--line);
    }

    .hero:after {
        content: "";
        position: absolute;
        inset: 0;
        pointer-events: none;
        opacity: .18;
        background-image:
        linear-gradient(rgba(255,255,255,.06) 1px,
        transparent 1px),
        linear-gradient(90deg,rgba(255,255,255,.06) 1px,
        transparent 1px);
        background-size: 48px 48px;
    }

    .hero-word {
        font-size: clamp(78px,13vw,174px);
        line-height: .78;
        font-weight: 900;
        letter-spacing: -.025em;
    }

    .hero-sub {
        font-size: clamp(13px,1.3vw,17px);
        letter-spacing: .28em;
        color: #c2c8d3;
        text-transform: uppercase;
    }

    .hero-orbit {
        position: absolute;
        right: 9%;
        top: 14%;
        width: min(34vw,390px);
        aspect-ratio: 1;
        border: 1px solid rgba(116,145,255,.28);
        border-radius: 50%;
        box-shadow: 0 0 90px rgba(49,91,232,.12);
    }

    .hero-orbit:before,
    .hero-orbit:after {
        content: "";
        position: absolute;
        inset: 12%;
        border: 1px solid rgba(116,145,255,.25);
        border-radius: 50%;
        transform: rotate(38deg) scaleX(1.45);
    }

    .hero-orbit:after {
        transform: rotate(-38deg) scaleX(1.45);
    }

    .infinity-symbol {
        font-size: clamp(95px,16vw,190px);
        font-family: 'Space Grotesk';
        color: rgba(219,226,255,.82);
        text-shadow: 0 0 42px rgba(71,112,255,.45);
    }

    .section-label {
        font-size: 10px;
        letter-spacing: .24em;
        text-transform: uppercase;
        color: #8da9ff;
        font-weight: 700;
    }

    .section-title {
        font-family: 'Barlow Condensed', sans-serif;
        text-transform: uppercase;
        font-size: clamp(36px,5vw,58px);
        line-height: .98;
        font-weight: 800;
    }

    .story {
        width: 94px;
        flex-shrink: 0;
        text-align: center;
        cursor: pointer;
    }

    .story-ring {
        width: 78px;
        height: 78px;
        border-radius: 50%;
        padding: 3px;
        margin: auto;
        background: linear-gradient(145deg,#477bff,#5132a6,#8d54cf);
    }

    .story-inner {
        height: 100%;
        width: 100%;
        border-radius: 50%;
        background: #121827;
        border: 2px solid #090b0f;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .story-label {
        font-size: 11px;
        font-weight: 600;
        color: #d9deea;
        margin-top: 9px;
        white-space: nowrap;
    }

    .poster {
        position: relative;
        overflow: hidden;
        min-height: 205px;
        background: #151b29;
        border: 1px solid var(--line);
        border-radius: 3px;
        transition: transform .25s, border-color .25s;
    }

    .poster:hover {
        transform: translateY(-5px);
        border-color: rgba(105,143,255,.7);
    }

    .poster:before {
        content: "";
        position: absolute;
        inset: 0;
        background: linear-gradient(
            135deg,
            rgba(49,91,232,.33),
            transparent 48%,
            rgba(99,55,184,.30)
        );
    }

    .poster.violet:before {
        background: linear-gradient(
            135deg,
            rgba(93,47,172,.52),
            transparent 60%,
            rgba(39,75,186,.25)
        );
    }

    .poster.silver:before {
        background: linear-gradient(
            135deg,
            rgba(173,185,207,.16),
            transparent 58%,
            rgba(49,91,232,.2)
        );
    }

    .poster-icon {
        font-size: 60px;
        color: rgba(239,243,255,.88);
        filter: drop-shadow(0 0 18px rgba(91,126,255,.55));
    }

    .poster-watermark {
        position: absolute;
        right: 8px;
        bottom: -22px;
        font-family: 'Barlow Condensed';
        font-size: 100px;
        font-weight: 900;
        color: rgba(255,255,255,.045);
        line-height: 1;
    }

    .poster-tag {
        font-size: 9px;
        letter-spacing: .2em;
        color: #9bb2ff;
        font-weight: 700;
    }

    .poster-title {
        font-family: 'Barlow Condensed';
        font-size: 30px;
        text-transform: uppercase;
        font-weight: 800;
        line-height: 1;
    }

    .glass {
        background: linear-gradient(
            145deg,
            rgba(24,30,44,.94),
            rgba(13,16,24,.96)
        );
        border: 1px solid var(--line);
        border-radius: 4px;
    }

    .gallery-tile {
        aspect-ratio: 1;
        background: linear-gradient(
            145deg,#1b2945,#0c1019 65%,#39245c
        );
        border: 1px solid rgba(255,255,255,.08);
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        overflow: hidden;
    }

    .gallery-tile:after {
        content: "";
        position: absolute;
        inset: 0;
        background: repeating-linear-gradient(
            135deg,
            transparent 0 18px,
            rgba(255,255,255,.025) 19px 20px
        );
    }

    .gallery-tile .q-icon {
        z-index: 1;
    }

    .team-banner {
        background:
        radial-gradient(ellipse at 50% 120%,
        rgba(54,94,228,.32), transparent 55%),
        linear-gradient(110deg,#151a25,#080a0f 65%);
        border: 1px solid var(--line);
        position: relative;
        overflow: hidden;
    }

    .team-banner:after {
        content: "∞";
        position: absolute;
        right: 3%;
        top: -100px;
        font-size: 360px;
        color: rgba(255,255,255,.035);
        font-family: 'Space Grotesk';
    }

    .q-field--outlined .q-field__control:before {
        border-color: rgba(210,220,245,.24)!important;
    }

    .q-field__native,
    .q-field__label {
        color: #edf0f8!important;
    }

    @media(max-width:700px) {
        .desktop-nav { display: none!important; }
        .hero-orbit {
            right: -18%;
            top: 22%;
            opacity: .5;
            width: 65vw;
        }
        .hero-word { font-size: 82px; }
        .story { width: 82px; }
        .story-ring {
            width: 68px;
            height: 68px;
        }
    }

    </style>
    """)

    # ---------------- NAVIGATION HELPER ----------------

    def scroll_to(section: str) -> None:
        ui.run_javascript(
            f"document.getElementById('{section}')?.scrollIntoView({{behavior:'smooth'}})"
        )

    # ====================================================
    # MAIN PAGE
    # ====================================================

    with ui.column().classes("infinity-page w-full gap-0"):

        # ---------------- HEADER ----------------

        with ui.row().classes(
            "topbar w-full justify-center sticky top-0 z-50"
        ):
            with ui.row().classes(
                "w-full max-w-7xl items-center justify-between px-6 py-3"
            ):

                with ui.row().classes("items-center gap-2"):
                    ui.label("∞").classes("brand-mark")

                    with ui.column().classes("gap-0"):
                        ui.label("INFINITY").classes(
                            "space text-base font-bold tracking-[.24em]"
                        )
                        ui.label("THE TECH SOCIETY").classes(
                            "text-[8px] tracking-[.25em] text-slate-400"
                        )

                with ui.row().classes(
                    "desktop-nav items-center gap-7"
                ):
                    for label, section in [
                        ("Home", "home"),
                        ("About", "about"),
                        ("Highlights", "highlights"),
                        ("Gallery", "gallery"),
                        ("Team", "team"),
                        ("Contact", "contact"),
                    ]:
                        ui.button(
                            label,
                            on_click=lambda s=section: scroll_to(s)
                        ).props("flat dense no-caps").classes("nav-link")

                with ui.row().classes("items-center gap-2"):
                    ui.button(
                        "Instagram",
                        on_click=lambda: ui.run_javascript(
                            "window.open('https://www.instagram.com/infinity.sggscc/','_blank')"
                        )
                    ).props("flat dense no-caps").classes(
                        "text-xs text-slate-300"
                    )

                    ui.button(
                        "Connect",
                        on_click=lambda: scroll_to("contact")
                    ).classes("blue-btn")

        # ---------------- HERO SECTION ----------------

        with ui.element("section").props(
            'id="home"'
        ).classes("hero w-full"):

            with ui.row().classes(
                "relative z-10 w-full max-w-7xl mx-auto px-6 py-24 md:py-32 items-center"
            ):

                with ui.column().classes("w-full md:w-3/5 gap-5"):

                    ui.label(
                        "SGGSCC · STUDENT TECHNOLOGY COMMUNITY"
                    ).classes("section-label")

                    ui.label("THINK").classes(
                        "display hero-word"
                    )

                    ui.label("BEYOND").classes(
                        "display hero-word text-transparent"
                    ).style(
                        "-webkit-text-stroke:1px rgba(225,231,245,.8)"
                    )

                    ui.label("LIMITS.").classes(
                        "display hero-word"
                    )

                    ui.label(
                        "EXPLORE · INNOVATE · CONNECT"
                    ).classes("hero-sub mt-3")

                    ui.label(
                        "With minds to explore and tech as our guide, "
                        "curiosity fuels us, side by side!"
                    ).classes("muted max-w-xl leading-7")

                    with ui.row().classes("gap-3 flex-wrap pt-2"):

                        ui.button(
                            "Explore the society",
                            on_click=lambda: scroll_to("about")
                        ).classes("blue-btn")

                        ui.button(
                            "View highlights",
                            on_click=lambda: scroll_to("highlights")
                        ).classes("outline-btn")

                with ui.column().classes(
                    "w-full md:w-2/5 items-center justify-center"
                ):

                    with ui.element("div").classes("hero-orbit"):
                        pass

                    ui.label("∞").classes(
                        "infinity-symbol relative z-10"
                    )
                    # ---------------- SOCIETY HIGHLIGHTS ----------------

        with ui.element("section").props(
            'id="highlights"'
        ).classes("w-full border-b border-slate-800"):

            with ui.column().classes(
                "w-full max-w-7xl mx-auto px-6 py-14 gap-7"
            ):

                with ui.row().classes(
                    "w-full items-end justify-between"
                ):

                    with ui.column().classes("gap-2"):
                        ui.label("FROM OUR COMMUNITY").classes(
                            "section-label"
                        )

                        ui.label("SOCIETY HIGHLIGHTS").classes(
                            "section-title"
                        )

                    ui.label(
                        "A glimpse into INFINITY"
                    ).classes("muted text-xs")

                with ui.row().classes(
                    "w-full gap-4 overflow-x-auto pb-3"
                ):

                    for title, icon, category in HIGHLIGHTS:

                        with ui.column().classes(
                            "story items-center"
                        ).on(
                            "click",
                            lambda t=title: ui.notify(
                                f"{t} highlight selected"
                            )
                        ):

                            with ui.element("div").classes(
                                "story-ring"
                            ):

                                with ui.element("div").classes(
                                    "story-inner"
                                ):
                                    ui.icon(icon).classes(
                                        "text-3xl text-indigo-100"
                                    )

                            ui.label(title).classes("story-label")

        # ---------------- ABOUT SECTION ----------------

        with ui.element("section").props(
            'id="about"'
        ).classes("w-full"):

            with ui.row().classes(
                "w-full max-w-7xl mx-auto px-6 py-20 gap-12 items-center"
            ):

                with ui.column().classes(
                    "w-full md:w-1/2 gap-4"
                ):

                    ui.label("WHO WE ARE").classes(
                        "section-label"
                    )

                    ui.label(
                        "CURIOSITY IS OUR COMPASS."
                    ).classes("section-title")

                    ui.label(
                        "INFINITY — The Tech Society"
                    ).classes(
                        "space text-xl font-semibold text-slate-100"
                    )

                    ui.label(
                        "A student-led technology community at "
                        "Sri Guru Gobind Singh College of Commerce, "
                        "bringing together curious minds to explore "
                        "technology, creativity and innovation."
                    ).classes("muted leading-8")

                    with ui.row().classes("gap-2 flex-wrap"):

                        for chip in [
                            "TECHNOLOGY",
                            "CREATIVITY",
                            "COMMUNITY",
                            "INNOVATION",
                        ]:
                            ui.label(chip).classes(
                                "text-[9px] tracking-[.16em] "
                                "border border-slate-700 px-3 py-2 "
                                "text-slate-300"
                            )

                with ui.column().classes("w-full md:w-1/2"):

                    with ui.element("div").classes(
                        "team-banner w-full min-h-[300px] "
                        "flex items-center justify-center"
                    ):

                        with ui.column().classes(
                            "items-center gap-2 relative z-10"
                        ):

                            ui.label("∞").classes(
                                "brand-mark text-[100px]"
                            )

                            ui.label("INFINITY").classes(
                                "display text-6xl font-bold tracking-widest"
                            )

                            ui.label(
                                "THE TECH SOCIETY · SGGSCC"
                            ).classes(
                                "text-xs tracking-[.25em] text-slate-300"
                            )


        
        # ---------------- EVENTS AND INITIATIVES ----------------

        # Fetch published events from SQL Server
        event_result = get_published_events()
        DATABASE_EVENTS = []

        if event_result["success"]:

            for item in event_result["events"]:

                category = str(item.get("Category") or "Community")

                category_styles = {
                    "Gaming": {
                        "icon": "gamepad-2",
                        "tone": "tone-blue",
                    },
                    "Technology": {
                        "icon": "cpu",
                        "tone": "tone-violet",
                    },
                    "Business": {
                        "icon": "briefcase-business",
                        "tone": "tone-cyan",
                    },
                    "Community": {
                        "icon": "users",
                        "tone": "tone-indigo",
                    },
                }

                style = category_styles.get(
                    category,
                    {
                        "icon": "calendar-days",
                        "tone": "tone-indigo",
                    }
                )

                event_date = item.get("EventDate")

                if event_date:
                    event_date = event_date.strftime("%d %b %Y")
                else:
                    event_date = "Date to be announced"

                DATABASE_EVENTS.append({
                    "id": item.get("EventID"),
                    "name": item.get("Title") or "Untitled Event",
                    "desc": item.get("Description") or "More details coming soon.",
                    "category": category,
                    "tag": category.upper(),
                    "icon": style["icon"],
                    "tone": style["tone"],
                    "date": event_date,
                    "venue": item.get("Venue") or "Venue to be announced",
                })

        else:
            print(
                "Could not load website events:",
                event_result["message"]
            )

        with ui.element("section").props(
            'id="events"'
        ).classes(
            "w-full bg-[#0d1119] border-y border-slate-800"
        ):

            with ui.column().classes(
                "w-full max-w-7xl mx-auto px-6 py-20 gap-8"
            ):

                with ui.row().classes(
                    "w-full items-end justify-between flex-wrap gap-4"
                ):

                    with ui.column().classes("gap-2"):

                        ui.label("WHAT WE DO").classes(
                            "section-label"
                        )

                        ui.label(
                            "EVENTS & INITIATIVES"
                        ).classes("section-title")

                        ui.label(
                            "Explore events and initiatives by INFINITY."
                        ).classes("muted text-sm")

                    search = ui.input(
                        placeholder="Search events..."
                    ).props(
                        "outlined dense"
                    ).classes("w-full sm:w-64")

                filters = ui.row().classes("gap-2 flex-wrap")

                event_grid = ui.grid(columns=1).classes(
                    "w-full grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6"
                )

                active_filter = {"value": "All"}
                filter_buttons = []

                
            def open_registration_dialog(event):
                    
                    with ui.dialog() as dialog:
                        with ui.card().classes("w-full max-w-md p-6"):

                            ui.label("EVENT REGISTRATION").classes(
                                "text-xl font-bold"
                            )

                            ui.label(event["name"]).classes(
                                "text-blue-400 font-semibold"
                            )

                            ui.separator()

                            name_input = ui.input(
                                "Full Name",
                                placeholder="Enter your full name"
                            ).classes("w-full")

                            email_input = ui.input(
                                "Email Address",
                                placeholder="Enter your email"
                            ).classes("w-full")

                            phone_input = ui.input(
                                "Phone Number",
                                placeholder="Enter your phone number"
                            ).classes("w-full")

                            def submit_registration():

                                result = register_for_event(
                                    name_input.value,
                                    email_input.value,
                                    phone_input.value,
                                    event["id"]
                                )

                                if result["success"]:

                                    ui.notify(
                                        result["message"],
                                        type="positive"
                                    )

                                    dialog.close()

                                else:

                                    ui.notify(
                                        result["message"],
                                        type="negative"
                                    )

                            with ui.row().classes("w-full justify-end mt-4"):

                                ui.button(
                                    "CANCEL",
                                    on_click=dialog.close
                                ).props("outline")

                                ui.button(
                                    "REGISTER NOW",
                                    on_click=submit_registration
                                ).classes("blue-btn")

                    dialog.open()

            def render_event_cards(query=""):
                event_grid.clear()

                query = (query or "").strip().lower()

                matches = [
                    event for event in DATABASE_EVENTS
                    if (
                        active_filter["value"] == "All"
                        or event["category"].lower()
                        == active_filter["value"].lower()
                    )
                    and query in (
                        event["name"] + " "
                        + event["desc"] + " "
                        + event["category"] + " "
                        + event["venue"]
                    ).lower()
                ]
                

                with event_grid:

                    if not matches:

                        ui.label(
                            "No published events found."
                            if not DATABASE_EVENTS
                            else "No events match your search."
                        ).classes("muted p-5")

                    for event in matches:

                        with ui.card().classes(
                            f"poster {event['tone']} p-5"
                        ):

                            with ui.row().classes(
                                "w-full justify-between items-start"
                            ):

                                ui.label(
                                    event["tag"]
                                ).classes("poster-tag")

                                ui.icon(
                                    event["icon"]
                                ).classes("text-slate-400")

                            ui.space()

                            ui.icon(
                                event["icon"]
                            ).classes("poster-icon")

                            ui.label(
                                event["name"]
                            ).classes("poster-title mt-3")

                            ui.label(
                                event["desc"]
                            ).classes(
                                "text-xs text-slate-300 leading-5"
                            )

                            ui.label(
                                f"DATE: {event['date']}"
                            ).classes(
                                "text-xs text-slate-400 mt-3"
                            )

                            ui.label(
                                f"VENUE: {event['venue']}"
                            ).classes(
                                "text-xs text-slate-400"
                            )

                            ui.label(
                                "INFINITY EVENT"
                            ).classes(
                                "text-[9px] tracking-[.15em] "
                                "text-blue-300 mt-3"
                            )

                            ui.label("∞").classes(
                                "poster-watermark"
                            )

                            ui.button(
                                "REGISTER NOW",
                                on_click=lambda e=event: open_registration_dialog(e)
                                ).classes("blue-btn w-full mt-4")

                def choose_filter(category):

                    active_filter["value"] = category

                    for button, label in filter_buttons:

                        button.props(
                            "color=primary"
                            if label == category
                            else "outline"
                        )

                    render_event_cards(search.value or "")

                with filters:

                    for category in [
                        "All",
                        "Gaming",
                        "Technology",
                        "Business",
                        "Community",
                    ]:

                        button = ui.button(
                            category,
                            on_click=lambda c=category: choose_filter(c)
                        ).props(
                            "dense no-caps"
                        ).classes("text-xs")

                        if category == "All":
                            button.props("color=primary")
                        else:
                            button.props("outline")

                        filter_buttons.append(
                            (button, category)
                        )

                search.on_value_change(
                    lambda value: render_event_cards(value or "")
                )

            render_event_cards()


        # ---------------- GALLERY ----------------
        

        with ui.element("section").props(
            'id="gallery"'
        ).classes("w-full"):

            with ui.column().classes(
                "w-full max-w-7xl mx-auto px-6 py-20 gap-8"
            ):

                with ui.row().classes(
                    "items-end justify-between flex-wrap"
                ):

                    with ui.column().classes("gap-2"):

                        ui.label("VISUAL ARCHIVE").classes(
                            "section-label"
                        )

                        ui.label(
                            "MOMENTS THAT MOVE US."
                        ).classes("section-title")

                    
            
            
            gallery_photos = [
                (
                    "INFINITY TECH MOMENTS",
                    "assets/gallery/pexels-thisisengineering-19895774.jpg"
                ),
                (
                    "TEAM COLLABORATION",
                    "assets/gallery/pexels-rashed-hossain-1520582336-32866724.jpg"
                ),
                (
                    "CREATIVE ENVIRONMENT",
                    "assets/gallery/pexels-bertellifotografia-18999483.jpg"
                )
            ]

            with ui.element("div").classes(
                "w-full grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5"
            ):
                for title, image_path in gallery_photos:

                    with ui.card().classes(
                        "w-full overflow-hidden p-0 bg-slate-900"
                    ):
                        ui.image(image_path).classes(
                            "w-full h-64 object-cover"
                        )

                        ui.label(title).classes(
                            "text-xs font-bold tracking-widest p-4 text-white"
                        )



                    # ---------------- CORE TEAM ----------------

        with ui.element("section").props(
            'id="team"'
        ).classes("w-full px-6 pb-20"):

            with ui.column().classes(
                "team-banner w-full max-w-7xl mx-auto "
                "px-7 md:px-14 py-14 gap-4"
            ):

                ui.label(
                    "THE PEOPLE BEHIND THE POSSIBILITIES"
                ).classes("section-label")

                ui.label("CORE TEAM").classes(
                    "display text-6xl md:text-8xl font-black"
                )

                ui.label("2026 — 27").classes(
                    "display text-4xl text-slate-300"
                )

                ui.label(
                    "A community powered by ideas, "
                    "collaboration and curiosity."
                ).classes("muted max-w-xl")

                ui.button(
                    "Meet the society",
                    on_click=lambda: ui.notify(
                        "Team profiles will appear here once "
                        "approved member details are added."
                    )
                ).classes("blue-btn self-start")

        # ---------------- CONTACT ----------------

        with ui.element("section").props(
            'id="contact"'
        ).classes(
            "w-full bg-[#0d1119] border-t border-slate-800"
        ):

            with ui.row().classes(
                "w-full max-w-7xl mx-auto px-6 py-16 gap-12"
            ):

                with ui.column().classes(
                    "w-full md:w-1/2 gap-4"
                ):

                    ui.label("GET IN TOUCH").classes(
                        "section-label"
                    )

                    ui.label(
                        "LET'S BUILD WHAT'S NEXT."
                    ).classes("section-title")

                    ui.label(
                        "Follow INFINITY for society updates, "
                        "events and community highlights."
                    ).classes("muted leading-7")

                    ui.button(
                        "Instagram ↗",
                        on_click=lambda: ui.run_javascript(
                            "window.open("
                            "'https://www.instagram.com/infinity.sggscc/',"
                            "'_blank')"
                        )
                    ).classes("outline-btn self-start")

                    ui.button(
                        "LinkedIn ↗",
                        on_click=lambda: ui.run_javascript(
                            "window.open("
                            "'https://www.linkedin.com/company/infinitysggscc/',"
                            "'_blank')"
                        )
                    ).classes("outline-btn self-start")

                # CONTACT FORM CARD
                with ui.card().classes(
                    "glass w-full md:w-1/2 p-6 gap-3"
                ):

                    ui.label("SEND A MESSAGE").classes(
                        "section-label"
                    )

                    contact_name = ui.input(
                        "Your name"
                    ).props("outlined").classes("w-full")

                    contact_email = ui.input(
                        "Email address"
                    ).props("outlined type=email").classes("w-full")

                    contact_message = ui.textarea(
                        "Your message"
                    ).props("outlined").classes("w-full")

                    # ---------------- SUBMIT FUNCTION ----------------

                    def send_message():

                        # Read form values
                        name = (contact_name.value or "").strip()
                        email = (contact_email.value or "").strip()
                        message = (contact_message.value or "").strip()

                        # Save message in SQL Server
                        result = submit_contact_message(
                            name,
                            email,
                            "",
                            message
                        )

                        if result["success"]:

                            ui.notify(
                                result["message"],
                                type="positive"
                            )

                            # Clear form after successful submission
                            contact_name.value = ""
                            contact_email.value = ""
                            contact_message.value = ""

                        else:

                            ui.notify(
                                result["message"],
                                type="negative"
                            ) 
    # CONTACT FORM SUBMIT BUTTON
                    ui.button(
                        "SEND MESSAGE",
                        on_click=send_message
                    ).classes("blue-btn w-full")                            


    # ---------------- INFINITY AI ASSISTANT ----------------

    ai_history = []

    def send_ai_message():

        message = (ai_input.value or "").strip()

        if not message:
            return

        ai_input.value = ""

        with ai_messages:
            ui.chat_message(
                message,
                name="You",
                sent=True
            )

        result = ask_infinity(message, ai_history)

        if result["success"]:

            ai_history.append({
                "role": "user",
                "text": message
            })

            ai_history.append({
                "role": "model",
                "text": result["reply"]
            })

        with ai_messages:
            ui.chat_message(
                result["reply"],
                name="INFINITY AI",
                sent=False
            )

    with ui.dialog() as ai_dialog:

        with ui.card().classes(
            "w-[90vw] max-w-md p-0 gap-0 overflow-hidden"
        ):

            with ui.row().classes(
                "w-full items-center justify-between p-4 bg-slate-900"
            ):

                with ui.column().classes("gap-0"):
                    ui.label("INFINITY AI").classes(
                        "text-lg font-bold text-white"
                    )

                    ui.label("Your Tech Society Assistant").classes(
                        "text-xs text-slate-400"
                    )

                ui.button(
                    icon="close",
                    on_click=ai_dialog.close
                ).props("flat round color=white")

            ai_messages = ui.column().classes(
                "w-full h-80 overflow-y-auto p-4 gap-3"
            )

            with ai_messages:
                ui.chat_message(
                    "Hey! I'm INFINITY AI. Ask me about our society, events and registrations!",
                    name="INFINITY AI",
                    sent=False
                )

            with ui.row().classes(
                "w-full items-center p-3 gap-2"
            ):

                ai_input = ui.input(
                    placeholder="Ask INFINITY anything..."
                ).classes("flex-grow")

                ui.button(
                    "SEND",
                    icon="send",
                    on_click=send_ai_message
                ).classes("blue-btn")

    ui.button(
        "Ask INFINITY",
        icon="smart_toy",
        on_click=ai_dialog.open
    ).classes(
        "fixed bottom-6 right-6 z-50 shadow-lg blue-btn"
    )
