"""Chat agent intent detection + endpoint tests."""
from app.agents.chat_agent import detect_intent


def test_intent_english():
    assert detect_intent("Which dishes lose money?") == "margin"
    assert detect_intent("Should I raise prices?") == "price"
    assert detect_intent("How do I cut waste?") == "waste"
    assert detect_intent("Any marketing ideas?") == "marketing"
    assert detect_intent("What is my health score?") == "score"
    assert detect_intent("hello there") == "greet"


def test_intent_cantonese():
    assert detect_intent("邊啲菜蝕錢？") == "margin"
    assert detect_intent("應該加價嗎？") == "price"
    assert detect_intent("點樣減少浪費？") == "waste"
    assert detect_intent("推廣建議？") == "marketing"


def test_chat_endpoint_bilingual(client):
    shops = client.get("/api/shops").json()
    sid = shops[0]["id"]

    en = client.post("/api/chat", json={"message": "Which dishes lose money?", "lang": "en", "shop_id": sid})
    assert en.status_code == 200
    body = en.json()
    assert body["intent"] == "margin"
    assert body["lang"] == "en"
    assert body["reply"]

    zh = client.post("/api/chat", json={"message": "邊啲菜蝕錢？", "lang": "zh", "shop_id": sid})
    assert zh.status_code == 200
    zbody = zh.json()
    assert zbody["intent"] == "margin"
    assert zbody["lang"] == "zh"
    # Cantonese reply should contain CJK characters
    assert any("\u4e00" <= ch <= "\u9fff" for ch in zbody["reply"])


def test_chat_without_shop(client):
    r = client.post("/api/chat", json={"message": "hi", "lang": "en"})
    assert r.status_code == 200
    assert r.json()["intent"] == "greet"
