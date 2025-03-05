from datetime import datetime
from lunar_python import Lunar
import random

class LunarFestival:
    """农历节日运势计算类"""
    
    FESTIVALS = {
        "春节": {"month": 1, "day": 1, "description": "新年开始，万象更新"},
        "元宵": {"month": 1, "day": 15, "description": "正月十五闹元宵"},
        "端午": {"month": 5, "day": 5, "description": "端午佳节，驱邪避灾"},
        "七夕": {"month": 7, "day": 7, "description": "牛郎织女相会日"},
        "中秋": {"month": 8, "day": 15, "description": "八月中秋，月圆人团圆"},
        "重阳": {"month": 9, "day": 9, "description": "登高望远，敬老怀远"},
        "腊八": {"month": 12, "day": 8, "description": "腊八节日，祈福纳祥"},
        "除夕": {"month": 12, "day": 30, "description": "辞旧迎新，阖家团圆"}
    }

    FESTIVAL_FORTUNES = [
        "节日喜庆，五福临门",
        "佳节欢聚，和气致祥",
        "节庆欢腾，百事亨通",
        "传统佳节，吉祥如意",
        "喜庆祥和，万事顺遂",
        "节日祈福，事事如意",
        "欢度佳节，阖家安康",
        "节日祝愿，幸福美满"
    ]

    @staticmethod
    def get_current_festival() -> dict:
        """获取当前或最近的农历节日"""
        current_date = datetime.now()
        lunar = Lunar.fromDate(current_date)
        
        lunar_month = lunar.getMonth()
        lunar_day = lunar.getDay()
        
        # 查找最近的节日
        current_festival = None
        min_days_diff = float('inf')
        
        for festival_name, festival_info in LunarFestival.FESTIVALS.items():
            month_diff = festival_info["month"] - lunar_month
            day_diff = festival_info["day"] - lunar_day
            
            total_days_diff = month_diff * 30 + day_diff
            if total_days_diff < 0:
                total_days_diff += 360  # 约一年的天数
            
            if total_days_diff < min_days_diff:
                min_days_diff = total_days_diff
                current_festival = {
                    "name": festival_name,
                    "info": festival_info,
                    "days_until": total_days_diff
                }
        
        return current_festival

    @staticmethod
    def get_festival_fortune(festival_name: str) -> dict:
        """获取节日运势"""
        # 使用当前时间微秒作为随机种子
        random.seed(datetime.now().microsecond)
        
        return {
            "overall": random.choice(["上上", "上", "中上", "中", "中下"]),
            "fortune": random.choice(LunarFestival.FESTIVAL_FORTUNES),
            "suggestions": [
                "宜：" + "、".join(random.sample([
                    "祈福", "拜访", "团聚", "庆贺", "宴请",
                    "出行", "谈事", "交友", "结缘", "办事"
                ], 3)),
                "忌：" + "、".join(random.sample([
                    "争执", "外出远行", "操劳", "过度劳累",
                    "独处", "忧思", "急躁", "轻率决策"
                ], 2))
            ]
        }
