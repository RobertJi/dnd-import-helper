import json
import os

from dotenv import load_dotenv
import requests

load_dotenv()
NOTION_TOKEN = os.getenv('NOTION_API_KEY')
DND_CREATURES_DB_ID = os.getenv('NOTION_CREATURE_DB_ID') #

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def transform_creature_profile(creature_profile, skills):
	return {
		'组织': {
			'rich_text': [
				{
					"text": {
						"content": creature_profile["组织"]
					}
				}
			]
		},
		'专长': {
			'multi_select': skills
		},
		'生物类型': {
			'multi_select': [{
				"name": creature_profile["生物类型"]
			}]
		},
		'体型': {
			'select': {
				"name": creature_profile["体型"]
			}
		},
		'挑战等级': {
			'number': creature_profile["挑战等级"]
		},
		'环境': {
			'select': {
				"name": creature_profile["环境"]
			}
		},
		'智力': {
			'rich_text': [
				{
					"text": {
						"content": creature_profile["智力"]
					}
				}
			]
		},
		'阵营': {
			'select': {
				"name": creature_profile["阵营"]
			}
		},
		'视觉': {
			'multi_select': [{
				"name": creature_profile["视觉"]
			}]
		},
		'力量': {
			'rich_text': [
				{
					"text": {
						"content": creature_profile["力量"]
					}
				}
			]
		},
		'抗性': {
			'rich_text': [
				{
					"text": {
						"content": creature_profile["抗性"]
					}
				}
			]
		},
		'先攻': {
			'number': creature_profile["先攻"]
		},
		'速度': {
			'rich_text': [
				{
					"text": {
						"content": creature_profile["速度"]
					}
				}
			]
		},
		'体质': {
			'rich_text': [
				{
					"text": {
						"content": creature_profile["体质"]
					}
				}
			]
		},
		'特性': {
			'rich_text': [
				{
					"text": {
						"content": creature_profile["特性"]
					}
				}
			]
		},
		'基本攻击/擒抱': {
			'rich_text': [
				{
					"text": {
						"content": creature_profile["基本攻击"]
					}
				}
			]
		},
		'技能': {
			'rich_text': [
				{
					"text": {
						"content": creature_profile["技能"]
					}
				}
			]
		},
		'生命骰': {
			'rich_text': [
				{
					"text": {
						"content": creature_profile["生命骰"]
					}
				}
			]
		},
		'敏捷': {
			'rich_text': [
				{
					"text": {
						"content": creature_profile["敏捷"]
					}
				}
			]
		},
		'感知': {
			'rich_text': [
				{
					"text": {
						"content": creature_profile["感知"]
					}
				}
			]
		},
		'豁免': {
			'rich_text': [
				{
					"text": {
						"content": creature_profile["豁免"]
					}
				}
			]
		},
		'进化': {
			'rich_text': [
				{
					"text": {
						"content": creature_profile["进化"]
					}
				}
			]
		},
		'魅力': {
			'rich_text': [
				{
					"text": {
						"content": creature_profile["魅力"]
					}
				}
			]
		},
		'特殊攻击': {
			'rich_text': [
				{
					"text": {
						"content": creature_profile["特殊攻击"]
					}
				}
			]
		},
		'全回合攻击': {
			'rich_text': [
				{
					"text": {
						"content": creature_profile["全回合攻击"]
					}
				}
			]
		},
		'防御等级': {
			'rich_text': [
				{
					"text": {
						"content": creature_profile["防御等级"]
					}
				}
			]
		},
		'中文名': {
			'title': [
				{
					"text": {
						"content": creature_profile["中文名"]
					}
				}
			]
		},
		'英文名': {
			'rich_text': [
				{
					"text": {
						"content": creature_profile["英文名"]
					}
				}
			]
		}
	}

def transform_creature_profile_skills(creature_profile):
	skills = creature_profile['专长']
	print(skills)
	structured_skills = []
	for skill in skills:
		structured_skills.append({
			'name': skill
		})
	return structured_skills

def add_creature(creature_profile_text):
	create_url = "https://api.notion.com/v1/pages"
	creature_profile = json.loads(creature_profile_text)
	skills = transform_creature_profile_skills(creature_profile)
	profile = transform_creature_profile(creature_profile, skills)
	data = {
        "parent": {"database_id": DND_CREATURES_DB_ID},
        "properties": profile,
		"children": [
			{
				"object": "block",
				"type": "paragraph",
				"paragraph": {
				"rich_text": [
					{
						"type": "text",
						"text": {
							"content": creature_profile["说明"],
						}
					}
				]
			}
			},
			{
				"object": "block",
				"type": "heading_2",
				"heading_2": {
					"rich_text": [{"type": "text", "text": {"content": "特殊攻击"}}]
				}
			},
			{
				"object": "block",
				"type": "paragraph",
				"paragraph": {
					"rich_text": [
						{
							"type": "text",
							"text": {
								"content": creature_profile["特殊攻击描述"],
							}
						}
					]
				}
			},
			{
				"object": "block",
				"type": "heading_2",
				"heading_2": {
					"rich_text": [{"type": "text", "text": {"content": "其他信息"}}]
				}
			},
			{
				"object": "block",
				"type": "paragraph",
				"paragraph": {
					"rich_text": [
						{
							"type": "text",
							"text": {
								"content": creature_profile["其他信息"],
							}
						}
					]
				}
			}
		]
    }

	response = requests.post(create_url, headers=headers, json=data)
	return response.json()
