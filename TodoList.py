"""命令列待辦清單：新增、列出、編輯、完成、刪除，資料存於同目錄的 todos.json。"""

import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / "todos.json"


# ---------- 資料存取 ----------

def load_todos():
    if not DATA_FILE.exists():
        return []
    try:
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        print("讀取存檔失敗，將以空清單開始。")
        return []
    return data if isinstance(data, list) else []


def save_todos(todos):
    DATA_FILE.write_text(json.dumps(todos, ensure_ascii=False, indent=2), encoding="utf-8")


# ---------- 輸入工具 ----------

def ask_text(prompt):
    text = input(prompt).strip()
    if not text:
        print("內容不可空白。")
        return None
    return text


def ask_index(todos):
    if not todos:
        print("目前沒有任何待辦。")
        return None
    raw = input(f"請輸入編號 (1-{len(todos)})：").strip()
    if not raw.isdigit() or not 1 <= int(raw) <= len(todos):
        print("編號無效。")
        return None
    return int(raw) - 1


# ---------- 功能 ----------

def show(todos):
    if not todos:
        print("目前沒有任何待辦。")
        return
    for i, todo in enumerate(todos, start=1):
        mark = "x" if todo["done"] else " "
        print(f"{i:>3}. [{mark}] {todo['title']}")


def add(todos):
    title = ask_text("待辦內容：")
    if title:
        todos.append({"title": title, "done": False})
        print("已新增。")


def edit(todos):
    show(todos)
    index = ask_index(todos)
    if index is None:
        return
    title = ask_text("新的內容：")
    if title:
        todos[index]["title"] = title
        print("已更新。")


def toggle_done(todos):
    show(todos)
    index = ask_index(todos)
    if index is not None:
        todos[index]["done"] = not todos[index]["done"]
        print("已標記為完成。" if todos[index]["done"] else "已取消完成。")


def remove(todos):
    show(todos)
    index = ask_index(todos)
    if index is not None:
        removed = todos.pop(index)
        print(f"已刪除：{removed['title']}")


ACTIONS = {
    "1": ("列出待辦", show),
    "2": ("新增待辦", add),
    "3": ("編輯待辦", edit),
    "4": ("完成／取消完成", toggle_done),
    "5": ("刪除待辦", remove),
}


def main():
    todos = load_todos()
    while True:
        print("\n=== 待辦清單 ===")
        for key, (label, _) in ACTIONS.items():
            print(f"{key}. {label}")
        print("0. 離開")

        choice = input("請選擇：").strip()
        if choice == "0":
            print("再見！")
            break
        if choice not in ACTIONS:
            print("選項無效，請重新輸入。")
            continue

        ACTIONS[choice][1](todos)
        save_todos(todos)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n已結束。")
