from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key= openai_api_key)

dnd_creature_analyze_prompt = """
你的任务是检视讲述d&d 3e的生物属性和介绍的文章，并将其转化为格式化的json输出。
要求
1. 所有的括号，逗号等符号一律使用半角符号。
2. 不要自己生产内容，一切以文章中提供的内容为准。
3. 专长如果有和下面的列表类似但不一样的，则修正成下面的（例如，顺劈斩和下面列表中的顺势斩其实是一个专长。这时应使用顺势斩。）否则就使用文章中的（例如，文章中出现超级先攻这个专长，和下面列表中的任何一个都不类似，是一个新专长，应该直接套用文章中的。）
4. 如果有多个特殊攻击描述，他们之间要有一个额外的空行。

一些字段的样例：
- 防御等级：42（+14敏捷，+18天生）
- 如果文中没有的属性，例如基本攻击，宝物等，留“-”
- 有些生物可能没有力量，敏捷，智力，感知，体质或魅力，这种情况下留“-”
- 所有标记为种族调整值的技能需要忽略。
- 抗性为生物信息中 DR和抗力的部分，比如 引导抗力+2, DR10/银
- 生物类型不需要带括号。例如不死生物（火系）是不对的，应该是“不死生物”
- 阵营必然为如下之一：守序善良，中立善良，混乱善良，守序中立，绝对中立，混乱中立，守序邪恶，中立邪恶，混乱邪恶
- “其他信息”包含没有在其他任何返回字段的内容（如战术和策略，通过检定可以知道的知识等）。开头应该有一个换行。如果该字段没有任何内容，则为"-".

专长列表:
- 精通先攻，闪电反射，动物亲和，闪避，飞越攻击，钢铁意志，突刺，灵活移动，隐秘，警觉，战斗施法，猛力攻击，顺势斩，强力顺势斩，精通冲撞，无畏一击，精通击破武器
- 精通重击(这里可能有很多武器类型)，武器专攻(这里可能有很多武器类型)，能力专攻(这里可能有很多能力类型)，强化天生攻击(这里可能有很多武器类型)
- 法术专精(这里可能有很多法术类型)，技能专攻(这里可能有很多技术类型)
- 武器娴熟，战斗反射，跳跃攻击，盲斗，强韧加强，强壮，追踪，拨挡箭矢，灵狐步，快步跟进，震慑拳，近程射击，精确射击，快速射击，移动射击，寓守于攻，精通解除武器
- 精通绊摔，法术穿透，坚韧，飞跑，防御战斗训练，穷追不舍，旋风攻击，灵活战技，导能打击，要害打击，致命瞄准，双武器格斗，精通双武器格斗，精通徒手击打
- 抵近射击，精准射击，快拔，施法免材，直觉闪避，恐怖殴击，致盲重击，定身击，爆击，欺瞒，如影随形，精通引导，法术默发，疾风步，多重攻击，威逼
"""

structured_json_output = {}

class CreatureProfile(BaseModel):
	中文名: str
	英文名: str
	体型: str
	生物类型: str
	阵营: str
	挑战等级: int
	生命骰: str
	面宽: str
	触及: str
	先攻: int
	速度: str
	防御等级: str
	组织: str
	视觉: str
	力量: str
	敏捷: str
	体质: str
	智力: str
	感知: str
	魅力: str
	豁免: str
	基本攻击: str
	全回合攻击: str
	特殊攻击: str
	抗性: str
	特性: str
	专长: list[str]
	来源: str
	技能: str
	环境: str
	组织: str
	# 宝物: str
	进化: str
	说明: str
	特殊攻击描述: str
	其他信息: str


def analyze_creature(creature_text):
	system_prompt = dnd_creature_analyze_prompt
	response = client.beta.chat.completions.parse(
		model="gpt-4o-2024-08-06",  # Specify the model as GPT-4
		messages=[
			{"role": "system", "content": system_prompt},
			{"role": "user", "content": creature_text}
		],
		response_format=CreatureProfile,
		temperature=0.5
	)

	return response.choices[0].message.content
