"""
将 base_skills.json 按 room 字段分组
"""
import json
from pathlib import Path

data_dir = Path(__file__).parent
input_file = data_dir / "base_skills.json"
output_file = data_dir / "skills_by_room.json"

# 读取原始数据
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# 按房间分组
rooms = {}
for operator, skills in data.items():
    for skill in skills:
        room = skill.get("room", "未知")
        if room not in rooms:
            rooms[room] = {}
        if operator not in rooms[room]:
            rooms[room][operator] = []
        rooms[room][operator].append(skill)

# 写入新文件
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(rooms, f, ensure_ascii=False, indent=2)

print(f"已完成！按房间分组的数据已保存到: {output_file}")
print(f"\n各房间干员数量:")
for room, operators in sorted(rooms.items()):
    print(f"  {room}: {len(operators)} 名干员")
