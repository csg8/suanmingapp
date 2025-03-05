import datetime
from typing import Dict, List, Tuple

class ZiWeiCalculator:
    """紫薇斗数计算类"""

    # 十二宫名称
    PALACES = ["命宫", "兄弟", "夫妻", "子女", "财帛", "疾厄", 
               "迁移", "交友", "官禄", "田宅", "福德", "父母"]

    # 天干
    HEAVENLY_STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

    # 地支
    EARTHLY_BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", 
                       "午", "未", "申", "酉", "戌", "亥"]

    # 主星
    MAIN_STARS = ["紫微", "天机", "太阳", "武曲", "天同", "廉贞", 
                  "天府", "太阴", "贪狼", "巨门", "天相", "天梁", "七杀", "破军"]

    # 宫位解释
    PALACE_MEANINGS = {
        "命宫": "主性格、个性、人生走向",
        "兄弟": "主手足关系、同辈互动",
        "夫妻": "主婚姻、感情、伴侣",
        "子女": "主子女、后代、创造力",
        "财帛": "主财运、收入、理财",
        "疾厄": "主健康、困难、化解",
        "迁移": "主行动、变化、旅行",
        "交友": "主朋友、人际、社交",
        "官禄": "主事业、地位、成就",
        "田宅": "主房产、居所、投资",
        "福德": "主心理、福分、休闲",
        "父母": "主长辈、贵人、靠山"
    }

    # 星曜吉凶
    STAR_QUALITIES = {
        "紫微": "吉", "天机": "吉", "太阳": "吉",
        "武曲": "吉", "天同": "吉", "廉贞": "凶",
        "天府": "吉", "太阴": "吉", "贪狼": "凶",
        "巨门": "中", "天相": "吉", "天梁": "吉",
        "七杀": "凶", "破军": "凶"
    }

    def __init__(self, birth_datetime: datetime.datetime, gender: str):
        """初始化紫薇斗数计算器"""
        self.birth_datetime = birth_datetime
        self.gender = gender
        self.lunar_date = self._convert_to_lunar()

    def _convert_to_lunar(self) -> Dict:
        """将公历转换为农历日期"""
        # TODO: 实现农历转换逻辑
        return {
            "year": self.birth_datetime.year,
            "month": self.birth_datetime.month,
            "day": self.birth_datetime.day,
            "hour": self.birth_datetime.hour
        }

    def calculate_ming_gong(self) -> str:
        """计算命宫位置"""
        month = self.lunar_date["month"]
        hour_branch = self._get_hour_branch(self.lunar_date["hour"])

        # 简化的命宫计算逻辑
        index = (month - 1 + self.EARTHLY_BRANCHES.index(hour_branch)) % 12
        return self.EARTHLY_BRANCHES[index]

    def _get_hour_branch(self, hour: int) -> str:
        """获取时辰地支"""
        branch_index = hour // 2
        return self.EARTHLY_BRANCHES[branch_index]

    def calculate_main_stars(self) -> Dict[str, str]:
        """计算主星位置"""
        main_star_positions = {}
        ming_gong = self.calculate_ming_gong()

        # 简化的主星安排逻辑
        for star in self.MAIN_STARS:
            # 这里使用简化的逻辑，实际应该根据紫薇斗数规则计算
            position = self.EARTHLY_BRANCHES[(self.EARTHLY_BRANCHES.index(ming_gong) + 
                                           self.MAIN_STARS.index(star)) % 12]
            main_star_positions[star] = position

        return main_star_positions

    def _analyze_palace_stars(self, stars: List[str]) -> str:
        """分析宫位中星曜组合的吉凶"""
        # 扩展的星曜组合分析
        good_stars = sum(1 for star in stars if self.STAR_QUALITIES.get(star) == "吉")
        bad_stars = sum(1 for star in stars if self.STAR_QUALITIES.get(star) == "凶")

        if good_stars > bad_stars + 1:
            return "大吉"
        elif good_stars > bad_stars:
            return "吉"
        elif good_stars == bad_stars:
            return "平"
        elif bad_stars > good_stars + 1:
            return "大凶"
        else:
            return "凶"

    def get_palace_meaning(self, palace: str) -> str:
        """获取宫位的详细解释"""
        return self.PALACE_MEANINGS.get(palace, "暂无解释")

    def get_fortune_prediction(self) -> Dict[str, str]:
        """获取运势预测"""
        predictions = {}
        main_stars = self.calculate_main_stars()

        # 扩展的运势判断逻辑
        for palace in self.PALACES:
            stars_in_palace = [star for star, pos in main_stars.items() 
                             if pos == self.EARTHLY_BRANCHES[self.PALACES.index(palace)]]

            if stars_in_palace:
                prediction = self._analyze_palace_stars(stars_in_palace)
                stars_desc = "、".join(stars_in_palace)
                palace_meaning = self.get_palace_meaning(palace)
                prediction = f"{prediction} - {palace_meaning}\n落星：{stars_desc}"
            else:
                prediction = f"平 - {self.get_palace_meaning(palace)}\n无主星入驻"

            predictions[palace] = prediction

        return predictions

    def generate_chart_data(self) -> Dict:
        """生成命盘数据"""
        return {
            "ming_gong": self.calculate_ming_gong(),
            "main_stars": self.calculate_main_stars(),
            "predictions": self.get_fortune_prediction(),
            "birth_info": {
                "year": self.lunar_date["year"],
                "month": self.lunar_date["month"],
                "day": self.lunar_date["day"],
                "hour": self.lunar_date["hour"],
                "gender": self.gender
            }
        }