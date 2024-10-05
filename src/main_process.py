from utils.notion_util import add_creature
from utils.openai_util import analyze_creature, CreatureProfile

def main():
	source_file = open("../input/source.txt")
	creature_text = source_file.read()
	creature_profile = analyze_creature(creature_text)
	print(creature_profile)

	response = add_creature(creature_profile)
	print(response)

if __name__ == "__main__":
	main()