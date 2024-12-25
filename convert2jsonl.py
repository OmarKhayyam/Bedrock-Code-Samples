#!/usr/bin/python3

## This still requires square brackets at the beginning and the end

import json

with open('prompt_dict_updated.json', 'r') as data_file:
    json_data = json.load(data_file)

training_data = []

count = 0
for jsentry in json_data:
        training_data.append(jsentry)
        count = count + 1
        if count == 10000:
                break

system_prompt = "You are Claude, an AI assistant created by Anthropic to be helpful, harmless, and honest. Your goal is to provide informative and substantive responses to queries while avoiding potential harms. You are are to respond to user queries about automobile specifications and the automobile market."


with open('prompt_data.jsonl', 'w') as outfile:
        for entry in training_data:
                new_entry = {"system": system_prompt,"messages": [{"role": "user", "content": entry['prompt']},{"role": "assistant", "content": entry['completion']}]}
                json.dump(new_entry,outfile)
                outfile.write('\n')
