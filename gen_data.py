# create fake data

'''
A question looks like the following json
{
	"question_id":<incremental number>,
	"question":<the text of the question>,
	"multiple_choice":<boolean 1 or 0>,
	if multiple choice:
		"answers":<list of possible answers>,
		"correct_answer":<one of the values in the above list>,
	else:
		"marking_guide":<paragraph dictating how to assign marks>,
	"marks":<integer number of marks assigned>,
	"img":<0 if no image, otherwise the filename of the image>,
	"tags":<list of tags that apply to the question>
}
'''

import lorem
import random

def make_questions(number, starting_id=0):
	question_list=[]
	for i in range(number):
		question={}
		question['question_id']=starting_id+i
		question['question']=lorem.sentence()+'?'
		multiple_choice=random.randint(0,1)
		question['multiple_choice']=multiple_choice
		question['tags']=[]
		if multiple_choice:
			answers=['answer '+str(1+a) for a in range(random.randint(2,6))]
			question['answers']=answers
			correct_answer=random.choice(answers)
			question['correct_answer']=correct_answer
			question['marks']=1
			question['tags'].append('multiple_choice')
		else:
			question['marking_guide']=lorem.paragraph()
			question['marks']=random.randint(1,6)
			question['tags'].append('short_answer')
		has_image=random.randint(0,1)
		if has_image:
			question['img']='please-give-me-good-marks.jpg'
			question['tags'].append('has_image')
		else:
			question['img']=0
		question_list.append(question)
	return question_list