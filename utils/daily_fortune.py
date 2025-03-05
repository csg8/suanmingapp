import random
from datetime import datetime

class DailyFortune:
    """每日运势和智慧语录管理类"""

    FORTUNE_LEVELS = ["大吉", "吉", "平", "凶", "大凶"]

    WISDOM_QUOTES = [
        "宁静致远，淡泊明志",
        "天行健，君子以自强不息",
        "厚德载物，自强不息",
        "己所不欲，勿施于人",
        "修身齐家，治国平天下",
        "仁者无敌",
        "知己知彼，百战不殆",
        "天道酬勤",
        "福祸相依，塞翁失马",
        "一张一弛，文武之道",
        "谋定而后动，知止而有得",
        "君子坦荡荡，小人长戚戚",
        "以和为贵，和气生财",
        "顺其自然，厚德载物",
        "静以修身，俭以养德",
        "大道至简，有容乃大",
        "天时地利人和",
        "居安思危，思则有备",
        "水善利万物而不争",
        "君子不器",
        "大巧若拙，大智若愚",
        "见贤思齐焉，见不贤而内自省也",
        "温故知新，可以为师矣",
        "三人行，必有我师焉"
    ]

    LOVE_QUOTES = [
        "有缘千里来相会",
        "天涯何处无芳草",
        "有情人终成眷属",
        "月老红线，姻缘天定",
        "金风玉露一相逢，便胜却人间无数",
        "十年修得同船渡，百年修得共枕眠",
        "愿得一心人，白头不相离",
        "两情若是久长时，又岂在朝朝暮暮",
        "衣带渐宽终不悔，为伊消得人憔悴",
        "相见时难别亦难，东风无力百花残",
        "人生若只如初见，何事秋风悲画扇",
        "曾经沧海难为水，除却巫山不是云",
        "身无彩凤双飞翼，心有灵犀一点通",
        "在天愿作比翼鸟，在地愿为连理枝",
        "此情可待成追忆，只是当时已惘然",
        "春风十里，不如你",
        "山无陵，江水为竭，冬雷震震，夏雨雪，天地合，乃敢与君绝",
        "玲珑骰子安红豆，入骨相思知不知",
        "愿我如星君如月，夜夜流光相皎洁",
        "执子之手，与子偕老",
        "人生自是有情痴，此恨不关风与月",
        "相思树底说相思，春风春雨落双枝"
    ]

    DAILY_TIPS = [
        "宜：结婚、搬家、开业、出行",
        "忌：动土、安葬、开张、远行",
        "宜：祈福、求财、开市、交易",
        "忌：诉讼、动工、理发、置业",
        "宜：入学、考试、谈判、签约",
        "忌：置业、乔迁、远行、开业",
        "宜：交友、谈判、签约、出行",
        "忌：动土、装修、搬家、开业",
        "宜：开张、求财、谈判、旅行",
        "忌：婚嫁、动土、开业、搬迁",
        "宜：考试、面试、谈判、签约",
        "忌：装修、开业、搬家、远行"
    ]

    @staticmethod
    def get_daily_fortune(date: datetime = None) -> dict:
        """获取每日运势"""
        if date is None:
            date = datetime.now()

        # 不使用日期作为种子，让每次刷新都随机
        random.seed()

        # 根据日期生成不同的运势组合
        day_num = int(date.strftime("%d"))
        month_num = int(date.strftime("%m"))

        # 使用日期数字影响运势的生成
        fortune_weights = {
            "大吉": 0.2 + (day_num % 5) * 0.05,
            "吉": 0.3 + (month_num % 3) * 0.05,
            "平": 0.3,
            "凶": 0.15 - (day_num % 3) * 0.02,
            "大凶": 0.05 - (month_num % 2) * 0.01
        }

        return {
            "overall": random.choices(DailyFortune.FORTUNE_LEVELS, 
                                   weights=[fortune_weights[level] for level in DailyFortune.FORTUNE_LEVELS])[0],
            "love": random.choice(DailyFortune.FORTUNE_LEVELS),
            "career": random.choice(DailyFortune.FORTUNE_LEVELS),
            "wealth": random.choice(DailyFortune.FORTUNE_LEVELS),
            "wisdom": random.choice(DailyFortune.WISDOM_QUOTES),
            "love_quote": random.choice(DailyFortune.LOVE_QUOTES),
            "tips": random.sample(DailyFortune.DAILY_TIPS, 2)
        }

    @staticmethod
    def get_lucky_colors() -> list:
        """获取幸运颜色"""
        colors = ["红色", "黄色", "蓝色", "绿色", "紫色", "金色", "银色", "白色", 
                 "橙色", "粉色", "青色", "棕色", "藏青色", "玫瑰金", "翡翠绿", "靛青色"]
        return random.sample(colors, 2)

    @staticmethod
    def get_lucky_numbers() -> list:
        """获取幸运数字"""
        return random.sample(range(1, 10), 2)

    @staticmethod
    def get_lucky_directions() -> list:
        """获取吉利方位"""
        directions = ["东", "南", "西", "北", "东南", "西南", "东北", "西北",
                     "正东", "正南", "正西", "正北", "艮", "坤", "震", "巽"]
        return random.sample(directions, 2)