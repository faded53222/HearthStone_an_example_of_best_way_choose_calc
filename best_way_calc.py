import functools
import pickle
class hero:
	def __init__(self,name,health):
		self.name=name
		self.health=health
		self.attack=0
		self.able_to_attack=1
	def judge_equal(self,another):
		if self.name==another.name and self.health==another.health and self.attack==another.attack and self.able_to_attack==another.able_to_attack:
			return 1
		return 0
	def set_health(self,health):
		self.health=health
	def list_of_enemy_targets_aboard(self,with_repetition):
		if self is hero1:
			on_board_target_list=on_board_minion_list2.copy()
		else:
			on_board_target_list=on_board_minion_list1.copy()
		if with_repetition==0:
			remove_num=0
			for i in range(len(on_board_target_list)):
				for j in range(i+1,len(on_board_target_list)):
					j-=remove_num
					if on_board_target_list[i].judge_equal(on_board_target_list[j]):
						on_board_target_list.remove(on_board_target_list[j])
						remove_num+=1
		if self is hero1:
			on_board_target_list.append(hero2)								
		else:
			on_board_target_list.append(hero1)
		return on_board_target_list2
hero1=hero('Your hero',1)
hero2=hero('Enemy hero',2)
current_Crystal1=0
current_Crystal2=0
on_board_minion_list1=[]
on_board_minion_list2=[]
hands_list1=[]
hands_list2=[]
deathrattles_todo_list=[]
rand_lab=0
rand_results={}
def detect_win():
	if hero2.health<=0:
		if hero1.health>0:
			return 1
		else:
			return 2
	else:
		if hero1.health<=0:
			return -1
		else:
			return 0
class card:
	def __init__(self,name,cost):
		self.cost=cost
		self.name=name
		self.has_choice=0
	def list_of_enemy_targets_aboard(self,with_repetition):
		if self in hands_list1 or self in on_board_minion_list1:
			on_board_target_list=on_board_minion_list2.copy()
		else:
			on_board_target_list=on_board_minion_list1.copy()
		if with_repetition==0:
			remove_num=0
			for i in range(len(on_board_target_list)):
				for j in range(i+1,len(on_board_target_list)):
					j-=remove_num
					if on_board_target_list[i].judge_equal(on_board_target_list[j]):
						on_board_target_list.remove(on_board_target_list[j])
						remove_num+=1
		if self in hands_list1 or self in on_board_minion_list1:
			on_board_target_list.append(hero2)
		else:
			on_board_target_list.append(hero1)						
		return on_board_target_list
class magic(card):
	def __init__(self,name,cost):
		card.__init__(self,name,cost)
	def judge_equal(self,another):
		if self.name==another.name and self.cost==another.cost:
			return 1
		return 0
class Shadow_Bolt(magic):
	def __init__(self,name,cost):
		minion.__init__(self,name,cost)
		self.has_choice=1
	def get_possible_targets(self,with_repetition):
		tr=on_board_minion_list1+on_board_minion_list2
		if with_repetition==0:
			remove_num=0
			for i in range(len(tr)):
				for j in range(i+1,len(tr)):
					j-=remove_num
					if tr[i].judge_equal(tr[j]):
						tr.remove(tr[j])
						remove_num+=1
		return tr
	def cast(self,target):
		global current_Crystal1
		global current_Crystal2
		target.health-=4
		if self in hands_list1:
			hands_list1.remove(self)
			current_Crystal1-=self.cost
		if self in hands_list2:
			hands_list2.remove(self)
			current_Crystal2-=self.cost
class minion(card):
	def __init__(self,name,cost,able_to_attack=0,has_deathrattle=0,has_battlecry=0):
		card.__init__(self,name,cost)
		self.able_to_attack=able_to_attack
		self.has_deathrattle=has_deathrattle
		self.has_battlecry=has_battlecry
	def judge_equal(self,another):
		if self.name==another.name and self.cost==another.cost and self.able_to_attack==another.able_to_attack:
			return 1
		return 0
	def attack_another(self,another):
		self.health-=another.attack
		another.health-=self.attack
		self.able_to_attack-=1
	def death(self):
		#print(self.name+' is dead')
		if self in on_board_minion_list1:
			on_board_minion_list1.remove(self)
		if self in on_board_minion_list2:
			on_board_minion_list2.remove(self)
		if self.has_deathrattle==1:
			deathrattles_todo_list.append(self)
	def summon(self):
		global current_Crystal1
		global current_Crystal2
		if self.has_battlecry==1:
			self.battlecry()
		if self in hands_list1:
			hands_list1.remove(self)
			on_board_minion_list1.append(self)
			current_Crystal1-=self.cost
		if self in hands_list2:
			hands_list2.remove(self)
			on_board_minion_list2.append(self)
			current_Crystal2-=self.cost
class Lord_Godfrey(minion):
	def __init__(self,name,cost,able_to_attack,health,attack):
		minion.__init__(self,name,cost,able_to_attack,0,1)
		self.health=health
		self.attack=attack
class Goblin_Bomb(minion):
	def __init__(self,name,cost,able_to_attack,health,attack):
		minion.__init__(self,name,cost,able_to_attack,1,0)
		self.health=health
		self.attack=attack
	def deathrattles(self):
		if self in on_board_minion_list1:
			hero2.health-=2
		else:
			hero1.health-=2
class Mad_Bomer(minion):
	def __init__(self,name,cost,able_to_attack,health,attack):
		minion.__init__(self,name,cost,able_to_attack,0,1)
		self.health=health
		self.attack=attack
	def battlecry(self):
		global rand_lab
		global rand_result
		rand_lab=1
		count_all=0
		targets=[hero1]+[hero2]+on_board_minion_list1+on_board_minion_list2
		result_dic={}
		for i in targets:
			i.health-=1
			for j in targets:
				if j.health<=0 and j is not hero1 and j is not hero2:
					continue
				j.health-=1
				for k in targets:
					if k.health<=0 and k is not hero1 and k is not hero2:
						continue
					count_all+=1
					k.health-=1
					data=pickle.dumps((hero1,hero2,current_Crystal1,current_Crystal2,on_board_minion_list1,on_board_minion_list2,hands_list1,hands_list2))
					if data not in result_dic:
						result_dic[data]=0
					result_dic[data]+=1
					k.health+=1
				j.health+=1
			i.health+=1
		#print(result_dic.values())
		for each in result_dic.keys():
			rand_results[each]=result_dic[each]/count_all
			#print(rand_results[each])
class harm_less_1_1(minion):
	def __init__(self,name,cost,health,attack):
		minion.__init__(self,name,cost)
		self.health=health
		self.attack=attack	
class Violet_Wurm(minion):
	def __init__(self,name,cost,able_to_attack,health,attack):
		minion.__init__(self,name,cost,able_to_attack,1,)
		self.health=health
		self.attack=attack
	def deathrattles(self):
		if self in on_board_minion_list1:
			deal_place=on_board_minion_list1
		else:
			deal_place=on_board_minion_list2	
		for i in range(7-len(deal_place)):
			new_hl=harm_less_1_1('1-1',1,1,1)
			deal_place.append(new_hl)
def detect_death():
	for each in on_board_minion_list1+on_board_minion_list2:
		if each.health<=0:
			each.death()
def deal_deathrattles():
	for each in deathrattles_todo_list:
		each.deathrattles()
	deathrattles_todo_list.clear()
def get_all_choices(side):
	can_do_lis=[]
	global current_Crystal1
	global current_Crystal2
	if side==1:
		minion_list=on_board_minion_list1.copy()
		hand_list=hands_list1.copy()
		hero=hero1
		current_Crystal=current_Crystal1
	if side==2:
		minion_list=on_board_minion_list2.copy()
		hand_list=hands_list2.copy()
		hero=hero2
		current_Crystal=current_Crystal2
	remove_num1=0
	for i in range(len(hand_list)):
		for j in range(i+1,len(hand_list)):
			j-=remove_num1
			if hand_list[i].judge_equal(hand_list[j]):
				hand_list.remove(hand_list[j])
				remove_num1+=1
	remove_num2=0
	for i in range(len(minion_list)):
		for j in range(i+1,len(minion_list)):
			j-=remove_num2
			if minion_list[i].judge_equal(minion_list[j]):
				minion_list.remove(minion_list[j])	
				remove_num2+=1	
	target_list=minion_list.copy()
	target_list.append(hero)
	for each in target_list:
		if each.attack>0 and each.able_to_attack==1:
			for target in each.list_of_enemy_targets_aboard(0):
				can_do_lis.append((('dic_glob["'+str(each.name)+'"].attack_another(dic_glob["'+str(target.name)+'"])'),(str(each.name)+' #attack# '+str(target.name))))
	for each in hand_list:
		if each.cost<=current_Crystal:
			if isinstance(each,minion):
				if len(on_board_minion_list1)==7:
					continue
				if each.has_choice==1:
					for target in each.get_possible_targets():
						can_do_lis.append((('dic_glob["'+str(each.name)+'"].summon(dic_glob["'+str(target.name)+'"])'),('summon# '+str(each.name)+' #aim# '+str(target.name))))
				else:
					can_do_lis.append((('dic_glob["'+str(each.name)+'"].summon()'),('summon# '+str(each.name))))
			if isinstance(each,magic):
				if each.has_choice==1:
					for target in each.get_possible_targets(0):
						can_do_lis.append((('dic_glob["'+str(each.name)+'"].cast(dic_glob["'+str(target.name)+'"])'),('cast# '+str(each.name)+' #aim# '+str(target.name))))
				else:
					can_do_lis.append((('dic_glob["'+str(each.name)+'"].cast()'),('cast# '+str(each.name))))
	return can_do_lis
happened_dic={}
dic_glob={}
def out_load(data):
	global hero1
	global hero2
	global current_Crystal1
	global current_Crystal2
	global on_board_minion_list1
	global on_board_minion_list2
	global hands_list1
	global hands_list2
	global dic_glob
	(hero1,hero2,current_Crystal1,current_Crystal2,on_board_minion_list1,on_board_minion_list2,hands_list1,hands_list2)=pickle.loads(data)
	loads_tuple=(hero1,hero2,current_Crystal1,current_Crystal2,on_board_minion_list1,on_board_minion_list2,hands_list1,hands_list2)
	for count0 in range(len(loads_tuple)):
		if isinstance(loads_tuple[count0],list):
			for count in range(len(loads_tuple[count0])):
				dic_glob[loads_tuple[count0][count].name]=loads_tuple[count0][count]
		if isinstance(loads_tuple[count0],hero):
			dic_glob[loads_tuple[count0].name]=loads_tuple[count0]	
class node:
	def __init__(self,is_leaf=0,record='',is_rand=0):
		self.record=record
		self.step_records=record
		self.data=''
		self.is_rand=is_rand
		self.value=0
		self.win_pos=0
		self.tie_pos=0
		self.los_pos=0
		self.child_nodes=[]
		self.is_leaf=is_leaf
		self.best_child=[]
		if is_leaf==0 and is_rand!=1:
			self.choices=get_all_choices(1)
			on_board_minion_list1.sort(key=lambda x:x.name)
			on_board_minion_list2.sort(key=lambda x:x.name)
			hands_list1.sort(key=lambda x:x.name)
			hands_list2.sort(key=lambda x:x.name)
			self.data=pickle.dumps((hero1,hero2,current_Crystal1,current_Crystal2,on_board_minion_list1,on_board_minion_list2,hands_list1,hands_list2))
	def load(self):
		global hero1
		global hero2
		global current_Crystal1
		global current_Crystal2
		global on_board_minion_list1
		global on_board_minion_list2
		global hands_list1
		global hands_list2
		global dic_glob
		(hero1,hero2,current_Crystal1,current_Crystal2,on_board_minion_list1,on_board_minion_list2,hands_list1,hands_list2)=pickle.loads(self.data)
		loads_tuple=(hero1,hero2,current_Crystal1,current_Crystal2,on_board_minion_list1,on_board_minion_list2,hands_list1,hands_list2)
		for count0 in range(len(loads_tuple)):
			if isinstance(loads_tuple[count0],list):
				for count in range(len(loads_tuple[count0])):
					dic_glob[loads_tuple[count0][count].name]=loads_tuple[count0][count]
			if isinstance(loads_tuple[count0],hero):
				dic_glob[loads_tuple[count0].name]=loads_tuple[count0]
	def set_rand_results(self,rand_results):
		self.rand_results=rand_results
	def set_pos(self,pos):
		self.pos=pos
	def grow(self,step):
		global happened_dic
		global rand_lab
		global rand_results
		if (len(self.choices)==0):
			#print('over without choice')
			self.los_pos=1
			self.value=-1
		for each in self.choices:
			#print('step:'+str(step))
			self.load()
			#print(each[1])
			exec(each[0])
			if rand_lab==1:
				ap_node=node(0,each[1],1)
				ap_node.set_rand_results(rand_results.copy())
				self.child_nodes.append(ap_node)
				rand_results.clear()
				rand_lab=0
				for X in ap_node.rand_results.keys():
					out_load(X)
					detect_death()
					deal_deathrattles()
					win=detect_win()
					#print((hero1.health,hero2.health))
					#print(win)
					is_leaf=(win!=0)
					status='pos: '+str(ap_node.rand_results[X])
					status+='\nhero1:'+str(hero1.health)+'    hero2:'+str(hero2.health)+'\n'
					status+='side1: '
					for II in on_board_minion_list1:
						status+=str(II.name)+'    '
					status+='\nside2: '
					for II in on_board_minion_list2:
						status+=str(II.name)+'    '
					ap_node2=node(is_leaf,status)
					ap_node2.set_pos(ap_node.rand_results[X])
					ap_node.child_nodes.append(ap_node2)
					if win==0:
						if ap_node2.data in happened_dic:
							ap_node2=happened_dic[ap_node2.data]
							#print('case calc already')
							continue
						happened_dic[ap_node2.data]=ap_node2
						ap_node2.grow(step+1)
					if win==1:
						ap_node2.value=1
						ap_node2.win_pos=1
					if win==-1:
						ap_node2.value=-1
						ap_node2.los_pos=1
					if win==2:
						ap_node2.value=0
						ap_node2.tie_pos=1					
				continue
			detect_death()
			deal_deathrattles()
			win=detect_win()
			is_leaf=(win!=0)
			#print('win: '+str(win))
			ap_node=node(is_leaf,each[1])
			self.child_nodes.append(ap_node)
			if win==0:
				if ap_node.data in happened_dic:
					ap_node=happened_dic[ap_node.data]
					#print('case calc already')
					continue
				happened_dic[ap_node.data]=ap_node	
				ap_node.grow(step+1)
			if win==1:
				ap_node.value=1
				ap_node.win_pos=1
			if win==-1:
				ap_node.value=-1
				ap_node.los_pos=1
			if win==2:
				ap_node.value=0
				ap_node.tie_pos=1
def initialize():
	global current_Crystal1
	global current_Crystal2
	current_Crystal1=9
	happened_dic.clear()
	dic_glob.clear()
	on_board_minion_list1.clear()
	on_board_minion_list2.clear()
	hands_list1.clear()
	hands_list2.clear()
	lg=Lord_Godfrey('Lord_Godfrey',7,1,1,1)
	hl=harm_less_1_1('1-1',0,1,1)
	sb=Shadow_Bolt('Shadow_Bolt',3)
	gb1=Goblin_Bomb('Goblin_Bomb',1,0,1,1)
	gb2=Goblin_Bomb('Goblin_Bomb',1,0,1,1)
	vw=Violet_Wurm('Violet_Wurm',8,0,1,1)
	mb1=Mad_Bomer('Mad_Bomer',1,0,1,1)
	mb2=Mad_Bomer('Mad_Bomer',1,0,1,1)
	hands_list1.append(sb)
	hands_list1.append(mb1)
	hands_list1.append(mb2)
	on_board_minion_list1.append(lg)
	on_board_minion_list2.append(hl)
	on_board_minion_list2.append(gb1)
	on_board_minion_list2.append(gb2)
	on_board_minion_list2.append(vw)
def generate_nodes(node):
	if node.is_leaf:
		return
	if node.is_rand==1:
		for each in node.child_nodes:
			generate_nodes(each)
			node.win_pos+=each.pos*each.win_pos
			node.tie_pos+=each.pos*each.tie_pos
			node.los_pos+=each.pos*each.los_pos
			node.value+=each.pos*each.value
	else:
		max_value=-1
		for each in node.child_nodes:
			generate_nodes(each)
			if each.value>max_value:
				max_value=each.value
		node.value=max_value
		for each in node.child_nodes:
			if each.value==max_value:
				node.best_child.append(each)
				####
				node.win_pos=each.win_pos
				node.tie_pos=each.tie_pos
				node.los_pos=each.los_pos
				break
#def run_down_the_tree(node):
def show_the_tree(node,step):
	print('at step '+str(step)+':')
	print('best mean score is: '+str(node.value))
	if node.is_rand==1:
		lab=0
		for each in node.child_nodes:
			if lab==1:
				print('or')
			lab=1
			print('(step'+str(step)+') under case:')
			print(each.record)
			print('value: '+str(each.value))
			if(len(each.best_child)>0 or each.is_rand==1):
				show_the_tree(each,step+1)		
	else:
		lab=0
		for each in node.best_child:
			if lab==1:
				print('or')
			lab=1
			print('(step'+str(step)+') under choice:')
			print(each.record)
			if(len(each.best_child)>0 or each.is_rand==1):
				show_the_tree(each,step+1)
def deal():
	initialize()
	rootnode=node(0)
	rootnode.grow(0)
	generate_nodes(rootnode)
	mean=rootnode.value
	print('best mean is: '+str(mean))
	print('under best mean win_pos: '+str(rootnode.win_pos)+'  tie_pos: '+str(rootnode.tie_pos)+'  los_pos: '+str(rootnode.los_pos))
	show_the_tree(rootnode,1)
if __name__ == "__main__":
	deal()
