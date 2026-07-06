"""
Lightweight translation helper for EN/AR UI labels.
"""

from typing import Dict


_TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "en": {
        "home_start_button": "Begin Game",
        "language_toggle": "EN/AR",
        "mode_title": "Select Your Opponent",
        "back_button": "Back",
        "play_with_friend": "Human Challenger",
        "play_with_bot": "Strategic AI",
        "difficulty_title": "Select Difficulty",
        "difficulty_easy": "EASY",
        "difficulty_medium": "MEDIUM",
        "difficulty_hard": "HARD",
        "difficulty_confirm": "CONFIRM",
        "sidebar_new_game": "New Game",
        "button_start_game": "Start Game",
        "button_load_saved_game": "Load Saved Game",
        "button_restart_game": "Restart Game",
        "button_undo_last_move": "Undo Last Move",
        "button_back_home": "Back To Home",
        "info_no_active_game": "No active game yet. Start a new game from the sidebar.",
        "subheader_game_state": "Game State",
        "subheader_board": "Board",
        "subheader_move_history": "Move History",
        "label_game_mode": "Mode",
        "label_status": "Status",
        "label_turn": "Turn",
        "label_move_count": "Move count",
        "label_difficulty": "Difficulty",
        "label_winner": "Winner",
        "label_end_reason": "End reason",
        "warning_check": "Check",
        "subheader_make_move": "Make Move",
        "subheader_promotion": "Promotion",
        "move_from": "From",
        "move_to": "To",
        "move_promotion": "Promotion",
        "button_play_move": "Play Move",
        "button_confirm_promotion": "Confirm Promotion",
        "button_cancel": "Cancel",
        "board_click_hint": "Click your piece, then click the destination square.",
        "board_selected_from": "Selected piece",
        "board_fen": "Board FEN",
        "info_no_legal_moves": "No legal moves available in this position.",
        "error_illegal_move": "Illegal move for the current position.",
        "caption_no_moves": "No moves played yet.",
        "promotion_queen": "Queen",
        "promotion_rook": "Rook",
        "promotion_bishop": "Bishop",
        "promotion_knight": "Knight",
    },
    "ar": {
        "home_start_button": "ابدأ اللعبة",
        "language_toggle": "EN/AR",
        "mode_title": "اختيار نوع الخصم",
        "back_button": "رجوع",
        "play_with_friend": "لاعب بشري",
        "play_with_bot": "ذكاء اصطناعي",
        "difficulty_title": "اختيار مستوى الصعوبة",
        "difficulty_easy": "سهل",
        "difficulty_medium": "متوسط",
        "difficulty_hard": "صعب",
        "difficulty_confirm": "تأكيد",
        "sidebar_new_game": "لعبة جديدة",
        "button_start_game": "ابدأ اللعبة",
        "button_load_saved_game": "تحميل لعبة محفوظة",
        "button_restart_game": "إعادة اللعبة",
        "button_undo_last_move": "تراجع عن آخر نقلة",
        "button_back_home": "العودة للرئيسية",
        "info_no_active_game": "لا توجد لعبة نشطة. ابدأ لعبة جديدة من الشريط الجانبي.",
        "subheader_game_state": "حالة اللعبة",
        "subheader_board": "اللوحة",
        "subheader_move_history": "سجل النقلات",
        "label_game_mode": "النمط",
        "label_status": "الحالة",
        "label_turn": "الدور",
        "label_move_count": "عدد النقلات",
        "label_difficulty": "الصعوبة",
        "label_winner": "الفائز",
        "label_end_reason": "سبب النهاية",
        "warning_check": "كش",
        "subheader_make_move": "تنفيذ نقلة",
        "subheader_promotion": "الترقية",
        "move_from": "من",
        "move_to": "إلى",
        "move_promotion": "الترقية",
        "button_play_move": "نفّذ النقلة",
        "button_confirm_promotion": "تأكيد الترقية",
        "button_cancel": "إلغاء",
        "board_click_hint": "اضغط على القطعة ثم اضغط على خانة الهدف.",
        "board_selected_from": "القطعة المحددة",
        "board_fen": "صيغة FEN",
        "info_no_legal_moves": "لا توجد نقلات قانونية في هذا الوضع.",
        "error_illegal_move": "النقلة غير قانونية في الوضع الحالي.",
        "caption_no_moves": "لم يتم لعب أي نقلة بعد.",
        "promotion_queen": "وزير",
        "promotion_rook": "قلعة",
        "promotion_bishop": "فيل",
        "promotion_knight": "حصان",
    },
}


def normalize_language(language: str | None) -> str:
    if not language:
        return "en"

    language = language.lower().strip()

    if language.startswith("ar"):
        return "ar"

    return "en"


def t(key: str, language: str | None = None) -> str:
    lang = normalize_language(language)
    lang_map = _TRANSLATIONS.get(lang, _TRANSLATIONS["en"])

    if key in lang_map:
        return lang_map[key]

    return _TRANSLATIONS["en"].get(key, key)
