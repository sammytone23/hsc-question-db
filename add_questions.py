# add questions

def parse_question():
	print('Question')
	question_text=input('> ')
	print('Multiple choice? (y/n)')
	m_c=input('> ')
	while m_c.lower() not in 'yn':
		print('Incorrect input')
		print('Multiple choice? (y/n)')
		m_c=input('> ')
	if m_c=='y':
		options=[]
		print('Option:')
		option=input('> ')
		while option:
			options.append(option)
			print('Option:')
			option=input('> ')
		print('\n'.join(['Option '+str(p)+' ---> '+option for p,option in enumerate(options)]))
		print('Correct answer:')
		correct_option=int(input('> '))
		while correct_option >len(options)-1:
			print('invalid input')
			print('Correct answer:')
			correct_option=int(input('> '))
		answer=options[correct_option]
		tags=[]
		print('Tag:')
		tag=input('> ')
		while tag:
			tags.append(tag)
			print('tag:')
			tag=input('> ')
		return {'question':question_text,'multiple_choice':1, 'answers':options,'correct_answer':answer,'marks':1,'tags':tags}
	else:
		print('Enter marking guide:')
		marking_guide=input()
		print('Marks:')
		marks=int(input('> '))
		tags=[]
		print('Tag:')
		tag=input('> ')
		while tag:
			tags.append(tag)
			print('tag:')
			tag=input('> ')
		return {'question':question_text,'multiple_choice':0, 'marking_guide':marking_guide,'marks':marks,'tags':tags}


def multiple_questions():
	print('Leave input blank if exit')
	cont=input('> ')
	while cont:
		print(parse_question())
		print('Leave input blank if exit')
		cont=input('> ')