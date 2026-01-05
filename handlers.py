if data == "shopping":
    context.user_data["mode"] = "shopping_items"
    await query.message.reply_text(
        get_text("ask_shopping", lang)
    )
    return

if data == "shop_today":
    items = context.user_data.pop("shopping_items", [])
    save_shopping(user_id, items, "today")
    await query.message.reply_text(
        get_text("shopping_saved_today", lang),
        reply_markup=main_menu()
    )
    return

if data == "shop_history":
    rows = get_shopping_history(user_id)
    text = format_history(rows)
    await query.message.reply_text(
        text or get_text("no_shopping_history", lang),
        reply_markup=main_menu()
    )
    return
