#!/usr/bin/env python
# coding: utf-8

# In[71]:


with open('current_temp.txt', 'r') as current_temp:
    temp = current_temp.readlines()
    temp = int(temp[0])
    current_temp.close()
with open('temp_scale.txt', 'r') as temp_scale:
    temps = temp_scale.readlines()
    dict_temp = eval(temps[0])
    temp_scale.close()
with open('temp_scale.txt', 'w') as temp_scale:
    dict_temp[temp] += 3
    temp_scale.write(str(dict_temp))
    temp_scale.close()

# In[ ]:





