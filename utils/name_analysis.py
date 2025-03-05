import random
from datetime import datetime

def analyze_name(name: str) -> dict:
    """Analyze Chinese name based on stroke counts and five elements."""

    # 扩展笔画字典
    stroke_count = {
        "李": 7, "王": 4, "张": 11, "刘": 6, "陈": 10, "杨": 7,
        "黄": 12, "赵": 9, "吴": 7, "周": 8, "徐": 10, "孙": 10,
        "马": 10, "朱": 6, "胡": 9, "郭": 11, "何": 7, "高": 10,
        "林": 8, "罗": 8, "郑": 9, "梁": 11, "谢": 12, "宋": 7,
        "唐": 10, "许": 6, "韩": 13, "冯": 9, "邓": 8, "曹": 11
    }

    # 五行属性和权重
    elements_data = {
        "木": {
            "chars": ["李", "杨", "林", "植", "桂", "柳"],
            "weight": random.uniform(0.8, 1.2)
        },
        "火": {
            "chars": ["丁", "朱", "赵", "炎", "焱", "熊"],
            "weight": random.uniform(0.8, 1.2)
        },
        "土": {
            "chars": ["王", "张", "孙", "田", "房", "黄"],
            "weight": random.uniform(0.8, 1.2)
        },
        "金": {
            "chars": ["陈", "徐", "钱", "铭", "钧", "锋"],
            "weight": random.uniform(0.8, 1.2)
        },
        "水": {
            "chars": ["吴", "江", "何", "洪", "沈", "潘"],
            "weight": random.uniform(0.8, 1.2)
        }
    }

    # 使用当前时间毫秒数来增加随机性
    current_ms = datetime.now().microsecond
    random.seed(current_ms)

    # Calculate strokes for each character
    name_strokes = {}
    total_strokes = 0
    name_elements = []
    element_weights = []

    for char in name:
        # 随机化笔画数在合理范围内
        base_strokes = stroke_count.get(char, random.randint(4, 15))
        variation = random.randint(-1, 1)  # 添加±1的变化
        final_strokes = max(1, base_strokes + variation)
        name_strokes[char] = final_strokes
        total_strokes += final_strokes

        # 确定字的五行属性，使用加权随机
        found_element = False
        for element, data in elements_data.items():
            if char in data["chars"]:
                name_elements.append(element)
                element_weights.append(data["weight"])
                found_element = True
                break

        if not found_element:
            # 如果找不到对应的五行，随机选择一个，但权重较低
            element = random.choice(list(elements_data.keys()))
            name_elements.append(element)
            element_weights.append(random.uniform(0.5, 0.9))

    # 计算五行组合得分
    element_combo_score = len(set(name_elements)) * 5  # 五行种类越多越好

    # 计算五行相生相克关系
    element_relations = {
        "木": {"生": "火", "克": "土"},
        "火": {"生": "土", "克": "金"},
        "土": {"生": "金", "克": "水"},
        "金": {"生": "水", "克": "木"},
        "水": {"生": "木", "克": "火"}
    }

    relation_score = 0
    for i in range(len(name_elements)):
        for j in range(i + 1, len(name_elements)):
            if name_elements[j] == element_relations[name_elements[i]]["生"]:
                relation_score += 10
            elif name_elements[j] == element_relations[name_elements[i]]["克"]:
                relation_score -= 5

    # 总分计算
    base_score = (total_strokes % 81) + 60
    weighted_score = sum([w * 10 for w in element_weights]) / len(element_weights)
    final_score = min(100, max(60, base_score + element_combo_score + relation_score + weighted_score))

    # 根据分数范围选择描述
    descriptions = {
        (90, 101): [
            "天赋异禀，前途无量",
            "大展宏图，前程似锦",
            "福星高照，万事顺遂",
            "智慧超群，前程似锦",
            "天资聪颖，鹏程万里"
        ],
        (80, 90): [
            "吉祥如意，平安顺遂",
            "事业有成，名利双收",
            "贵人相助，前程远大",
            "心想事成，前途光明",
            "和气生财，诸事顺遂"
        ],
        (70, 80): [
            "平稳发展，循序渐进",
            "勤勉上进，终有所成",
            "踏实稳健，渐入佳境",
            "稳步向前，未来可期",
            "厚积薄发，终成大器"
        ],
        (60, 70): [
            "平平安安，平稳发展",
            "谨慎行事，稳中求进",
            "勤勉上进，终有所获",
            "宜守不宜进，稳健为上",
            "谨慎行事，静待花开"
        ]
    }

    # 选择适合分数的描述
    for score_range, desc_list in descriptions.items():
        if score_range[0] <= final_score <= score_range[1]:
            description = random.choice(desc_list)
            break

    # 生成五行分析
    element_analysis = {}
    for element in set(name_elements):
        count = name_elements.count(element)
        element_analysis[element] = {
            "count": count,
            "percentage": round(count / len(name_elements) * 100, 1)
        }

    return {
        "strokes": name_strokes,
        "total_strokes": total_strokes,
        "elements": name_elements,
        "element_analysis": element_analysis,
        "overall_score": final_score,
        "description": description
    }