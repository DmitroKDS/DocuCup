async def json_convert(chat: str):
    chat_json = []
    for line in chat.split('\n'):
        if line=="----AI----":
            chat_json.append({"type": "answer", "content": ""})
        elif line=="----User----":
            chat_json.append({"type": "message", "content": ""})
        elif len(chat_json)>0:
            chat_json[-1]["content"] += line + "<br>"

    return chat_json