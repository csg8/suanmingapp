import random
from datetime import datetime
from typing import List, Dict

class TarotReader:
    """塔罗牌占卜系统"""
    
    # 主要牌阵
    MAJOR_ARCANA = {
        "愚者": {
            "upright": "新的开始、冒险、纯真",
            "reversed": "鲁莽、不确定、危险的选择",
            "description": "象征纯真与新生，代表一段旅程的开始"
        },
        "魔术师": {
            "upright": "创造力、技能、意志力",
            "reversed": "技能未熟、欺骗、能力误用",
            "description": "象征着创造与实现的能力"
        },
        "女祭司": {
            "upright": "直觉、神秘、内在知识",
            "reversed": "隐藏的动机、表面信息",
            "description": "象征智慧与神秘的力量"
        },
        "女皇": {
            "upright": "丰盛、孕育、母性",
            "reversed": "依赖、过度保护、创造力受阻",
            "description": "象征着滋养与创造力"
        },
        "皇帝": {
            "upright": "权威、建立、成就",
            "reversed": "专制、僵化、过度控制",
            "description": "象征着权力与稳定"
        }
    }

    # 小阿卡纳牌 - 示例部分
    MINOR_ARCANA = {
        "权杖": {
            "ace": {
                "upright": "新机会、灵感、潜力",
                "reversed": "延迟的开始、错失机会",
                "description": "象征新的开始与创造力"
            }
        },
        "圣杯": {
            "ace": {
                "upright": "感情、直觉、新关系",
                "reversed": "情感阻塞、错失良机",
                "description": "象征感情与内在世界"
            }
        },
        "宝剑": {
            "ace": {
                "upright": "清晰、真理、突破",
                "reversed": "混乱、虚假、障碍",
                "description": "象征思维与交流"
            }
        },
        "金币": {
            "ace": {
                "upright": "物质机会、繁荣、丰富",
                "reversed": "错失机会、物质损失",
                "description": "象征物质与现实世界"
            }
        }
    }

    @staticmethod
    def draw_cards(num_cards: int = 3) -> List[Dict]:
        """抽取指定数量的塔罗牌"""
        # 使用当前时间微秒作为随机种子
        random.seed(datetime.now().microsecond)
        
        # 合并所有牌
        all_cards = []
        for card_name, card_info in TarotReader.MAJOR_ARCANA.items():
            all_cards.append({
                "name": card_name,
                "type": "major",
                "info": card_info,
                "reversed": random.choice([True, False])
            })
        
        # 随机抽取指定数量的牌
        drawn_cards = random.sample(all_cards, min(num_cards, len(all_cards)))
        
        # 添加位置解释
        positions = ["过去", "现在", "未来", "建议", "结果"]
        for i, card in enumerate(drawn_cards):
            card["position"] = positions[i] if i < len(positions) else "补充"
        
        return drawn_cards

    @staticmethod
    def interpret_reading(cards: List[Dict]) -> str:
        """解读塔罗牌阵"""
        interpretation = []
        
        for card in cards:
            card_name = card["name"]
            position = card["position"]
            is_reversed = card["reversed"]
            
            meaning = card["info"]["reversed" if is_reversed else "upright"]
            orientation = "逆位" if is_reversed else "正位"
            
            interpretation.append(f"""
            {position}牌位：{card_name}（{orientation}）
            含义：{meaning}
            解释：{card["info"]["description"]}
            """)
        
        return "\n".join(interpretation)

    @staticmethod
    def get_reading_summary(cards: List[Dict]) -> Dict:
        """获取塔罗牌阵整体解读"""
        # 计算整体倾向
        reversed_count = sum(1 for card in cards if card["reversed"])
        
        if reversed_count > len(cards) // 2:
            overall_tendency = "需要注意挑战与障碍"
        else:
            overall_tendency = "整体发展趋势向好"
            
        return {
            "overall_tendency": overall_tendency,
            "suggestion": "建议深入思考牌面启示，合理规划未来",
            "timing": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
