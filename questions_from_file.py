# get question objects from file
import json

def questions_from_file(path):
	with open(path) as f:
		questions=json.load(f)['questions']
	with open('static/fake_db.json') as f:
		fake_db=json.load(f)
	starting_index=len(fake_db['questions'])-1
	i=0
	for question in questions:
		if 'img' not in question.keys():
			question['img']=0
		question['question_id']=starting_index+i
		question['multiple_choice']=1
		question['marks']=1
		question['tags']=['multiple_choice', '2021_HSC']
		fake_db['questions'].append(question)
		i+=1
	with open('static/fake_db.json', 'w') as f:
		f.write(json.dumps(fake_db))

if __name__ == '__main__':
	questions_from_file('mult-choice-2021.json')