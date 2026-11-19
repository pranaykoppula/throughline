"""The concept families: one folder each, in the order SPEC section 3.3 lists them.

Each family is a field you'd look a concept up under. make_graph.py and make_map.py both read this list,
and check_links.py fails if a folder of concept pages isn't in it.
"""

FAMILIES = {
    "dsa": ("Algorithms and data structures", "DSA", "#1baa7a"),
    "data": ("Data systems", "Data", "#2a78d6"),
    "performance": ("Performance", "Performance", "#e09a1a"),
    "economics": ("Economics", "Economics", "#a87b4f"),
    "security": ("Security", "Security", "#d64a4a"),
    "languages": ("Programming languages", "Languages", "#e86fe0"),
    "practice": ("Engineering practice", "Practice", "#8fb339"),
    "ai": ("Machine learning and AI", "AI", "#8a5cd6"),
    "math": ("Mathematics", "Math", "#31b6d1"),
    "info": ("Information and meaning", "Information", "#6e7781"),
    "signals": ("Signals and control", "Signals", "#ff8f6b"),
}
