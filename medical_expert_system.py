from experta import *

diseases_list = []
diseases_symptoms = []
symptom_map = {}
d_desc_map = {}
d_treatment_map = {}

def preprocess():
    global diseases_list, diseases_symptoms, symptom_map, d_desc_map, d_treatment_map
    diseases = open("diseases.txt", encoding="utf-8")
    diseases_t = diseases.read()
    diseases_list = diseases_t.split("\n")
    diseases.close()

    for disease in diseases_list:
        disease_s_file = open("Disease symptoms/" + disease + ".txt", encoding="utf-8")
        disease_s_data = disease_s_file.read()
        s_list = disease_s_data.split("\n")
        diseases_symptoms.append(s_list)
        symptom_map[str(s_list)] = disease
        disease_s_file.close()

        disease_s_file = open("Disease descriptions/" + disease + ".txt", encoding="utf-8")
        disease_s_data = disease_s_file.read()
        d_desc_map[disease] = disease_s_data
        disease_s_file.close()

        disease_s_file = open("Disease treatments/" + disease + ".txt", encoding="utf-8")
        disease_s_data = disease_s_file.read()
        d_treatment_map[disease] = disease_s_data
        disease_s_file.close()
	

def identify_disease(*arguments):
	symptom_list = []
	for symptom in arguments:
		symptom_list.append(symptom)
	# Handle key error
	return symptom_map[str(symptom_list)]

def get_details(disease):
	return d_desc_map[disease]

def get_treatments(disease):
	return d_treatment_map[disease]

def if_not_matched(disease):
		print("")
		id_disease = disease
		disease_details = get_details(id_disease)
		treatments = get_treatments(id_disease)
		print("")
		print("Căn bệnh có khả năng cao nhất mà bạn đang mắc phải là %s\n" %(id_disease))
		print("Một mô tả ngắn gọn về căn bệnh được trình bày dưới đây :\n")
		print(disease_details+"\n")
		print("Các loại thuốc và phương pháp điều trị phổ biến được các bác sĩ thực tế khuyến nghị bao gồm: \n")
		print(treatments+"\n")

# @my_decorator is just a way of saying just_some_function = my_decorator(just_some_function)
#def identify_disease(headache, back_pain, chest_pain, cough, fainting, sore_throat, fatigue, restlessness,low_body_temp ,fever,sunken_eyes):
class Greetings(KnowledgeEngine):
	@DefFacts()
	def _initial_action(self):
		print("")
		print("Chào bạn! Tôi là bác sĩ , tôi ở đây để giúp bạn cải thiện sức khỏe của mình.")
		print("Để làm được điều đó, bạn sẽ cần trả lời một vài câu hỏi về tình trạng sức khỏe của mình. Bạn hãy trả lời yes hoặc no nhé.")
		print("Bạn có cảm thấy bất kỳ triệu chứng nào sau đây không:")
		print("")
		yield Fact(action="find_disease")


	@Rule(Fact(action='find_disease'), NOT(Fact(headache=W())),salience = 1)
	def symptom_0(self):
		self.declare(Fact(headache=input("Headache(Đau đầu): ")))

	@Rule(Fact(action='find_disease'), NOT(Fact(back_pain=W())),salience = 1)
	def symptom_1(self):
		self.declare(Fact(back_pain=input("Back pain(Đau lưng): ")))

	@Rule(Fact(action='find_disease'), NOT(Fact(chest_pain=W())),salience = 1)
	def symptom_2(self):
		self.declare(Fact(chest_pain=input("Chest pain(Đau ngực): ")))

	@Rule(Fact(action='find_disease'), NOT(Fact(cough=W())),salience = 1)
	def symptom_3(self):
		self.declare(Fact(cough=input("Cough(Ho): ")))

	@Rule(Fact(action='find_disease'), NOT(Fact(fainting=W())),salience = 1)
	def symptom_4(self):
		self.declare(Fact(fainting=input("Fainting(Ngất xỉu): ")))

	@Rule(Fact(action='find_disease'), NOT(Fact(fatigue=W())),salience = 1)
	def symptom_5(self):
		self.declare(Fact(fatigue=input("Fatigue:(Mệt mỏi): ")))
	 
	@Rule(Fact(action='find_disease'), NOT(Fact(sunken_eyes=W())),salience = 1)
	def symptom_6(self):
		self.declare(Fact(sunken_eyes=input("Sunken eyes(Mắt hõm): ")))
	
	@Rule(Fact(action='find_disease'), NOT(Fact(low_body_temp=W())),salience = 1)
	def symptom_7(self):
		self.declare(Fact(low_body_temp=input("Low body temperature(Thân nhiệt thấp): ")))
	
	@Rule(Fact(action='find_disease'), NOT(Fact(restlessness=W())),salience = 1)
	def symptom_8(self):
		self.declare(Fact(restlessness=input("Restlessness(Mất ngủ, lo âu): ")))
	
	@Rule(Fact(action='find_disease'), NOT(Fact(sore_throat=W())),salience = 1)
	def symptom_9(self):
		self.declare(Fact(sore_throat=input("Sore throat(Đau họng): ")))
	
	@Rule(Fact(action='find_disease'), NOT(Fact(fever=W())),salience = 1)
	def symptom_10(self):
		self.declare(Fact(fever=input("Fever(Sốt): ")))

	@Rule(Fact(action='find_disease'), NOT(Fact(nausea=W())),salience = 1)
	def symptom_11(self):
		self.declare(Fact(nausea=input("Nausea(Buồn nôn): ")))

	@Rule(Fact(action='find_disease'), NOT(Fact(blurred_vision=W())),salience = 1)
	def symptom_12(self):
		self.declare(Fact(blurred_vision=input("Blurred_vision(Mắt mờ): ")))

	@Rule(Fact(action='find_disease'),Fact(headache="no"),Fact(back_pain="no"),Fact(chest_pain="no"),Fact(cough="no"),Fact(fainting="no"),Fact(sore_throat="no"),Fact(fatigue="yes"),Fact(restlessness="no"),Fact(low_body_temp="no"),Fact(fever="yes"),Fact(sunken_eyes="no"),Fact(nausea="yes"),Fact(blurred_vision="no"))
	def disease_0(self):
		self.declare(Fact(disease="Jaundice"))

	@Rule(Fact(action='find_disease'),Fact(headache="no"),Fact(back_pain="no"),Fact(chest_pain="no"),Fact(cough="no"),Fact(fainting="no"),Fact(sore_throat="no"),Fact(fatigue="no"),Fact(restlessness="yes"),Fact(low_body_temp="no"),Fact(fever="no"),Fact(sunken_eyes="no"),Fact(nausea="no"),Fact(blurred_vision="no"))
	def disease_1(self):
		self.declare(Fact(disease="Alzheimers"))

	@Rule(Fact(action='find_disease'),Fact(headache="no"),Fact(back_pain="yes"),Fact(chest_pain="no"),Fact(cough="no"),Fact(fainting="no"),Fact(sore_throat="no"),Fact(fatigue="yes"),Fact(restlessness="no"),Fact(low_body_temp="no"),Fact(fever="no"),Fact(sunken_eyes="no"),Fact(nausea="no"),Fact(blurred_vision="no"))
	def disease_2(self):
		self.declare(Fact(disease="Arthritis"))

	@Rule(Fact(action='find_disease'),Fact(headache="no"),Fact(back_pain="no"),Fact(chest_pain="yes"),Fact(cough="yes"),Fact(fainting="no"),Fact(sore_throat="no"),Fact(fatigue="no"),Fact(restlessness="no"),Fact(low_body_temp="no"),Fact(fever="yes"),Fact(sunken_eyes="no"),Fact(nausea="no"),Fact(blurred_vision="no"))
	def disease_3(self):
		self.declare(Fact(disease="Tuberculosis"))

	@Rule(Fact(action='find_disease'),Fact(headache="no"),Fact(back_pain="no"),Fact(chest_pain="yes"),Fact(cough="yes"),Fact(fainting="no"),Fact(sore_throat="no"),Fact(fatigue="no"),Fact(restlessness="yes"),Fact(low_body_temp="no"),Fact(fever="no"),Fact(sunken_eyes="no"),Fact(nausea="no"),Fact(blurred_vision="no"))
	def disease_4(self):
		self.declare(Fact(disease="Asthma"))

	@Rule(Fact(action='find_disease'),Fact(headache="yes"),Fact(back_pain="no"),Fact(chest_pain="no"),Fact(cough="yes"),Fact(fainting="no"),Fact(sore_throat="yes"),Fact(fatigue="no"),Fact(restlessness="no"),Fact(low_body_temp="no"),Fact(fever="yes"),Fact(sunken_eyes="no"),Fact(nausea="no"),Fact(blurred_vision="no"))
	def disease_5(self):
		self.declare(Fact(disease="Sinusitis"))

	@Rule(Fact(action='find_disease'),Fact(headache="no"),Fact(back_pain="no"),Fact(chest_pain="no"),Fact(cough="no"),Fact(fainting="no"),Fact(sore_throat="no"),Fact(fatigue="yes"),Fact(restlessness="no"),Fact(low_body_temp="no"),Fact(fever="no"),Fact(sunken_eyes="no"),Fact(nausea="no"),Fact(blurred_vision="no"))
	def disease_6(self):
		self.declare(Fact(disease="Epilepsy"))

	@Rule(Fact(action='find_disease'),Fact(headache="no"),Fact(back_pain="no"),Fact(chest_pain="yes"),Fact(cough="no"),Fact(fainting="no"),Fact(sore_throat="no"),Fact(fatigue="no"),Fact(restlessness="no"),Fact(low_body_temp="no"),Fact(fever="no"),Fact(sunken_eyes="no"),Fact(nausea="yes"),Fact(blurred_vision="no"))
	def disease_7(self):
		self.declare(Fact(disease="Heart Disease"))

	@Rule(Fact(action='find_disease'),Fact(headache="no"),Fact(back_pain="no"),Fact(chest_pain="no"),Fact(cough="no"),Fact(fainting="no"),Fact(sore_throat="no"),Fact(fatigue="yes"),Fact(restlessness="no"),Fact(low_body_temp="no"),Fact(fever="no"),Fact(sunken_eyes="no"),Fact(nausea="yes"),Fact(blurred_vision="yes"))
	def disease_8(self):
		self.declare(Fact(disease="Diabetes"))

	@Rule(Fact(action='find_disease'),Fact(headache="yes"),Fact(back_pain="no"),Fact(chest_pain="no"),Fact(cough="no"),Fact(fainting="no"),Fact(sore_throat="no"),Fact(fatigue="no"),Fact(restlessness="no"),Fact(low_body_temp="no"),Fact(fever="no"),Fact(sunken_eyes="no"),Fact(nausea="yes"),Fact(blurred_vision="yes"))
	def disease_9(self):
		self.declare(Fact(disease="Glaucoma"))

	@Rule(Fact(action='find_disease'),Fact(headache="no"),Fact(back_pain="no"),Fact(chest_pain="no"),Fact(cough="no"),Fact(fainting="no"),Fact(sore_throat="no"),Fact(fatigue="yes"),Fact(restlessness="no"),Fact(low_body_temp="no"),Fact(fever="no"),Fact(sunken_eyes="no"),Fact(nausea="yes"),Fact(blurred_vision="no"))
	def disease_10(self):
		self.declare(Fact(disease="Hyperthyroidism"))

	@Rule(Fact(action='find_disease'),Fact(headache="yes"),Fact(back_pain="no"),Fact(chest_pain="no"),Fact(cough="no"),Fact(fainting="no"),Fact(sore_throat="no"),Fact(fatigue="no"),Fact(restlessness="no"),Fact(low_body_temp="no"),Fact(fever="yes"),Fact(sunken_eyes="no"),Fact(nausea="yes"),Fact(blurred_vision="no"))
	def disease_11(self):
		self.declare(Fact(disease="Heat Stroke"))

	@Rule(Fact(action='find_disease'),Fact(headache="no"),Fact(back_pain="no"),Fact(chest_pain="no"),Fact(cough="no"),Fact(fainting="yes"),Fact(sore_throat="no"),Fact(fatigue="no"),Fact(restlessness="no"),Fact(low_body_temp="yes"),Fact(fever="no"),Fact(sunken_eyes="no"),Fact(nausea="no"),Fact(blurred_vision="no"))
	def disease_12(self):
		self.declare(Fact(disease="Hypothermia"))

	@Rule(Fact(action='find_disease'),Fact(disease=MATCH.disease),salience = -998)
	def disease(self, disease):
		print("")
		id_disease = disease
		disease_details = get_details(id_disease)
		treatments = get_treatments(id_disease)
		print("")
		print("Căn bệnh có khả năng cao nhất mà bạn đang mắc phải là %s\n" %(id_disease))
		print("Một mô tả ngắn gọn về căn bệnh được trình bày dưới đây :\n")
		print(disease_details+"\n")
		print("Các loại thuốc và phương pháp điều trị phổ biến được các bác sĩ thực tế khuyến nghị bao gồm: \n")
		print(treatments+"\n")

	@Rule(Fact(action='find_disease'),
		  Fact(headache=MATCH.headache),
		  Fact(back_pain=MATCH.back_pain),
		  Fact(chest_pain=MATCH.chest_pain),
		  Fact(cough=MATCH.cough),
		  Fact(fainting=MATCH.fainting),
		  Fact(sore_throat=MATCH.sore_throat),
		  Fact(fatigue=MATCH.fatigue),
		  Fact(low_body_temp=MATCH.low_body_temp),
		  Fact(restlessness=MATCH.restlessness),
		  Fact(fever=MATCH.fever),
		  Fact(sunken_eyes=MATCH.sunken_eyes),
		  Fact(nausea=MATCH.nausea),
		  Fact(blurred_vision=MATCH.blurred_vision),NOT(Fact(disease=MATCH.disease)),salience = -999)

	def not_matched(self,headache, back_pain, chest_pain, cough, fainting, sore_throat, fatigue, restlessness,low_body_temp ,fever ,sunken_eyes ,nausea ,blurred_vision):
		print("\nDid not find any disease that matches your exact symptoms")
		lis = [headache, back_pain, chest_pain, cough, fainting, sore_throat, fatigue, restlessness,low_body_temp ,fever ,sunken_eyes ,nausea ,blurred_vision]
		max_count = 0
		max_disease = ""
		for key,val in symptom_map.items():
			count = 0
			temp_list = eval(key)
			for j in range(0,len(lis)):
				if(temp_list[j] == lis[j] and lis[j] == "yes"):
					count = count + 1
			if count > max_count:
				max_count = count
				max_disease = val
		if_not_matched(max_disease)


if __name__ == "__main__":
	preprocess()
	engine = Greetings()
	while(1):
		engine.reset()  # Prepare the engine for the execution.
		engine.run()  # Run it!
		print("Bạn có muốn chẩn đoán thêm một số triệu chứng khác không?")
		if input() == "no":
			exit()
		#print(engine.facts)